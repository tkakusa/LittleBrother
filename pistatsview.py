#!/usr/bin/python3

from pymongo import MongoClient
import json
import pprint
import sys, getopt
from gpiozero import RGBLED
from time import sleep
import pika

# Setup the LED pinouts
led = RGBLED(13, 19, 26)

# Open the database
client = MongoClient()
db1 = client.host1
db2 = client.host2

# Get the posts from the database
posts1 = db1.posts
posts2 = db2.posts
postscurr = 0

#address='172.29.42.45'
#vhost='little_brother'
#usr='monitor'
#pswd='monitorpassword'

# Default connection Info parameters
address=''
vhost=''
usr=''
pswd=''
routing_key=''

# Make sure that the input parameters have been placed correctly
try:
    opts, args = getopt.getopt(sys.argv[1:], "hb:p:c:k:")
except getopt.GetoptError:
    print ('pistatsview -b message broker [-p virtual host] [-c login:password] -k routing key')
    sys.exit(2)
for opt, arg in opts:
    if opt == '-h':
        print ('pistatsview -b message broker [-p virtual host] [-c login:password] -k routing key')
        sys.exit()
    elif opt in ("-b"):
        address = arg
    elif opt in ("-p"):
        vhost = arg
    elif opt in ("-c"):
        (usr, pswd) = arg.split(":")
    elif opt in ("-k"):
        routing_key = arg

# Print Connection Information for Debugging purposes
print ("Address:        ", address)
print ("Virtual Host:   ", vhost)
print ("User Name:      ", usr)
print ("Password:       ", pswd)
print ("Routing Key:    ", routing_key)

# Returns a connection to the rabbitmq server described by arguments. The returned
# connection should be closed using '.close()' to make sure message buffers are
# flushed and connection closes gracefully.
#
# @param 'address' = IP address of rabbitmq broker
# @param 'vhost' = vhost on rabbitmq broker that user connects to. Default: '/'
# @param 'usr' = name of user connecting to rabbitmq broker. Default: ''
# @param 'pswd' = password for user connecting to rabbitmq broker. Default: ''
def rmq_open_sub_cxn(address, callback, vhost='/', usr='', pswd=''):
    credentials = pika.PlainCredentials(usr, pswd)

    connectFail = True
    attempts = 5
    while(connectFail and attempts > 0):
        try:
            connection = pika.BlockingConnection(pika.ConnectionParameters(host=address,
                                                                           port=5672, #default rabbitmq port
                                                                           virtual_host=vhost,
                                                                           credentials=credentials))
        except pika.exceptions.ConnectionClosed:
            print("There was a problem connecting to the server.")
            print("Trying to reconnect...")
            sleep(3)
            attempts = attempts - 1

        except pika.exceptions.ProbableAuthenticationError:
            print("Could not authenticate with the server. Please check your vhost name and credentials.")
            sys.exit()

    if(attempts == 0):
        print("Could not connect to the server.")
        sys.exit()

    return connection

# Subscribes to an exchange based on the rkeys provided, and starts listening.
# Listening is blocking, so no code will be executed after this function is called.
# Executes callback function upon receiving a message fitting the rkeys. 'callback'
# has to be declared this way: def [ftn_name](ch, method, properties, body)
#
# @param 'cxn': existing opened connection to a rabbitmq broker
# @param 'rkey': routing key that this subscription will listen for
# @param 'callback': callback function for when a message is received
def rmq_subscribe(cxn, rkey, callback):
    if(cxn==None):
        print("Subscription Error: Connection provided in argument was not properly established.")
        return

    ch = cxn.channel()

    queue_name = str(rkey + "_q")
    ch.queue_declare(queue=queue_name)
    ch.basic_qos(prefetch_count=1)
    ch.basic_consume(callback,
                     queue=queue_name)

    ch.start_consuming()

# Updates the color of the LED based on the CPU utilization
# Consulted reference: https://www.raspberrypi.org/files/education/posters/GPIO_Zero_Cheatsheet.pdf
#
# @param 'utilization': the CPU utilization, between 0 (0%) and 1 (100%)
def updateLED(utilization):

	# Check for invalid input
	if utilization > 1:
		print("Warning: CPU utilization reported over 100%")
	elif utilization < 0:
		print("Warning: CPU utilization reported under 0%")

	if utilization <= .25:
		# green
		led.color = (0, 1, 0)
	elif utilization <= .5:
		# yellow
		led.color = (1, .5, 0)
	else:
		# red
		led.color = (1, 0, 0)


# When you receive messages, this function will be called. It needs to have these
# arguments to be called properly. The routing key and message itself can be extracted
# as shown in this example method.
def callback(ch, method, properties, body):
    # Temp variables used to store the hi and lo values
    cpu_hi = 0
    cpu_lo = 10
    lo_rx_hi = 0
    lo_rx_lo = 10
    lo_tx_hi = 0
    lo_tx_lo = 10
    eth0_rx_hi = 0
    eth0_rx_lo = 10
    eth0_tx_hi = 0
    eth0_tx_lo = 10
    wlan0_rx_hi = 0
    wlan0_rx_lo = 10
    wlan0_tx_hi = 0
    wlan0_tx_lo = 10

    # Decode the body of the message from byte to string
    body = json.loads(body.decode("utf-8"))
    try:
        
        # Test to see that the format is correct
        temp = body['cpu']
        temp = body['cpu']
        temp = body['net']['lo']['rx']
        temp = body['net']['lo']['rx']
        temp = body['net']['lo']['tx']
        temp = body['net']['lo']['tx']
        temp = body['net']['eth0']['rx']
        temp = body['net']['eth0']['rx']
        temp = body['net']['eth0']['tx']
        temp = body['net']['eth0']['tx']
        temp = body['net']['wlan0']['rx']
        temp = body['net']['wlan0']['rx']
        temp = body['net']['wlan0']['tx']
        temp = body['net']['wlan0']['tx']
        
        # Check the routing key and store appropriately
        if (method.routing_key == "host1"):
            posts1.insert_one(body)
            postscurr = posts1
        elif (method.routing_key == "host2"):
            posts2.insert_one(body)
            postscurr = posts2
        # Loop through the storage locations in order to calculate the high and low values
        for post in postscurr.find():
            cpu_hi = post['cpu'] if post['cpu'] > cpu_hi else cpu_hi
            cpu_lo = post['cpu'] if post['cpu'] < cpu_lo else cpu_lo
            lo_rx_hi = post['net']['lo']['rx'] if post['net']['lo']['rx'] > lo_rx_hi else lo_rx_hi
            lo_rx_lo = post['net']['lo']['rx'] if post['net']['lo']['rx'] < lo_rx_lo else lo_rx_lo
            lo_tx_hi = post['net']['lo']['tx'] if post['net']['lo']['tx'] > lo_tx_hi else lo_tx_hi
            lo_tx_lo = post['net']['lo']['tx'] if post['net']['lo']['tx'] < lo_tx_lo else lo_tx_lo
            eth0_rx_hi = post['net']['eth0']['rx'] if post['net']['eth0']['rx'] > eth0_rx_hi else eth0_rx_hi
            eth0_rx_lo = post['net']['eth0']['rx'] if post['net']['eth0']['rx'] < eth0_rx_lo else eth0_rx_lo
            eth0_tx_hi = post['net']['eth0']['tx'] if post['net']['eth0']['tx'] > eth0_tx_hi else eth0_tx_hi
            eth0_tx_lo = post['net']['eth0']['tx'] if post['net']['eth0']['tx'] < eth0_tx_lo else eth0_tx_lo
            wlan0_rx_hi = post['net']['wlan0']['rx'] if post['net']['wlan0']['rx'] > wlan0_rx_hi else wlan0_rx_hi
            wlan0_rx_lo = post['net']['wlan0']['rx'] if post['net']['wlan0']['rx'] < wlan0_rx_lo else wlan0_rx_lo
            wlan0_tx_hi = post['net']['wlan0']['tx'] if post['net']['wlan0']['tx'] > wlan0_tx_hi else wlan0_tx_hi
            wlan0_tx_lo = post['net']['wlan0']['tx'] if post['net']['wlan0']['tx'] < wlan0_tx_lo else wlan0_tx_lo
    
        # Update the LED
        updateLED(body['cpu'])

        # Print the updated utilization
        print(method.routing_key , ":")
        print("cpu: " , body['cpu'] , " [Hi: " , cpu_hi , ", Lo: " , cpu_lo , "]")
        print("lo: rx=" , body['net']['lo']['rx'] , " B/s [Hi: " , lo_rx_hi , " B/s, Lo: " , lo_rx_lo , " B/s], tx=" , body['net']['lo']['tx'] , " B/s [Hi: " , lo_tx_hi , " B/s, Lo: " , lo_tx_lo , " B/s]")
        print("eth0: rx=" , body['net']['eth0']['rx'] , " B/s [Hi: " , eth0_rx_hi , " B/s, Lo: " , eth0_rx_lo , " B/s], tx=" ,body['net']['eth0']['tx'] , " B/s [Hi: " , eth0_tx_hi , " B/s, Lo: " , eth0_tx_lo , " B/s]")
        print("wlan0: rx=" , body['net']['wlan0']['rx'] , " B/s [Hi: " , wlan0_rx_hi , " B/s, Lo: " , wlan0_rx_lo , " B/s], tx=" ,body['net']['wlan0']['tx'] , " B/s [Hi: " , wlan0_tx_hi , " B/s, Lo: " , wlan0_tx_lo , " B/s]")
        print()

    except:
        print ("Error parsing data: Incorrect Format")
    # Acknowledge the message has been properly read in
    ch.basic_ack(delivery_tag = method.delivery_tag)


# establish a connection with the rabbitmq broker
connection = rmq_open_sub_cxn(address, callback, vhost, usr, pswd)

# arbitrary print statement so user knows what's going on
print(" [x] Listening for messages...")

# start listening for messages with the routing keys listed in the second argument
connectionDropped = True
while(connectionDropped):
    try:
        rmq_subscribe(connection, routing_key, callback)
    except pika.exceptions.ConnectionClosed:
        connection = rmq_open_sub_cxn(address, callback, vhost, usr, pswd)
    else:
        connectionDropped = False 

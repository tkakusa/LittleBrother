#Net Apps - Assignment #2 - Host

#imports
import sys, os, getopt, pika, json
from time import sleep

# Returns a connection to the rabbitmq server described by arguments. The returned
# connection should be closed using '.close()' to make sure message buffers are
# flushed and connection closes gracefully.
#
# @param 'address' = IP address of rabbitmq broker
# @param 'vhost' = vhost on rabbitmq broker that user connects to. Default: '/'
# @param 'usr' = name of user connecting to rabbitmq broker. Default: ''
# @param 'pswd' = password for user connecting to rabbitmq broker. Default: ''
def rmq_open_pub_cxn(address, rkey, vhost='/', usr='', pswd=''):
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

        else:
            connectFail = False
            ch = connection.channel()
            ch.exchange_declare(exchange='lb_exch',
                                type='direct')

            ch.queue_declare(queue=rkey+"_q")
            queue_name = str(rkey + "_q")
            ch.queue_bind(exchange='lb_exch',
                          queue=queue_name,
                          routing_key=rkey)

    if(attempts == 0):
        print("Could not connect to the server.")
        sys.exit()

    return connection

# Publishes a message to the rabbitmq server based on the connection provided as 'cxn'
#
# @param 'cxn' = existing opened connection to a rabbitmq broker
# @param 'msg' = string message to be sent to broker
# @param 'rkey' = routing key to be associated with the message being sent
def rmq_publish(cxn, msg, rkey):
    ch = cxn.channel()

    ch.basic_publish(exchange='lb_exch',
                     routing_key=rkey,
                     body=msg)

address = ''
virtualHost = '/'
username = ''
password = ''
routingKey = ''

# Parse command line arguments
try:
    opts, args = getopt.getopt(sys.argv[1:], "hb:p:c:k:")
except getopt.GetoptError:
    print('usage: pistatsd -b message broker [-p virtual host] [-c login:password] -k routing key')
    sys.exit(2)
for opt, arg in opts:
    if opt == '-h':
        print('usage: pistatsd -b message broker [-p virtual host] [-c login:password] -k routing key')
        sys.exit()
    elif opt in ("-b"):
        address = arg
    elif opt in ("-p"):
        virtualHost = arg
    elif opt in ("-c"):
        (username,password) = arg.split(":")
    elif opt in ("-k"):
        routingKey = arg
if (address == '' or routingKey == ''):
    print('usage: pistatsd -b message broker [-p virtual host] [-c login:password] -k routing key')
    sys.exit(2)
    
#Declare and initialize variables
last_idle     = last_total    = 0
eth0_rx_last  = eth0_tx_last  = 0
lo_rx_last    = lo_tx_last    = 0
wlan0_rx_last = wlan0_tx_last = 0
counter       = 0
wait_time     = 1

#Set up RabbitMQ Publishing connection
connection = rmq_open_pub_cxn(address, routingKey, virtualHost, username, password)

while True:
    #Calculate CPU usage (using code from https://rosettacode.org/wiki/Linux_CPU_utilization)
    with open('/proc/stat') as f:
        fields = [float(column) for column in f.readline().strip().split()[1:]]
    idle, total = fields[3], sum(fields)
    idle_delta, total_delta = idle - last_idle, total - last_total
    last_idle, last_total = idle, total
    cpu_utilization = 1.0 * (1.0 - idle_delta / total_delta)

    #Get Network Usage Data (with help from serverfault.com/questions/533513/how-to-get-tx-rx-bytes-without-ifconfig)
    with open('/proc/net/dev') as f:
        network_info = f.readlines()

    #Calculate network usage by eth0
    eth0_rx, eth0_tx = int(network_info[4].split()[1]), int(network_info[4].split()[9])
    eth0_rx_throughput, eth0_tx_throughput = eth0_rx - eth0_rx_last, eth0_tx - eth0_tx_last
    eth0_rx_last, eth0_tx_last = eth0_rx, eth0_tx

    #Calculate network usage by lo
    lo_rx, lo_tx = int(network_info[3].split()[1]), int(network_info[3].split()[9])
    lo_rx_throughput, lo_tx_throughput = lo_rx - lo_rx_last, lo_tx - lo_tx_last
    lo_rx_last, lo_tx_last = lo_rx, lo_tx

    #Calculate network usage by wlan0
    wlan0_rx, wlan0_tx = int(network_info[2].split()[1]), int(network_info[2].split()[9])
    wlan0_rx_throughput, wlan0_tx_throughput = wlan0_rx - wlan0_rx_last, wlan0_tx - wlan0_tx_last
    wlan0_rx_last, wlan0_tx_last = wlan0_rx, wlan0_tx

    if (counter > 0):
        #Print values for debugging
        print ('_____________________________________ - ' + str(counter) + " seconds elapsed")
        print ('CPU utilization: ' + str(cpu_utilization))
        print ('eth0 rx: ' + str(eth0_rx_throughput) + ', eth0 tx: ' + str(eth0_tx_throughput))
        print ('lo rx: ' + str(lo_rx_throughput) + ', lo tx: ' + str(lo_tx_throughput))
        print ('wlan0 rx: ' + str(wlan0_rx_throughput) + ', wlan0 tx: ' + str(wlan0_tx_throughput))

        #Create json object containing the CPU and network usage values
        json_object = {
            "cpu": cpu_utilization,
            "net": {
                "lo": {
                    "rx": lo_rx_throughput,
                    "tx": lo_tx_throughput
                    },
                "eth0": {
                    "rx": eth0_rx_throughput,
                    "tx": eth0_tx_throughput
                    },
                "wlan0": {
                    "rx": wlan0_rx_throughput,
                    "tx": wlan0_tx_throughput
                    }
                }
            }
        #print(json.dumps(json_object))

        #Publish json object using RabbitMQ
        connectionDropped = True # assume that connection was dropped
        while(connectionDropped):
            try:
                rmq_publish(connection, json.dumps(json_object), routingKey)
            except pika.exceptions.ConnectionClosed:
                connection = rmq_open_pub_cxn(address, routingKey, virtualHost, username, password)
            else:
                connectionDropped = False

    #Wait one second before re-calculating values
    counter = counter + wait_time
    sleep(wait_time)

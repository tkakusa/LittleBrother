#!/usr/bin/python3

from pymongo import MongoClient
import rabbitmq_lib as rmq
import json
import pprint
import sys, getopt
client = MongoClient()
db1 = client.host1
db2 = client.host2

posts1 = db1.posts
posts2 = db2.posts

#address='172.29.42.45'
#vhost='little_brother'
#usr='monitor'
#pswd='monitorpassword'
address=''
vhost=''
usr=''
pswd=''
routing_key=''
metrics = {
    "host1": {
        "cpu": {
            "hi": 0,
            "lo": 0 },
        "lo": {
            "rx": {
                "hi": 0,
                "lo": 0 },
            "tx": {
                "hi": 0,
                "lo": 0 },
            },
        "eth0": {
            "rx": {
                "hi": 0,
                "lo": 0 },
            "tx": {
                "hi": 0,
                "lo": 0 },
            },
        "wlan0": {
            "rx": {
                "hi": 0,
                "lo": 0 },
            "tx": {
                "hi": 0,
                "lo": 0 },
            },
        },
    "host2": {
        "cpu": {
            "hi": 0,
            "lo": 0 },
        "lo": {
            "rx": {
                "hi": 0,
                "lo": 0 },
            "tx": {
                "hi": 0,
                "lo": 0 },
            },
        "eth0": {
            "rx": {
                "hi": 0,
                "lo": 0 },
            "tx": {
                "hi": 0,
                "lo": 0 },
            },
        "wlan0": {
            "rx": {
                "hi": 0,
                "lo": 0 },
            "tx": {
                "hi": 0,
                "lo": 0 },
            },
        }
    }
    
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

print ("Address:        ", address)
print ("Virtual Host:   ", vhost)
print ("User Name:      ", usr)
print ("Password:       ", pswd)
print ("Routing Key:    ", routing_key)
        

# When you receive messages, this function will be called. It needs to have these
# arguments to be called properly. The routing key and message itself can be extracted
# as shown in this example method.
def callback(ch, method, properties, body):
    print ("Entered")
    metrics[method.routing_key]['cpu']['hi'] = body[method.routing_key]['cpu']['hi'] if body[method.routing_key]['cpu']['hi'] > metrics[method.routing_key]['cpu']['hi'] else metrics[method.routing_key]['cpu']['hi']
    metrics[method.routing_key]['cpu']['lo'] = body[method.routing_key]['cpu']['lo'] if body[method.routing_key]['cpu']['lo'] < metrics[method.routing_key]['cpu']['lo'] else metrics[method.routing_key]['cpu']['lo']
    metrics[method.routing_key]['lo']['rx']['hi'] = body[method.routing_key]['lo']['rx']['hi'] if body[method.routing_key]['lo']['rx']['hi'] > metrics[method.routing_key]['lo']['rx']['hi'] else metrics[method.routing_key]['lo']['rx']['hi']
    metrics[method.routing_key]['lo']['rx']['lo'] = body[method.routing_key]['lo']['rx']['lo'] if body[method.routing_key]['lo']['rx']['lo'] < metrics[method.routing_key]['lo']['rx']['lo'] else metrics[method.routing_key]['lo']['rx']['lo']
    metrics[method.routing_key]['lo']['tx']['hi'] = body[method.routing_key]['lo']['tx']['hi'] if body[method.routing_key]['lo']['tx']['hi'] > metrics[method.routing_key]['lo']['tx']['hi'] else metrics[method.routing_key]['lo']['tx']['hi']
    metrics[method.routing_key]['lo']['tx']['lo'] = body[method.routing_key]['lo']['tx']['lo'] if body[method.routing_key]['lo']['tx']['lo'] < metrics[method.routing_key]['lo']['tx']['lo'] else metrics[method.routing_key]['lo']['tx']['lo']
    metrics[method.routing_key]['eth0']['rx']['hi'] = body[method.routing_key]['eth0']['rx']['hi'] if body[method.routing_key]['eth0']['rx']['hi'] > metrics[method.routing_key]['eth0']['rx']['hi'] else metrics[method.routing_key]['eth0']['rx']['hi']
    metrics[method.routing_key]['eth0']['rx']['lo'] = body[method.routing_key]['eth0']['rx']['lo'] if body[method.routing_key]['eth0']['rx']['lo'] < metrics[method.routing_key]['eth0']['rx']['lo'] else metrics[method.routing_key]['eth0']['rx']['lo']
    metrics[method.routing_key]['eth0']['tx']['hi'] = body[method.routing_key]['eth0']['tx']['hi'] if body[method.routing_key]['eth0']['tx']['hi'] > metrics[method.routing_key]['eth0']['tx']['hi'] else metrics[method.routing_key]['eth0']['tx']['hi'] 
    metrics[method.routing_key]['eth0']['tx']['lo'] = body[method.routing_key]['eth0']['tx']['lo'] if body[method.routing_key]['eth0']['tx']['lo'] < metrics[method.routing_key]['eth0']['tx']['lo'] else metrics[method.routing_key]['eth0']['tx']['lo']
    metrics[method.routing_key]['wlan0']['rx']['hi'] = body[method.routing_key]['wlan0']['rx']['hi'] if body[method.routing_key]['wlan0']['rx']['hi'] > metrics[method.routing_key]['wlan0']['rx']['hi'] else metrics[method.routing_key]['wlan0']['rx']['hi']
    metrics[method.routing_key]['wlan0']['rx']['lo'] = body[method.routing_key]['wlan0']['rx']['lo'] if body[method.routing_key]['wlan0']['rx']['lo'] < metrics[method.routing_key]['wlan0']['rx']['lo'] else metrics[method.routing_key]['wlan0']['rx']['lo']
    metrics[method.routing_key]['wlan0']['tx']['hi'] = body[method.routing_key]['wlan0']['tx']['hi'] if body[method.routing_key]['wlan0']['tx']['hi'] > metrics[method.routing_key]['wlan0']['tx']['hi'] else metrics[method.routing_key]['wlan0']['tx']['hi']
    metrics[method.routing_key]['wlan0']['tx']['lo'] = body[method.routing_key]['wlan0']['tx']['lo'] if body[method.routing_key]['wlan0']['tx']['lo'] < metrics[method.routing_key]['wlan0']['tx']['lo'] else metrics[method.routing_key]['wlan0']['tx']['lo']
    if (method.routing_key == "host1"):
        posts1.insert_one(json.loads(body.decode("utf-8")))
    elif (method.routing_key == "host2"):
        posts1.insert_one(json.loads(body.decode("utf-8")))
    print(metrics)
#    print(" [x] Rxd from: " + method.routing_key + " Message: " + str(body))

# establish a connection with the rabbitmq broker
connection = rmq.rmq_connection(address, vhost, usr, pswd)

# arbitrary print statement so user knows what's going on
print(" [x] Listening for messages...")

# start listening for messages with the routing keys listed in the second argument
rmq.rmq_subscribe(connection, routing_key, callback)

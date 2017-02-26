import rabbitmq_lib as rmq
from time import sleep
import sys
import json
# arbitrary method of determining which host this is
if(len(sys.argv) > 1):
    host_number = sys.argv[1]
else:
    host_number = input("Which host is this? ")

# establish a connection with the rabbitmq broker
connection = rmq.rmq_connection('172.25.18.104', 'little_brother', 'host'+host_number, 'host'+host_number+'password')


# do things and send messages about it indefinitely
i = 0
while(1):
    message = {
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
    rmq.rmq_publish(connection, json.dumps(message), 'host'+host_number)
    i = i + 1
    sleep(2)
'''
message = 

rmq.rmq_publish(connection, json.dumps(message), 'host'+host_number)
sleep(2)

'''

# close the connection once we're done
connection.close()

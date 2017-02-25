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
connection = rmq.rmq_open_pub_cxn('192.168.1.124', "host"+host_number, 'little_brother', 'host'+host_number, 'host'+host_number+'password')

# do things and send messages about it indefinitely
i = 0
while(1):
    message = {"host": host_number, "message count": i}
    rmq.rmq_publish(connection, json.dumps(message), 'host'+host_number)
    i = i + 1
    sleep(2)

# close the connection once we're done
connection.close()

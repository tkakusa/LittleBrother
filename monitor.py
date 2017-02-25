import rabbitmq_lib as rmq
import sys

# When you receive messages, this function will be called. It needs to have these
# arguments to be called properly. The routing key and message itself can be extracted
# as shown in this example method.
def callback(ch, method, properties, body):
    print(" [x] Rxd from: " + method.routing_key + " Message: " + str(body))

    ch.basic_ack(delivery_tag = method.delivery_tag)

if(len(sys.argv) > 1):
    cur_rkey = sys.argv[1]
else:
    cur_rkey = input("What routing_key are you listening for? ")

# establish a connection with the rabbitmq broker
connection = rmq.rmq_open_sub_cxn(address='192.168.1.124',
                                  callback = callback,
                                  vhost='little_brother',
                                  usr='monitor',
                                  pswd='monitorpassword')

# arbitrary print statement so user knows what's going on
print(" [x] Listening for messages...")

# start listening for messages with the routing keys listed in the second argument
rmq.rmq_subscribe(connection, cur_rkey, callback)

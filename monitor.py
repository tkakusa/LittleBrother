import rabbitmq_lib as rmq

# When you receive messages, this function will be called. It needs to have these
# arguments to be called properly. The routing key and message itself can be extracted
# as shown in this example method.
def callback(ch, method, properties, body):
    print(" [x] Rxd from: " + method.routing_key + " Message: " + str(body))

# establish a connection with the rabbitmq broker
connection = rmq.rmq_connection(address='172.25.17.98',
                                vhost='ittle_brother',
                                usr='monitor',
                                pswd='monitorpassword')

# arbitrary print statement so user knows what's going on
print(" [x] Listening for messages...")

# start listening for messages with the routing keys listed in the second argument
rmq.rmq_subscribe(connection, ["host1", "host2"], callback)

import pika

# Returns a connection to the rabbitmq server described by arguments. The returned
# connection should be closed using '.close()' to make sure message buffers are
# flushed and connection closes gracefully.
#
# @param 'address' = IP address of rabbitmq broker
# @param 'vhost' = vhost on rabbitmq broker that user connects to. Default: '/'
# @param 'usr' = name of user connecting to rabbitmq broker. Default: ''
# @param 'pswd' = password for user connecting to rabbitmq broker. Default: ''
def rmq_connection(address, vhost='/', usr='', pswd=''):
    credentials = pika.PlainCredentials(usr, pswd)

    try:
        connection = pika.BlockingConnection(pika.ConnectionParameters(host=address,
                                                                       port=5672, #default rabbitmq port
                                                                       virtual_host=vhost,
                                                                       credentials=credentials)
    except pika.exceptions.ConnectionClosed:
        print("There was a problem connecting to the server.")
        return None
    else:
        return connection

# Publishes a message to the rabbitmq server based on the connection provided as 'cxn'
#
# @param 'cxn' = existing opened connection to a rabbitmq broker
# @param 'msg' = string message to be sent to broker
# @param 'rkey' = routing key to be associated with the message being sent
def rmq_publish(cxn, msg, rkey):
    if(cxn==None):
        print("Publication Error: Connection provided in argument was not properly established.")
        return

    ch = cxn.channel()

    ch.exchange_declare(exchange='lb_exch',
                        type='direct')

    ch.basic_publish(exchange='lb_exch',
                     routing_key=rkey,
                     body=msg)

# Subscribes to an exchange based on the rkeys provided, and starts listening.
# Listening is blocking, so no code will be executed after this function is called.
# Executes callback function upon receiving a message fitting the rkeys. 'callback'
# has to be declared this way: def [ftn_name](ch, method, properties, body)
#
# @param 'cxn': existing opened connection to a rabbitmq broker
# @param 'rkeys': list of strings that are routing keys that this subscription will listen for
# @param 'callback': callback function for when a message is received
def rmq_subscribe(cxn, rkeys, callback):
    if(cxn==None):
        print("Subscription Error: Connection provided in argument was not properly established.")
        return

    ch = cxn.channel()

    ch.exchange_declare(exchange='lb_exch',
                        type='direct')

    result = ch.queue_declare(exclusive=True)
    queue_name = result.method.queue

    for key in rkeys:
        ch.queue_bind(exchange='lb_exch',
                      queue=queue_name,
                      routing_key=key)

    ch.basic_consume(callback,
                     queue=queue_name,
                     no_ack=True)

    ch.start_consuming()

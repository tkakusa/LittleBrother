#Net Apps - Assignment #2 - Host

#imports
from __future__ import print_function
import sys, os, getopt
from time import sleep

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

#Declare and initialize variables
last_idle     = last_total    = 0
eth0_rx_last  = eth0_tx_last  = 0
lo_rx_last    = lo_tx_last    = 0
wlan0_rx_last = wlan0_tx_last = 0

last_eth0  = eth0_total  = 0
last_lo    = lo_total    = 0
last_wlan0 = wlan0_total = 0
counter    = 0

while True:
    #Calculate CPU usage
    with open('/proc/stat') as f:
        fields = [float(column) for column in f.readline().strip().split()[1:]]
    idle, total = fields[3], sum(fields)
    idle_delta, total_delta = idle - last_idle, total - last_total
    last_idle, last_total = idle, total
    cpu_utilization = 1.0 * (1.0 - idle_delta / total_delta)
    print(cpu_utilization)
    #Get Network Usage Data
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

    #Print values for debugging
##    print ('_____________________________________ - ' + str(counter) + " seconds elapsed")
##    print ('CPU utilization: ' + str(cpu_utilization))
##    print ('eth0 rx: ' + str(eth0_rx_throughput) + ', eth0 tx: ' + str(eth0_tx_throughput))
##    print ('lo rx: ' + str(lo_rx_throughput) + ', lo tx: ' + str(lo_tx_throughput))
##    print ('wlan0 rx: ' + str(wlan0_rx_throughput) + ', wlan0 tx: ' + str(wlan0_tx_throughput))

    #Create json object containing the CPU and network usage values
    json_object = '{\n\t\"net\": {\n' + \
                  '\t\t\"lo\": {\n' + \
                  '\t\t\t\"rx\": ' + str(lo_rx_throughput) + ',\n' + \
                  '\t\t\t\"tx\": ' + str(lo_tx_throughput) + '\n' + \
                  '\t\t},\n\t\t\"wlan0\": {\n' + \
                  '\t\t\t\"rx\": ' + str(wlan0_rx_throughput) + ',\n' + \
                  '\t\t\t\"tx\": ' + str(wlan0_tx_throughput) + '\n' + \
                  '\t\t},\n\t\t\"eth0\": {\n' + \
                  '\t\t\t\"rx\": ' + str(eth0_rx_throughput) + ',\n' + \
                  '\t\t\t\"tx\": ' + str(eth0_tx_throughput) + '\n' + \
                  '\t\t}\n\t},\n' + \
                  '\t\"cpu\": ' + str(cpu_utilization) + '\n' + \
                  '}'

    print(json_object)
    #Wait one second before re-calculating values
    sleep(1)
    counter = counter + 1

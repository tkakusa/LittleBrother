# LittleBrother

Steps to set up the RabbitMQ Message Broker on a Rasberry Pi running Raspbian
1) Follow the instructions on "www.rabbitmq.com/install-debian.html" under the heading "Using rabbitmq.com APT Repository"
2) Run the following commands to set up the VHost:
  2a) sudo rabbitmqctl add_vhost "little_brother" 
  2b) sudo rabbitmqctl add_user "host1" "host1password"
  2c) sudo rabbitmqctl add_user "host2" "host2password" 
  2d) sudo rabbitmqctl add_user "monitor" "monitorpassword"
  2e) sudo rabbitmqctl set_permissions -p "little_brother" host1 ".*" ".*" ".*"
  2f) sudo rabbitmqctl set_permissions -p "little_brother" host2 ".*" ".*" ".*"
  2g) sudo rabbitmqctl set_permissions -p "little_brother" monitor ".*" ".*" ".*"
  
To setup the noSQL Database 
1) Follow the instructions listed on "https://api.mongodb.com/python/current/installation.html"
2) Start the database using the command "mongod"
3) Use the tutorial on this page: "https://api.mongodb.com/python/current/tutorial.html" to get the commands necessary for using the database

For the RabbitMQ wrapper functions, the "pika" Python library be installed. 

For the host Raspberry Pi, run the pistatsd.py script to begin sending out CPU and Network data formatted as a JSON object to the server.

For the monitor Raspberry Pi, run the pistatsview.py script to begin monitoring the host's CPU usage.
The monitor Pi should have the following hardware connections:
  The ground of the RGB LED should be connected to a ground pin on the Pi
  The red, green, and blue connectors of the RGB LED should be connected to pins 13, 19, and 26 respectively on the Pi,
    each through a 330 ohm resistor.

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

For the RabbitMQ wrapper functions, the "pika" Python library be installed. 

For the host Raspberry Pi, run the pistatsd.py script to begin sending out CPU and Network data formatted as a JSON object to the server.


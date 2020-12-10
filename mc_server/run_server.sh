echo 'Changing directory to server folder...'
cd /home/ec2-user/server
echo 'Starting up server...'
java -Xmx1024M -Xms1024M -jar server.jar nogui
#!/bin/bash
#PATH: /home/<USER>/code/Crypt

user=$(whoami)
echo "Changing directory owner to $user"
sudo chown -R $user .

echo "Compiling..." 
(cd frontend/; npm run build > /dev/null)
echo "Compiled!"
echo 

echo "Moving compiled version to nginx serving directory..."
cp -r frontend/build/* www
echo "Done!"
echo 

echo "Frontend compiled and moved to nginx serving directory!"




# Remote Render Server

This is a simple project which acts as the destination for the remote renderer located in the led-sectional. It providers two functionalities through different scripts.

The remote renderer send requests to set LED colors via UDP packets. This enables you to work on and enhance led sectional software without needing to run the software on a slow raspberry PI and still have some way to visualize the LEDs. 

Two scripts are provided for this purpose, but provide different functionality.

By default the remote renderer listens on port 5006. The web server option runs on port 5005.

## pi_udp_server.py

If you have a poster all wired up you can run this script on the raspberry pi. It will listen for those UDP packets sent out by the remote renderer and updates the lights accordingly. 

    # Edit the pi_udp_server.py to setup 
    # the correct number of LEDs and run.
    sudo python3.7 pi_udp_server.py
    

## udp_server.py

If you don't yet have a poster wired up and you want to work on the software. Setup the remote renderer and use the udp_server.py script. 

This is a simple webserver and angular application which visually creates LEDs on a web page which are then updated in real time in reponse to those same UDP packets. 

    cd angular
    ng build
    cd ..
    python server.py
    ... open browser to http://localhost:5005
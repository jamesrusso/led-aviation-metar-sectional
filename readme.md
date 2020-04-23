# LED Sectional Map

This is a major rewrite of Dylan Rush's and John Marzulli's great sectional application. I re-wrote it to add some additional features like make it completely modern clean multi-threaded Python and also used Flask to add a RESTful API to enable you to configure the appplication from a browser.

The browser application will even download the current METAR to make sure you are adding valid identifiers which do have ASOS/AWOS.

## Todo

- Add support for setting up WIFI
    - Bluetooth LE?
    - Button to enable Wifi "server mode"
- Add support for alternative display modes
    - personal minimum mode
    - wind mode
- Add support for control via AWS/SQS
- Installer?



## Support for Remote Renderers

In addition to support for WS2801 and WS2811 LEDS, I also added support for a remote renderer which allows you to run the software on your computer and still manipulate the LEDS on the raspberry PI. This is accomplished by sending UDP packets to a service (included) running on the Pi. This is primarily used for debugging and development. See the remote-render-server.

## Configuration File

    The configuration file is a YAML file in config/config.yaml

### Conditions Table

        The conditions table lists the various conditions (IFR, INOP, INVALID, LIFT, MVFR, NIGHT, NIGHT_DARK, SMOKE and VFR). The color value is a color in #rrggbb format and then another value to indicate if the LED should blink.

                conditions:
                    IFR:
                        blink: false
                        color: '#ff0000'
                    INOP:
                        blink: false
                        color: '#000000'
                    INVALID:
                        blink: false
                        color: '#ffc0cb'
                    LIFR:
                        blink: false
                        color: '#ff00ff'
                    MVFR:
                        blink: false
                        color: '#0000ff'
                    NIGHT:
                        blink: false
                        color: '#ffff00'
                    NIGHT_DARK:
                        blink: false
                        color: '#010105'
                    SMOKE:
                        blink: false
                        color: '#323232'
                    VFR:
                        blink: false
                        color: '#00ff00'

### Timeout/Intervals

            metar_refresh_interval: <int>
                The number of minutes between each METAR refresh.
            
            sunrise_refresh_interval: <int>
                The number of minutes between obtaining new sunrise/sunset info. 
            
            metar_invalid_age: <int>
                The number of minutes before an METAR becomes invalid.
            
            metar_inop_age: <int>
                The number of minutes before a METAR becomes INOP

            night_lights: <true/false>
                Use the night_light functionality
            
            pixel_map: <dict>
                a table listing each LED and its corresponding airport. The key is the 
                led and the value is the airport identifier
            
            pixel_count: <int>
                the number of pixels on the string (this is setup via the webapp normally)
            
            setup_complete: <true/false>
                if true, when the application starts it'll do a self-test and launch the threads.

            renderer_config <dict>
                a table with the name of the renderer along with any arguments that renderer requires.


## Setup

    First you may need to edit the config/config.yaml file and setup the correct renderer. The default configuration is ws2811 on D18.

    The WS2811 module needs to run as root, so login as root or su - to root and install
    the following modules:

    pip3 install pyyaml colour python-dateutil coloredlogs

    cd sectional-webapp
    ng build --watch
,    
    python main.py

    use a browser to http://localhost:5001 and click on the setup menu at the top.

    It will ask you the number of LEDS, peform a self test, and then light up each LED as you work through assigning each LED
    to a airport using its identifier (KLEE, etc) 

    Once you finish, click finalize and it will start everything. 


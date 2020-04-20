# LED Sectional Map

This is a major rewrite of Dylan Rush's and John Marzulli's great sectional application. I re-wrote it to add some additional features like make it completely modern clean multi-threaded Python and also used Flask to add a RESTful API to enable you to configure the appplication from a browser.

The browser application will even download the current METAR to make sure you are adding valid identifiers which do have ASOS/AWOS.

## Support for Remote Renderers

In addition to support for WS2801 and WS2811 LEDS, I also added support for a remote renderer which allows you to run the software on your computer and still manipulate the LEDS on the raspberry PI. This is accomplished by sending UDP packets to a service (included) running on the Pi. This is primarily used for debugging and development. See the remote-render-server.



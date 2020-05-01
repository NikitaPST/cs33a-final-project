# Chat App

Simple chat application. My final project for CS33a class. It incorportes usage of django channels to access websockets. It also use several public API.

*Class: CSCI E-33a "Web Programming with Python and JavaScript"*

*Instructor: Brian Yu*

*TA: Barbara Karakyriakou*

![Screenshot](/screen.png "Screenshot")

### Dependencies

*Server side:*

- *channels 2.4.0* - extends Django abilities beyond to handle WebSockets.
- *django 2.2.5* - free and open-source web framework, which follows the model-template-view architectural pattern.

*Client side:* (accessed through CDN)

- *moment 2.24.0* - a lightweight date library for parsing, validating, manipulating, and formatting dates.
- *mustache 3.1.0* - logic-less template system.

### Chat commands

- *!image \[url\]* - posts image into a chat room.
- *!location* - returns your current loction (you must allow browser to send geolocation data).
- *!weather* - returns current weather for your loction (you must allow browser to send geolocation data).

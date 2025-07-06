# Getting started with Lynxmotion servomotors

## Introduction

For creating your own robotic body, we used [Lynxmotion smart servomotors](https://wiki.lynxmotion.com/info/wiki/lynxmotion/view/ses-v2/lynxmotion-smart-servo/).

![](https://wiki.lynxmotion.com/info/wiki/lynxmotion/download/ses-v2/lynxmotion-smart-servo/WebHome/LSS-Servo-Horns.PNG?width=350&height=350)

These motors are easier to control than a standard servomotor because they 
include a microcontroller that implements a serial communication protocol. The electronics inside the servo include the following:
- H-bridge motor controller
- Microcontroller (Cortex M0)
- Magnetic position sensor
- Voltage sensor
- Temperature sensor
- Current sensor

In [serial communication](https://learn.sparkfun.com/tutorials/serial-communication), bits are transmitted in sequence (in opposition to parallel communication), and the number of wires is minimal: basically a receiver RX, a transmitter TX, and GND.

![](https://cdn.sparkfun.com/r/700-700/assets/2/5/c/4/5/50e1ce8bce395fb62b000000.png)

The block of circuitry responsible for implementing serial communication is called universal asynchronous receiver-transmitter (UART).

Serial communication is available basically in any microcontroller.

Each Lynxmotion servo has an ID (a number) that is used in the communication. In this project, we have many servo and for this we create loop and each servo ID went through this loop and perform specific movement.
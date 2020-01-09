//upload this on the Arduino which gets carriers' buttons 

//this Arduino only uses I2C communication

//enable i2c communication with other Arduino
#include <Wire.h>

void setup()
{
    pinMode(2, INPUT);  //button input
    pinMode(3, INPUT);  //button input
    pinMode(4, INPUT);  //button input
    pinMode(5, INPUT);  //button input
    pinMode(6, INPUT);  //button input
    pinMode(7, INPUT);  //button input
    pinMode(8, INPUT);  //button input
    pinMode(9, INPUT);  //button input
    pinMode(10, INPUT); //button input
    pinMode(11, INPUT); //button input
    pinMode(12, INPUT); //button input
    pinMode(13, INPUT); //button input
    Wire.begin();   //begin I2C communication as I2C master
}

void loop()
{
    int a;  //get button status
    char data;  //use 1 byte data for I2C communication
    a = digitalRead(2);
    if (a > 0) {
        data = 11;
        Wire.write(data);   //send the data to other Arduino
    }
    a = digitalRead(3);
    if (a > 0) {
        data = 12;
        Wire.write(data);   //send the data to other Arduino
    }
    a = digitalRead(4);
    if (a > 0) {
        data = 13;
        Wire.write(data);   //send the data to other Arduino
    }
    a = digitalRead(5);
    if (a > 0) {
        data = 14;
        Wire.write(data);   //send the data to other Arduino
    }
    a = digitalRead(6);
    if (a > 0) {
        data = 15;
        Wire.write(data);   //send the data to other Arduino
    }
    a = digitalRead(7);
    if (a > 0) {
        data = 16;
        Wire.write(data);   //send the data to other Arduino
    }
    a = digitalRead(8);
    if (a > 0) {
        data = 17;
        Wire.write(data);   //send the data to other Arduino
    }
    a = digitalRead(9);
    if (a > 0) {
        data = 18;
        Wire.write(data);   //send the data to other Arduino
    }
    a = digitalRead(10);
    if (a > 0) {
        data = 19;
        Wire.write(data);   //send the data to other Arduino
    }
    a = digitalRead(11);
    if (a > 0) {
        data = 20;
        Wire.write(data);   //send the data to other Arduino
    }
    a = digitalRead(12);
    if (a > 0) {
        data = 21;
        Wire.write(data);   //send the data to other Arduino
    }
    a = digitalRead(13);
    if (a > 0) {
        data = 22;
        Wire.write(data);   //send the data to other Arduino
    }
}
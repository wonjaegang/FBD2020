//upload this on the Arduino which gets layers' buttons 

//this Arduino only uses SoftwareSerial communication

//enable software serial communication with other Arduino
#include <SoftwareSerial.h>
SoftwareSerial button(12, 13);  //SoftwareSerial pin

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
    button.begin(9600); //begin SoftwareSerial communication, BPS:9600
}

void loop()
{
    int a;  //get button status
    char data;
    a = digitalRead(2);
    if (a > 0) {
        data = 1;
        button.write(data);   //send the data to other Arduino
    }
    a = digitalRead(3);
    if (a > 0) {
        data = 2;
        button.write(data);   //send the data to other Arduino
    }
    a = digitalRead(4);
    if (a > 0) {
        data = 3;
        button.write(data);   //send the data to other Arduino
    }
    a = digitalRead(5);
    if (a > 0) {
        data = 4;
        button.write(data);   //send the data to other Arduino
    }
    a = digitalRead(6);
    if (a > 0) {
        data = 5;
        button.write(data);   //send the data to other Arduino
    }
    a = digitalRead(7);
    if (a > 0) {
        data = 6;
        button.write(data);   //send the data to other Arduino
    }
    a = digitalRead(8);
    if (a > 0) {
        data = 7;
        button.write(data);   //send the data to other Arduino
    }
    a = digitalRead(9);
    if (a > 0) {
        data = 8;
        button.write(data);   //send the data to other Arduino
    }
    a = digitalRead(10);
    if (a > 0) {
        data = 9;
        button.write(data);   //send the data to other Arduino
    }
    a = digitalRead(11);
    if (a > 0) {
        data = 10;
        button.write(data);   //send the data to other Arduino
    }
}
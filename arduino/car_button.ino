//upload this on the Arduino which gets cars' button

//this Arduino only uses I2C communication

//enable i2c communication with other Arduino
#include <Wire.h>

int state2=2, state3=2, state4=2, state5=2, state6=2, state7=2, state8=2, state9=2, state10=2, state11=2, state12=2, state13=2;

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
    char data;
    a = digitalRead(2);
    if (a != state2) {
        data = 11;
        state2=a;
        Wire.write(data);   //send the data to other Arduino
    }
    a = digitalRead(3);
    if (a != state3) {
        data = 12;
        state3=a;
        Wire.write(data);   //send the data to other Arduino
    }
    a = digitalRead(4);
    if (a != state4) {
        data = 13;
        state4=a;
        Wire.write(data);   //send the data to other Arduino
    }
    a = digitalRead(5);
    if (a != state5) {
        data = 14;
        state5=a;
        Wire.write(data);   //send the data to other Arduino
    }
    a = digitalRead(6);
    if (a != state6) {
        data = 15;
        state6=a;
        Wire.write(data);   //send the data to other Arduino
    }
    a = digitalRead(7);
    if (a != state7) {
        data = 16;
        state7=a;
        Wire.write(data);   //send the data to other Arduino
    }
    a = digitalRead(8);
    if (a != state8) {
        data = 17;
        state8=a;
        Wire.write(data);   //send the data to other Arduino
    }
    a = digitalRead(9);
    if (a != state9) {
        data = 18;
        state9=a;
        Wire.write(data);   //send the data to other Arduino
    }
    a = digitalRead(10);
    if (a != state10) {
        data = 19;
        state10=a;
        Wire.write(data);   //send the data to other Arduino
    }
    a = digitalRead(11);
    if (a != state11) {
        data = 20;
        state11=a;
        Wire.write(data);   //send the data to other Arduino
    }
}

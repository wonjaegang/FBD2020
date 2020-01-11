//upload this on the Arduino which gets cars' button

//this Arduino only uses I2C communication

//enable i2c communication with other Arduino
#include <Wire.h>
#define Slave 0x10

int state2 = 2, state3 = 2, state4 = 2, state5 = 2, state6 = 2, state7 = 2, state8 = 2, state9 = 2, state10 = 2, state11 = 2, state12 = 2, state13 = 2;

void setup()
{
    pinMode(2, INPUT); //button input
    pinMode(3, INPUT); //button input
    pinMode(4, INPUT); //button input
    pinMode(5, INPUT); //button input
    pinMode(6, INPUT); //button input
    pinMode(7, INPUT); //button input
    pinMode(8, INPUT); //button input
    pinMode(9, INPUT); //button input
    pinMode(10, INPUT); //button input
    pinMode(11, INPUT); //button input
    pinMode(12, INPUT); //button input
    pinMode(13, INPUT); //button input
    Wire.begin(); //begin I2C communication as I2C master
}

void loop()
{
    int a; //get button status
    char data;
    a = digitalRead(2);
    if (a != state2) {
        data = 'K';
        state2 = a;
        Wire.beginTransmission(Slave);
        Wire.write(data); //send the data to other Arduino
        Wire.endTransmission();
    }
    a = digitalRead(3);
    if (a != state3) {
        data = 'L';
        state3 = a;
        Wire.beginTransmission(Slave);
        Wire.write(data); //send the data to other Arduino
        Wire.endTransmission();
    }
    a = digitalRead(4);
    if (a != state4) {
        data = 'M';
        state4 = a;
        Wire.beginTransmission(Slave);
        Wire.write(data); //send the data to other Arduino
        Wire.endTransmission();
    }
    a = digitalRead(5);
    if (a != state5) {
        data = 'N';
        state5 = a;
        Wire.beginTransmission(Slave);
        Wire.write(data); //send the data to other Arduino
        Wire.endTransmission();
    }
    a = digitalRead(6);
    if (a != state6) {
        data = 'O';
        state6 = a;
        Wire.beginTransmission(Slave);
        Wire.write(data); //send the data to other Arduino
        Wire.endTransmission();
    }
    a = digitalRead(7);
    if (a != state7) {
        data = 'P';
        state7 = a;
        Wire.beginTransmission(Slave);
        Wire.write(data); //send the data to other Arduino
        Wire.endTransmission();
    }
    a = digitalRead(8);
    if (a != state8) {
        data = 'Q';
        state8 = a;
        Wire.beginTransmission(Slave);
        Wire.write(data); //send the data to other Arduino
        Wire.endTransmission();
    }
    a = digitalRead(9);
    if (a != state9) {
        data = 'R';
        state9 = a;
        Wire.beginTransmission(Slave);
        Wire.write(data); //send the data to other Arduino
        Wire.endTransmission();
    }
    a = digitalRead(10);
    if (a != state10) {
        data = 'S';
        state10 = a;
        Wire.beginTransmission(Slave);
        Wire.write(data); //send the data to other Arduino
        Wire.endTransmission();
    }
    a = digitalRead(11);
    if (a != state11) {
        data = 'T';
        state11 = a;
        Wire.beginTransmission(Slave);
        Wire.write(data); //send the data to other Arduino
        Wire.endTransmission();
    }
    a = digitalRead(12);
    if (a != state12) {
        data = 'U';
        state12 = a;
        Wire.beginTransmission(Slave);
        Wire.write(data); //send the data to other Arduino
        Wire.endTransmission();
    }
    a = digitalRead(13);
    if (a != state13) {
        data = 'V';
        state13 = a;
        Wire.beginTransmission(Slave);
        Wire.write(data); //send the data to other Arduino
        Wire.endTransmission();
    }
}

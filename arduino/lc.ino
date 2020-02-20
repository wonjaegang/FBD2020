//upload this on the Arduino which gets cars' button

//this Arduino only uses I2C communication

//enable i2c communication with other Arduino
#include <Wire.h>
#define Slave 0x10

int state2 = 1, state3 = 1, state4 = 1, state5 = 1, state6 = 1, state7 = 1, state8 = 1, state9 = 1, state10 = 1, state11 = 1, state12 = 1, state13 = 1;

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
    if (a == 1 && state2 == 1) {
        data = 'K';
        state2 = 0;
        Wire.beginTransmission(Slave);
        Wire.write(data); //send the data to other Arduino
        Wire.endTransmission();
    }
    if (a == 0)
        state2 = 1;

    a = digitalRead(3);
    if (a == 1 && state3 == 1) {
        data = 'L';
        state3 = 0;
        Wire.beginTransmission(Slave);
        Wire.write(data); //send the data to other Arduino
        Wire.endTransmission();
    }
    if (a == 0)
        state3 = 1;

    a = digitalRead(4);
    if (a == 1 && state4 == 1) {
        data = 'M';
        state4 = 0;
        Wire.beginTransmission(Slave);
        Wire.write(data); //send the data to other Arduino
        Wire.endTransmission();
    }
    if (a == 0)
        state4 = 1;

    a = digitalRead(5);
    if (a == 1 && state5 == 1) {
        data = 'N';
        state5 = 0;
        Wire.beginTransmission(Slave);
        Wire.write(data); //send the data to other Arduino
        Wire.endTransmission();
    }
    if (a == 0)
        state5 = 1;

    a = digitalRead(6);
    if (a == 1 && state6 == 1) {
        data = 'O';
        state6 = 0;
        Wire.beginTransmission(Slave);
        Wire.write(data); //send the data to other Arduino
        Wire.endTransmission();
    }
    if (a == 0)
        state6 = 1;

    a = digitalRead(7);
    if (a == 1 && state7 == 1) {
        data = 'P';
        state7 = 0;
        Wire.beginTransmission(Slave);
        Wire.write(data); //send the data to other Arduino
        Wire.endTransmission();
    }
    if (a == 0)
        state7 = 1;

    a = digitalRead(8);
    if (a == 1 && state8 == 1) {
        data = 'Q';
        state8 = 0;
        Wire.beginTransmission(Slave);
        Wire.write(data); //send the data to other Arduino
        Wire.endTransmission();
    }
    if (a == 0)
        state8 = 1;

    a = digitalRead(9);
    if (a == 1 && state9 == 1) {
        data = 'R';
        state9 = 0;
        Wire.beginTransmission(Slave);
        Wire.write(data); //send the data to other Arduino
        Wire.endTransmission();
    }
    if (a == 0)
        state9 = 1;

    a = digitalRead(10);
    if (a == 1 && state10 == 1) {
        data = 'S';
        state10 = 0;
        Wire.beginTransmission(Slave);
        Wire.write(data); //send the data to other Arduino
        Wire.endTransmission();
    }
    if (a == 0)
        state10 = 1;

    a = digitalRead(11);
    if (a == 1 && state11 == 1) {
        data = 'T';
        state11 = 0;
        Wire.beginTransmission(Slave);
        Wire.write(data); //send the data to other Arduino
        Wire.endTransmission();
    }
    if (a == 0)
        state11 = 1;

    a = digitalRead(12);
    if (a == 1 && state12 == 1) {
        data = 'U';
        state12 = 0;
        Wire.beginTransmission(Slave);
        Wire.write(data); //send the data to other Arduino
        Wire.endTransmission();
    }
    if (a == 0)
        state12 = 1;

    a = digitalRead(13);
    if (a == 1 && state13 == 1) {
        data = 'V';
        state13 = 0;
        Wire.beginTransmission(Slave);
        Wire.write(data); //send the data to other Arduino
        Wire.endTransmission();
    }
    if (a == 0)
        state13 = 1;
}

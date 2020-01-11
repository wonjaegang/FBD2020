//upload this on the Arduino which gets layers' buttons 

//this Arduino only uses SoftwareSerial communication

//enable software serial communication with other Arduino
#include <SoftwareSerial.h>
SoftwareSerial button(12, 13);  //SoftwareSerial pin

int state2=2, state3=2, state4=2, state5=2, state6=2, state7=2, state8=2, state9=2, state10=2, state11=2;

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
    if (a != state2) {
        data = 'A';
        state2=a;
        button.write(data);   //send the data to other Arduino
    }
    a = digitalRead(3);
    if (a != state3) {
        data = 'B';
        state3=a;
        button.write(data);   //send the data to other Arduino
    }
    a = digitalRead(4);
    if (a != state4) {
        data = 'C';
        state4=a;
        button.write(data);   //send the data to other Arduino
    }
    a = digitalRead(5);
    if (a != state5) {
        data = 'D';
        state5=a;
        button.write(data);   //send the data to other Arduino
    }
    a = digitalRead(6);
    if (a != state6) {
        data = 'E';
        state6=a;
        button.write(data);   //send the data to other Arduino
    }
    a = digitalRead(7);
    if (a != state7) {
        data = 'F';
        state7=a;
        button.write(data);   //send the data to other Arduino
    }
    a = digitalRead(8);
    if (a != state8) {
        data = 'G';
        state8=a;
        button.write(data);   //send the data to other Arduino
    }
    a = digitalRead(9);
    if (a != state9) {
        data = 'H';
        state9=a;
        button.write(data);   //send the data to other Arduino
    }
    a = digitalRead(10);
    if (a != state10) {
        data = 'I';
        state10=a;
        button.write(data);   //send the data to other Arduino
    }
    a = digitalRead(11);
    if (a != state11) {
        data = 'J';
        state11=a;
        button.write(data);   //send the data to other Arduino
    }
}
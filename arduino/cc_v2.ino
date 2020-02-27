//upload this on the Arduino which gets cc

//for OddEvenSplitAlgorithm and HighLowSplitAlgorithm

//this Arduino only uses SoftwareSerial communication

//enable software serial communication with other Arduino
#include <SoftwareSerial.h>
SoftwareSerial button(12, 13); //SoftwareSerial pin

//save buttons' states
int state2 = 1, state3 = 1, state4 = 1, state5 = 1, state6 = 1, state7 = 1, state8 = 1, state9 = 1, state10 = 1, state11 = 1;

void setup()
{
    //set pins as buttons
    pinMode(2, INPUT);
    pinMode(3, INPUT);
    pinMode(4, INPUT);
    pinMode(5, INPUT);
    pinMode(6, INPUT);
    pinMode(7, INPUT);
    pinMode(8, INPUT);
    pinMode(9, INPUT);
    pinMode(10, INPUT);
    pinMode(11, INPUT);
    //begin SoftwareSerial communication, BPS:9600
    button.begin(9600);
}

void loop()
{
    //save button status
    int a;
    //data to send to the other Arduino and PC
    char data;

    a = digitalRead(2);
    if (a == 1 && state2 == 1) {
        state2 = 0;
        int counts = 0;
        while(a==1)
        {
            //check the button pressed time
            a=digitalRead(2);
            counts = counts + 1;
            delay(100);
        }
        state2 = 1;
        //send the data to the other Arduino
        if (counts < 5)
            data = 'a';
        else
            data = 'b';
        button.write(data); 
    }
    if (a == 0)
        state2 = 1;

    a = digitalRead(3);
    if (a == 1 && state3 == 1) {
        data = 'B';
        state3 = 0;
        //send the data to the other Arduino
        button.write(data);
    }
    if (a == 0)
        state3 = 1;

    a = digitalRead(4);
    if (a == 1 && state4 == 1) {
        state4 = 0;
        int counts = 0;
        while(a==1)
        {
            //check the button pressed time
            a=digitalRead(4);
            counts = counts + 1;
            delay(100);
        }
        state4 = 1;
        //send the data to the other Arduino
        if (counts < 5)
            data = 'c';
        else
            data = 'd';
        button.write(data);
    }

    a = digitalRead(5);
    if (a == 1 && state5 == 1) {
        data = 'D';
        state5 = 0;
        //send the data to the other Arduino
        button.write(data);
    }
    if (a == 0)
        state5 = 1;

    a = digitalRead(6);
    if (a == 1 && state6 == 1) {
        data = 'E';
        state6 = 0;
        //send the data to the other Arduino
        button.write(data);
    }
    if (a == 0)
        state6 = 1;

    a = digitalRead(7);
    if (a == 1 && state7 == 1) {
        data = 'F';
        state7 = 0;
        //send the data to the other Arduino
        button.write(data); 
    }
    if (a == 0)
        state7 = 1;

    a = digitalRead(8);
    if (a == 1 && state8 == 1) {
        data = 'G';
        state8 = 0;
        //send the data to the other Arduino
        button.write(data); 
    }
    if (a == 0)
        state8 = 1;

    a = digitalRead(9);
    if (a == 1 && state9 == 1) {
        data = 'H';
        state9 = 0;
        //send the data to the other Arduino
        button.write(data);
    }
    if (a == 0)
        state9 = 1;

    a = digitalRead(10);
    if (a == 1 && state10 == 1) {
        data = 'I';
        state10 = 0;
        //send the data to the other Arduino
        button.write(data); 
    }
    if (a == 0)
        state10 = 1;

    a = digitalRead(11);
    if (a == 1 && state11 == 1) {
        data = 'J';
        state11 = 0;
        //send the data to the other Arduino
        button.write(data);
    }
    if (a == 0)
        state11 = 1;
}

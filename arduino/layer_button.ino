#include <SoftwareSerial.h>
SoftwareSerial button(12, 13);

void setup()
{
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
    button.begin(9600);
}

void loop()
{
    int a;
    char data;
    a = digitalRead(2);
    if (a > 0) {
        data = 1;
        button.write(data);
    }
    a = digitalRead(3);
    if (a > 0) {
        data = 2;
        button.write(data);
    }
    a = digitalRead(4);
    if (a > 0) {
        data = 3;
        button.write(data);
    }
    a = digitalRead(5);
    if (a > 0) {
        data = 4;
        button.write(data);
    }
    a = digitalRead(6);
    if (a > 0) {
        data = 5;
        button.write(data);
    }
    a = digitalRead(7);
    if (a > 0) {
        data = 6;
        button.write(data);
    }
    a = digitalRead(8);
    if (a > 0) {
        data = 7;
        button.write(data);
    }
    a = digitalRead(9);
    if (a > 0) {
        data = 8;
        button.write(data);
    }
    a = digitalRead(10);
    if (a > 0) {
        data = 9;
        button.write(data);
    }
    a = digitalRead(11);
    if (a > 0) {
        data = 10;
        button.write(data);
    }
}
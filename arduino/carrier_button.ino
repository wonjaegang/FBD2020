#include <Wire.h>

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
    pinMode(12, INPUT);
    pinMode(13, INPUT);
    Wire.begin();
}

void loop()
{
    int a;
    char data;
    a = digitalRead(2);
    if (a > 0) {
        data = 11;
        Wire.write(data);
    }
    a = digitalRead(3);
    if (a > 0) {
        data = 12;
        Wire.write(data);
    }
    a = digitalRead(4);
    if (a > 0) {
        data = 13;
        Wire.write(data);
    }
    a = digitalRead(5);
    if (a > 0) {
        data = 14;
        Wire.write(data);
    }
    a = digitalRead(6);
    if (a > 0) {
        data = 15;
        Wire.write(data);
    }
    a = digitalRead(7);
    if (a > 0) {
        data = 16;
        Wire.write(data);
    }
    a = digitalRead(8);
    if (a > 0) {
        data = 17;
        Wire.write(data);
    }
    a = digitalRead(9);
    if (a > 0) {
        data = 18;
        Wire.write(data);
    }
    a = digitalRead(10);
    if (a > 0) {
        data = 19;
        Wire.write(data);
    }
    a = digitalRead(11);
    if (a > 0) {
        data = 20;
        Wire.write(data);
    }
    a = digitalRead(12);
    if (a > 0) {
        data = 21;
        Wire.write(data);
    }
    a = digitalRead(13);
    if (a > 0) {
        data = 22;
        Wire.write(data);
    }
}
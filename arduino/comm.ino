#include <Wire.h>
#define Slave 0x10

#include <SoftwareSerial.h>
SoftwareSerial button(12, 13);

int b = 2;
int c = 2;
int d = 2;
int e = 2;

void setup()
{
    pinMode(2, OUTPUT);
    pinMode(3, INPUT);
    pinMode(4, INPUT);
    pinMode(5, INPUT);
    pinMode(6, INPUT);
    digitalWrite(2, HIGH);
    Wire.begin(Slave);
    Wire.onReceive(receiveFromMaster);
    button.begin(9600);
    Serial.begin(9600);
}

char data_i2c;
char data_serial;

void loop()
{
    if (button.available() > 0) {
        data_serial = button.read();
        Serial.write(data_serial);
        data_serial = 0;
    }
    int a;
    char data;
    a = digitalRead(3);
    if (a != b) {
        b = a;
        data = 23;
        Serial.write(data);
    }
    a = digitalRead(4);
    if (a != c) {
        c = a;
        data = 24;
        Serial.write(data);
    }
    a = digitalRead(5);
    if (a != d) {
        d = a;
        data = 25;
        Serial.write(data);
    }
    a = digitalRead(6);
    if (a != e) {
        e = a;
        data = 26;
        Serial.write(data);
    }
}

void receiveFromMaster(int nByteNum)
{
    for (int i = 0; i < nByteNum; i++)
        data_i2c = Wire.read();
    Serial.write(data_i2c);
    data_i2c = 0;
}
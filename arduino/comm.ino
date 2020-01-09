#include <Wire.h>
#define Slave 0x10

#include <SoftwareSerial.h>
SoftwareSerial button(12, 13);

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
}

void receiveFromMaster(int nByteNum)
{
    for (int i = 0; i < nByteNum; i++)
        data_i2c = Wire.read();
    Serial.write(data_i2c);
    data_i2c = 0;
}
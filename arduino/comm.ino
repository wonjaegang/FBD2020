// upload this on the Arduino which connects with PC by Serial communication

//this Arduino uses all communication (I2C, SoftwareSerial, Hardware Serial)

//enable i2c communication with other Arduino
#include <Wire.h>
//I2C address
#define Slave 0x10 

//enable software serial communication with other Arduino
#include <SoftwareSerial.h>
SoftwareSerial button(12, 13); //SoftwareSerial pin

//save buttons' states
int state2 = 1, state3 = 1;

void setup()
{
    //set pins as buttons
    pinMode(2, INPUT); 
    pinMode(3, INPUT); 
    //begin I2C communication as I2C slave
    Wire.begin(Slave); 
    //function for I2C call from master
    Wire.onReceive(receiveFromMaster);
    //begin SoftwareSerial communication, BPS:9600 
    button.begin(9600);
    //begin Serial communication, BPS: 9600
    Serial.begin(9600); 
}

//data from other Arduino by I2C communication
char data_i2c; 
//data from other Arduino by SoftwareSerial communication
char data_serial; 

void loop()
{
    //if there is a button input with SoftwareSerial communication
    if (button.available() > 0) {
        //read the data by SoftwareSerial communication
        data_serial = button.read(); 
        //send the data to PC
        Serial.println(data_serial);
        //initializing 
        data_serial = 0;
    }
    //save button status
    int a;
    //data to send to PC
    char data; 

    a = digitalRead(2);
    if (a == 1 && state2 == 1) {
        data = 'W';
        state2 = 0;
        //send the data to the PC
        Serial.println(data); 
    }
    if (a == 0 && state2 == 0) {
        data = 'W';
        state2 = 1;
        //send the data to the PC
        Serial.println(data);
    }

    a = digitalRead(3);
    if (a == 1 && state3 == 1) {
        data = 'X';
        state3 = 0;
        //send the data to the PC
        Serial.println(data); 
    }
    if (a == 0 && state3 == 0) {
        data = 'X';
        state3 = 1;
        //send the data to the PC
        Serial.println(data);
    }
}

//if there is a call from I2C master device
void receiveFromMaster(int nByteNum)
{
    //read the data by I2C communication
    for (int i = 0; i < nByteNum; i++)
        data_i2c = Wire.read(); 
    //send the data to PC
    Serial.println(data_i2c); 
    //initializing 
    data_i2c = 0;
}

// upload this on the Arduino which connects with PC by Serial communication

//this Arduino uses all communication (I2C, SoftwareSerial, Hardware Serial)

//enable i2c communication with other Arduino
#include <Wire.h>
#define Slave 0x10  //I2C address

//enable software serial communication with other Arduino
#include <SoftwareSerial.h>
SoftwareSerial button(12, 13);  //SoftwareSerial pin

//save the status of switch
int state2 = 2, state3 = 2;

void setup()
{
    pinMode(2, INPUT);  //button input
    pinMode(3, INPUT);  //button input
    Wire.begin(Slave);  //begin I2C communication as I2C slave
    Wire.onReceive(receiveFromMaster);  //function for I2C call from master
    button.begin(9600); //begin SoftwareSerial communication, BPS:9600
    Serial.begin(9600); //begin Serial communication, BPS: 9600
}

char data_i2c;      //data from other Arduino by I2C communication
char data_serial;   //data from other Arduino by SoftwareSerial communication

void loop()
{
    if (button.available() > 0) {
        //if there is a signal with SoftwareSerial communication
        data_serial = button.read();    //read the data by SoftwareSerial communication
        Serial.println(data_serial);      //send the data to PC
        data_serial = 0;    
    }
    int a;  //get switch status
    char data;  //use 1 byte data for serial communication with PC
    a = digitalRead(2);
    if (a != state2) {
        //if the status of button is changed
        state2 = a;  //save new status
        data = 'W';  
        Serial.println(data); //send the data to PC
    }
    a = digitalRead(3);
    if (a != state3) {
        //if the status of button is changed
        state3 = a;  //save new status
        data = 'X';
        Serial.println(data); //send the data to PC
    }
}

void receiveFromMaster(int nByteNum)
{
    //if there is a call from I2C master device
    for (int i = 0; i < nByteNum; i++)
        data_i2c = Wire.read(); //read the data by I2C communication
    Serial.println(data_i2c); //send the data to PC
    data_i2c = 0;
}
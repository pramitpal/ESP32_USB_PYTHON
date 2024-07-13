/**
 * Simple HID keyboard
 * author: chegewara
 */


#include "hidkeyboard.h"
#include "Wire.h"
#if CFG_TUD_HID
#define KEYBOARD_I2C_ADDR     0X5f

HIDkeyboard dev;

void setup()
{
    Serial.begin(115200);
    Wire.begin(7,8);
    dev.begin();
}

void loop()
{
    delay(5);
    dev.sendString("hello how are you I am ok, my name is pal\n");
}

#endif

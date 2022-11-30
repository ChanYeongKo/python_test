import matplotlib.pyplot as plt
import matplotlib.image as img
import thingspeak
import time
import random
import sys
from pymata4 import pymata4
from gtts import gTTS
import speech_recognition as sr
import re
from playsound import playsound

img_cat1 = img.imread('ddd.jpg')
POLL_TIME = 2  
CB_PIN_MODE = 0
CB_PIN = 1
CB_VALUE = 2
CB_TIME = 3
TRIGGER_PIN = 3#소나함수(초음파센서)
ECHO_PIN = 2#소나함수(초음파센서)
DIGITAL_PIN1 = 12#블링크 핀번호
DIGITAL_PIN2 = 13#블링크 핀번호
board = pymata4.Pymata4()
channel_id = 1930794 # put here the ID of the channel you created before
write_key = 'I2VETT2ND4FYL52R' # update the "WRITE KEY"

def measure(channel):
    board.set_pin_mode_dht(4, sensor_type=11, differential=.05)
    board.set_pin_mode_sonar(TRIGGER_PIN, ECHO_PIN)#초음파센서
    value = board.dht_read(4)
    board.set_pin_mode_digital_output(DIGITAL_PIN1)#블링크 
    try:
        temperature = value[0];
        humidity = value[1];
        value = board.sonar_read(TRIGGER_PIN)[0]
        print('Humidity = {0:0.1f}% Temperature = {1:0.1f}*C'.format(temperature, humidity))
        print(f'소나: {board.sonar_read(TRIGGER_PIN)[0]}')
        response = channel.update({'field1': temperature, 'field2': humidity,'field3':value})
        plt.subplot(111)
        if((value < 15) and (temperature > 20 and humidity > 15)):
            #tts = gTTS(text="Go Away")
            #tts.save("test.mp3")
            LED_ON(board, 13)
            playsound("test.mp3")
            plt.imshow(img_cat1)
            plt.show(block=False)
            plt.pause(1)
            plt.close()
            
        else:
            #tts = gTTS(text="Come on")
            #tts.save("test2.mp3")
            LED_OFF(board,13)
            playsound("test2.mp3")
            
    except:
           print("connection failure")
           
def LED_ON(my_board, pin):
    my_board.set_pin_mode_digital_output(pin)
    my_board.digital_pin_write(pin, 1)

def LED_OFF(my_board, pin):
    my_board.set_pin_mode_digital_output(pin)
    my_board.digital_pin_write(pin, 0)
if __name__ == "__main__":
        channel = thingspeak.Channel(id=channel_id, write_key=write_key)
        while True:
            measure(channel)
        #free account has a limitation of 15sec between the updates
            time.sleep(1)

"""
가변저항기 초음파센서 thingspeak출력
"""

import thingspeak
import time
import random
import sys
from pymata4 import pymata4
from gtts import gTTS
import speech_recognition as sr
from playsound import playsound

img_cat1 = img.imread('ddd.jpg')
POLL_TIME = 2  
CB_PIN_MODE = 0
CB_PIN = 1
CB_VALUE = 2
CB_TIME = 3
TRIGGER_PIN = 3#소나함수(초음파센서)
ECHO_PIN = 2#소나함수(초음파센서)
board = pymata4.Pymata4()
channel_id = 1930794 # put here the ID of the channel you created before
write_key = 'I2VETT2ND4FYL52R' # update the "WRITE KEY"
"""
    가변저항기 vcc out gnd
"""
tts = gTTS(text = "시작하겠습니다.", lang='ko')
tts.save("teste.mp3")
tts = gTTS(text = "종료했습니다.", lang='ko')
tts.save("teste2.mp3")
tts = gTTS(text = "올렸습니다..", lang='ko')
tts.save("test55.mp3")

channel_id = 1930794 # put here the ID of the channel you created before
write_key = 'I2VETT2ND4FYL52R' # update the "WRITE KEY"

def the_callback(data):
    print(f'Distance in cm: {data[DISTANCE_CM]}')
    if (data[DISTANCE_CM] <= 30):
        LED_ON(board, 13)
        print("LED ON")
    else:
        LED_OFF(board, 13)
        print("LED_OFF")

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
        plt.figure(figsize=(10,10))
        plt.subplot(111)
        if(temperature > 50 and humidity > 24):
#            tts = gTTS(text="접근 금지", lang='ko')
#            tts.save("test.mp3")
            playsound("test.mp3")
            plt.imshow(img_cat1)
            plt.show(block=False)
            plt.pause(1)
            plt.close()
            board.digital_write(DIGITAL_PIN1, 1)#블링크
            board.digital_write(DIGITAL_PIN2, 0)#블링크 
        else:
#            tts = gTTS(text="조금만 더 가까이 오세요", lang='ko')
#            tts.save("test2.mp3")
            playsound("test2.mp3")
            board.digital_write(DIGITAL_PIN1, 0)#블링크
            board.digital_write(DIGITAL_PIN2, 1)#블링크 
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




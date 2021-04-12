import time

import serial
from pocketsphinx import LiveSpeech


class VoiceArmController:
    def __init__(self, comport):
        #create an object to recongite the voice
        self.speech = LiveSpeech()
        #creating a serial commincation port
        self.ser = serial.Serial()
        self.ser.baudrate = 2400
        self.ser.port = comport
        self.ser.timeout = 10

    #function wich wait when the keyword is said and after that call the write to arduino function
    def Listen(self):
        firstWord = []


        for phrase in self.speech:
            for word1 in firstWord:
                for word2 in phrase.segments():
                    if word1 == 'light' and word2 == 'on':
                        self.writeToArduino('1')
                    if word1 == 'light' and (word2 == 'off' or word2 == 'off(2)'):
                        self.writeToArduino('0')
                    if word1 == 'light' and (word2 == 'out'):
                        self.writeToArduino('0')
            firstWord = phrase.segments()

    #open Comport and sends a command to arduino
    def writeToArduino(self, data):
        try:
            self.ser.open()
            time.sleep(2)
            self.ser.write(data.encode())
            self.ser.close()
            print("sended " + data +  " to the arduino")
        except:
            #failed to connect to the comport
            print('Comport: ', self.ser.port, ' unable to send data')



contrllr = VoiceArmController('COM2')
contrllr.Listen()



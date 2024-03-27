# -*- coding: utf-8 -*-
from PIL import Image
from PIL import ImageFont
from PIL import ImageDraw
import numpy as np
import serial
import time
class Reader:
    def __init__(self):
        self.lab_name = ' '
    def old_read_name(self, string):
        string = ''.join(string.split('\n'))
        return string[1:]
    def old_read_cicuit(self, path):
        arr = []
        img_arr = []
        f = open(path, "r")
        while True:
            s = f.readline()
            if (not s):
                break
            elif (s[0] == '*'):
                if (self.lab_name == ' '):
                    self.lab_name = self.old_read_name(f.readline())
            else:
                arr.append(s.split())
        for c in arr:
            img_arr.append('src//imgs//%s.png' %c[0][0])
        imgs = [ Image.open(i) for i in img_arr ]
        font = ImageFont.truetype("/usr/share/fonts/TTF/OpenSans-Regular.ttf", 24)
        for i in range(len(imgs)):
            draw = ImageDraw.Draw(imgs[i])
            if not(arr[i][0][0] == 'A'):
                draw.text((60, 40), arr[i][0], (7, 7, 7), font=font)
                draw.text((130, 27), arr[i][1], (7, 7, 7), font=font)
                draw.text((70, 140), arr[i][3], (7, 7, 7), font=font)
                draw.text((130, 255), arr[i][2], (7, 7, 7), font=font)
            else:
                draw.text((60, 40), arr[i][0], (7, 7, 7), font=font)
                draw.text((95, 65), arr[i][1], (7, 7, 7), font=font)
                draw.text((200, 65), arr[i][2], (7, 7, 7), font=font)
                draw.text((140, 260), arr[i][3], (7, 7, 7), font=font)
        min_shape = sorted( [(np.sum(i.size), i.size ) for i in imgs])[0][1]
        imgs_comb = np.hstack( [np.asarray( i.resize(min_shape) ) for i in imgs ] ) 
        imgs_comb = Image.fromarray(imgs_comb)
        imgs_comb.save('out//Circuit.png')
class Speaker():
    def __init__(self):
        self.log = 'Start.\n'
    def clear_output(self):
        f = open('out//raw_output.txt', 'w')
        f.write('')
        f.close()
    def write_to_out(self, string):
        f = open('out//raw_output.txt', 'a')
        f.write(string + '\n')
        f.close()
    def send_to_COM_port(self, com_name, path):
        ser = serial.Serial(com_name, 115200, timeout=1)
        f = open(path, "r")
        while True:
            s = f.readline()
            if (not s):
                break
            else:
                s = s[:-1]
                ser.write(str.encode(s))
                self.log += 'Sent: ' + s + '\n'
                data = ser.readline()
                self.log += 'Recieved: ' + data.decode()
                data = ser.readline()
                self.log += '          ' + data.decode()
        self.log += 'End of communication.'
        f.close()
        log_f = open('out//log.txt', 'w')
        log_f.write('')
        log_f.write(self.log)
        log_f.close()
class Converter():
    def __init__(self):
        self.raw_arr = []
        self.converted_arr = []
        self.err = False
    def convert(self):
        for_check = []
        r = ['CMT ', 'MSR ', 'NOD ']
        i = -1
        for n in range(len(self.raw_arr)):
            for item in self.raw_arr[n]:
                if (item[0] == '-'):
                    i+=1
                    for_check = []
                    continue
                result = r[i]
                if (item in for_check) or (int(item)>16) or (int(item)<0):
                    self.converted_arr = []
                    self.err = True
                    break
                else:
                    for_check.append(item)
                    if not (i == 2):
                        result = result + item + f' {(n) % 9}' 
                    else:
                        result = result + item
                    self.converted_arr.append(result)
    def read(self, path):
        f = open(path, 'r')
        arr = []
        while True:
            s = f.readline()
            if (not s):
                break
            else:
                arr.append(s.split())
        self.raw_arr = arr
    def write(self, path):
        f = open(path, 'a')
        f.write('\n')
        f.write('STT' + '\n')
        f.write('RST' + '\n')
        for item in self.converted_arr:
            f.write(f'{item}' + '\n')
        f.write('STP' + '\n')
        f.close()
    def clear(self, path):
        f = open(path, 'w')
        f.write('')
        f.close()

 

#!/usr/bin/env python3
# *************************************************************************
#
# Copyright (c) 2022 Andrei Gramakov. All rights reserved.
#
# site:    https://agramakov.me
# e-mail:  mail@agramakov.me
#
# *************************************************************************
from time import sleep
from tkinter import NW, Tk, Canvas
from PIL import ImageTk,Image
from images import *
from threading import Thread
from brain_pycore.zmq import (
    ZmqPublisherThread, ZmqSubscriberThread, ZmqServerThread, ZmqClientThread)

def back(canvas: Canvas):
    img_angry = ImageTk.PhotoImage(Image.open(ANGRY_JPG))
    img_blink = ImageTk.PhotoImage(Image.open(BLINK_JPG))
    img_calm = ImageTk.PhotoImage(Image.open(CALM_JPG))
    img_happy = ImageTk.PhotoImage(Image.open(HAPPY_JPG))
    img_sad = ImageTk.PhotoImage(Image.open(SAD_JPG))
    
    while (1):
        for img in [img_angry, img_blink, img_calm, img_happy,img_sad]:
            canvas.create_image(0, 0, anchor=NW, image=img)
            sleep(1)
        
class Backend():
    ADDRESS = "localhost"
    PORT = 55580
    TOPIC = "Hot Topic"

    
    def __init__(self, canvas) -> None:
        self.canvas = canvas
        self.faces = {
            "angry": ImageTk.PhotoImage(Image.open(ANGRY_JPG)),
            "blink": ImageTk.PhotoImage(Image.open(BLINK_JPG)),
            "calm": ImageTk.PhotoImage(Image.open(CALM_JPG)),
            "happy": ImageTk.PhotoImage(Image.open(HAPPY_JPG)),
            "sad": ImageTk.PhotoImage(Image.open(SAD_JPG)),
        }
        self.thread = Thread(target=self.__main)
        self.sub = ZmqSubscriberThread(port=self.PORT, topic=self.TOPIC,
                                  callback=self.subscriber_callback,
                                  address=self.ADDRESS)
    
    def __main(self):
        while (1):
            for img in self.faces.values():
                self.canvas.create_image(0, 0, anchor=NW, image=img)
                sleep(1)
    
    @staticmethod
    def subscriber_callback(msg: str):
        print(msg)
                
    def start(self):
        self.thread.start()
        self.sub.start()
            
    

    

if __name__ == "__main__":
    
    root = Tk()  
    canvas = Canvas(root, width = 336, height = 256)  
    canvas.pack()
    back = Backend(canvas=canvas)
    back.start()
    root.mainloop()
    
     

# import subprocess
# import json 
# import asyncio
# from pynput.keyboard import Controller,Key
# from LLM import call_LLM


# # prompt = 'in the right side of window(in file manager) make one new folder name folder1 using mouse'
# # prompt = 'write content of a research paper on adaptive traffic signal timer in iEEE format contains abstract , introduction , methodology, refference research papers '
# # prompt='make one project of e-commerce website using html,css and javascript'
# # prompt='open chrome and search amazon.com and add any one mobile to cart'
# # prompt='open amazon.in and add any one smart tv to cart'
# # prompt='Send "when you will come" to bhushan more on whatsapp'
# prompt='open comet app'
# res = asyncio.run(call_LLM(prompt,0))


from pynput.mouse import Controller, Button
import time, json
import base64
import pyautogui
from PIL import ImageGrab

mouse = Controller()
screenshot = ImageGrab.grab()
width, height = pyautogui.size()

print(screenshot.size)
# # width = 1430
# # height = 1000
# x = int(width * 0.987)
# y = int(height * 0.99)
# pyautogui.moveTo(x,y, duration=0.3)




'''tools.py (tools use by LLM to perform given tasks)'''

import os
import json
import subprocess
import webbrowser
from pathlib import Path
from pynput.keyboard import Controller as KeyboardController, Key
from pynput.mouse import Controller as MouseController, Button
import asyncio
import io
import time
import base64
import pyautogui
from PIL import ImageGrab


WORKING_DIR = os.getenv('WORKING_DIRECTORY', os.getcwd())


async def execute_cmd_command(input_data): # sample input_data = '{"command": "mkdir D:\temporary\desktop-agent-files\project1"}'
    try:  
        data = json.loads(input_data)         
        command = data["command"]       
        print("Executing:", command)
        subprocess.run(command, shell=True, capture_output=True, text=True)
        return f"{command} has run successfully"
    except Exception as err: 
        print("error in tool(execute_cmd_command) =>", err)
        return f"error in tool(execute_cmd_command) => {err}"
    

async def open_file(input_data):  # sample input_data = '{"file_path": "D:/Coding/All Codes/C++/tempp/A.cpp"}'
    try:
        data = json.loads(input_data)
        file_path = data["file_path"]
        json_to_send = json.dumps({"command": f'code "{file_path}"'})
        res = await execute_cmd_command(json_to_send)
        return f"{file_path} file opened successfully"
    except Exception as err:
        print("error in tool(open_file) =>", err)
        return f"error in tool(open_file) => {err}"


async def open_app(input_data):  # sample input_data = '{"app_name":"nodepad"}'
    try:
        data = json.loads(input_data)
        app_to_start=data["app_name"]
        json_to_send = json.dumps({"command": f"start {app_to_start}"})
        res = await execute_cmd_command(json_to_send)
        return f"{app_to_start} opened successfully"
    except Exception as err:
        print("error in tool(open_app) =>", err)
        return f"error in tool(open_app) => {err}"


async def open_website(input_data): # sample input_data = '{"website":"https://www.youtube.com/"}' 
    try:
        data = json.loads(input_data)
        website_to_open = data["website"]
        webbrowser.open(website_to_open)
        return f"{website_to_open} has opened successfully"
    except Exception as err:
        print("error in tool(open_website) =>", err)
        return  f"error in tool(open_website) => {err}"


async def press_keyboard_key(input_data): # Using pynput.keyboard | sample input_data = '{"keys_to_press": ["ctrl","shift","esc"]}' 
    try:
        keyboard = KeyboardController()
        data = json.loads(input_data)
        keys_to_press=data["keys_to_press"]
        for k in keys_to_press:
            key_obj = getattr(Key, k, k)
            keyboard.press(key_obj)
            await asyncio.sleep(0.05)
        for k in reversed(keys_to_press):
            key_obj = getattr(Key, k, k)
            keyboard.release(key_obj)
            await asyncio.sleep(0.05)
        return f"{keys_to_press} pressed successfully"
    except Exception as err:
        print("error in tool(press_keyboard_key) =>", err)
        return  f"error in tool(press_keyboard_key) => {err}"


async def write_content(input_data): # sample input_data = '{"content": "any content to write"}'
    try:
        keyboard = KeyboardController()
        data = json.loads(input_data)
        content = data["content"]
        keyboard.type(content)
        return f"content written successfully"
    except Exception as err:
        print("error in tool(write_content) =>", err)
        return  f"error in tool(write_content) => {err}"


async def give_screenshot(input_data): # sample input_data = '{}'
    try:    
        screenshot = ImageGrab.grab()
        width, height = screenshot.size
        screenshot.save("h.png")
        buf = io.BytesIO()
        screenshot.save(buf, format="PNG")
        buf.seek(0)
        png_bytes = buf.getvalue()
        base64_bytes = base64.b64encode(png_bytes)
        base64_string = base64_bytes.decode('utf-8')
        return [base64_string, width, height]
    except Exception as err:
        print("error in tool(give screenshot) =>", err)
        return  f"error in tool(give screenshot) => {err}"


async def move_mouse_pointer(input_data):  # sample input_data = '{"x": 0.15, "y": 0.9}'
    try:
        data = json.loads(input_data)
        x_per = data["x"]
        y_per = data["y"]
        width, height = pyautogui.size()

        x = int(width * x_per)
        y = int(height * y_per)
        pyautogui.moveTo(x, y, duration=0.5)
        print(f"mouse is successfully moved to position ({x}, {y})") 
        return f"mouse is successfully moved to given position"
    except Exception as err:
        print("❌ error in tool(move_mouse_pointer) =>", err)
        return f"error in tool(move_mouse_pointer) => {err}"


async def click_mouse_buttons(input_data):  # sample input_data = '{"button": "left","clicks": 2 }'
    try:
        mouse = MouseController()
        data = json.loads(input_data)

        button_name = data.get("button", "left").lower()
        clicks = int(data.get("clicks", 1))

        if button_name == "left":
            button = Button.left
        elif button_name == "right":
            button = Button.right
        elif button_name == "middle":
            button = Button.middle
        else:
            return f"Invalid button name: {button_name}"

        for _ in range(clicks):
            mouse.click(button)
            await asyncio.sleep(0.1)

        current_pos = mouse.position
        return f"Clicked {button_name} button {clicks} times at {current_pos}"

    except Exception as err:
        print("❌ error in tool(click_mouse_buttons) =>", err)
        return f"error in tool(click_mouse_buttons) => {err}"









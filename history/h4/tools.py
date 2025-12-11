import os
import json
import subprocess
import webbrowser
from pathlib import Path
from pynput.keyboard import Controller, Key
import asyncio

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


async def write_into_file(input_data): # sample input_data = '{"file_path": "D:/Coding/All Codes/C++/tempp/A.cpp","content":"any content to write in the file."}'
    try: 
        data=json.loads(input_data)
        file_path=data['file_path']
        content=data['content']
        with open(file_path, 'w',encoding='utf-8') as f: 
            f.write(content)
        return f"provided content is successfully written to file {file_path}"
    except Exception as err:
        print("error in tool(write_into_file) => ",err)
        return f"error in tool(write_into_file) => {err}"


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
        keyboard = Controller()
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


async def type_content(input_data): # sample input_data = '{"content": "any content to write"}'
    try:
        keyboard = Controller()
        data = json.loads(input_data)
        content = data["content"]
        keyboard.type(content)
        return f"content written successfully"
    except Exception as err:
        print("error in tool(type_content) =>", err)
        return  f"error in tool(type_content) => {err}"

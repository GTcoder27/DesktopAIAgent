import os
import json
import asyncio
import google.generativeai as genai
from dotenv import load_dotenv
from tools import (execute_cmd_command, write_into_file, open_file, open_app, open_website, press_keyboard_key, type_content) 

load_dotenv() 

WORKING_DIR = os.getenv('WORKING_DIRECTORY', os.getcwd())
GEMINI_API_KEY=os.getenv('GEMINI_API_KEY')

chat_history = []

SYSTEM_PROMPT = f"""You are a Continuous Windows Desktop Automation AI Assistant that works on tasks autonomously and maintains context across multiple operations

CRITICAL: You MUST respond with ONLY valid JSON. Do NOT wrap it in markdown code blocks.
Do NOT use triple backticks. Response must start with {{ and end with }}

## One command one action mode:
- You complete tasks automatically without waiting for user confirmation
- You maintain context of what you've created/opened

## Working Directory Context:
- ALL file operations happen in: {WORKING_DIR}
- Remember folder paths you create for subsequent operations
- Track which apps/files you've opened
- Build upon previous actions in the session

## Available Tools:
- execute_cmd_command(input_data): # sample input_data = {{"command": "mkdir \\"D:/temporary/desktop-agent-files/project1\\""}}
- write_into_file(input_data): # sample input_data = {{"file_path": "D:/Coding/All Codes/C++/tempp/A.cpp", "content": "any content to write in the file."}}
- open_file(input_data): # sample input_data = {{"file_path": "D:/Coding/All Codes/C++/tempp/A.cpp"}}
- open_app(input_data): # sample input_data = {{"app_name": "notepad"}}
- open_website(input_data): # sample input_data = {{"website": "https://www.youtube.com/"}}
- press_keyboard_key(input_data): # Using pynput.keyboard # sample input_data = {{"keys_to_press": ["ctrl", "shift", "esc"]}}
- type_content(input_data): # sample input_data = {{"content": "any content to write"}}

## STRICT Rules:
1. ALWAYS respond with exactly ONE JSON object per message
2. NO markdown, NO explanations, ONLY JSON
3. Remember context from previous actions
4. If you did not able to understand the user query so give:
{{
  "tool": "give_valid_command",
  "input_data": {{
    "reason": "small description (of 1 line)"
  }}
}}

## JSON Format:
{{ 
    "tool": "name of tool", 
    "input_data": "according to available tools sample input_data (in json)" 
}}

Examples of response:
User: "make a folder"
Expected Output:
{{
  "tool": "execute_cmd_command",
  "input_data": {{
    "command": "mkdir D:\\\\temporary\\\\desktop-agent-files\\\\project1"
  }}
}}
Don't return any other only json is expected containing tool and input_data
"""

genai.configure(api_key=GEMINI_API_KEY)

model = genai.GenerativeModel(
    model_name="gemini-2.0-flash",
    system_instruction=SYSTEM_PROMPT
)

chat = model.start_chat(history=chat_history)


def LLM_extraction(data):
    response = data.text
    if response.startswith("```json"):
        response = response[7:]  # Remove ```json
    if response.startswith("```"):
        response = response[3:]  # Remove ```
    if response.endswith("```"):
        response = response[:-3]  # Remove trailing ```
    response = json.loads(response)
    return response


async def call_LLM(prompt):
    print("🤖 calling LLM => ")
    res = chat.send_message(prompt)
    response = LLM_extraction(res)
    print("response:",response)
    tool_res = await execute_tool(response["tool"], response["input_data"])
    chat_history.append({"role": "user", "parts": [prompt]})
    chat_history.append({"role": "model", "parts": [tool_res]})
    
    if(len(chat_history) > 10): # if chat history gets very large
        del chat_history[:2]
    return tool_res


async def execute_tool(tool, input_data):    
    match tool:
        case 'execute_cmd_command':
            return await execute_cmd_command(json.dumps(input_data))
        case 'write_into_file':
            return await write_into_file(json.dumps(input_data))
        case 'open_file':
            return await open_file(json.dumps(input_data))
        case 'open_app':
            return await open_app(json.dumps(input_data))
        case 'open_website':
            return await open_website(json.dumps(input_data))
        case 'press_keyboard_key':
            return await press_keyboard_key(json.dumps(input_data))
        case 'type_content':
            return await type_content(json.dumps(input_data))
        case 'give_valid_command':
            print('Invalid command - please rephrase your request')
            return 'Invalid command received'
        case _:
            return f'Error: Unknown tool: {tool}'


            
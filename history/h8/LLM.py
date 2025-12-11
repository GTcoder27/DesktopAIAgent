'''LLM.py (to call LLM)'''

import os
import json
import asyncio
import google.generativeai as genai
from PIL import Image
from dotenv import load_dotenv
from tools import (execute_cmd_command, open_file, open_app, open_website, press_keyboard_key, write_content,give_screenshot,move_mouse_pointer,click_mouse_buttons) 

load_dotenv() 

WORKING_DIR = os.getenv('WORKING_DIRECTORY', os.getcwd())
GEMINI_API_KEY=os.getenv('GEMINI_API_KEY')

chat_history = []

SYSTEM_PROMPT = f"""
You are a Continuous Windows Desktop Automation AI Assistant that autonomously performs desktop operations step-by-step while maintaining full context between actions.

CRITICAL: You MUST respond with ONLY valid JSON. 
- Do NOT wrap responses in markdown or code blocks.
- Do NOT use triple backticks.
- Response must start with {{ and end with }}.

========================================================
## CONTINUOUS OPERATION MODE:
========================================================
- You operate continuously and autonomously without waiting for confirmation.
- You maintain full context across multiple commands.
- You plan and execute tasks step-by-step until fully complete.
- You perform one tool action per response and immediately plan the next.
- Once the entire task is complete, you MUST call the 'stop' tool with a one-line completion message.

========================================================
## WORKING DIRECTORY CONTEXT:
========================================================
- All file and folder operations occur inside: {WORKING_DIR}
- Always remember paths and files you create for later use.
- Keep track of opened files, folders, or applications for continuity.

========================================================
## AVAILABLE TOOLS:
========================================================
- execute_cmd_command(input_data): 
    # Run a command in CMD
    # Example: {{"command": "mkdir \\"D:/temporary/desktop-agent-files/project1\\""}}

- open_file(input_data): 
    # Open a file using its default app
    # Example: {{"file_path": "D:/Coding/All Codes/C++/tempp/A.cpp"}}

- open_app(input_data): 
    # Open an application by name
    # Example: {{"app_name": "notepad"}}

- open_website(input_data): 
    # Open a website
    # Example: {{"website": "https://www.youtube.com/"}}

- press_keyboard_key(input_data): 
    # Press one or more keyboard keys using pynput
    # Example: {{"keys_to_press": ["ctrl", "shift", "esc"]}}

- write_content(input_data): 
    # Type text at the current cursor position
    # Example: {{"content": "Hello, world!"}}

- give_screenshot(input_data): 
    # Capture and analyze the screen
    # Example: {{"reason": "to locate a button before clicking"}}
    # You will receive a screenshot and its dimensions (width, height).
    # Use this to compute coordinates for mouse actions.

- move_mouse_pointer(input_data): 
    # Move the mouse pointer based on screen dimensions (percentage coordinates)
    # Example: {{"x": 0.98, "y": 0.02}}
    # x, y are percentages of total screen width and height.
    # Example: 0.98 = 98% from left, 0.02 = 2% from top.

- click_mouse_buttons(input_data): 
    # Click a mouse button one or multiple times
    # Example: {{"button": "left", "clicks": 2}}

- stop(input_data): 
    # End task with summary
    # Example: {{"message": "Completed folder creation and opened in VS Code"}}

========================================================
## MOUSE EFFICIENCY RULES:
========================================================
1. Before performing any mouse movement or click, always call 'give_screenshot' first (if screen context is required).
2. Always compute relative coordinates (x, y) using percentages — never use pixel values directly.
3. When identifying on-screen elements, reason based on visual layout or positional assumptions.
4. Always use 'move_mouse_pointer' before any 'click_mouse_buttons'.
5. To close apps or interact with UI, rely on mouse clicks instead of CMD process kills.
6. If unsure where to click or move, call 'give_screenshot' and stop with explanation.

========================================================
## OPERATION FLOW:
========================================================
Plan → Execute first action → Execute next action → ... → Stop

========================================================
## STRICT RULES:
========================================================
1. Each response must contain exactly ONE JSON object.
2. No markdown, no explanations, no plain text.
3. Always include:
   - "tool"
   - "input_data"
   - "next_command"
4. Work continuously until task completion.
5. For unclear requests, respond with 'give_valid_command' and then 'stop'.
6. Use 'stop' after all steps are finished.
7. Never use CMD commands to kill apps or move mouse — always use mouse tools.
8. Always interpret screenshot size correctly when computing mouse coordinates.
9. If any step depends on screen content, first request a screenshot.
10. Always describe clearly what the next command should do.

========================================================
## JSON RESPONSE FORMAT:
========================================================
{{
  "tool": "name of tool",
  "input_data": {{
    // tool-specific parameters in JSON
  }},
  "next_command": "description of next action or 'stop agent'"
}}

========================================================
## FOR INVALID OR UNCLEAR REQUESTS:
========================================================
{{
  "tool": "give_valid_command",
  "input_data": {{
    "reason": "why the request cannot be processed"
  }},
  "next_command": "stop agent"
}}

========================================================
## EXAMPLES
========================================================

### Example 1 – Multi-step Task:
User: "Create a folder called 'sorting-project', make a Python file with insertion sort, and open it in VS Code"

Response 1:
{{
  "tool": "execute_cmd_command",
  "input_data": {{
    "command": "mkdir \\"{WORKING_DIR}\\\\sorting-project\\""
  }},
  "next_command": "create insertion_sort.py file"
}}

Response 2:
{{
  "tool": "write_into_file",
  "input_data": {{
    "file_path": "{WORKING_DIR}\\\\sorting-project\\\\insertion_sort.py",
    "content": "def insertion_sort(arr):\\n    for i in range(1, len(arr)):\\n        key = arr[i]\\n        j = i - 1\\n        while j >= 0 and arr[j] > key:\\n            arr[j + 1] = arr[j]\\n            j -= 1\\n        arr[j + 1] = key\\n    return arr"
  }},
  "next_command": "open folder in VS Code"
}}

Response 3:
{{
  "tool": "execute_cmd_command",
  "input_data": {{
    "command": "code \\"{WORKING_DIR}\\\\sorting-project\\""
  }},
  "next_command": "stop agent"
}}

Response 4:
{{
  "tool": "stop",
  "input_data": {{
    "message": "Created sorting-project folder, added insertion_sort.py, and opened it in VS Code"
  }},
  "next_command": "task ended"
}}

### Example 2 – Simple Task:
User: "Open YouTube"

Response:
{{
  "tool": "open_website",
  "input_data": {{
    "website": "https://www.youtube.com/"
  }},
  "next_command": "stop agent"
}}

### Example 3 – Invalid Request:
User: "asdfghjkl"

Response:
{{
  "tool": "give_valid_command",
  "input_data": {{
    "reason": "Unrecognized command. Please provide a clear automation task."
  }},
  "next_command": "stop agent"
}}

========================================================
## REMEMBER:
========================================================
- Respond ONLY with valid JSON.
- Each step = exactly ONE tool action.
- Indicate the next action in "next_command".
- Use screenshots for all visual or mouse-based tasks.
- Stop when the full task is done.
"""


genai.configure(api_key=GEMINI_API_KEY)

model = genai.GenerativeModel(
    model_name="gemini-2.5-flash",
    system_instruction=SYSTEM_PROMPT,
    generation_config=genai.GenerationConfig(
        max_output_tokens=8192, 
        temperature=0.8, 
        top_p=0.95,
        top_k=40,
    )
)

def LLM_extraction(data):
    # print(data)
    response = data.text
    if response.startswith("```json"):
        response = response[7:]  # Remove ```json
    if response.startswith("```"):
        response = response[3:]  # Remove ```
    if response.endswith("```"):
        response = response[:-3]  # Remove trailing ```
    response = json.loads(response)
    # print("d=>",response)
    return response


async def call_LLM(prompt,times_called):
    print("🤖 calling LLM => ")
    chat = model.start_chat(history=chat_history)
    res = chat.send_message(prompt)
    # print(res)
    response = LLM_extraction(res)
    print("response:",response)
    tool_res = await execute_tool(response["tool"], response["input_data"])
    # print(tool_res,"\n")
    if times_called == 0: 
        chat_history.append({"role": "user", "parts": [prompt]})

    if(len(chat_history) > 30): # if chat history gets very large
        del chat_history[:2]

    if tool_res != 'stop_agent':
        # await asyncio.sleep(0.1)
        tool_res = await call_LLM(response["next_command"],times_called+1)
    return 'task done'


async def execute_tool(tool, input_data):    
    match tool:
        case 'execute_cmd_command':
            res = await execute_cmd_command(json.dumps(input_data))
            chat_history.append({"role": "model", "parts": [res]})
            return res
        case 'open_file':
            res = await open_file(json.dumps(input_data))
            chat_history.append({"role": "model", "parts": [res]})
            return res
        case 'open_app':
            res = await open_app(json.dumps(input_data))
            chat_history.append({"role": "model", "parts": [res]})
            return res
        case 'open_website':
            res = await open_website(json.dumps(input_data))
            chat_history.append({"role": "model", "parts": [res]})
            return res
        case 'press_keyboard_key':
            res = await press_keyboard_key(json.dumps(input_data))
            chat_history.append({"role": "model", "parts": [res]})
            return res
        case 'write_content':
            res = await write_content(json.dumps(input_data))
            chat_history.append({"role": "model", "parts": [res]})
            return res
        case 'move_mouse_pointer':
            res = await move_mouse_pointer(json.dumps(input_data))
            print("respo ",res)
            chat_history.append({"role": "model", "parts": [res]})
            return res
        case 'click_mouse_buttons':
            res = await click_mouse_buttons(json.dumps(input_data))
            chat_history.append({"role": "model", "parts": [res]})
            return res
        case 'give_screenshot':
            res = await give_screenshot(json.dumps(input_data))
            image_part = {
                "inline_data": {
                    "data": res[0], 
                    "mime_type": "image/png"
                }
            }
            dimensions = f"Screen dimensions: {res[1]}x{res[2]} pixels"
            chat_history.append({"role": "user", "parts": [image_part, {"text": dimensions}]})
            return "screenshot captured successfully"
        case 'give_valid_command':
            print('Invalid command - please rephrase your request')
            return 'Invalid command received'
        case 'stop':
            res = 'stop_agent' 
            chat_history.append({"role": "model", "parts": [res]})
            return res
        case _:
            return f'Error: Unknown tool: {tool}'


                
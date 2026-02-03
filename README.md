
# Desktop AI Agent 🤖💻

**Desktop AI Agent** is a voice-controlled, autonomous desktop assistant powered by Google Gemini (Gemini 2.5 Flash). It listens to your voice commands, interprets your intent using an LLM, and performs actions on your computer such as file management, web browsing, application control, and mouse/keyboard automation.

It features a modern GUI built with PySide6 and runs a continuous loop to handle multi-step tasks autonomously.

## ✨ Features

* **🎙️ Voice Control:** Real-time speech-to-text using `SpeechRecognition`.
* **🧠 LLM Intelligence:** Powered by Google's `gemini-2.5-flash` for understanding context and planning execution steps.
* **🔄 Continuous Mode:** The agent maintains context across actions, allowing it to perform multi-step tasks (e.g., "Make a folder, create a file inside it, and open it in VS Code") without needing constant prompts.
* **🛠️ Extensive Toolset:**
* **File System:** Create folders, write to files, open files.
* **Navigation:** Open applications and websites.
* **Input Control:** Simulate keyboard typing and shortcuts.
* **Mouse Control:** Move pointer and click buttons based on screen coordinates.
* **Vision:** Capture and analyze screenshots to understand the screen layout.
* **Terminal:** Execute system CMD commands.


* **🖥️ Modern GUI:** Clean interface built with PySide6 (Qt) featuring status updates and logs.
* **🔊 Text-to-Speech:** Audio feedback for status updates.

## 📂 Project Structure

* **`main.py`**: The entry point of the application.
* **`homepage.py`**: Manages the Frontend UI, signals, and user interactions.
* **`backend.py`**: Handles background threads for Voice Recognition and Text-to-Speech.
* **`LLM.py`**: Core logic for communicating with the Gemini API, managing chat history, and the recursive execution loop.
* **`tools.py`**: Implementation of the actual tools (OS interaction, mouse/keyboard control, etc.) used by the LLM.
* **`components.py`**: Reusable UI components (Styled Buttons, Signals).

## 🚀 Installation

### Prerequisites

* Python 3.8+
* A Google Gemini API Key

### 1. Clone the Repository

```bash
git clone <your-repo-url>
cd desktop-ai-agent

```

### 2. Install Dependencies

Install the required Python packages:

```bash
pip install google-generativeai pyside6 SpeechRecognition pyttsx3 pynput pyautogui pillow python-dotenv

```

*Note: You may also need to install `pyaudio` for microphone access. If `pip install pyaudio` fails, look for specific installation instructions for your OS.*

### 3. Environment Setup

Create a `.env` file in the root directory of the project and add your API key and working directory:

```env
GEMINI_API_KEY=your_google_gemini_api_key_here
WORKING_DIRECTORY=D:\path\to\your\workspace

```

* `GEMINI_API_KEY`: Get this from Google AI Studio.
* `WORKING_DIRECTORY`: The default path where the agent will perform file operations.

## 🎮 Usage

1. Run the application:
```bash
python main.py

```


2. The GUI will open.
3. Click the **"▶️ Start Listening"** button.
4. Speak a command clearly.
* *Example: "Create a project folder named 'Website', create an index.html file inside it, and open it in Notepad."*
* *Example: "Open YouTube and search for Python tutorials."*


5. The agent will process the audio, display the recognized text, and begin executing the necessary steps on your computer.
6. Click **"⏹️ Stop Listening"** to pause voice capture.

## ⚠️ Important Safety Note

This agent has the ability to **execute shell commands, move the mouse, type on your keyboard, and modify files**.

* **Review Code:** Ensure you understand what `tools.py` does before running.
* **Sandbox:** It is recommended to run this in a controlled environment or define a specific `WORKING_DIRECTORY` that contains only non-critical files.
* **Mouse/Keyboard:** When the agent is moving the mouse or typing, avoid using the computer manually to prevent interference.

## 🛠️ Customization

You can add new capabilities to the agent by modifying **`tools.py`** to define the function and **`LLM.py`** to add the tool definition to the `SYSTEM_PROMPT`.


---

**Created by GTcoder**

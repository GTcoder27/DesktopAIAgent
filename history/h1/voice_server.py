from flask import Flask, jsonify, request
from flask_cors import CORS
import speech_recognition as sr
import pyttsx3
import threading
import time

app = Flask(__name__)
CORS(app)

recognizer = sr.Recognizer()
engine = pyttsx3.init()
is_listening = False
listening_thread = None

def speak(text):
    """Text to speech"""
    engine.say(text)
    engine.runAndWait()

def listen_continuous():
    """Continuous listening in background thread"""
    global is_listening
    
    while is_listening:
        try:
            with sr.Microphone() as source:
                print("🎧 Listening...")
                recognizer.adjust_for_ambient_noise(source, duration=0.5)
                audio = recognizer.listen(source, timeout=2, phrase_time_limit=3)
                
            # Recognize speech
            text = recognizer.recognize_google(audio)
            print(f"📝 Recognized: {text}")
            
            # Send to frontend (you can add WebSocket for real-time updates)
            # For now, we'll use polling
            
        except sr.WaitTimeoutError:
            print("⏱️ Timeout - no speech detected")
        except sr.UnknownValueError:
            print("❓ Could not understand audio")
        except Exception as e:
            print(f"❌ Error: {e}")
            time.sleep(1)

@app.route('/speak', methods=['POST'])
def api_speak():
    """Endpoint to make Jarvis speak"""
    data = request.json
    text = data.get('text', '')
    
    if text:
        threading.Thread(target=speak, args=(text,)).start()
        return jsonify({'status': 'success', 'message': 'Speaking'})
    
    return jsonify({'status': 'error', 'message': 'No text provided'}), 400

@app.route('/listen', methods=['POST'])
def api_listen():
    """Single listening request"""
    try:
        with sr.Microphone() as source:
            print("🎧 Listening for command...")
            recognizer.adjust_for_ambient_noise(source, duration=0.5)
            audio = recognizer.listen(source, timeout=5, phrase_time_limit=10)
        
        text = recognizer.recognize_google(audio)
        print(f"📝 Recognized: {text}")
        
        return jsonify({
            'status': 'success',
            'text': text,
            'confidence': 1.0
        })
        
    except sr.WaitTimeoutError:
        return jsonify({'status': 'error', 'message': 'Timeout - no speech detected'}), 408
    except sr.UnknownValueError:
        return jsonify({'status': 'error', 'message': 'Could not understand audio'}), 400
    except Exception as e:
        return jsonify({'status': 'error', 'message': str(e)}), 500

@app.route('/start', methods=['POST'])
def start_listening():
    """Start continuous listening"""
    global is_listening, listening_thread
    
    if not is_listening:
        is_listening = True
        listening_thread = threading.Thread(target=listen_continuous)
        listening_thread.start()
        return jsonify({'status': 'success', 'message': 'Started listening'})
    
    return jsonify({'status': 'error', 'message': 'Already listening'}), 400

@app.route('/stop', methods=['POST'])
def stop_listening():
    """Stop continuous listening"""
    global is_listening
    
    if is_listening:
        is_listening = False
        return jsonify({'status': 'success', 'message': 'Stopped listening'})
    
    return jsonify({'status': 'error', 'message': 'Not listening'}), 400

@app.route('/status', methods=['GET'])
def status():
    """Check server status"""
    return jsonify({
        'status': 'online',
        'listening': is_listening
    })

if __name__ == '__main__':
    speak("Initializing Jarvis...")
    print("🚀 Jarvis Voice Server Started")
    print("📡 Server running on http://localhost:5000")
    app.run(host='0.0.0.0', port=5000, debug=False)


"""
Backend
"""

import speech_recognition as sr
import pyttsx3
import threading
from typing import Callable, Optional, List


class VoiceRecognitionBackend:
    """Backend class for voice recognition and text-to-speech"""
    
    def __init__(self):
        """Initialize the voice recognition backend"""
        self.recognizer = sr.Recognizer()
        self.engine = None
        self.is_listening = False
        self.listening_thread = None
        
        # Callbacks
        self.on_text_recognized: Optional[Callable[[str], None]] = None
        self.on_status_update: Optional[Callable[[str, str], None]] = None
        self.on_error: Optional[Callable[[str], None]] = None
        
        # Initialize TTS engine
        self._init_tts_engine()
        
    def _init_tts_engine(self):
        """Initialize text-to-speech engine with error handling"""
        try:
            self.engine = pyttsx3.init()
            self.engine.setProperty('rate', 150)  # Speed
            self.engine.setProperty('volume', 0.9)  # Volume
        except Exception as e:
            self.engine = None
            print(f"TTS initialization error: {e}")
            
    def get_microphone_list(self) -> List[str]:
        """Get list of available microphones"""
        try:
            mic_list = sr.Microphone.list_microphone_names()
            if not mic_list:
                return ["Default Microphone"]
            return mic_list
        except Exception as e:
            print(f"Error getting microphones: {e}")
            return ["Default Microphone"]
            
    def set_callbacks(self, 
                     on_text_recognized: Optional[Callable[[str], None]] = None,
                     on_status_update: Optional[Callable[[str, str], None]] = None,
                     on_error: Optional[Callable[[str], None]] = None):
        """Set callback functions for events"""
        if on_text_recognized:
            self.on_text_recognized = on_text_recognized
        if on_status_update:
            self.on_status_update = on_status_update
        if on_error:
            self.on_error = on_error
            
    def _emit_status(self, message: str, color: str = "#2196F3"):
        """Emit status update"""
        if self.on_status_update:
            self.on_status_update(message, color)
            
    def _emit_text(self, text: str):
        """Emit recognized text"""
        if self.on_text_recognized:
            self.on_text_recognized(text)
            
    def _emit_error(self, error: str):
        """Emit error"""
        if self.on_error:
            self.on_error(error)
            
    def speak(self, text: str):
        """Text to speech in a separate thread"""
        if not self.engine:
            print("TTS engine not available")
            return
            
        def speak_thread():
            try:
                self.engine.say(text)
                self.engine.runAndWait()
            except Exception as e:
                print(f"Speech error: {e}")
        
        thread = threading.Thread(target=speak_thread, daemon=True)
        thread.start()
        
    def _listen_continuous(self, mic_index: int):
        """Continuous listening in background thread"""
        while self.is_listening:
            try:
                # Use selected microphone or default
                if mic_index > 0:
                    mic = sr.Microphone(device_index=mic_index)
                else:
                    mic = sr.Microphone()
                    
                with mic as source:
                    self._emit_status("🎧 Listening... Speak now!", "#2196F3")
                    self.recognizer.adjust_for_ambient_noise(source, duration=0.5)
                    audio = self.recognizer.listen(source, timeout=2, phrase_time_limit=5)
                
                # Recognize speech
                self._emit_status("🔄 Processing your speech...", "#FF9800")
                text = self.recognizer.recognize_google(audio)
                print(text)
                self._emit_text(text)
                self._emit_status(f"✅ Recognized: {text}", "#4CAF50")
                
            except sr.WaitTimeoutError:
                self._emit_status("⏱️ No speech detected, still listening...", "#FF9800")
            except sr.UnknownValueError:
                self._emit_status("❓ Could not understand, please speak clearly", "#FF5722")
            except sr.RequestError as e:
                self._emit_error(f"Network error: {str(e)}\n\nPlease check your internet connection.")
                self.is_listening = False
                break
            except Exception as e:
                self._emit_error(f"Error: {str(e)}")
                self.is_listening = False
                break
                
    def start_listening(self, mic_index: int = 0):
        """Start listening for speech"""
        if not self.is_listening:
            self.is_listening = True
            self.listening_thread = threading.Thread(
                target=self._listen_continuous, 
                args=(mic_index,),
                daemon=True
            )
            self.listening_thread.start()
            return True
        return False
            
    def stop_listening(self):
        """Stop listening for speech"""
        if self.is_listening:
            self.is_listening = False
            if self.listening_thread:
                self.listening_thread.join(timeout=3)
            self._emit_status("⏹️ Stopped listening", "#757575")
            return True
        return False
        
    def test_speech(self):
        """Test text-to-speech functionality"""
        if self.engine:
            self.speak("Hello! This is a test of the text to speech system. The voice recognition is working properly.")
            self._emit_status("🔊 Testing text-to-speech...", "#2196F3")
            return True
        else:
            self._emit_error("Text-to-speech engine is not available.")
            return False
            
    def is_tts_available(self) -> bool:
        """Check if text-to-speech is available"""
        return self.engine is not None
        
    def cleanup(self):
        """Clean up resources"""
        self.stop_listening()
        if self.engine:
            try:
                self.engine.stop()
            except:
                pass

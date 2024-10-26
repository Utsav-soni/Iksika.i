# Importing libraries
import streamlit as st
import base64
import os
from gtts import gTTS
import tempfile

# To load the logo svg and converting into base64 format
def get_base64_of_bin_file(bin_file):
    with open(bin_file, 'rb') as f:
        return base64.b64encode(f.read()).decode()

# Audio related class, handles all the operation related to Audio
class TTSManager:
    def __init__(self):
        self.is_speaking = False
        self.current_audio = None
        self._setup_temp_dir()

    def _setup_temp_dir(self):
        """Setup temporary directory for audio files"""
        self.temp_dir = tempfile.mkdtemp()
        if not os.path.exists(self.temp_dir):
            os.makedirs(self.temp_dir)

    def _cleanup_temp_files(self):
        """Clean up temporary audio files"""
        for file in os.listdir(self.temp_dir):
            if file.endswith('.mp3'):
                try:
                    os.remove(os.path.join(self.temp_dir, file))
                except Exception as e:
                    st.error(f"Error cleaning up temporary files: {str(e)}")

    def create_audio(self, text, language='en'):
        """Create and play audio from text"""
        try:
            self._cleanup_temp_files()
            
            # Generate unique temporary file path
            temp_file = os.path.join(self.temp_dir, f'audio_{hash(text)}.mp3')
            
            # Create TTS audio file
            tts = gTTS(text=text, lang=language, slow=False)
            tts.save(temp_file)
            
            # Read the audio file and convert to base64
            with open(temp_file, 'rb') as audio_file:
                audio_bytes = audio_file.read()
                audio_base64 = base64.b64encode(audio_bytes).decode()
            
            # Create audio element in Streamlit
            audio_html = f"""
                <audio autoplay>
                    <source src="data:audio/mp3;base64,{audio_base64}" type="audio/mp3">
                    Your browser does not support the audio element.
                </audio>
            """
            st.markdown(audio_html, unsafe_allow_html=True)
            
            self.current_audio = audio_html
            self.is_speaking = True
            
        except Exception as e:
            st.error(f"Error creating audio: {str(e)}")
            self.is_speaking = False
            self.current_audio = None

    def stop_audio(self):
        """Stop currently playing audio"""
        if self.is_speaking:
            # Clear the audio element
            st.markdown("""
                <script>
                    var audios = document.getElementsByTagName('audio');
                    for(var i = 0, len = audios.length; i < len; i++){
                        audios[i].pause();
                        audios[i].currentTime = 0;
                    }
                </script>
            """, unsafe_allow_html=True)
            
            self.is_speaking = False
            self.current_audio = None

    def play_sound(self, sound_file):
        """Play a sound effect from a file"""
        try:
            with open(sound_file, 'rb') as f:
                audio_bytes = f.read()
                audio_base64 = base64.b64encode(audio_bytes).decode()
                
            audio_html = f"""
                <audio autoplay>
                    <source src="data:audio/mp3;base64,{audio_base64}" type="audio/mp3">
                    Your browser does not support the audio element.
                </audio>
            """
            st.markdown(audio_html, unsafe_allow_html=True)
            
        except Exception as e:
            st.error(f"Error playing sound: {str(e)}")

    def __del__(self):
        """Cleanup on deletion"""
        self._cleanup_temp_files()
        try:
            os.rmdir(self.temp_dir)
        except:
            pass

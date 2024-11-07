# ┏━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━┓
# ┃                                                       ┃
# ┃     Iksika.i - By Utsav Soni for Groq Bounty 1        ┃
# ┃                                                       ┃
# ┃         ── Discover Life in Every Frame ──            ┃
# ┃                                                       ┃
# ┗━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━┛
#
#  Email id : soniutsav22@gmail.com
# Linked in : www.linkedin.com/in/utsav-soni-9067b31b3

# Importing libraries
import streamlit as st
import os
from dotenv import load_dotenv
from src.tts_manager import TTSManager, get_base64_of_bin_file
from src.utils import capture_image, upload_image
from src.logger import logger
from groq import Groq
import time
from deep_translator import GoogleTranslator  # Using deep-translator for translation
from src.image_to_text import image_to_text


# Load environment variables
load_dotenv()

# Check for API keys and initialize services
GROQ_API_KEY = os.getenv("GROQ_API_KEY")
LANGSMITH_API_KEY = os.getenv("LANGSMITH_API_KEY")

# Initialize Groq client
client = Groq(api_key=GROQ_API_KEY)
llama_3_2 = 'llama-3.2-90b-vision-preview'

# For Groq communitiy and other developers: Paste your API keys here, If you want to explore the APP
#GROQ_API_KEY = XXXXXXXXXXXXXXXXX
#LANGSMITH_API_KEY = XXXXXXXXXXXX


# Error handling to check for Groq API
if not GROQ_API_KEY:
    logger.error("GROQ_API_KEY not set in the environment variables")
    st.error("API key for Groq is missing. Check your .env file.")
    st.stop()

# Initialize session state and constants
if 'tts_manager' not in st.session_state:
    st.session_state.tts_manager = TTSManager()

# Langsmith Tracing
os.environ["LANGCHAIN_TRACING_V2"] = "true"
os.environ["LANGCHAIN_PROJECT"] = "vision_app"
os.environ["LANGCHAIN_API_KEY"] = LANGSMITH_API_KEY

# All the supported languages in the app
SUPPORTED_LANGUAGES = {
'afrikaans': 'af', 'albanian': 'sq', 'amharic': 'am', 'arabic': 'ar', 'armenian': 'hy','assamese': 'as', 'aymara': 'ay', 'azerbaijani': 'az', 
'bambara': 'bm', 'basque': 'eu', 'belarusian': 'be', 'bengali': 'bn', 'bhojpuri': 'bho', 'bosnian': 'bs', 'bulgarian': 'bg',
'catalan': 'ca', 'cebuano': 'ceb', 'chichewa': 'ny', 'chinese (simplified)': 'zh-CN', 'chinese (traditional)': 'zh-TW', 'corsican': 'co', 'croatian': 'hr', 'czech': 'cs', 
'danish': 'da', 'dhivehi': 'dv', 'dogri': 'doi', 'dutch': 'nl', 
'english': 'en', 'esperanto': 'eo', 'estonian': 'et', 'ewe': 'ee', 
'filipino': 'tl', 'finnish': 'fi', 'french': 'fr', 'frisian': 'fy', 
'galician': 'gl', 'georgian': 'ka', 'german': 'de', 'greek': 'el', 'guarani': 'gn', 'gujarati': 'gu', 
'haitian creole': 'ht', 'hausa': 'ha', 'hawaiian': 'haw', 'hebrew': 'iw', 'hindi': 'hi', 'hmong': 'hmn', 'hungarian': 'hu', 
'icelandic': 'is', 'igbo': 'ig', 'ilocano': 'ilo', 'indonesian': 'id', 'irish': 'ga', 'italian': 'it', 
'japanese': 'ja', 'javanese': 'jw', 
'kannada': 'kn', 'kazakh': 'kk', 'khmer': 'km', 'kinyarwanda': 'rw', 'konkani': 'gom', 'korean': 'ko', 'krio': 'kri', 'kurdish (kurmanji)': 'ku', 'kurdish (sorani)': 'ckb', 'kyrgyz': 'ky', 
'lao': 'lo', 'latin': 'la', 'latvian': 'lv', 'lingala': 'ln', 'lithuanian': 'lt', 'luganda': 'lg', 'luxembourgish': 'lb', 
'macedonian': 'mk', 'maithili': 'mai', 'malagasy': 'mg', 'malay': 'ms', 'malayalam': 'ml', 'maltese': 'mt', 'maori': 'mi', 'marathi': 'mr', 'meiteilon (manipuri)': 'mni-Mtei', 'mizo': 'lus', 'mongolian': 'mn', 'myanmar': 'my', 
'nepali': 'ne', 'norwegian': 'no', 
'odia (oriya)': 'or', 'oromo': 'om', 
'pashto': 'ps', 'persian': 'fa', 'polish': 'pl', 'portuguese': 'pt', 'punjabi': 'pa', 
'quechua': 'qu', 
'romanian': 'ro', 'russian': 'ru', 
'samoan': 'sm', 'sanskrit': 'sa', 'scots gaelic': 'gd', 'sepedi': 'nso', 'serbian': 'sr', 'sesotho': 'st', 'shona': 'sn', 'sindhi': 'sd', 'sinhala': 'si', 'slovak': 'sk', 'slovenian': 'sl', 'somali': 'so', 'spanish': 'es', 'sundanese': 'su', 'swahili': 'sw', 'swedish': 'sv', 
'tajik': 'tg', 'tamil': 'ta', 'tatar': 'tt', 'telugu': 'te', 'thai': 'th', 'tigrinya': 'ti', 'tsonga': 'ts', 'turkish': 'tr', 'turkmen': 'tk', 'twi': 'ak', 
'ukrainian': 'uk', 'urdu': 'ur', 'uyghur': 'ug', 'uzbek': 'uz', 
'vietnamese': 'vi', 
'welsh': 'cy', 
'xhosa': 'xh', 
'yiddish': 'yi', 'yoruba': 'yo', 
'zulu': 'zu'}

# Initialize session state variables
def init_session_state():
    if 'last_response' not in st.session_state:
        st.session_state.last_response = None
    if 'last_processed_image' not in st.session_state:
        st.session_state.last_processed_image = None
    if 'description_visible' not in st.session_state:
        st.session_state.description_visible = False
    if 'needs_audio_playback' not in st.session_state:
        st.session_state.needs_audio_playback = False
    if 'input_mode' not in st.session_state:
        st.session_state.input_mode = 'capture'
    if 'tts_language' not in st.session_state:
        st.session_state.tts_language = 'en'
    if 'auto_speak' not in st.session_state:
        st.session_state.auto_speak = True
    if 'selected_language_name' not in st.session_state:
        st.session_state.selected_language_name = 'english'

# Adding css in this file
css_path = os.path.join('static', 'style.css')
with open(css_path) as f:
    st.markdown(f'<style>{f.read()}</style>', unsafe_allow_html=True)

# Loading logos and converting them into base64
logo_left_b64 = get_base64_of_bin_file('assets/mark2.svg')
logo_right_b64 = get_base64_of_bin_file('assets/mark1.svg') 

# Setting up logos on the web app
st.markdown(f"""
    <div style="display: flex; justify-content: center; align-items: center; gap: 20px;">
        <div style="background-color: #ededed; border-radius: 50px; padding: 10px; width: 420px; text-align: center;">
            <img src="data:image/svg+xml;base64,{logo_left_b64}" style="height: 69px; width: 190px; object-fit: contain;">
        </div>
        <div style="background-color: #ededed; border-radius: 50px; padding: 10px; width: 420px; text-align: center;">
            <img src="data:image/svg+xml;base64,{logo_right_b64}" style="height: 69px; width: 240px; object-fit: contain;">
        </div>
    </div>
""", unsafe_allow_html=True)

# UI and Settings for button and other language related configurations 
 
def create_settings_ui():
    with st.expander("🔧  Language  Settings", expanded=False):
        
        st.markdown("## Language & Audio Settings")
        selected_language = st.selectbox(
            "Select Language",
            options=list(SUPPORTED_LANGUAGES.keys()),
            index=list(SUPPORTED_LANGUAGES.keys()).index(st.session_state.selected_language_name)
        )
        
        if selected_language != st.session_state.selected_language_name:
            st.session_state.tts_manager.play_sound("assets/button3.mp3")
            st.session_state.selected_language_name = selected_language
            st.session_state.tts_language = SUPPORTED_LANGUAGES[selected_language]

        auto_speak = st.checkbox(
            "Auto Speak Description",
            value=st.session_state.auto_speak,
            help="Automatically speak the description when generated"
        )
        
        if auto_speak != st.session_state.auto_speak:
            st.session_state.auto_speak = auto_speak
            
        if st.button("🔊 Test Audio"):
            test_text = f"This is a test message in {selected_language}"
            st.session_state.tts_manager.create_audio(test_text, language=st.session_state.tts_language)


# Process the captured or uploaded image and generate the response in respective language, by default it's English
def process_image(base64_image):
    if base64_image and base64_image != st.session_state.last_processed_image:
        st.session_state.last_processed_image = base64_image
        st.session_state.description_visible = False
        st.session_state.last_response = None

        prompt="Describe this image smartly in 4-5 lines to the person who is completely unaware of the surroundings in a descriptive way."

        with st.spinner("Generating description..."):
            # Simulated image processing response
            response = image_to_text(client, llama_3_2, base64_image, prompt)
            
            selected_language = st.session_state.tts_language
            if selected_language != 'en':
                translator = GoogleTranslator(source='en', target=selected_language)
                response = translator.translate(response)
            
            st.session_state.last_response = response
            st.session_state.description_visible = True
            
            if st.session_state.auto_speak:
                st.session_state.tts_manager.create_audio(
                    response,
                    language=selected_language
                )

# main function to handle the flow and overall logic for the webApp
def main():
    init_session_state()
    st.markdown("""
    <h1 style="text-align: center;">
        <span class="gradient-text">Iksika.i</span><span class="normal-eye"> 𓆩👁️𓆪</span>
    </h1>
""", unsafe_allow_html=True)

    st.markdown("""📸 Take a picture or Upload one to receive an instant Audio Description in your selected Language !""")
    st.markdown(""" """)
    
    # Capture Mode Button for turning on camera and Upload mode Button for uploading image from
    col1, col2 = st.columns([1, 1])
    with col1:
        if st.button("📸 Capture Mode", use_container_width=True, 
                    type="primary" if st.session_state.input_mode == 'capture' else "secondary"):
            st.session_state.tts_manager.play_sound("assets/button1.mp3")
            st.session_state.input_mode = 'capture'
            st.session_state.last_processed_image = None
            st.rerun()
    
    with col2:
        if st.button("📤 Upload Mode", use_container_width=True,
                    type="primary" if st.session_state.input_mode == 'upload' else "secondary"):
            st.session_state.tts_manager.play_sound("assets/button2.mp3")
            st.session_state.input_mode = 'upload'
            st.session_state.last_processed_image = None
            st.rerun()

    # Logic to control Caputure and Upload image logic
    with st.container():
        base64_image = None
        if st.session_state.input_mode == 'capture':
            base64_image = capture_image()
        else:
            base64_image = upload_image()

        if base64_image:
            process_image(base64_image)

    if st.session_state.description_visible and st.session_state.last_response:
        st.markdown("### Image Description:", unsafe_allow_html=True)
        st.write(st.session_state.last_response)

    # Importing Language Setting button and UI
    create_settings_ui()

    # Regenerate Description and  Replay Audio button
    col1, col2 = st.columns([1, 1])
    with col1:
        if st.button("📸 Regenerate Description", use_container_width=True):
            st.session_state.tts_manager.play_sound("assets/button1.mp3")
            st.session_state.last_processed_image = None
            st.session_state.needs_audio_playback = True
            st.rerun()
    
    with col2:
        if st.button("🔊 Replay Audio", use_container_width=True):
            st.session_state.tts_manager.play_sound("assets/button2.mp3")
            if st.session_state.last_response:
                st.session_state.tts_manager.create_audio(
                    st.session_state.last_response,
                    language=st.session_state.tts_language
                )
                
    if "show_contact_info" not in st.session_state:
        st.session_state.show_contact_info = False

    # Create two empty columns for centering content
   col2= st.columns([1])

# Centered button and logic to show contact information
    with col2:
        if st.button("Contact Developer"):
            st.session_state.show_contact_info = True

# Centered contact information if the button is clicked
    if st.session_state.show_contact_info:
        with col2:
            st.markdown("""
            ---
            **Let's Connect**
            - **Email:** soniutsav22@gmail.com
            """, unsafe_allow_html=True)

# Run main() only if this script is executed directly
if __name__ == "__main__":
    main()

# Iksika.i - Discover Life in Every Frame

live @: https://iksika-by-utsav-soni.streamlit.app/

## Introduciton

For further use cases and comprehensive documentation, please refer to this URL: https://github.com/Utsav-soni/Iksika.i/blob/main/iksika.i_By_Utsav_Soni.pdf

Iksika/Ikshika, rooted in the Sanskrit word for "a glance" or "look," perfectly captures the essence of this comprehensive vision AI application. Demonstrating the power of modern Vision AI, Iksika is designed to serve general and specialized applications alike. Using Meta's LLaMA 3.2 90B Vision Preview model (Powered with Groq’s LPU Inference Engine), the app is hosted on Streamlit to seamlessly analyze images captured in real-time via camera or uploaded from a device. With a quick analysis, it provides detailed descriptions of surroundings and generates responses in over 130+ languages with text-to-speech functionality, delivering an instant text and voice description in the chosen language.

The application is intentionally built to support visually impaired individuals, aligning with its primary goal of making the world more accessible to those with visual challenges. The UI is intuitively designed for easy adaptation and interaction, empowering users to experience the environment using just a device’s camera and speaker. Beyond accessibility, Iksika has diverse applications across social and business domains, from tourism to translation, education, personalized assistance, and many more.

Regarding development, Iksika’s codebase is modularly structured to enhance scalability and customization. The project reflects proficiency in CSS integration, Python function interactions, and the use of open-source libraries like Groq, Streamlit, PIL, gTTS, Deep Translator, and Logger alongside APIs such as Groq and LangSmith. Developed solely by Utsav Soni, Iksika embodies vision AI capabilities aimed at creating social impact and business value.



## Features of Iksika

- **Real-Time Image Analysis**: Capture live images or upload them from your device, and instantly get a detailed description of your surroundings in your language.
- **Groq Powered LLaMA 3.2 Vision**: Utilizes Meta’s LLaMA 3.2-90B Vision Preview model, optimized with Groq's inference engine for high-performance image recognition and analysis.
- **Multi-Language Support**: Provides descriptions in over 50 languages, making it accessible to users globally with customizable language selection.
- **Instant Talkback**: Generates text-to-speech output in the selected language, enabling users to hear the description for hands-free interaction.
- **Regenerate Description**: Offers a "Regenerate Description" button for obtaining an updated or alternative description with a single click, ensuring accurate insights.
- **Replay Audio**: Features a "Replay Audio" button to easily listen to the description again, providing an effortless way to revisit information.
- **Traceable Insights with LangSmith**: Integrates LangSmith for traceable insights, offering transparent tracking and logging for analysis accuracy.
- **Intuitive UI for Accessibility**: Designed with a user-friendly interface that’s easy to navigate and **accessible to visually impaired users**.
- **Modular Code Structure**: Organized in modules to support easy scalability, customization, and integration of additional features.
- **Open-Source Library Integration**: Uses a suite of powerful libraries, including Groq, Streamlit, gTTS, Logger, and Deep Translator, for seamless functionality.
- **Designed for Diverse Use Cases**: Adaptable for various applications, from assisting visually impaired users to supporting tourism, education, and business needs.


## Prerequisites

- Python 3.9+
- Required APIs:
   - Groq
   - Langsmith
 
  
## Installation

1. Clone the repository:
```bash
git clone https://github.com/Utsav-soni/Iksika.i.git
```
```bash
cd Iksika.i
```

2. Install dependencies:
requirements.txt: Prepared in such a way that it can be used for Scaleability and other GenAI Application
```bash
pip install -r requriements.txt
```


## Usage

1. Get your Groq and Langsmith API key:
  - Sign up on Groq and Langsmith
  - Go to the API section
  - Create a new API and copy it

2. Enter your Groq and Langsmith API key in the commented line in iksika.py or Create .env file and paste it into the same folder as the iksika.py
   Format for .env:
   `GROQ_API_KEY=XXXXXXX, LANGSMITH_API_KEY=XXXXXXXXXXX`

3. Run it using the streamlit run command using the command given below.

4. Start the application but before that complete the following steps:
```bash
streamlit run ikshika.py
```

5. Click on the link generated in the output terminal, e.g.
`http://192.168.XXX.XX:XXXX` or `http://localhoat:XXXX`


## Development

The application uses:
- Streamlit for web interface
- Groq for accessing the Llama model
- Langsmith for tracking
- PIL for image processing and resizing
- Custom CSS for accessible UI
- Markdown formatting for logo
- JSON to handle data in a structured way
- logging to emit log messages from Python programs
- base64 for converting images from PNG to base64 and vice versa
- gTTS for text-to-speech
- deep-translator for translating English to other languages 
   
## Acknowledgements

- Powered by Groq for fast inference
- Deployed using Streamlit

## Let's Connect

- Name: Utsav Soni
- Mail id: soniutsav22@gmail.com
- Linked In: www.linkedin.com/in/utsav-soni-9067b31b3

# Importing libraries
from src.logger import logger
import streamlit as st
from langsmith import traceable

# Tracing it at Langsmith 
@traceable
def image_to_text(client, model, base64_image, prompt):
    """Convert an image to text using the Groq client."""
    try:
        chat_completion = client.chat.completions.create(
            messages=[
                {
                    "role": "user",
                    "content": [
                        {"type": "text", "text": prompt},
                        {"type": "image_url", "image_url": {"url": f"data:image/png;base64,{base64_image}"}}
                    ]
                }
            ],
            model=model
        )
        return chat_completion.choices[0].message.content
    except Exception as e:
        st.error(f"Error generating description: {str(e)}")
        return None
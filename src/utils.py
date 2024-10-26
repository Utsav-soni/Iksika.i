# Importing libraries
import streamlit as st
from PIL import Image
import io
import base64
from src.logger import logger
import json
import time

# Reducing image size to 1120 x 1120 as per L
def target_image_size(img):
    """
    Process image size - compress if larger than 1120x1120, maintain aspect ratio if smaller
    
    Args:
        img (PIL.Image): Input image
        
    Returns:
        PIL.Image: Processed image
    """
    width, height = img.size
    target_size = (1120, 1120)
    
    # If image is smaller than target in both dimensions, keep original size
    if width <= target_size[0] and height <= target_size[1]:
        return img
        
    # Calculate aspect ratio
    aspect_ratio = width / height
    
    # Determine new dimensions while maintaining aspect ratio
    if aspect_ratio > 1:  # Width is larger
        new_width = target_size[0]
        new_height = int(new_width / aspect_ratio)
    else:  # Height is larger or equal
        new_height = target_size[1]
        new_width = int(new_height * aspect_ratio)
        
    # Resize image with LANCZOS resampling for better quality
    resized_img = img.resize((new_width, new_height), Image.Resampling.LANCZOS)
    return resized_img

# Saving the base64 image in output.txt for debugging the image size and quality
def save_base64_image(base64_image):
    """Save the Base64 image string to a text file."""
    try:
        json_data = json.dumps({"image": base64_image})
        filename = 'output.txt'
        with open(filename, 'w') as file:
            json.dump(json_data, file, indent=4)
    except Exception as e:
        st.error(f"Error saving image data: {str(e)}")


# Capture the image and return the base64 format of captured image
def capture_image():
    """Capture an image from the webcam and encode it as Base64."""
    with st.container():
        img_file = st.camera_input("Take a picture", help="Click to take a photo")

    if img_file:
        st.session_state.tts_manager.play_sound("assets/camera.mp3")
        try:
            img = Image.open(img_file)
            # Process image size
            img = target_image_size(img)
            img_bytes = io.BytesIO()
            img.save(img_bytes, format='PNG')
            img_bytes = img_bytes.getvalue()
            base64_image = base64.b64encode(img_bytes).decode('utf-8')
            save_base64_image(base64_image)
            return base64_image
        except Exception as e:
            st.error(f"Error capturing image: {str(e)}")
            return None
    return None


# upload the image and return the base64 format of uploaded image
def upload_image():
    """Upload an image from gallery and encode it as Base64."""
    uploaded_file = st.file_uploader("Upload an image", type=["png", "jpg", "jpeg"])
    
    if uploaded_file:
        try:
            # Read the image
            img = Image.open(uploaded_file)
            
            # Display preview
            st.markdown("<div class='upload-preview'>", unsafe_allow_html=True)
            st.image(img, caption="Preview", use_column_width=True)
            st.markdown("</div>", unsafe_allow_html=True)
            
            # Process the image
            img_bytes = io.BytesIO()
            img = target_image_size(img)
            img.save(img_bytes, format='PNG')
            img_bytes = img_bytes.getvalue()
            base64_image = base64.b64encode(img_bytes).decode('utf-8')
            save_base64_image(base64_image)
            
            # Play camera sound for consistency
            st.session_state.tts_manager.play_sound("assets/camera.mp3")
            
            return base64_image
        except Exception as e:
            st.error(f"Error uploading image: {str(e)}")
            return None
    return None


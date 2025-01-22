import streamlit as st
import anthropic
from PIL import Image
import io
import base64
import os
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# Get API Key from environment variable
ANTHROPIC_API_KEY = os.getenv("ANTHROPIC_API_KEY")

if not ANTHROPIC_API_KEY:
    st.error("❌ API Key not found. Please set the ANTHROPIC_API_KEY environment variable.")
    st.stop()

def format_analysis(response):
    # Extract the text content from the response
    text = response.content[0].text
    
    # Split into sections
    sections = text.split('\n\n')
    
    # Create formatted output
    st.subheader("📊 Analysis Results")
    
    # Use columns for better layout
    col1, col2 = st.columns(2)
    
    with col1:
        st.markdown("### 🎯 Position Analysis")
        st.markdown("#### Keyboard Position")
        st.write(sections[1].replace("1. Location of keyboard relative to table edges:\n", ""))
        
        st.markdown("#### Mouse Position")
        st.write(sections[2].replace("2. Location of mouse relative to table edges:\n", ""))
    
    with col2:
        st.markdown("### 📏 Measurements")
        st.markdown("#### Alignment")
        st.write(sections[3].replace("3. Whether keyboard and mouse are aligned:\n", ""))
        
        st.markdown("#### Distances")
        st.write(sections[4].replace("4. Approximate measurements and distances:\n", ""))

def main():
    st.title("🖥️ Workspace Ergonomics Analyzer")
    st.write("Upload an image of your workspace to analyze keyboard and mouse positioning")
    
    # File uploader
    uploaded_file = st.file_uploader("Choose an image", type=["jpg", "jpeg", "png"])
    
    if uploaded_file is not None:
        # Display original image
        image = Image.open(uploaded_file)
        st.image(image, caption="Uploaded Image", use_column_width=True)
        
        # Convert image to base64
        buffered = io.BytesIO()
        image.save(buffered, format=image.format)
        img_str = base64.b64encode(buffered.getvalue()).decode()
        
        # Initialize Anthropic client
        client = anthropic.Client(api_key=ANTHROPIC_API_KEY)
        
        if st.button("Analyze Workspace"):
            with st.spinner("🔍 Analyzing your workspace..."):
                try:
                    # Call Claude API
                    message = client.messages.create(
                        model="claude-3-opus-20240229",
                        max_tokens=1024,
                        messages=[{
                            "role": "user",
                            "content": [
                                {
                                    "type": "text",
                                    "text": """Please analyze this workspace image and provide:
                                    1. Location of keyboard relative to table edges
                                    2. Location of mouse relative to table edges
                                    3. Whether keyboard and mouse are aligned
                                    4. Approximate measurements and distances"""
                                },
                                {
                                    "type": "image",
                                    "source": {
                                        "type": "base64",
                                        "media_type": "image/jpeg",
                                        "data": img_str
                                    }
                                }
                            ]
                        }]
                    )
                    
                    # Display formatted results
                    st.success("✅ Analysis Complete!")
                    format_analysis(message)
                    
                except Exception as e:
                    st.error(f"❌ An error occurred: {str(e)}")
                    st.write("Please check your API key and try again.")

if __name__ == "__main__":
    main()

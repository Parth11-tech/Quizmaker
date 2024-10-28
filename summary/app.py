import streamlit as st
import openai
import fitz  # PyMuPDF
import os

# Set your OpenAI API key
openai.api_key = 'AIzaSyCVAjNdQyM37DKzmnrfkSmZTFYZjj_1oCs'

def extract_text_from_pdf(file_path):
    text = ""
    with fitz.open(file_path) as doc:
        for page in doc:
            text += page.get_text()
    return text

def generate_summary(text):
    response = openai.ChatCompletion.create(
        model="models/gemini-1.5-pro",
        messages=[{"role": "user", "content": f"Summarize the following text:\n\n{text}"}]
    )
    return response['choices'][0]['message']['content']

def main():
    st.title("PDF Summarizer")

    uploaded_file = st.file_uploader("Choose a PDF file", type="pdf")
    
    if uploaded_file is not None:
        # Save the uploaded file temporarily
        file_path = os.path.join("uploads", uploaded_file.name)
        with open(file_path, "wb") as f:
            f.write(uploaded_file.getbuffer())
        
        # Extract text and generate summary
        text = extract_text_from_pdf(file_path)
        summary = generate_summary(text)
        
        st.subheader("Summary:")
        st.write(summary)

        # Optionally, delete the temporary file
        os.remove(file_path)

if __name__ == "__main__":
    main()

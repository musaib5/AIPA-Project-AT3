import streamlit as st
import PyPDF2
import io
import os
import openai
from dotenv import load_dotenv

load_dotenv()

st.set_page_config(page_title="CVision- AI Resume Critic", page_icon="📃", layout="centered")

st.markdown("""
    <link rel="stylesheet" href="https://cdnjs.cloudflare.com/ajax/libs/font-awesome/6.5.0/css/all.min.css">
    <div style='text-align: center; padding-top: 1rem;'>
        <h1 style='font-size: 2.5em; margin-bottom: 0.2em;'>
            <i class="fas fa-file-alt" style="color:#4F8BF9;"></i> CVision- AI Resume Critic
        </h1>
        <p style='font-size: 1.2em; color: grey;'>
            Upload your resume , get AI-powered feedback tailored to your needs and a customized cover letter!
        </p>
    </div>
""", unsafe_allow_html=True)

OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")

uploaded_file = st.file_uploader("Upload your resume (PDF of TXT)", type=["pdf", "txt"])
job_role = st.text_input("Enter the job role you're targeting (optional)")

analyze = st.button("Analyze Resume")

def extract_text_from_pdf(pdf_file):
    pdf_reader = PyPDF2.PdfReader(pdf_file)
    text = ""
    for page in pdf_reader.pages:
        text += page.extract_text() + "\n"
    return text

def extract_text_from_file(uploaded_file):
    if uploaded_file.type == "application/pdf":
        return extract_text_from_pdf(io.BytesIO(uploaded_file.read()))
    return uploaded_file.read().decode("utf-8")

if analyze and uploaded_file:
    try:
        file_content = extract_text_from_file(uploaded_file)
        
        if not file_content.strip():
            st.error("File does not have any content...")
            st.stop()
        
        prompt = f"""Please analyze this resume and provide constructive feedback. 
        Focus on the following aspects:
        1. Content clarity and impact
        2. Skills presentation
        3. Experience descriptions
        4. Specific improvements for {job_role if job_role else 'general job applications'}
        
        Resume content:
        {file_content}
        
        Please provide your analysis in a clear, structured format with specific recommendations.
        Please generate a cover letter tailored for {job_role if job_role else 'general job applications'} with the help of my resume content.
        End the response without providing any follow up lines. """
        
        client = openai.OpenAI(api_key=OPENAI_API_KEY)
        response = client.chat.completions.create(
            model="gpt-4o",
            messages=[
                {"role": "system", "content": "You are an expert resume reviewer with years of experience in HR and recruitment."},
                {"role": "user", "content": prompt}
            ],
            temperature=0.7,
            max_tokens=1000
        )
        st.markdown("### Analysis Results")
        st.markdown(response.choices[0].message.content)
    
    except Exception as e:
        st.error(f"An error occurred: {str(e)}")



from dotenv import load_dotenv
load_dotenv()
import streamlit as st
from PIL import Image
import io
import os
import pdf2image
import base64
import google.generativeai as genai

genai.configure(api_key=os.getenv("GOOGLE_API"))

def get_gemini_response(input, pdf, prompt):
    model = genai.GenerativeModel('gemini-1.5-flash')  
    response = model.generate_content([input, pdf[0], prompt])
    return response.text


def input_pdf(uploaded_file):
    if uploaded_file is not None:
        images = pdf2image.convert_from_bytes(uploaded_file.read())
        first_page = images[0]

        img_byte_arr = io.BytesIO()
        first_page.save(img_byte_arr, format='JPEG')
        img_byte_arr = img_byte_arr.getvalue()

        pdf_parts = [
            {
                "mime_type": "image/jpeg",
                "data": base64.b64encode(img_byte_arr).decode()
            }
        ]
        return pdf_parts
    else:
        raise FileNotFoundError("File not Found")

st.set_page_config(page_title="Resume Analyzer")
st.header("Automated Resume Analyzer")
input_text = st.text_area("Job Description", key="input")
uploaded_file = st.file_uploader("Upload Resume (PDF)", type=["pdf"])


submit1 = st.button("Read my Resume")
submit2 = st.button("Percentage Match")

prompt1 = """You are a highly experienced Human Resource Manager in any field of Computer Science. Your task is to review the provided resume and job description.
              Share your professional evaluation on whether the candidate's profile aligns with the given job description. 
              Highlight the strengths and areas for improvement of the applicant in relation to the specified job description."""

prompt2 = """You are an expert ATS (Applicant Tracking System) with a deep understanding of any field in Computer Science and ATS functionality. 
             Your task is to evaluate the uploaded resume against a given job description and give the percentage match between the job description and the resume.
             First, the output should come as a percentage, then list the missing keywords, and finally provide your overall thoughts on it."""

if submit1:
    if uploaded_file is not None:
        pdf_content = input_pdf(uploaded_file)
        response = get_gemini_response(prompt1, pdf_content, input_text)
        st.subheader("The Response is")
        st.write(response)
    else:
        st.warning("⚠️ Please upload the resume before proceeding!")

if submit2:
    if uploaded_file is not None:
        pdf_content = input_pdf(uploaded_file)
        response = get_gemini_response(prompt2, pdf_content, input_text)
        st.subheader("The Response is")
        st.write(response)
    else:
        st.warning("⚠️ Please upload the resume before proceeding!")

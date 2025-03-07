import streamlit as st
from utils.display_logo import add_logo

def main():
    # Set page configuration
    st.set_page_config(page_title="🤖 AI-Powered Interview Question Generator", page_icon="📄", layout="wide")
    
    # Display logo at the top
    add_logo()
    
    # Page title
    st.markdown(
        "<h1 style='text-align: center; color: #3366cc;'>AI-Powered Interview Question Generator</h1>",
        unsafe_allow_html=True
    )
    
    # Objective Section
    st.markdown("## 🎯 Objective")
    st.info(
        "This system analyzes job descriptions and dynamically generates tailored screening and interview questions for different personas: **HR, Recruiter, Hiring Manager, and Technical Interviewer**. Suggested answers help interviewers evaluate candidate responses effectively."
    )
    
    # Key Features Section
    st.markdown("## 🔑 Key Features")
    col1, col2 = st.columns(2)

    with col1:
        st.markdown("✔ **Upload Job Description**: Supports **TXT, PDF, DOCX** formats.")
        st.markdown("✔ **AI-Powered Question Generation**: Tailored for **HR, Recruiter, Hiring Manager, and Technical Interviewer**.")
        st.markdown("✔ **Role-Specific Inquiries**: Covers general, experience-based, managerial, and technical questions.")

    with col2:
        st.markdown("✔ **Suggested Answers**: AI-generated responses to assist evaluation.")
        st.markdown("✔ **Structured Output**: View/download as **PDF or DOCX**.")
        st.markdown("✔ **User-Friendly Interface**: Simple upload and download process.")
    
    # How It Works Section
    st.markdown("## 🛠 How It Works")
    st.markdown(
        """
        **1️⃣ Upload Job Description** – Provide a job description in **TXT, PDF, or DOCX** format  
        **2️⃣ AI Analyzes Key Requirements** – Extracts relevant skills, responsibilities, and qualifications  
        **3️⃣ Generates Persona-Based Questions** – Tailored for **HR, Recruiter, Hiring Manager, and Technical Interviewer**  
        **4️⃣ AI Provides Suggested Answers** – Helps interviewers assess responses  
        **5️⃣ Download Structured Report** – Get the questions and answers in **PDF/DOCX** format  
        """
    )
    
    # Divider Line
    st.markdown("---")
    
    # Call-to-Action (Start Button)
    st.markdown("<h3 style='text-align: center;'>📄 Ready to Generate Questions?</h3>", unsafe_allow_html=True)
    
    col1, col2, _ = st.columns([1, 2, 1])  # Adjust the middle column width for better centering

    with col2:  # Place the button in the center column
        if st.button("🚀 Upload Job Description", use_container_width=True):
            if "user_email" in st.session_state and "user_name" in st.session_state:
                st.session_state.start_assessment = True
                st.experimental_rerun()
            else:
                st.warning("⚠ Please log in before starting the assessment.")
                st.switch_page("pages/0_Login.py")  # Redirect to login page


if __name__ == "__main__":
    main()

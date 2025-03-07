import streamlit as st
import requests
import os

from utils.display_logo import add_logo

FASTAPI_URL = os.getenv("BACKEND_API_URL", "http://localhost:8000")

# Ensure user is logged in
if "user_email" not in st.session_state or "user_name" not in st.session_state:
    st.warning("⚠ You need to log in before starting the assessment.")

    col1, col2, col3 = st.columns([1, 2, 1])
    with col2:
        if st.button("🔑 Go to Login", use_container_width=True):
            st.switch_page("pages/0_Login.py")

    st.stop()  # Stop further execution if not logged in

st.set_page_config(page_title="AI Powered Interview", page_icon="🧠", layout="centered")

# Add logo and title
add_logo()
st.title("AI-Generated Interview Questions")
st.markdown("---")


# Ensure session state variables exist
if "selected_personas" not in st.session_state:
    st.session_state["selected_personas"] = set()
if "job_description" not in st.session_state:
    st.session_state["job_description"] = None  # Set default to None
if "responses" not in st.session_state:
    st.session_state["responses"] = {}

# Show Job Description Upload Section only if no job description is stored
if not st.session_state["job_description"]:
    st.markdown("## 📄 Upload Job Description")

    uploaded_file = st.file_uploader("Upload a job description document (PDF or DOCX)", type=["pdf", "docx"])
    text_input = st.text_area("Or enter job description text manually")

    # Create three columns and place the button in the center column
    col1, col2, col3, col4 = st.columns([1, 2, 2, 2])  # Adjust the ratio to center properly
    with col3:
        if st.button("Upload"):
            API_URL = f"{FASTAPI_URL}/extract-text/"
            if uploaded_file and text_input:
                st.error("❌ Provide either a file OR text, not both.")
            elif uploaded_file:
                files = {"file": (uploaded_file.name, uploaded_file, uploaded_file.getvalue())}
                response = requests.post(API_URL, files=files)
            elif text_input:
                data = {"text": text_input}
                response = requests.post(API_URL, data=data)
            else:
                st.error("❌ No file or text provided.")
                response = None

            if response and response.status_code == 200:
                try:
                    response_json = response.json() if response.headers.get("Content-Type") == "application/json" else {"extracted_text": response.text}
                    extracted_text = response_json if isinstance(response_json, str) else response_json.get("extracted_text", "No text extracted.")
                except ValueError:
                    extracted_text = "Invalid response from server."

                st.session_state["job_description"] = extracted_text  # Store job description in session state
                st.success("✅ Job description uploaded successfully!")
                st.rerun()  # Rerun to hide the upload section

# Only show persona selection if job description is available
if st.session_state["job_description"]:
    st.markdown("## 🎭 Select Interview Persona")
    st.text_area("Job Description:", st.session_state["job_description"], height=150, disabled=True)

    # Get available personas excluding already selected ones
    all_personas = ["HR", "Recruiter", "Hiring Manager", "Technical Interviewer"]
    available_personas = [p for p in all_personas if p not in st.session_state["selected_personas"]]

    # Persona selection dropdown
    persona = st.selectbox("Choose the interviewer persona:", ["Select Option"] + available_personas)

    if persona != "Select Option":
        st.session_state["persona"] = persona
        
        # Show the Generate Questions button **only when a persona is selected**
        if st.button("🛠 Generate Questions", use_container_width=True):
            api_url = f"{FASTAPI_URL}/generate-questions/"
            payload = {
                "email": st.session_state["user_email"],
                "job_description": st.session_state["job_description"],
                "persona": st.session_state["persona"]
            }

            with st.spinner("Generating interview questions... ⏳"):
                response = requests.post(api_url, json=payload)

            if response.status_code == 200:
                result = response.json()
                st.session_state["questions"] = result.get("questions", [])
                st.session_state["suggested_answers"] = result.get("suggested_answers", [])
                st.session_state["selected_personas"].add(st.session_state["persona"])  # Mark persona as used
                st.success("✅ Questions generated successfully!")
                st.rerun()
            else:
                st.error("❌ Failed to generate questions. Please try again.")

# Display Generated Questions **outside of buttons**
if "questions" in st.session_state and st.session_state["questions"]:
    st.markdown(f"## {st.session_state["persona"]}")
    st.markdown("### 🎤 Generated Interview Questions")

    answers_to_save = []  # Collect all answers in a list before making an API call

    for i, question in enumerate(st.session_state["questions"]):
        st.markdown(f"**Q{i+1}:** {question}")
        user_input = st.text_area("Your Answer:", value=st.session_state["responses"].get(question, ""), key=f"answer_{i}")
        st.session_state["responses"][question] = user_input

        answers_to_save.append(user_input)

    # Save Responses on "Next" Button Click
    st.markdown("---")
    if st.button("➡ Next", use_container_width=True):
        save_url = f"{FASTAPI_URL}/save-response/"
        payload = {
            "email": st.session_state["user_email"],
            "persona": st.session_state["persona"],
            "answers": answers_to_save  
        }
        requests.post(save_url, json=payload)

        del st.session_state["persona"]
        del st.session_state["questions"]
        del st.session_state["responses"]

        if len(st.session_state["selected_personas"]) == 4:
            st.success("🎉 Your interview is successfully completed! ✅")
        else:
            st.rerun()

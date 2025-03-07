import streamlit as st
import requests
import os
from io import BytesIO
from reportlab.lib.pagesizes import letter
from reportlab.lib.utils import simpleSplit
from reportlab.pdfgen import canvas

# Fetch API URL from environment variable
FASTAPI_URL = os.getenv("BACKEND_API_URL", "http://localhost:8000")

# Page Configuration
st.set_page_config(page_title="Results - AI Powered Interview", page_icon="📊", layout="wide")

# Add Logo & Page Title
st.markdown("<h1 style='text-align: center;'>📊 Candidate Assessment Results</h1>", unsafe_allow_html=True)
st.markdown("---")

# Admin enters candidate's email
user_email = st.text_input("🔍 Enter Candidate's Email to View Results:")

if user_email:
    # Fetch results from backend
    api_url = f"{FASTAPI_URL}/get-results/{user_email}"
    response = requests.get(api_url)

    if response.status_code == 200:
        results = response.json()
        st.session_state["assessment_results"] = results
    else:
        st.session_state["assessment_results"] = None

    results = st.session_state["assessment_results"]

    if not results:
        st.warning("⚠ No assessment results found for this email.")
    else:
        st.success("✅ Results retrieved successfully!")

        # ✅ Handle results as a list or dict
        if isinstance(results, list) and results:
            candidate_name = results[0].get("name", "N/A")  
            assessments = results
        elif isinstance(results, dict):
            candidate_name = results.get("name", "N/A")
            assessments = results.get("assessment_results", [])
        else:
            candidate_name = "N/A"
            assessments = []

        # Display Candidate Information
        st.markdown(f"### 👤 Candidate: **{candidate_name}**")
        st.markdown("---")

        # Function to generate PDF
        def generate_pdf(candidate_name, assessments, user_email):
            buffer = BytesIO()
            pdf = canvas.Canvas(buffer, pagesize=letter)
            width, height = letter

            # Margins
            left_margin = 50
            right_margin = 50
            top_margin = 150  # Space for persona title and candidate details
            bottom_margin = 150  # Ensures no text is too close to the bottom
            max_width = width - left_margin - right_margin
            line_spacing = 20

            def wrap_text(text, max_width):
                """Wrap text so it fits within the page width."""
                return simpleSplit(text, "Helvetica", 10, max_width-10)

            def add_persona_header(persona_name):
                """Add candidate name, email, and persona title at the start of each persona."""
                pdf.setFont("Helvetica-Bold", 12)
                pdf.drawString(left_margin, height - 50, f"Candidate Name: {candidate_name}")
                pdf.drawString(left_margin, height - 70, f"Email: {user_email}")
                pdf.setFont("Helvetica-Bold", 14)
                pdf.drawString(left_margin + 150, height - 100, f"🎭 {persona_name} Assessment Report")
                pdf.line(left_margin, height - 110, width - right_margin, height - 110)  # Separator line

            first_persona = True  # Track if it's the first persona (to control page breaks)

            for assessment in assessments:
                if not first_persona:
                    pdf.showPage()  # Start a new page only when switching personas
                first_persona = False  # After first persona, we always start a new page

                persona = assessment.get("persona", "Unknown Persona")
                add_persona_header(persona)

                questions = assessment.get("questions", [])  
                responses = assessment.get("responses", ["No response provided"])
                suggested_answers = assessment.get("suggested_answers", ["No suggested answer available"])

                max_length = max(len(questions), len(responses), len(suggested_answers))
                questions += ["Question not available"] * (max_length - len(questions))
                responses += ["No response provided"] * (max_length - len(responses))
                suggested_answers += ["No suggested answer available"] * (max_length - len(suggested_answers))

                y_position = height - top_margin

                for i, (question, response, suggested_answer) in enumerate(zip(questions, responses, suggested_answers)):
                    # Wrap the question to fit within page margins
                    wrapped_question = wrap_text(f"Q{i+1}: {question}", max_width-100)
                    question_height = len(wrapped_question) * line_spacing
                    
                    # Check if question fits, else start a new page
                    if y_position - question_height < bottom_margin:
                        pdf.showPage()
                        add_persona_header(persona)  # Only add persona title at new page start
                        y_position = height - top_margin

                    # Print Question
                    pdf.setFont("Helvetica-Bold", 12)
                    for line in wrapped_question:
                        pdf.drawString(left_margin, y_position, line)
                        y_position -= line_spacing

                    # Candidate's Answer
                    pdf.setFont("Helvetica-Bold", 10)
                    pdf.drawString(left_margin, y_position, "📝 Candidate's Answer:")
                    y_position -= line_spacing
                    pdf.setFont("Helvetica", 10)
                    wrapped_response = wrap_text(response, max_width)
                    for line in wrapped_response:
                        pdf.drawString(left_margin + 20, y_position, line)
                        y_position -= line_spacing

                    # Suggested Answer
                    pdf.setFont("Helvetica-Bold", 10)
                    pdf.drawString(left_margin, y_position, "💡 Suggested Answer:")
                    y_position -= line_spacing
                    pdf.setFont("Helvetica", 10)
                    wrapped_suggested = wrap_text(suggested_answer, max_width)
                    for line in wrapped_suggested:
                        pdf.drawString(left_margin + 20, y_position, line)
                        y_position -= line_spacing

                    y_position -= 20  # Extra spacing between questions

            pdf.save()
            buffer.seek(0)
            return buffer



        # Generate PDF and provide download button
        pdf_buffer = generate_pdf(candidate_name, assessments, user_email)
        st.download_button(
            label="📥 Download Report as PDF",
            data=pdf_buffer,
            file_name=f"{candidate_name}_assessment_report.pdf",
            mime="application/pdf"
        )

        # Display each persona separately
        for assessment in assessments:
            persona = assessment.get("persona", "Unknown Persona")
            questions = assessment.get("questions", [])  
            responses = assessment.get("responses", ["No response provided"])
            suggested_answers = assessment.get("suggested_answers", ["No suggested answer available"])

            max_length = max(len(questions), len(responses), len(suggested_answers))
            questions += ["Question not available"] * (max_length - len(questions))
            responses += ["No response provided"] * (max_length - len(responses))
            suggested_answers += ["No suggested answer available"] * (max_length - len(suggested_answers))

            st.markdown(f"<h2 style='color:#1f77b4;'>🎭 {persona}</h2>", unsafe_allow_html=True)

            for i, (question, response, suggested_answer) in enumerate(zip(questions, responses, suggested_answers)):
                with st.expander(f"**Q{i+1}:** {question}", expanded=False):
                    st.markdown(f"📝 **Candidate's Answer:**\n{response}")
                    st.markdown(f"💡 **Suggested Answer:**\n{suggested_answer}")

            st.markdown("---")  # Separator for each persona

    col1, col2, col3, col4 = st.columns([1,2,2,2])
    with col3:
        # Button to get AI-based similarity score
        if st.button("🤖 Get AI-Based Similarity Score"):
            compare_api_url = f"{FASTAPI_URL}/compare-answers-ai/{user_email}"
            compare_response = requests.get(compare_api_url)

            if compare_response.status_code == 200:
                scores = compare_response.json()
                st.write("### 🔹 AI-Recommended Percentage per Persona")
                for persona, score in scores.items():
                    st.write(f"**🎭 {persona}: {score}% match")
            else:
                st.error("❌ Error calculating similarity score.")
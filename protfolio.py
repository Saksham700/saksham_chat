import streamlit as st
import google.generativeai as genai
from PIL import Image
import io
import base64
import requests
from datetime import datetime
import json

# Configure the page
st.set_page_config(
    page_title="Saksham's AI Assistant",
    page_icon="🤖",
    layout="wide"
)

# Configure Gemini API
GOOGLE_API_KEY = "AIzaSyB46mW-7p4MIrKSe-oudQLpjxWli6XjVpE"
genai.configure(api_key=GOOGLE_API_KEY)

# Your professional information
PERSONAL_INFO = {
    "name": "Saksham Raj",
    "email": "sakshamraj0170@gmail.com",
    "phone": "7004028809",
    "linkedin": "https://www.linkedin.com/in/saksham-raj-07863b203/",
    "github": "https://github.com/Saksham700/",
    "portfolio": "https://protfolio-saksham.streamlit.app/",
    "resume": "https://drive.google.com/file/d/1t-PnuV0ivjh4_1Cu2Fi-BQPi8ZsIpwSI/view"
}

# Professional context (you can expand this based on your actual experience)
PROFESSIONAL_CONTEXT = """
You are Saksham Raj, a professional with the following details:

Contact Information:
- Email: sakshamraj0170@gmail.com
- Phone: 7004028809
- LinkedIn: https://www.linkedin.com/in/saksham-raj-07863b203/
- GitHub: https://github.com/Saksham700/
- Portfolio: https://protfolio-saksham.streamlit.app/

Professional Background:
- Experienced in software development and data science
- Skilled in Python, machine learning, and web development
- Active on GitHub with various projects
- Has a professional portfolio showcasing work
- Available for collaborations and professional opportunities

Key Skills:
- Python Programming
- Machine Learning & AI
- Web Development (Streamlit, Flask)
- Data Analysis
- Software Engineering
- Project Management

You should respond as Saksham when drafting emails, messages, or answering questions about your professional background.
Always maintain a professional but friendly tone in communications.
"""

def initialize_session_state():
    if 'messages' not in st.session_state:
        st.session_state.messages = []
    if 'model' not in st.session_state:
        st.session_state.model = genai.GenerativeModel('gemini-2.0-flash-001')
    if 'vision_model' not in st.session_state:
        st.session_state.vision_model = genai.GenerativeModel('gemini-2.0-flash-001')

def get_ai_response(prompt, context=""):
    try:
        full_prompt = f"{PROFESSIONAL_CONTEXT}\n\n{context}\n\nUser Request: {prompt}"
        response = st.session_state.model.generate_content(full_prompt)
        return response.text
    except Exception as e:
        return f"Error generating response: {str(e)}"

def analyze_image_and_generate_content(image, prompt, content_type):
    try:
        context = f"""
        {PROFESSIONAL_CONTEXT}
        
        The user has uploaded an image (likely a job description, announcement, or professional content) 
        and wants you to generate a {content_type} based on it.
        
        Instructions:
        - Analyze the image content carefully
        - Generate a professional {content_type} from Saksham's perspective
        - Include relevant skills and experience from the professional context
        - Maintain appropriate tone for the content type
        """
        
        full_prompt = f"{context}\n\nSpecific request: {prompt}"
        response = st.session_state.vision_model.generate_content([full_prompt, image])
        return response.text
    except Exception as e:
        return f"Error analyzing image: {str(e)}"

def create_email_template(subject, recipient, purpose):
    prompt = f"""
    Generate a professional email with the following details:
    - Subject: {subject}
    - Recipient: {recipient}
    - Purpose: {purpose}
    
    Include appropriate greeting, body, and closing.
    Make it professional but personable.
    Include relevant contact information in signature.
    """
    return get_ai_response(prompt)

def create_linkedin_message(context, purpose):
    prompt = f"""
    Generate a LinkedIn message for the following context:
    - Context: {context}
    - Purpose: {purpose}
    
    Keep it concise, professional, and engaging.
    Make it suitable for LinkedIn networking.
    """
    return get_ai_response(prompt)

def create_referral_request(company, position, referrer_name=""):
    prompt = f"""
    Generate a referral request message for:
    - Company: {company}
    - Position: {position}
    - Referrer: {referrer_name if referrer_name else "a connection"}
    
    Make it polite, professional, and highlight relevant qualifications.
    Include a brief mention of why you're interested in the role.
    """
    return get_ai_response(prompt)

def main():
    initialize_session_state()
    
    st.title("🤖 Saksham's Personal AI Assistant")
    st.markdown("*Your AI-powered communication helper for emails, messages, and professional content*")
    
    # Sidebar for quick actions
    st.sidebar.title("Quick Actions")
    st.sidebar.markdown("### 📧 Email Templates")
    st.sidebar.markdown("### 💼 LinkedIn Messages")
    st.sidebar.markdown("### 🤝 Referral Requests")
    st.sidebar.markdown("### 📱 General Messages")
    st.sidebar.markdown("### 🖼️ Image Analysis")
    
    # Main interface
    tab1, tab2, tab3, tab4, tab5 = st.tabs(["💬 Chat", "📧 Email Draft", "💼 LinkedIn", "🤝 Referrals", "🖼️ Image Analysis"])
    
    with tab1:
        st.header("General Chat Assistant")
        st.markdown("Ask me anything about yourself, your projects, or get help with general communication!")
        
        # Chat interface
        for message in st.session_state.messages:
            with st.chat_message(message["role"]):
                st.markdown(message["content"])
        
        if prompt := st.chat_input("Ask me anything about yourself or request help with communication..."):
            st.session_state.messages.append({"role": "user", "content": prompt})
            with st.chat_message("user"):
                st.markdown(prompt)
            
            with st.chat_message("assistant"):
                response = get_ai_response(prompt)
                st.markdown(response)
                st.session_state.messages.append({"role": "assistant", "content": response})
    
    with tab2:
        st.header("📧 Email Draft Generator")
        
        col1, col2 = st.columns(2)
        
        with col1:
            email_type = st.selectbox(
                "Email Type",
                ["Job Application", "Follow-up", "Networking", "Project Proposal", "Thank You", "Custom"]
            )
            
            recipient = st.text_input("Recipient Name/Company")
            subject = st.text_input("Email Subject")
            
        with col2:
            purpose = st.text_area("Email Purpose/Context", height=100)
            additional_notes = st.text_area("Additional Notes/Requirements", height=100)
        
        if st.button("Generate Email", type="primary"):
            if recipient and subject and purpose:
                context = f"Email Type: {email_type}\nAdditional Notes: {additional_notes}"
                email_content = create_email_template(subject, recipient, f"{purpose}\n{context}")
                
                st.subheader("Generated Email:")
                st.text_area("Email Content", email_content, height=300)
                
                # Copy button simulation
                st.code(email_content, language="text")
            else:
                st.error("Please fill in all required fields!")
    
    with tab3:
        st.header("💼 LinkedIn Message Generator")
        
        message_type = st.selectbox(
            "Message Type",
            ["Connection Request", "Follow-up", "Networking", "Job Inquiry", "Collaboration", "Thank You"]
        )
        
        col1, col2 = st.columns(2)
        
        with col1:
            recipient_info = st.text_input("Recipient Name/Title")
            company_info = st.text_input("Company (if applicable)")
        
        with col2:
            message_context = st.text_area("Context/Background", height=100)
            specific_ask = st.text_area("Specific Request/Goal", height=100)
        
        if st.button("Generate LinkedIn Message", type="primary"):
            if recipient_info and message_context:
                full_context = f"""
                Message Type: {message_type}
                Recipient: {recipient_info}
                Company: {company_info}
                Context: {message_context}
                Specific Ask: {specific_ask}
                """
                linkedin_message = create_linkedin_message(full_context, specific_ask)
                
                st.subheader("Generated LinkedIn Message:")
                st.text_area("Message Content", linkedin_message, height=200)
                st.code(linkedin_message, language="text")
            else:
                st.error("Please provide recipient info and context!")
    
    with tab4:
        st.header("🤝 Referral Request Generator")
        
        col1, col2 = st.columns(2)
        
        with col1:
            company_name = st.text_input("Company Name")
            position_title = st.text_input("Position Title")
        
        with col2:
            referrer_name = st.text_input("Referrer Name (optional)")
            relationship = st.text_input("Relationship to Referrer")
        
        additional_context = st.text_area("Additional Context (why this role, etc.)")
        
        if st.button("Generate Referral Request", type="primary"):
            if company_name and position_title:
                referral_message = create_referral_request(company_name, position_title, referrer_name)
                
                st.subheader("Generated Referral Request:")
                st.text_area("Referral Message", referral_message, height=250)
                st.code(referral_message, language="text")
            else:
                st.error("Please provide company and position information!")
    
    with tab5:
        st.header("🖼️ Image Analysis & Content Generation")
        st.markdown("Upload an image (job description, announcement, etc.) and get tailored content!")
        
        uploaded_file = st.file_uploader("Choose an image...", type=['png', 'jpg', 'jpeg'])
        
        if uploaded_file is not None:
            image = Image.open(uploaded_file)
            st.image(image, caption='Uploaded Image', use_column_width=True)
            
            content_type = st.selectbox(
                "What would you like me to generate?",
                ["Email", "LinkedIn Message", "Cover Letter", "Application Message", "Follow-up Email"]
            )
            
            additional_instructions = st.text_area("Additional Instructions/Context")
            
            if st.button("Analyze Image & Generate Content", type="primary"):
                with st.spinner("Analyzing image and generating content..."):
                    prompt = f"Generate a {content_type} based on this image. {additional_instructions}"
                    result = analyze_image_and_generate_content(image, prompt, content_type)
                    
                    st.subheader(f"Generated {content_type}:")
                    st.text_area("Generated Content", result, height=300)
                    st.code(result, language="text")
    
    # Footer with contact info
    st.markdown("---")
    st.markdown("### 📞 Contact Information")
    col1, col2, col3, col4 = st.columns(4)
    with col1:
        st.markdown(f"**Email:** {PERSONAL_INFO['email']}")
    with col2:
        st.markdown(f"**Phone:** {PERSONAL_INFO['phone']}")
    with col3:
        st.markdown(f"**[LinkedIn]({PERSONAL_INFO['linkedin']})**")
    with col4:
        st.markdown(f"**[Portfolio]({PERSONAL_INFO['portfolio']})**")

if __name__ == "__main__":
    main()

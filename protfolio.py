import streamlit as st
import google.generativeai as genai
from PIL import Image
import io

# Configure Streamlit
st.set_page_config(page_title="Personal Assistant", layout="wide")

# Your Personal Data
PERSONAL_DATA = {
    "name": "Saksham Raj",
    "email": "sakshamraj0170@gmail.com", 
    "phone": "7004028809",
    "linkedin": "https://www.linkedin.com/in/saksham-raj-07863b203/",
    "github": "https://github.com/Saksham700/",
    
    "bio": """Machine Learning Engineer and Data Scientist with expertise in predictive analytics, 
    healthcare technology, and agriculture solutions. Experienced in building end-to-end ML pipelines 
    and deploying AI solutions for real-world problems.""",
    
    "projects": {
        "GrowGuide": {
            "description": "AI-powered crop and fertilizer prediction system using ML algorithms to suggest optimal crops and predict yields for farmers",
            "tech": "Python, Scikit-learn, Pandas, NumPy, Jupyter",
            "impact": "Helps farmers make data-driven decisions for better crop yields",
            "domain": "Agriculture Technology"
        },
        "Data Scientist Salary Prediction": {
            "description": "ML model predicting data scientist salaries based on location, education, experience, company size, and industry factors",
            "tech": "Python, Machine Learning, Feature Engineering, Regression Models",
            "impact": "Provides salary insights for career planning in data science",
            "domain": "HR Analytics"
        },
        "Kidney Stone Prediction": {
            "description": "Healthcare ML system predicting kidney stone presence using clinical parameters and patient data",
            "tech": "Python, Classification Algorithms, Medical Data Analysis",
            "impact": "Early detection system for kidney stone diagnosis",
            "domain": "Healthcare Technology"
        },
        "Airlines Delay Prediction": {
            "description": "Predictive analytics system for flight delays using historical aviation data and weather patterns",
            "tech": "Python, Time Series Analysis, Feature Engineering",
            "impact": "Helps airlines and passengers plan better travel schedules",
            "domain": "Transportation Analytics"
        }
    },
    
    "skills": {
        "Programming": ["Python", "C++", "HTML"],
        "ML/AI": ["Machine Learning", "Deep Learning", "Predictive Analytics", "Feature Engineering"],
        "Data Science": ["Data Analysis", "Statistical Modeling", "Data Visualization"],
        "Tools": ["Jupyter Notebook", "Pandas", "NumPy", "Scikit-learn"],
        "Domains": ["Healthcare Tech", "Agriculture Tech", "HR Analytics", "Transportation Analytics"]
    },
    
    "achievements": [
        "Developed 4+ end-to-end ML projects with real-world applications",
        "Expertise in healthcare and agriculture AI solutions",
        "Strong background in predictive analytics and data modeling",
        "Open source contributor with projects on GitHub"
    ]
}

# Context Builder
def build_context():
    context = f"""
You are an AI assistant for {PERSONAL_DATA['name']}, helping him generate professional emails, messages, and responses.

PERSONAL PROFILE:
Name: {PERSONAL_DATA['name']}
Email: {PERSONAL_DATA['email']}
Phone: {PERSONAL_DATA['phone']}
LinkedIn: {PERSONAL_DATA['linkedin']}
GitHub: {PERSONAL_DATA['github']}

BIO: {PERSONAL_DATA['bio']}

KEY PROJECTS:
"""
    
    for project_name, details in PERSONAL_DATA['projects'].items():
        context += f"""
• {project_name}: {details['description']}
  Technologies: {details['tech']}
  Impact: {details['impact']}
  Domain: {details['domain']}
"""
    
    context += f"""
TECHNICAL SKILLS:
• Programming: {', '.join(PERSONAL_DATA['skills']['Programming'])}
• ML/AI: {', '.join(PERSONAL_DATA['skills']['ML/AI'])}
• Data Science: {', '.join(PERSONAL_DATA['skills']['Data Science'])}
• Tools: {', '.join(PERSONAL_DATA['skills']['Tools'])}
• Domain Expertise: {', '.join(PERSONAL_DATA['skills']['Domains'])}

KEY ACHIEVEMENTS:
"""
    for achievement in PERSONAL_DATA['achievements']:
        context += f"• {achievement}\n"
    
    return context

# Initialize Gemini
@st.cache_resource
def init_gemini():
    genai.configure(api_key="AIzaSyB46mW-7p4MIrKSe-oudQLpjxWli6XjVpE")
    return genai.GenerativeModel('gemini-pro'), genai.GenerativeModel('gemini-pro-vision')

def generate_content(model, prompt, context):
    try:
        full_prompt = f"{context}\n\n{prompt}"
        response = model.generate_content(full_prompt)
        return response.text
    except Exception as e:
        return f"Error: {str(e)}"

# UI
st.title("Personal AI Assistant")

model, vision_model = init_gemini()
context = build_context()

# Main Functions
col1, col2 = st.columns([1, 1])

with col1:
    st.subheader("📧 Email Generator")
    
    email_type = st.selectbox("Type", ["Job Application", "Referral Request", "LinkedIn Outreach", "Follow-up", "Custom"])
    company = st.text_input("Company/Person")
    role = st.text_input("Role/Position")
    details = st.text_area("Specific Details/Context", height=100)
    
    if st.button("Generate Email"):
        if details:
            prompt = f"""
Generate a professional {email_type.lower()} email for {PERSONAL_DATA['name']}.

Target: {company if company else 'Company'}
Role: {role if role else 'Position'}
Context: {details}

Requirements:
1. Professional but personable tone
2. Highlight most relevant projects and skills for this context
3. Include specific technical details and achievements
4. Clear call to action
5. Proper email format with subject line
6. Keep it concise but comprehensive
            """
            
            result = generate_content(model, prompt, context)
            st.text_area("Generated Email:", value=result, height=400)

with col2:
    st.subheader("💬 Message Generator")
    
    message_type = st.selectbox("Type", ["LinkedIn Message", "WhatsApp/Text", "Slack/Teams", "Twitter DM"])
    purpose = st.text_input("Purpose")
    recipient = st.text_input("Recipient")
    msg_context = st.text_area("Context", height=100)
    
    if st.button("Generate Message"):
        if msg_context:
            prompt = f"""
Generate a {message_type.lower()} for {PERSONAL_DATA['name']}.

To: {recipient if recipient else 'Recipient'}
Purpose: {purpose if purpose else 'General outreach'}
Context: {msg_context}

Requirements:
1. Platform-appropriate length and tone
2. Relevant skills/projects mention
3. Clear purpose
4. Professional yet friendly
5. Call to action if needed
            """
            
            result = generate_content(model, prompt, context)
            st.text_area("Generated Message:", value=result, height=300)

# Job Description Processor
st.subheader("📄 Job Description Processor")
job_desc = st.text_area("Paste Job Description", height=150)

col3, col4, col5 = st.columns(3)

with col3:
    if st.button("Generate Cover Letter"):
        if job_desc:
            prompt = f"""
Analyze this job description and create a tailored cover letter for {PERSONAL_DATA['name']}:

{job_desc}

Requirements:
1. Match specific requirements with Saksham's projects and skills
2. Highlight most relevant experience
3. Show clear value proposition
4. Professional format
5. Quantify achievements where possible
            """
            result = generate_content(model, prompt, context)
            st.text_area("Cover Letter:", value=result, height=400)

with col4:
    if st.button("Create Application Email"):
        if job_desc:
            prompt = f"""
Create a job application email for this position for {PERSONAL_DATA['name']}:

{job_desc}

Include:
1. Subject line
2. Relevant project highlights
3. Technical skills alignment
4. Professional closing
5. Resume attachment mention
            """
            result = generate_content(model, prompt, context)
            st.text_area("Application Email:", value=result, height=400)

with col5:
    if st.button("Skills Match Analysis"):
        if job_desc:
            prompt = f"""
Analyze this job description against {PERSONAL_DATA['name']}'s profile:

{job_desc}

Provide:
1. Matching skills and projects
2. Missing skills/requirements
3. How to position existing experience
4. Key points to emphasize
5. Suggested learning areas
            """
            result = generate_content(model, prompt, context)
            st.text_area("Analysis:", value=result, height=400)

# Image Processor
st.subheader("🖼️ Image Processor")
uploaded_file = st.file_uploader("Upload Job Posting/Document Image", type=['png', 'jpg', 'jpeg'])

if uploaded_file:
    image = Image.open(uploaded_file)
    st.image(image, width=300)
    
    process_type = st.selectbox("Generate", ["Email Application", "LinkedIn Message", "Analysis"])
    
    if st.button("Process Image"):
        prompt = f"""
Analyze this image (likely a job posting or professional document) for {PERSONAL_DATA['name']}.

Generate a {process_type.lower()} that:
1. Addresses specific requirements shown in image
2. Highlights relevant projects and skills
3. Uses appropriate tone and format
4. Shows clear alignment with the opportunity
        """
        
        try:
            result = vision_model.generate_content([prompt + "\n\nPersonal Context:\n" + context, image])
            st.text_area(f"Generated {process_type}:", value=result.text, height=400)
        except Exception as e:
            st.error(f"Error processing image: {str(e)}")

# Quick Q&A
st.subheader("❓ Quick Q&A")
question = st.text_input("Ask anything about your background, projects, or get professional advice")

if st.button("Get Answer"):
    if question:
        prompt = f"""
Answer this question about {PERSONAL_DATA['name']} professionally and accurately:

{question}

Provide specific details about projects, skills, and experience where relevant.
        """
        result = generate_content(model, prompt, context)
        st.text_area("Answer:", value=result, height=200)
import streamlit as st
import os
import re
import json
import pandas as pd
import PyPDF2
import google.generativeai as genai
from groq import Groq
from dotenv import load_dotenv
from fpdf import FPDF
from PIL import Image
import warnings
from streamlit.errors import StreamlitSecretNotFoundError
from pathlib import Path

# --- 1. CONFIGURATION & SETUP ---
# Suppress deprecation warnings
warnings.filterwarnings("ignore")

st.set_page_config(
    page_title="AI Career Assistant",
    page_icon="🚀",
    layout="wide",
    initial_sidebar_state="expanded"
)

# --- ROBUST ENV LOADING ---
# Explicitly find the .env file relative to this script
# This fixes issues where 'streamlit run' is executed from a different directory
env_path = Path(__file__).parent / ".env"
if env_path.exists():
    load_dotenv(dotenv_path=env_path)
else:
    # Fallback to standard load if path logic fails
    load_dotenv()

def get_api_key(key_name):
    """
    Robust helper to get API keys.
    It first checks local .env (os.getenv).
    If not found, it tries Streamlit Secrets (for Cloud).
    Catches StreamlitSecretNotFoundError to prevent local crashes.
    """
    # 1. Try Local Environment (.env)
    key = os.getenv(key_name)
    if key and key.strip(): # Ensure key is not empty string
        return key

    # 2. Try Streamlit Secrets (Cloud)
    try:
        # Accessing st.secrets triggers a file check
        if key_name in st.secrets:
            return st.secrets[key_name]
    except (StreamlitSecretNotFoundError, FileNotFoundError):
        return None
    except Exception:
        return None
        
    return None

GOOGLE_API_KEY = get_api_key("GOOGLE_API_KEY")
GROQ_API_KEY = get_api_key("GROQ_API_KEY")

# API Validation & UI Fallback
if not GOOGLE_API_KEY:
    with st.sidebar:
        st.header("🔐 API Configuration")
        st.warning("⚠️ Google API Key not found in .env")
        GOOGLE_API_KEY = st.text_input("Enter Google API Key manually", type="password", help="Get your key from aistudio.google.com")

if not GOOGLE_API_KEY:
    st.error("🚨 GOOGLE_API_KEY is required to run this app! Please set it in your .env file, Streamlit Secrets, or enter it in the sidebar.")
    st.stop()

# Configure Clients
try:
    genai.configure(api_key=GOOGLE_API_KEY)
except Exception as e:
    st.error(f"Error configuring Google API: {e}")

groq_client = None
if GROQ_API_KEY:
    try:
        groq_client = Groq(api_key=GROQ_API_KEY)
    except Exception as e:
        st.warning(f"Groq API Key found but client failed to initialize: {e}")

# --- 2. DEFAULT COURSE DATABASE ---
DEFAULT_COURSES = [
    {"Skill": "Data preprocessing", "Course Name": "Data Science Foundations", "URL": "https://skillsbuild.org/data-science", "Platform": "IBM SkillsBuild"},
    {"Skill": "Data pipelines", "Course Name": "ETL and Data Pipelines with Shell Airflow and Kafka", "URL": "https://www.coursera.org/learn/etl-and-data-pipelines-shell-airflow-kafka", "Platform": "Coursera"},
    {"Skill": "Insights", "Course Name": "Data Visualization with Python", "URL": "https://www.coursera.org/learn/python-for-data-visualization", "Platform": "Coursera"},
    {"Skill": "Machine Learning", "Course Name": "Machine Learning with Python", "URL": "https://www.coursera.org/learn/machine-learning-with-python", "Platform": "Coursera"},
    {"Skill": "Cloud", "Course Name": "Introduction to Cloud Computing", "URL": "https://www.coursera.org/learn/introduction-to-cloud", "Platform": "Coursera"},
    {"Skill": "Python", "Course Name": "Python for Everybody", "URL": "https://www.coursera.org/specializations/python", "Platform": "Coursera"},
    {"Skill": "SQL", "Course Name": "SQL for Data Science", "URL": "https://www.coursera.org/learn/sql-for-data-science", "Platform": "Coursera"},
    {"Skill": "Generative AI", "Course Name": "Introduction to Generative AI", "URL": "https://www.cloudskillsboost.google/course_templates/536", "Platform": "Google Cloud"},
    {"Skill": "AWS", "Course Name": "AWS Fundamentals", "URL": "https://www.coursera.org/specializations/aws-fundamentals", "Platform": "Coursera"},
    {"Skill": "Azure", "Course Name": "Microsoft Azure Fundamentals AZ-900", "URL": "https://learn.microsoft.com/en-us/credentials/certifications/azure-fundamentals/", "Platform": "Microsoft"},
    {"Skill": "Docker", "Course Name": "Docker for Developers", "URL": "https://www.udemy.com/topic/docker/", "Platform": "Udemy"},
    {"Skill": "Kubernetes", "Course Name": "Architecting with Google Kubernetes Engine", "URL": "https://www.coursera.org/specializations/architecting-with-google-kubernetes-engine", "Platform": "Google Cloud"},
    {"Skill": "HTML", "Course Name": "Introduction to HTML5", "URL": "https://www.coursera.org/learn/html", "Platform": "Coursera"},
    {"Skill": "CSS", "Course Name": "CSS3", "URL": "https://www.coursera.org/learn/intro-css", "Platform": "Coursera"},
    {"Skill": "JavaScript", "Course Name": "JavaScript Algorithms and Data Structures", "URL": "https://www.freecodecamp.org/learn/javascript-algorithms-and-data-structures/", "Platform": "freeCodeCamp"},
    {"Skill": "React", "Course Name": "Meta Front-End Developer Professional Certificate", "URL": "https://www.coursera.org/professional-certificates/meta-front-end-developer", "Platform": "Coursera"},
    {"Skill": "Node.js", "Course Name": "Developing Cloud Applications with Node.js and React", "URL": "https://www.coursera.org/learn/cloud-applications-nodejs-react", "Platform": "Coursera"},
    {"Skill": "Communication", "Course Name": "Effective Communication: Writing, Design, and Presentation", "URL": "https://www.coursera.org/specializations/effective-communication", "Platform": "Coursera"},
    {"Skill": "Leadership", "Course Name": "Strategic Leadership and Management", "URL": "https://www.coursera.org/specializations/strategic-leadership", "Platform": "Coursera"},
    {"Skill": "Project Management", "Course Name": "Google Project Management Professional Certificate", "URL": "https://www.coursera.org/professional-certificates/google-project-management", "Platform": "Coursera"},
    {"Skill": "Cybersecurity", "Course Name": "Google Cybersecurity Professional Certificate", "URL": "https://www.coursera.org/professional-certificates/google-cybersecurity", "Platform": "Coursera"}
]

# --- 3. CUSTOM UI STYLING (BLACK THEME) ---
def apply_custom_css():
    st.markdown("""
    <style>
        @import url('https://fonts.googleapis.com/css2?family=Poppins:wght@300;400;600&display=swap');
        
        /* Global Font & Text Color */
        html, body, [class*="css"]  {
            font-family: 'Poppins', sans-serif;
            color: #e0e0e0 !important;
            background-color: #0e1117; 
        }
        
        /* Main Background */
        .stApp {
            background-color: #0e1117;
        }
        
        /* Sidebar Styling */
        section[data-testid="stSidebar"] {
            background-color: #161b22;
            border-right: 1px solid #30363d;
        }
        
        /* Text Color Fixes */
        .stMarkdown, .stText, p, li, label, .stCaption, h1, h2, h3, h4, h5, h6 {
            color: #e0e0e0 !important;
        }
        
        /* Custom Button Style (Dark/Blue Gradient) */
        .stButton>button {
            background: linear-gradient(90deg, #238636 0%, #1a7f37 100%);
            color: white;
            border: 1px solid rgba(240, 246, 252, 0.1);
            padding: 10px 24px;
            border-radius: 8px;
            font-weight: 600;
            transition: all 0.2s ease;
            box-shadow: 0 2px 5px rgba(0,0,0,0.5);
            width: 100%;
        }
        .stButton>button:hover {
            background: linear-gradient(90deg, #2ea043 0%, #238636 100%);
            transform: translateY(-1px);
            box-shadow: 0 4px 12px rgba(0,0,0,0.8);
            color: #ffffff;
            border-color: #8b949e;
        }
        
        /* Input Fields */
        .stTextInput>div>div>input, .stTextArea>div>div>textarea {
            border-radius: 6px;
            border: 1px solid #30363d;
            padding: 10px;
            background-color: #0d1117;
            color: #e0e0e0 !important; 
        }
        .stTextInput>div>div>input:focus, .stTextArea>div>div>textarea:focus {
            border-color: #58a6ff;
            box-shadow: 0 0 0 2px rgba(88, 166, 255, 0.3);
        }
        
        /* Headers */
        h1, h2, h3 { font-weight: 600; }
        
        /* Containers */
        [data-testid="stVerticalBlockBorderWrapper"] > div {
            background-color: #161b22;
            border: 1px solid #30363d !important;
            border-radius: 8px;
        }
        
        /* File Uploader */
        [data-testid="stFileUploader"] {
            border: 2px dashed #30363d;
            border-radius: 12px;
            padding: 1rem;
            text-align: center;
            background-color: #0d1117;
        }
        
        /* Expander */
        .streamlit-expanderHeader {
            background-color: #161b22;
            color: #e0e0e0;
            border-radius: 8px;
        }
    </style>
    """, unsafe_allow_html=True)

apply_custom_css()

# --- 4. LLM HELPER FUNCTIONS ---

def generate_with_fallback(model_name, prompt, image_data=None):
    """
    Tries to generate content with the primary model.
    If it fails (e.g., 404 Not Found), falls back to gemini-1.5-flash.
    """
    try:
        real_model_name = model_name.replace("models/", "")
        model = genai.GenerativeModel(real_model_name)
        if image_data:
            return model.generate_content([prompt, image_data])
        return model.generate_content(prompt)
    except Exception as e:
        if "404" in str(e) or "not found" in str(e).lower():
            # Fallback to stable gemini-1.5-flash if 2.5 fails
            try:
                fallback_model = genai.GenerativeModel("gemini-1.5-flash")
                if image_data:
                    return fallback_model.generate_content([prompt, image_data])
                return fallback_model.generate_content(prompt)
            except Exception as fallback_error:
                raise fallback_error
        else:
            raise e

def query_llm(prompt, model_name, image_data=None):
    """Unified function to query either Gemini or Groq."""
    try:
        # GROQ LOGIC
        if model_name.startswith("groq/"):
            if not groq_client:
                return "Error: GROQ_API_KEY not found in secrets."
            
            real_model_name = model_name.replace("groq/", "")
            
            completion = groq_client.chat.completions.create(
                messages=[{"role": "user", "content": prompt}],
                model=real_model_name,
            )
            return completion.choices[0].message.content

        # GEMINI LOGIC (Default)
        else:
            response = generate_with_fallback(model_name, prompt, image_data)
            return response.text

    except Exception as e:
        return f"Error generating content: {str(e)}"

def extract_text_from_pdf(uploaded_file):
    try:
        reader = PyPDF2.PdfReader(uploaded_file)
        text = "\n".join([page.extract_text() for page in reader.pages if page.extract_text()])
        return text
    except Exception as e:
        st.error(f"Error reading PDF: {e}")
        return None

def parse_resume_to_json(text, model_name):
    prompt = f"""
    Extract keys: name, email, phone, links, summary, experience, education, skills, certifications.
    Return ONLY valid JSON.
    RESUME TEXT: {text}
    """
    json_str = query_llm(prompt, model_name)
    try:
        json_str = json_str.strip()
        if json_str.startswith("```json"):
            json_str = json_str[7:]
        if json_str.endswith("```"):
            json_str = json_str[:-3]
        return json.loads(json_str)
    except:
        return None

def create_pdf(markdown_text, theme_color="#000000"):
    if theme_color.startswith('#'): theme_color = theme_color.lstrip('#')
    try: r, g, b = int(theme_color[0:2], 16), int(theme_color[2:4], 16), int(theme_color[4:6], 16)
    except: r, g, b = 0, 0, 0

    pdf = FPDF()
    pdf.add_page()
    pdf.set_auto_page_break(auto=True, margin=15)
    pdf.set_font("Arial", size=11)

    for line in markdown_text.split('\n'):
        pdf.set_text_color(0, 0, 0)
        pdf.set_font("Arial", size=11)

        if line.startswith('# '):
            pdf.set_text_color(r, g, b)
            pdf.set_font("Arial", 'B', 16)
            pdf.cell(0, 10, line.replace('# ', ''), ln=True)
        elif line.startswith('## '):
            pdf.set_text_color(r, g, b)
            pdf.set_font("Arial", 'B', 14)
            pdf.cell(0, 10, line.replace('## ', ''), ln=True)
        elif line.startswith('### '):
            pdf.set_text_color(r, g, b)
            pdf.set_font("Arial", 'B', 12)
            pdf.cell(0, 10, line.replace('### ', ''), ln=True)
        else:
            clean_line = line.replace('**', '').replace('* ', '• ')
            try: clean_line = clean_line.encode('latin-1', 'replace').decode('latin-1')
            except: clean_line = clean_line.encode('ascii', 'ignore').decode('ascii')
            pdf.multi_cell(0, 6, clean_line)
            
    return pdf.output(dest='S').encode('latin-1')

def analyze_skill_gap(resume_text, job_desc, model_name):
    prompt = f"""
    Compare RESUME and JD.
    JD: {job_desc}
    RESUME: {resume_text}
    Output: 1. Matching Skills, 2. Missing Skills, 3. Verdict.
    """
    return query_llm(prompt, model_name)

def generate_resume(user_data, job_desc, model_name):
    prompt = f"""
    Create a resume (Markdown).
    Details: {json.dumps(user_data)}
    Target JD: {job_desc}
    """
    return query_llm(prompt, model_name)

def extract_missing_skills(analysis_text):
    missing = []
    lines = analysis_text.split('\n')
    capture = False
    for line in lines:
        s = line.strip()
        if "missing" in s.lower() and "skill" in s.lower(): capture = True; continue
        if capture and "verdict" in s.lower(): capture = False; break
        if capture:
            clean = re.sub(r"^[\-\*\•\d\.]+\s*", "", s).replace("**", "").split(":")[0].strip()
            if clean and len(clean) < 80: missing.append(clean)
    return list(dict.fromkeys(missing))

def recommend_courses(missing_skills, courses_df):
    recs = {}
    if courses_df is None or courses_df.empty: return recs
    for skill in missing_skills:
        skill_lower = skill.lower()
        matches = courses_df[courses_df['Skill'].str.lower().apply(lambda x: skill_lower in str(x) or str(x) in skill_lower)]
        if not matches.empty:
            recs[skill] = matches.drop_duplicates('Course Name')[['Course Name', 'URL']].head(2).to_dict('records')
    return recs

# --- 5. STREAMLIT UI LAYOUT ---

# Default model is now the standard flash alias
if "model_name" not in st.session_state:
    st.session_state["model_name"] = "gemini-2.5-flash"

if "resume_data" not in st.session_state:
    st.session_state["resume_data"] = {
        "name": "", "email": "", "phone": "", "links": "",
        "summary": "", "experience": "", "education": "", "skills": "", "certifications": ""
    }

# --- SIDEBAR ---
with st.sidebar:
    st.markdown("## 🚀 Career Assistant")
    st.caption("AI-Powered Career Optimization")
    st.markdown("---")
    
    app_mode = st.radio("Select Tool:", ["Skill Gap Analyzer", "Resume Builder", "Career Chatbot"])
    
    # Removed Settings/Model Selection - Hardcoded to Free Model
    st.session_state["model_name"] = "gemini-2.5-flash"
    resume_theme_color = "#4b6cb7"
    
    courses_df = None
    if app_mode == "Skill Gap Analyzer":
        st.markdown("---")
        st.caption("Database")
        uploaded_csv = st.file_uploader("Upload Course CSV", type="csv")
        csv_path = "data/skillsbuild_courses.csv"
        
        if uploaded_csv: 
            courses_df = pd.read_csv(uploaded_csv)
        elif os.path.exists(csv_path):
            try:
                courses_df = pd.read_csv(csv_path)
                rename_map = {}
                for c in courses_df.columns:
                    if "skill" in c.lower(): rename_map[c] = "Skill"
                    if "course" in c.lower(): rename_map[c] = "Course Name"
                    if "url" in c.lower(): rename_map[c] = "URL"
                courses_df.rename(columns=rename_map, inplace=True)
            except: pass
        else:
            courses_df = pd.DataFrame(DEFAULT_COURSES)

# --- APP MODES ---

# 1. SKILL GAP ANALYZER
if app_mode == "Skill Gap Analyzer":
    st.title("📊 Skill Gap Analyzer")
    st.markdown("### Find missing skills & get course recommendations.")
    
    with st.container(border=True):
        c1, c2 = st.columns(2)
        with c1: 
            st.markdown("#### 1. Upload Your Resume")
            uploaded_resume = st.file_uploader("Upload PDF", type="pdf")
        with c2: 
            st.markdown("#### 2. Target Job Description")
            job_desc = st.text_area("Paste JD text here...", height=150)
            
        analyze_btn = st.button("🔍 Run Analysis")

    if analyze_btn:
        if uploaded_resume and job_desc:
            with st.spinner("AI is analyzing your profile..."):
                text = extract_text_from_pdf(uploaded_resume)
                if text:
                    analysis = analyze_skill_gap(text, job_desc, st.session_state["model_name"])
                    missing = extract_missing_skills(analysis)
                    
                    st.markdown("---")
                    st.success("Analysis Complete!")
                    
                    c_res, c_rec = st.columns([1, 1])
                    
                    with c_res:
                        st.subheader("📝 Analysis Report")
                        with st.container(border=True):
                            st.markdown(analysis)
                    
                    with c_rec:
                        st.subheader("🎓 Recommended Courses")
                        if missing:
                            if courses_df is not None:
                                recs = recommend_courses(missing, courses_df)
                                if recs:
                                    for skill, links in recs.items():
                                        with st.expander(f"📚 {skill}", expanded=True):
                                            for l in links: st.markdown(f"[{l['Course Name']}]({l['URL']})")
                                else: st.info("No database matches found.")
                            else: st.warning("Upload a CSV to get course links.")
                        else: st.success("Profile matches well!")
        else: st.error("Upload both files to proceed.")

# 2. RESUME BUILDER
elif app_mode == "Resume Builder":
    st.title("📝 Resume Builder")
    st.markdown("### Create an ATS-optimized resume in minutes.")

    # Auto-fill
    with st.expander("📂 Import from existing Resume (Optional)", expanded=False):
        uploaded_auto = st.file_uploader("Upload PDF to Auto-Fill", type="pdf", key="auto_fill")
        if uploaded_auto:
            if st.button("⚡ Extract Data"):
                with st.spinner("Extracting..."):
                    text = extract_text_from_pdf(uploaded_auto)
                    if text:
                        extracted_data = parse_resume_to_json(text, st.session_state["model_name"])
                        if extracted_data:
                            st.session_state["resume_data"] = extracted_data
                            st.success("Data Imported!")
                            st.rerun()

    # Form
    with st.form("resume_form"):
        st.subheader("1. Contact Info")
        c1, c2 = st.columns(2)
        name = c1.text_input("Full Name", value=st.session_state["resume_data"].get("name", ""))
        email = c2.text_input("Email", value=st.session_state["resume_data"].get("email", ""))
        phone = c1.text_input("Phone", value=st.session_state["resume_data"].get("phone", ""))
        links = c2.text_input("Links (LinkedIn/Github)", value=st.session_state["resume_data"].get("links", ""))

        st.subheader("2. Profile & Work")
        summary = st.text_area("Summary", value=st.session_state["resume_data"].get("summary", ""))
        experience = st.text_area("Experience", height=150, value=st.session_state["resume_data"].get("experience", ""))

        st.subheader("3. Skills & Education")
        c3, c4 = st.columns(2)
        education = c3.text_area("Education", value=st.session_state["resume_data"].get("education", ""))
        skills = c4.text_area("Skills", value=st.session_state["resume_data"].get("skills", ""))
        certifications = st.text_area("Certifications", value=st.session_state["resume_data"].get("certifications", ""))

        st.subheader("4. Target Job (Tailoring)")
        target_jd = st.text_area("Paste Job Description (Optional)", height=100)
        
        submitted = st.form_submit_button("✨ Generate Resume")
    
    if submitted:
        if name and experience:
            with st.spinner("Generating Resume Documents..."):
                user_data = {
                    "name": name, "email": email, "phone": phone, "links": links,
                    "summary": summary, "experience": experience,
                    "education": education, "skills": skills,
                    "certifications": certifications
                }
                resume_content = generate_resume(user_data, target_jd, st.session_state["model_name"])
                
                # --- PREVIEW SECTION ---
                st.markdown("---")
                st.subheader("👀 Live Preview")
                
                st.markdown(f"""
                <style>
                div[data-testid="stMarkdownContainer"] h1, 
                div[data-testid="stMarkdownContainer"] h2, 
                div[data-testid="stMarkdownContainer"] h3 {{
                    color: {resume_theme_color} !important;
                }}
                </style>
                """, unsafe_allow_html=True)
                
                with st.container(border=True):
                    st.markdown(resume_content)
                
                # --- FILES AT THE BOTTOM ---
                st.markdown("<br><br>", unsafe_allow_html=True)
                
                with st.container():
                    st.markdown("""
                    <div style="background-color: #161b22; padding: 20px; border-radius: 10px; color: white; text-align: center; margin-bottom: 20px; border: 1px solid #30363d;">
                        <h2 style="color: white; margin:0;">📂 Download Your Files</h2>
                        <p style="color: #8b949e; margin-top: 5px;">Your resume has been generated in multiple formats.</p>
                    </div>
                    """, unsafe_allow_html=True)
                    
                    c_dl1, c_dl2 = st.columns(2)
                    
                    with c_dl1:
                        st.info("📄 **PDF Version**\n\nBest for emailing.")
                        try:
                            pdf_bytes = create_pdf(resume_content, resume_theme_color)
                            st.download_button("⬇️ Download PDF", data=pdf_bytes, file_name=f"{name}_Resume.pdf", mime="application/pdf", use_container_width=True)
                        except Exception as e: st.error(f"PDF Error: {e}")
                        
                    with c_dl2:
                        st.info("📝 **Markdown Version**\n\nBest for editing raw text.")
                        st.download_button("⬇️ Download Markdown", data=resume_content, file_name=f"{name}_Resume.md", mime="text/markdown", use_container_width=True)

        else: st.warning("Please fill in Name and Experience to generate.")

# 3. CHATBOT
elif app_mode == "Career Chatbot":
    st.title("💬 Career Coach")
    st.markdown("### Ask me about interviews, salaries, or career paths.")
    
    chat_container = st.container(border=True)
    with chat_container:
        if "messages" not in st.session_state: st.session_state.messages = []
        for message in st.session_state.messages:
            with st.chat_message(message["role"]): st.markdown(message["content"])

    uploaded_file = None
    col1, col2 = st.columns([0.85, 0.15])
    with col2:
        with st.popover("📎 Attach File"):
            uploaded_file = st.file_uploader("Upload Image or PDF", type=["png", "jpg", "jpeg", "pdf"], key="chat_attach")

    if prompt := st.chat_input("Type your question here..."):
        with chat_container:
            st.chat_message("user").markdown(prompt)
            if uploaded_file:
                if uploaded_file.type in ["image/png", "image/jpeg", "image/jpg"]:
                     st.chat_message("user").image(uploaded_file, caption="Attached Image", width=300)
                else:
                     st.chat_message("user").markdown(f"📎 *Attached: {uploaded_file.name}*")
            
            st.session_state.messages.append({"role": "user", "content": prompt})

            with st.spinner("Thinking..."):
                try:
                    context_prompt = "You are an expert AI Career Coach. Keep answers short.\n\nHistory:\n"
                    for msg in st.session_state.messages: context_prompt += f"{msg['role'].upper()}: {msg['content']}\n"
                    
                    image_data = None
                    if uploaded_file and uploaded_file.type in ["image/png", "image/jpeg", "image/jpg"]:
                        image_data = Image.open(uploaded_file)
                    
                    final_prompt = prompt
                    if uploaded_file and uploaded_file.type == "application/pdf":
                         pdf_text = extract_text_from_pdf(uploaded_file)
                         final_prompt = f"{prompt}\n\n[ATTACHED PDF CONTENT]:\n{pdf_text}"
                    
                    ai_reply = query_llm(context_prompt + f"\nUSER: {final_prompt}", st.session_state["model_name"], image_data)
                    
                    with st.chat_message("assistant"): st.markdown(ai_reply)
                    st.session_state.messages.append({"role": "assistant", "content": ai_reply})
                except Exception as e: st.error(f"Error: {e}")
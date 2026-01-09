# 🚀 AI Career Assistant

[![Python 3.8+](https://img.shields.io/badge/Python-3.8+-blue?logo=python&logoColor=white)](https://www.python.org/)
[![Streamlit](https://img.shields.io/badge/Streamlit-1.0+-red?logo=streamlit&logoColor=white)](https://streamlit.io/)
[![Google Generative AI](https://img.shields.io/badge/Google%20Gemini-API-4285F4?logo=google&logoColor=white)](https://ai.google.dev/)
[![License: MIT](https://img.shields.io/badge/License-MIT-green.svg)](LICENSE)
[![Status: Active](https://img.shields.io/badge/Status-Active%20Development-brightgreen)](https://github.com/)
[![SDG 8: Decent Work](https://img.shields.io/badge/SDG%208-Decent%20Work%20%26%20Economic%20Growth-green)](https://sustainabledevelopment.un.org/sdg8)

> **Empowering job seekers worldwide** with AI-powered resume optimization, skill gap analysis, and intelligent career coaching. Aligns with UN Sustainable Development Goal 8 (Decent Work & Economic Growth).

---

## 📋 Table of Contents

- [Overview](#-overview)
- [Key Features](#-key-features)
- [Tech Stack](#-tech-stack)
- [Project Structure](#-project-structure)
- [Installation](#-installation)
- [Configuration](#-configuration)
- [Usage](#-usage)
- [File Descriptions](#-file-descriptions)
- [Contributing](#-contributing)
- [License](#-license)
- [Contact](#-contact)

---

## 📖 Overview

The **AI Career Assistant** is a comprehensive, Streamlit-based web application designed to serve as your personal career coach. Powered by Google Gemini AI, it helps job seekers and professionals:

- 📊 **Analyze skill gaps** between their resume and target job descriptions
- 📝 **Generate ATS-optimized resumes** tailored to specific roles
- 💬 **Access intelligent career guidance** through an interactive chatbot
- 🎓 **Discover relevant learning paths** with curated course recommendations

Whether you're preparing for your dream job, transitioning careers, or looking to upskill, this tool provides actionable insights backed by advanced AI.

---

## ✨ Key Features

### 1. 📊 **Skill Gap Analyzer**

Compare your resume directly against job descriptions to identify exact skill matches and critical gaps.

**Capabilities:**
- ✅ Upload resume as PDF or image (JPG/PNG)
- ✅ Paste or upload job description
- ✅ AI-powered analysis highlighting:
  - Matching skills you already possess
  - Missing skills critical for the role
  - Expert verdict with actionable summary
- ✅ **Smart course recommendations** based on identified gaps
- ✅ Curated learning paths from Coursera, IBM SkillsBuild, Udemy, and more

**Use Case:** "I found a dream job posting. Now what skills do I need to learn?"

---

### 2. 📝 **AI Resume Builder**

Create professional, ATS-friendly resumes optimized for specific job roles.

**Capabilities:**
- ✅ **Auto-fill feature**: Upload existing resume (PDF/Image) to extract data
- ✅ **Smart form**: Organized sections for personal details, experience, education, and skills
- ✅ **Job-tailored generation**: Paste job description to optimize keywords
- ✅ **Multi-export formats**:
  - 📥 Download as Markdown (editable)
  - 📄 Download as professional PDF with custom accent colors
- ✅ **ATS optimization**: Automatically incorporates industry keywords
- ✅ **Action-verb enhancement**: Uses strong, impactful language
- ✅ **Achievement quantification**: Emphasizes measurable results

**Use Case:** "Create a resume that gets past ATS systems and impresses recruiters."

---

### 3. 💬 **Career Coach Chatbot**

An intelligent conversational AI that provides real-time career guidance.

**Capabilities:**
- ✅ **Multi-topic support**:
  - Interview preparation (behavioral, technical)
  - Salary negotiation strategies
  - Career transition planning
  - Professional development advice
- ✅ **Image attachment**: Attach images for context-aware feedback
- ✅ **Conversation memory**: Maintains chat history for coherent discussions
- ✅ **Professional tone**: Expert-level advice tailored to your needs
- ✅ **Real-time responses**: Powered by Google Gemini

**Use Case:** "Help me prepare for my technical interview next week."

---

### 4. 🎨 **Modern, Responsive UI**

- Dark-themed, modern interface with high-contrast design
- Card-based layout for easy navigation
- Smooth interactions and real-time feedback
- Fully responsive design (desktop and tablet optimized)

---

## 🛠️ Tech Stack

| Component | Technology | Details |
|-----------|-----------|---------|
| **Frontend** | Streamlit | Fast, interactive web apps without JavaScript |
| **AI Models** | Google Generative AI (Gemini) | State-of-the-art language models |
| **PDF Processing** | PyPDF2, FPDF | Extract text from PDFs & generate PDF exports |
| **Image Processing** | Pillow (PIL) | Handle resume images and attachments |
| **Data Processing** | Pandas | Manage course recommendations and data |
| **Environment** | Python-dotenv | Secure API key management |

---

## 📂 Project Structure

```
AI-Powered-Career-Assistant-SDG8/
├── 📄 app.py                           # Main application (535 lines)
│   ├── Configuration & Setup
│   ├── Custom UI Styling
│   ├── Core Functions
│   │   ├── extract_content_from_file()    # PDF/Image extraction
│   │   ├── parse_resume_to_json()         # Resume parsing
│   │   ├── analyze_skill_gap()            # Gap analysis engine
│   │   ├── generate_resume()              # Resume generation
│   │   ├── create_pdf()                   # PDF export
│   │   ├── recommend_courses()            # Course matching
│   │   └── extract_missing_skills()       # Skill extraction
│   └── UI Modes
│       ├── Skill Gap Analyzer             # Feature 1
│       ├── Resume Builder                 # Feature 2
│       └── Career Chatbot                 # Feature 3
│
├── 📋 requirements.txt                 # Python dependencies
│
├── 🔐 .env                            # API Keys (⚠️ Not in repo)
│   ├── GOOGLE_API_KEY=your_key
│   └── (Optional) GROQ_API_KEY
│
├── 📊 data/
│   ├── skillsbuild_courses.csv        # IBM SkillsBuild course database
│   └── skillsbuild_courses.csv.xlsx   # Excel version of dataset
│
└── 📖 README.md                       # This file

```

---

## ⚙️ Installation

### Prerequisites

- **Python 3.8+** installed on your system
- **pip** package manager
- A **Google API Key** for Gemini (Free tier available)

### Step 1: Clone the Repository

```bash
git clone https://github.com/yourusername/AI-Powered-Career-Assistant-SDG8.git
cd AI-Powered-Career-Assistant-SDG8
```

### Step 2: Create a Virtual Environment (Recommended)

```bash
# Windows
python -m venv venv
venv\Scripts\activate

# macOS/Linux
python3 -m venv venv
source venv/bin/activate
```

### Step 3: Install Dependencies

```bash
pip install -r requirements.txt
```

**Dependencies included:**
- `streamlit` - Web framework
- `google-generativeai` - Gemini API client
- `pypdf2` - PDF text extraction
- `pandas` - Data processing
- `python-dotenv` - Environment variable management
- `Pillow` - Image processing
- `fpdf` - PDF generation

### Step 4: Configure API Keys

Create a `.env` file in the root directory:

```bash
# .env file
GOOGLE_API_KEY=your_actual_gemini_api_key_here
```

**How to get your Google API Key:**
1. Visit [Google AI Studio](https://aistudio.google.com)
2. Click "Create API Key"
3. Copy the key and paste into `.env`

⚠️ **Security Note:** Never commit `.env` to version control. It's already in `.gitignore`.

### Step 5: Run the Application

```bash
streamlit run app.py
```

The app will open in your default browser at `http://localhost:8501`

---

## 🚀 Usage Guide

### **Mode 1: Skill Gap Analyzer** 📊

1. **Navigate** to "Skill Gap Analyzer" from the sidebar
2. **Upload Resume**: Select a PDF or image (JPG/PNG) of your resume
3. **Paste Job Description**: Copy the full job posting into the text area
4. **Click "Analyze Gap"** and wait for AI analysis
5. **Review Results**:
   - Matching skills (what you have)
   - Missing skills (what you need)
   - Expert verdict with next steps
6. **Explore Courses**: Click recommended courses to start learning

**Example:**
```
Resume: Software Engineer with Python & React skills
Job Description: Senior Software Engineer (Python, React, Docker, Kubernetes)
Missing Skills Found: Docker, Kubernetes, Cloud Deployment
Recommended Courses: [Docker Mastery] [Kubernetes from Scratch]
```

---

### **Mode 2: Resume Builder** 📝

#### Option A: Build from Scratch
1. **Navigate** to "Resume Builder"
2. **Fill the form** with your details:
   - Personal: Name, Email, Phone, LinkedIn
   - Professional: Summary, Experience, Education, Skills, Certifications
   - Optional: Paste target job description to optimize keywords
3. **Click "Generate Resume"**
4. **Download**: Choose Markdown or PDF format

#### Option B: Auto-Fill from Existing Resume
1. **Expand** "Import Data from Existing Resume"
2. **Upload** your current resume (PDF or image)
3. **Click "Extract & Fill"** - AI will parse and populate the form
4. **Review & Edit** the extracted information
5. **Click "Generate Resume"** to create tailored version
6. **Download** in your preferred format

**Features:**
- ✅ ATS keyword optimization
- ✅ Strong action verbs (coordinated, spearheaded, implemented)
- ✅ Achievement quantification ($X saved, Y% improvement)
- ✅ Custom color themes for PDF export

---

### **Mode 3: Career Coach Chatbot** 💬

1. **Navigate** to "Career Chatbot"
2. **Type your question** in the input box
3. **Optional: Attach Image** - Click 📎 to upload resume/portfolio image for feedback
4. **Send message** - AI responds in real-time
5. **Continue conversation** - Full context maintained

**Example Queries:**
- "How do I prepare for a technical interview?"
- "What should be my salary range for X role?"
- "I want to transition from Data Science to ML Engineering. How?"
- "Review my resume screenshot and give feedback"

---

## 📄 File Descriptions

### `app.py` (535 lines)
The complete Streamlit application containing:

| Section | Lines | Purpose |
|---------|-------|---------|
| Configuration & Setup | 1-30 | API initialization, page config |
| Custom CSS Styling | 31-108 | Dark theme & responsive design |
| Core Functions | 109-310 | AI operations & file processing |
| Skill Gap Analyzer UI | 350-410 | Resume vs JD comparison interface |
| Resume Builder UI | 411-480 | Form & resume generation interface |
| Career Chatbot UI | 481-535 | Chat interface with memory |

**Key Functions:**
- `extract_content_from_file()` - Handles PDF text & image processing
- `parse_resume_to_json()` - Extracts structured resume data
- `analyze_skill_gap()` - Generates gap analysis
- `generate_resume()` - Creates tailored resume
- `recommend_courses()` - Matches skills to courses
- `create_pdf()` - Exports professional PDF

### `requirements.txt`
Lists all Python package dependencies with versions:
```
streamlit>=1.0
google-generativeai>=0.3.0
pypdf2>=3.0
pandas>=1.3
python-dotenv>=0.19
Pillow>=9.0
fpdf>=1.7.2
```

### `data/skillsbuild_courses.csv`
Course recommendation database with columns:
- **Skill**: Technical skill (Python, Docker, AWS, etc.)
- **Course Name**: Official course title
- **URL**: Direct enrollment link
- **Provider**: Coursera, IBM SkillsBuild, Udemy, etc.

---

## 🔧 Configuration

### Customizing Colors & Themes

In `app.py` (lines 30-45), modify the CSS variables:

```css
/* Change primary accent color */
--color-primary: #FF6B9D;  /* Default: Green */

/* Change sidebar background */
section[data-testid="stSidebar"] {
    background-color: #1e1e1e;
}

/* Change main background */
.stApp {
    background-color: #0d0d0d;
}
```

### Using Custom Course Database

Replace `skillsbuild_courses.csv` with your own CSV following this format:

| Skill | Course Name | URL | Provider |
|-------|-------------|-----|----------|
| Python | Python for Everybody | https://... | Coursera |
| Docker | Docker Mastery | https://... | Udemy |

---

## 🌟 Advanced Features

### Model Selection
The app automatically detects available Gemini models:
- **Gemini 2.5 Flash** (Recommended) - Fastest responses
- **Gemini 1.5 Flash** - Balanced speed/quality
- **Gemini 1.5 Pro** - Best quality (slower)

### Multimodal Input
- **Text**: Direct paste of resumes/job descriptions
- **Images**: JPG/PNG upload for resume images
- **PDFs**: Direct PDF file upload with text extraction

### Session State Management
- Chat history persists within session
- Resume form data saved for multi-step workflows
- User selections remembered

---

## 📊 Example Workflow

### Complete Job Application Preparation

```
1. Start: Want to apply for "Senior Data Engineer" role
   ↓
2. Use Analyzer: Compare resume vs job description
   - Find 3 missing skills: Spark, Airflow, Docker
   ↓
3. Get Recommendations: AI suggests learning paths
   - Coursera: Apache Spark Advanced
   - Udemy: Airflow Mastery
   - Linux Academy: Docker Essentials
   ↓
4. Use Chatbot: Prepare for interview
   - "How to answer questions about Spark?"
   - "What salary should I ask for?"
   ↓
5. Use Builder: Create ATS-optimized resume
   - Import existing resume
   - Target "Senior Data Engineer" JD
   - Generate optimized version
   - Export as PDF
   ↓
6. Result: Ready to apply with confidence! 🎉
```

---

## 📈 Performance & Optimization

- **Fast**: Streamlit provides instant UI response
- **Scalable**: Handles multiple concurrent users
- **Reliable**: Error handling for file uploads & API calls
- **Efficient**: Session-based state management reduces redundant API calls

---

## 🐛 Troubleshooting

| Issue | Solution |
|-------|----------|
| "GOOGLE_API_KEY not found" | Create `.env` file with your API key |
| PDF upload fails | Ensure file is < 20MB and valid format |
| Slow responses | Use Gemini Flash for speed, Pro for quality |
| "No courses found" | Check `skillsbuild_courses.csv` exists |
| Chat not responding | Verify API key has sufficient quota |

---

## 🚀 Future Enhancements

- [ ] Support for Groq LLM models (Llama 3, Mixtral)
- [ ] Interview video recording & AI feedback
- [ ] LinkedIn integration for direct profile updates
- [ ] Salary negotiation calculator
- [ ] Portfolio website generator
- [ ] Cover letter assistant
- [ ] 1-on-1 mentorship matching
- [ ] Multi-language support

---

## 🤝 Contributing

Contributions are welcome! Here's how to help:

1. **Fork** the repository
2. **Create** a feature branch (`git checkout -b feature/AmazingFeature`)
3. **Commit** your changes (`git commit -m 'Add AmazingFeature'`)
4. **Push** to the branch (`git push origin feature/AmazingFeature`)
5. **Open** a Pull Request

### Development Guidelines
- Follow PEP 8 style guide
- Add docstrings to functions
- Test all features locally before submitting PR
- Update README for new features

---

## 📜 License

This project is licensed under the **MIT License** - see [LICENSE](LICENSE) file for details.

---

## 🌍 Sustainable Development Goals

This project aligns with **UN Sustainable Development Goal 8: Decent Work & Economic Growth**

By providing AI-powered career assistance, we empower individuals to:
- 📈 Access quality employment opportunities
- 💡 Develop in-demand skills
- 🌐 Reduce global employment disparities
- 🎯 Support economic growth through human capital development

**Impact:**
- Helps millions of job seekers globally
- Reduces hiring bias through skill-based matching
- Democratizes career coaching access

---

## 📞 Contact & Support

**Created by:** Vignesh R

**Email:** vv7640972@gmail.com

**LinkedIn:** [Vignesh R]((https://www.linkedin.com/in/vignesh-r-78bb82327/))

**GitHub:** [Vignesh-2402](https://github.com/Vignesh-2402/)

### Get Help
- 💬 Open an Issue for bugs
- 🤔 Start a Discussion for questions
- 📧 Email for direct support

---

## 🙏 Acknowledgments

- Google Generative AI (Gemini) for powerful language models
- Streamlit for an amazing web framework
- IBM SkillsBuild for course data
- All contributors and users of this project

---

## ⭐ Show Your Support

If this project helped you, please give it a **star** ⭐ on GitHub!

```
Your support motivates us to build better tools for career development.
```

---

**Made with ❤️ for job seekers and career professionals worldwide.**

*Last Updated: January 2026*

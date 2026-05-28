import streamlit as st
import pdfplumber
import os
import nltk
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity

# Download required nltk data

nltk.download('punkt')

# ---------------- FUNCTIONS ----------------

def extract_text_from_pdf(file):
    text =""
with pdfplumber.open(file) as pdf:
for page in pdf.pages:
page_text = page.extract_text()
if page_text:
text += page_text
return text

def calculate_ats_score(resume_text, job_description):
documents = [resume_text, job_description]

```
tfidf = TfidfVectorizer(stop_words='english')
matrix = tfidf.fit_transform(documents)

score = cosine_similarity(matrix[0:1], matrix[1:2])[0][0]

return round(score * 100, 2)
```

def extract_skills(text):
skills_list = [
"python", "java", "sql", "machine learning", "deep learning",
"nlp", "tensorflow", "pytorch", "opencv", "pandas", "numpy",
"excel", "data analysis", "statistics"
]

```
text = text.lower()
found_skills = []

for skill in skills_list:
    if skill in text:
        found_skills.append(skill)

return found_skills
```

# ---------------- STREAMLIT UI ----------------

st.set_page_config(page_title="AI Resume Analyzer", layout="wide")

st.title("🤖 AI Resume Analyzer & ATS Checker")
st.write("Upload your resume and compare it with a job description")

# Create uploads folder

if not os.path.exists("uploads"):
os.makedirs("uploads")

# Upload file

uploaded_file = st.file_uploader("Upload Resume (PDF)", type=["pdf"])

# Job description input

job_description = st.text_area("Paste Job Description")

resume_text = ""

# ---------------- PROCESS RESUME ----------------

if uploaded_file is not None:
file_path = os.path.join("uploads", uploaded_file.name)

```
# Save file
with open(file_path, "wb") as f:
    f.write(uploaded_file.getbuffer())

st.success("Resume uploaded successfully!")

# Extract text
resume_text = extract_text_from_pdf(uploaded_file)

st.subheader("📄 Resume Text")
st.write(resume_text)
```

# ---------------- ANALYSIS ----------------

if uploaded_file is not None and job_description:

```
st.subheader("📊 Analysis Result")

# Skills
skills = extract_skills(resume_text)
st.write("**Detected Skills:**", skills)

# ATS Score
ats_score = calculate_ats_score(resume_text, job_description)
st.write("**ATS Score:**", ats_score, "%")

# Result message
if ats_score >= 75:
    st.success("Strong Match ✔ Good Resume for this Job")
elif ats_score >= 50:
    st.warning("Moderate Match ⚠ Improve your Resume")
else:
    st.error("Weak Match ❌ Needs Improvement")
```

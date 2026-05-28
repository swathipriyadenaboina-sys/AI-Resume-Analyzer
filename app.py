
import streamlit as st
import pdfplumber
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity

st.set_page_config(page_title="AI Resume Analyzer")

st.title("AI Resume Analyzer")
st.write("Upload your resume PDF")

uploaded_file = st.file_uploader("Upload Resume", type=["pdf"])

job_description = st.text_area("Paste Job Description")

skills_db = [
    "Python",
    "Machine Learning",
    "Deep Learning",
    "SQL",
    "Java",
    "JavaScript",
    "React",
    "Flask",
    "TensorFlow",
    "PyTorch",
    "Scikit-learn",
    "Pandas",
    "NumPy",
    "OpenCV",
    "LangChain",
    "NLP",
    "Generative AI",
    "Artificial Intelligence",
    "Data Science",
    "Git",
    "GitHub",
    "API",
    "FastAPI",
    "Streamlit",
]

if uploaded_file:

    text = ""

    with pdfplumber.open(uploaded_file) as pdf:
        for page in pdf.pages:
            extracted = page.extract_text()

            if extracted:
                text += extracted

    st.subheader("Resume Text")
    st.write(text)

    found_skills = []

    for skill in skills_db:
        if skill.lower() in text.lower():
            found_skills.append(skill)

    st.subheader("Detected Skills")

    if found_skills:
        for skill in found_skills:
            st.success(skill)
    else:
        st.warning("No skills detected")

    ats_score = len(found_skills) * 4

    if ats_score > 100:
        ats_score = 100

    st.subheader("ATS Score")

    st.progress(ats_score / 100)

    st.write(f"ATS Score: {ats_score}%")

    if job_description:

        text_list = [text, job_description]

        vectorizer = TfidfVectorizer()

        vectors = vectorizer.fit_transform(text_list)

        similarity = cosine_similarity(vectors[0:1], vectors[1:2])

        match_percentage = int(similarity[0][0] * 100)

        st.subheader("Job Match Percentage")

        st.progress(match_percentage / 100)

        st.write(f"Match Percentage: {match_percentage}%")

    st.subheader("Suggestions")

    if ats_score < 50:
        st.error("Add more technical skills and projects.")
    elif ats_score < 80:
        st.warning("Resume is good but can be improved.")
    else:
        st.success("Excellent Resume!")
SKILLS = [
    "python", "java", "c", "c++",
    "html", "css", "javascript",
    "react", "angular", "node.js",
    "flask", "django", "spring",
    "sql", "mysql", "mongodb",
    "git", "github",
    "aws", "azure", "docker",
    "kubernetes",
    "rest api",
    "machine learning",
    "deep learning",
    "artificial intelligence",
    "nlp",
    "data science",
    "power bi",
    "excel",
    "linux",
    "oop",
    "communication",
    "problem solving"
]
from flask import Flask, request, render_template
import fitz  # PyMuPDF
import spacy

# -----------------------------
# Initialize Flask
# -----------------------------
app = Flask(__name__)

# -----------------------------
# Load spaCy Model
# -----------------------------
nlp = spacy.load("en_core_web_sm")


# -----------------------------
# Extract Job Description Keywords
# -----------------------------
def extract_job_keywords(job_description):

    job_description = job_description.lower()

    found_skills = []

    for skill in SKILLS:

        if skill.lower() in job_description:
            found_skills.append(skill)

    print("Job Skills:", found_skills)

    return found_skills

# -----------------------------
# Read Resume PDF
# -----------------------------
def extract_resume_text(file):

    text = ""

    pdf = fitz.open(stream=file.read(), filetype="pdf")

    for page in pdf:
        text += page.get_text()

    pdf.close()

    return text


# -----------------------------
# Match Resume Skills
# -----------------------------
def extract_skills(resume_text, job_keywords):

    resume_text = resume_text.lower()

    resume_skills = []

    for skill in SKILLS:

        if skill.lower() in resume_text:
            resume_skills.append(skill)

    matched = []

    missing = []

    for skill in job_keywords:

        if skill in resume_skills:
            matched.append(skill)
        else:
            missing.append(skill)

    if len(job_keywords) == 0:
        percentage = 0
    else:
        percentage = round((len(matched) / len(job_keywords)) * 100, 2)

    print("Resume Skills :", resume_skills)
    print("Matched :", matched)
    print("Missing :", missing)

    return matched, missing, percentage
# -----------------------------
# Home Page
# -----------------------------
@app.route("/")
def home():

    return render_template(
        "index.html",
        score=None,
        matched="",
        missing=""
    )


# -----------------------------
# Analyze Resume
# -----------------------------
@app.route("/predict", methods=["POST"])
def predict():

    if "resume" not in request.files:

        return render_template(
            "index.html",
            score=0,
            matched="",
            missing="No Resume Uploaded"
        )

    file = request.files["resume"]

    if file.filename == "":

        return render_template(
            "index.html",
            score=0,
            matched="",
            missing="Please Select Resume"
        )

    if not file.filename.lower().endswith(".pdf"):

        return render_template(
            "index.html",
            score=0,
            matched="",
            missing="Upload PDF Only"
        )

    job_description = request.form.get("job_description", "").strip()

    if job_description == "":

        return render_template(
            "index.html",
            score=0,
            matched="",
            missing="Please Enter Job Description"
        )

    resume_text = extract_resume_text(file)

    job_keywords = extract_job_keywords(job_description)

    matched, missing, percentage = extract_skills(
        resume_text,
        job_keywords
    )

    return render_template(
        "index.html",
        score=percentage,
        matched=", ".join(matched),
        missing=", ".join(missing)
    )


# -----------------------------
# Run Flask
# -----------------------------
if __name__ == "__main__":

    print("🚀 Flask server starting on http://127.0.0.1:5000")

    app.run(host="127.0.0.1", port=5000, debug=True)
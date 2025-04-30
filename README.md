# Incorporating-AI-Agents-for-Streamlining-HR-Recruitment-Process
This project leverages Generative AI and automation to streamline recruitment by automating email retrieval, resume evaluation, and candidate communication, reducing manual effort, bias, and time, and enabling faster, more objective hiring decisions.
AI-Driven Automated HR Recruitment System
Overview
This project is designed to automate the recruitment process using Generative AI and automation tools. It streamlines email retrieval, resume evaluation based on job descriptions, and candidate communication, reducing manual effort, time, and potential biases in hiring.

🚀 Features:

📬 Email Integration – Automatically fetches job application emails using IMAP.

📄 Resume Analysis – Evaluates resumes against a provided job description using a Language Model.

📊 Candidate Shortlisting – Stores filtered and ranked candidates in a structured CSV format.

📧 Email Notifications – Sends customized response emails to applicants based on their evaluation.


Tech Stack:

Python

IMAP (for email reading)

OpenAI / LLM Chain (for resume evaluation)

SMTP / Gmail Agent (for sending emails)

Pandas (for CSV file handling)

Setup Instructions:

Clone the repository

bash
Copy
Edit
git clone <repository-url>
cd HRP
Install dependencies

bash
Copy
Edit
pip install -r requirements.txt
Configure credentials

Update email credentials and OpenAI API keys in the .env or config file (if applicable).

Run the project

bash
Copy
Edit
python main.py
Folder Structure
graphql
Copy
Edit
HRP/
├── resumes/                 # Folder to store fetched resumes
├── job_description.txt      # Input JD for resume matching
├── results.csv              # Output of shortlisted candidates
├── email_handler.py         # Handles IMAP and SMTP communication
├── resume_evaluator.py      # Uses LLM to evaluate resumes
├── main.py                  # Entry point
└── README.md
Future Enhancements
Add web dashboard for HR interaction

Integrate with ATS (Applicant Tracking Systems)

Support for multilingual resumes

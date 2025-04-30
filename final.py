#Final.py
import streamlit as st
import os
from  attachments import download_pdfs
from resume import process_resumes_in_folder
from mail import send_mails, search_mails
from pathlib import Path
#jlsbkoanclltyfdy
# Set up Streamlit interface
st.title("Hire Assistant")
api_key="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"

# Set up environment variables
# os.environ["AZURE_OPENAI_ENDPOINT"] = "https://llm-api-gateway-v2.azurewebsites.net"
# os.environ["AZURE_OPENAI_API_KEY"] = "m8CHxff-D8N3PMQQBINku7JWGRX5JNJUeIDBcym286I"

# User inputs for Gmail credentials and job description
email_user = st.text_input("Gmail Address")
email_pass = st.text_input("Gmail Password", type="password")
job_description = st.text_area("Job Description")
folder_path = r'D:/HRP/Resumes'
# Create the folder if it doesn't exist
Path(folder_path).mkdir(parents=True, exist_ok=True)

# Step 1: Download PDFs
if st.button("Download Resumes"):
    if email_user and email_pass:
        downloaded_files, n = download_pdfs(folder_path, email_user, email_pass)
        st.success("Resumes downloaded successfully!")

        st.write(f"From last 24 hours, you have {n} mails related to job applications: ")
        for message in downloaded_files:
                st.write(message)
    else:
        st.error("Please provide your Gmail credentials.")

# Step 2: Process Resumes
if st.button("Process Resumes"):
    if job_description:
        results = process_resumes_in_folder(folder_path, job_description, api_key)
        st.success("Resumes processed and results saved to CSV!")

        # Display results
        st.write("### CANDIDATES RESULTS: ")
        for data in results:
            name, email, phone, percentage_match = data
            st.write(f"**Name:** {name}, **Email:** {email}, **Percentage Match:** {percentage_match}")
    else:
        st.error("Please provide a job description.")


# Step 3: Send Emails
if st.button("Send Emails"):
    shortlisted, rejected = send_mails()
    st.success("Emails sent to shortlisted candidates!")
    # Display summary of results
    total_candidates = len(shortlisted) + len(rejected)
    shortlisted_count = len(shortlisted)
    rejected_count = len(rejected)

    st.write(f"Out of {total_candidates} candidates, {shortlisted_count} are shortlisted and {rejected_count} got rejected.")

    # Display shortlisted candidates
    st.write("### Shortlisted Candidates")

    for candidate in shortlisted:
        name = candidate[0]  # Adjust index based on your CSV structure
        email = candidate[1]
        st.write(f"**Name:** {name}, **Email:** {email}")

    # Display rejected candidates
    st.write("### Rejected Candidates")
    for candidate in rejected:
        name = candidate[0]  # Adjust index based on your CSV structure
        email = candidate[1]
        st.write(f"**Name:** {name}, **Email:** {email}")

# # Step 4: Retrieve Emails
# st.write('### Search for the mails: ')
# query = st.text_input("Enter your query: ")
# if st.button("Retrieve Email"):
#     if query:
#         emails = search_mails(query)
#         if emails:
#             st.write("### Retrieved Emails:")
#             st.text(emails)  # Display the retrieved emails
#         else:
#             st.error("No emails found or an error occurred.")
#     else:
#         st.error("Please enter a query to search for emails.")

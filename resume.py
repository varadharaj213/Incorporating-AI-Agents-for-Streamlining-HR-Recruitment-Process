# resumee.py

import os
import re
import csv
# from langchain_openai import AzureChatOpenAI
from langchain_groq import ChatGroq
from langchain.prompts import PromptTemplate
from langchain.chains import LLMChain
import fitz

def read_all_pdf_pages(pdf_path):
    text = ''
    with fitz.open(pdf_path) as pdf_document:
        for page_num in range(pdf_document.page_count):
            page = pdf_document.load_page(page_num)
            text += page.get_text()
    return text

def setup_llm_chain(api_key):
    llm = ChatGroq(
    model="gemma2-9b-it",
    api_key="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"
)

    prompt_template ='''You are a highly skilled ATS (Applicant Tracking System) scanner with expertise in evaluating resumes against job_description given.

Your task is to analyze the provided context and compare it against the given job_description. Based on this comparison, you need to generate an ATS score, which is a percentage match between the context and the job_description. 

Please follow these steps:
1. Read the job description carefully.
2. Analyze the context for relevant skills, experiences, and qualifications.
3. Generate an ATS score as a percentage match (e.g., 85%).
4. Identify and list any critical keywords or skills that are missing from the resume.
5. Provide a concise justification for the ATS score based on your analysis.

Format your output as follows:
1. Name of the person: [Extracted Name]
2. Email of the person: [Extracted Email]
3. Phone number of the person: [Extracted Phone]
4. Percentage match: [Calculated Percentage Match]
5. Keywords missing from the resume: [List of Missing Keywords]
6. Final thoughts: [Your Justification]

Job Description: {job_description}
Context: {context}

Ensure your output is factual, and avoid making assumptions or fabricating information. If any required information is missing or cannot be determined, indicate that clearly.
'''

    prompt = PromptTemplate(
        input_variables=["job_description", "context"],
        template=prompt_template
    )
    return prompt | llm

def extract_information(response):
    # Extract the text from the AIMessage response
    if hasattr(response, 'content'):
        response_text = response.content
    else:
        response_text = str(response)  # Fallback if content attribute is missing

    # Now use regex to extract the needed information
    name = re.search(r'Name of the person:\s*(.*)', response_text).group(1).strip()
    email = re.search(r'Email of the person:\s*(.*)', response_text).group(1).strip()
    phone = re.search(r'Phone number of the person:\s*(.*)', response_text).group(1).strip()
    percentage_match = re.search(r'Percentage match:\s*(.*)', response_text).group(1).strip()

    return [name, email, phone, percentage_match]


def write_to_csv(data, filename='shortlist1.csv'):
    # Check if file exists to determine if we need to write headers
    file_exists = os.path.isfile(filename)
    
    with open(filename, 'a', newline='') as file:
        writer = csv.writer(file)
        
        # Write header only if file does not exist
        if not file_exists:
            writer.writerow(["Name", "Email", "Phone Number", "Percentage Match"])
        
        writer.writerow(data)

def process_resumes_in_folder(folder_path, job_description, api_key):
    chain = setup_llm_chain(api_key)
    results = []  # Collect results here
    
    for filename in os.listdir(folder_path):
        if filename.endswith('.pdf'):
            pdf_path = os.path.join(folder_path, filename)
            context = read_all_pdf_pages(pdf_path)
            response = chain.invoke({"job_description": job_description, "context": context})
            extracted_data = extract_information(response)
            results.append(extracted_data)  # Add extracted data to results list
            write_to_csv(extracted_data)  # Write to CSV 
    
    return results  # Return the collected results


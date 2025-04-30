# mail.py
import os
import csv
from langchain_community.agent_toolkits import GmailToolkit
from langchain import hub
from langgraph.prebuilt import create_react_agent
from langchain.agents import initialize_agent, AgentType
# from langchain_openai import AzureChatOpenAI
from langchain_groq import ChatGroq

from langchain_community.tools.gmail.utils import (
    build_resource_service,
    get_gmail_credentials,
)

credentials = get_gmail_credentials(
        token_file="token.json",
        scopes=["https://mail.google.com/"],
        client_secrets_file="cred.json",
    )

api_resource = build_resource_service(credentials=credentials)
toolkit = GmailToolkit(api_resource=api_resource)
tools = toolkit.get_tools()

llm = ChatGroq(
    model="gemma2-9b-it",
    api_key="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"
)
def send_mails(shortlist_filename='shortlist1.csv'):
    
    agent_executor = create_react_agent(llm, tools)

    shortlisted_candidates = []
    rejected_candidates = []

    with open(shortlist_filename, mode='r') as file:
        reader = csv.reader(file)
        header = next(reader)
        email_index = header.index("Email")
        match_index = header.index("Percentage Match")

        for row in reader:
            email_id = row[email_index]
            percentage_match = float(row[match_index].replace('%', ''))

            if percentage_match >= 75:
                example_query = f'''Send an email to {email_id} informing them that they have been shortlisted for the interview. 
                    Please ensure the email is structured in the following way: 
                    1. Begin with a warm greeting as candidate.
                    2. Confirm her selection for an interview with Roman Solutions Company.
                    3. Request her availability to schedule the interview.
                    4. Conclude with best regards from Roman Solutions Company.
                    Make sure to format the email into at least two paragraphs. Directly send it, don't ask for review.
                '''
#distinct
                events = agent_executor.stream(
                    {"messages": [("user", example_query)]},
                    stream_mode="values",
                )

                for event in events:
                    print(event["messages"][-1])

                shortlisted_candidates.append(row)  # Collect shortlisted candidates

            else:
                rejection_query = f'Draft an email to {email_id} informing them that they have not been shortlisted for the interview. Politely inform them that they have not been selected for the interview at Roman Solutions Company.'

                events = agent_executor.stream(
                    {"messages": [("user", rejection_query)]},
                    stream_mode="values",
                )

                for event in events:
                    print(event["messages"][-1])

                rejected_candidates.append(row)  # Collect rejected candidates

    return shortlisted_candidates, rejected_candidates  # Return both lists

def search_mails(query):
    try:
        agent = initialize_agent(
            tools=toolkit.get_tools(),
            llm=llm,
            agent=AgentType.STRUCTURED_CHAT_ZERO_SHOT_REACT_DESCRIPTION,
        )
        res = agent.run(f"Search for mail related to {query}. I would like to see the full content of the mail.")
        return res
    except Exception as e:
        return e
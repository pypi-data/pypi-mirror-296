import os
import json
import requests

import instructor
from pydantic import BaseModel, Field
from openai import OpenAI
from anthropic import Anthropic
from datetime import datetime

openai_api_key = os.environ["OPENAI_API_KEY"]
# anthropic_api_key = os.environ['ANTHROPIC_API_KEY']


# Define your desired output structure
class TenderInfo(BaseModel):
    tender_title: str = Field(description="The title of the tender document")
    tender_value: int = Field(description="The value/amount of the tender")
    tender_industry: str = Field(
        description="The industry in which the tender operates. If there are multiple industries, pick the most prominent one."
    )
    # project_start_date: str = Field(description="The date when the project can start.")
    deadline: datetime = Field(
        description="The deadline for submitting an application to the tender"
    )
    company_posting_tender: str = Field(
        description="The name of the company which posted the tender"
    )

    """contract_name: str = Field(description="The title for the contract")
    contract_date: datetime = Field(description="The date when the contract was signed or drafted")
    signatories: list = Field(description="Details of everyone who signed the contract")
    term: str = Field(description="The terms of the contract")
    quantity: int = Field(description="The quantity agreed to be transacted")
    fee_information: str = Field(description="The fees agreed upon")
    description_of_specifications: str = Field(description="Descriptions of specifications")
    """


def instructor_openai(TenderInfo, parsed_doc, retries=5):
    """Uses Instructor with OpenAI to extract small details in a structured format, from a huge document."""
    try:
        client = instructor.from_openai(OpenAI(api_key=openai_api_key))

        # Extract structured data from natural language
        doc_info = client.chat.completions.create(
            model="gpt-4-turbo",
            response_model=TenderInfo,
            messages=[{"role": "user", "content": parsed_doc}],
        )
        print("gpt-4-turbo result\n", doc_info, "\n")
        return doc_info
    except Exception as e:
        print("ERROR in instructor", e)
        if retries > 0:
            return instructor_openai(
                TenderInfo=TenderInfo, parsed_doc=parsed_doc, retries=retries - 1
            )
        else:
            return None


def instructor_anthropic(TenderInfo, parsed_doc):
    """Uses Instructor with Claude to extract small details in a structured format, from a huge document."""
    client = instructor.from_anthropic(Anthropic(api_key=anthropic_api_key))
    doc_info = client.messages.create(
        model="claude-3-opus-20240229",
        max_tokens=1024,
        messages=[{"role": "user", "content": parsed_doc}],
        response_model=TenderInfo,
    )
    print("claude3 result\n", doc_info, "\n")
    return doc_info

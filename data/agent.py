from typing import List, Literal
from pydantic import BaseModel, Field
from agents import Agent

# Minimal, clear schema for generated samples
class EmailExample(BaseModel):
    email: str = Field(..., description="The generated email body.")
    label: Literal["action_request", "information", "complaint", "urgent", "spam"] = Field(..., description="Email classification label.")

class BatchOutput(BaseModel):
    emails: List[EmailExample] = Field(..., description="List of generated emails.")

# Agent configured to produce balanced, original English emails
generator_agent = Agent(
    name="email_generator",
    model="gpt-4.1",
    instructions=(
        "You generate datasets to train an email classification model.\n"
        "Input provides the batch size as 'BATCH'.\n\n"
        "Produce realistic and ORIGINAL work-related emails in English only.\n"
        "Each item MUST include:\n"
        "- email: the email text\n"
        "- label: one of action_request | information | complaint | urgent | spam\n\n"
        "Requirements:\n"
        "- Language MUST be English.\n"
        "- No duplicates, avoid repeating sentences and structures.\n"
        "- Vary tone, length, context, formality, minor typos, etc.\n"
        "- Ensure each example is coherent and distinct.\n"
        "- Reflect real workplace scenarios.\n"
        "- Balance labels: generate BATCH/num_labels per label.\n\n"
        "Generate EXACTLY 'BATCH' items per call."
    ),
    output_type=BatchOutput,
)

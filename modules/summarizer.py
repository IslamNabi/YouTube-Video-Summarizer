import os
from openai import OpenAI
from typing import Optional, Union
from dotenv import load_dotenv

load_dotenv()
client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

MODELS = {
    "GPT-4o": "gpt-4o",
    "GPT-4-turbo": "gpt-4-turbo-preview",
    "GPT-3.5-turbo": "gpt-3.5-turbo"
}

def generate_summary(transcript: str, model: str = "gpt-4o") -> str:
    """Generate summary using OpenAI's API"""
    # Set conservative length limits based on model
    max_length = {
        "gpt-4o": 100000,
        "gpt-4-turbo-preview": 100000,
        "gpt-3.5-turbo": 30000
    }.get(model, 30000)
    
    # Ensure transcript is within limits
    processed_text = transcript[:max_length]
    
    response = client.chat.completions.create(
        model=model,
        messages=[
            {
                "role": "system",
                "content": "Create a concise YouTube video summary with:\n"
                          "1. Main topic (1 sentence)\n"
                          "2. 3-5 key bullet points\n"
                          "3. Key takeaways"
            },
            {
                "role": "user",
                "content": f"Transcript:\n{processed_text}"
            }
        ],
        temperature=0.3,
        max_tokens=500,
        top_p=0.9
    )
    return response.choices[0].message.content
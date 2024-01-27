import os
from openai import OpenAI
from typing import Any, List, Dict, Union

client = OpenAI(api_key=os.environ['OPENAI_API_KEY'])

def extract_content_from_gpt_response(function):
    def wrapper(*args, **kwargs):
        response_body = function(*args, **kwargs)
        try:
            return response_body.choices[0].message.content
        except AttributeError:
            return None
    return wrapper

@extract_content_from_gpt_response
def send_request_to_gpt(
        role_preprompt: str, 
        prompt: str,
        context: Union[str, Dict[str, str]],  
        stream: bool = False
        ) -> str:
    
    if isinstance(context, str):
        context = [{"role": "user", "content": context}]

    response = client.chat.completions.create(
        model="gpt-4-1106-preview",
        messages=[
            {
                "role": "system",
                "content": role_preprompt,
            },
            *context,
            {
                "role": "user",
                "content": prompt,
            },
        ],
        stream=stream,
    )

    return response
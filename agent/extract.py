import os
import json
import random
import time

from dotenv import load_dotenv
from openai import OpenAI

load_dotenv()

client = OpenAI(
    base_url="https://openrouter.ai/api/v1",
    api_key=os.getenv("OPENROUTER_API_KEY"),
)

MODEL = "openrouter/free"


def extract_information(app_name, urls):

    documentation = ""

    for i, url in enumerate(urls, start=1):
        documentation += f"""
Documentation {i}
{url}

"""

    prompt = f"""
You are an API Research Agent.

Research ONLY using the official documentation URLs below.

Application:
{app_name}

Official Documentation:
{documentation}

Return ONLY valid JSON.

Schema:

{{
    "category":"",
    "description":"",
    "authentication":"",
    "self_serve":"",
    "api_surface":"",
    "mcp":"",
    "buildability":"",
    "blocker":"",
    "evidence":""
}}

Rules

Category:
CRM
Support
Messaging
Marketing
Commerce
Finance
Developer Platform
Infrastructure
AI
Productivity
Database
Other

Description:
Maximum 20 words.

Authentication:
OAuth2
API Key
Bearer Token
Basic
Session Cookie
Unknown

Self Serve:
Yes
No
Partial

API Surface:
REST
GraphQL
REST + GraphQL
SOAP
REST + SOAP
Other

MCP:
Yes
No
Unknown

Buildability:
High
Medium
Low

Blocker:
None
Paid plan required
Partner approval
Enterprise only
No public API

Evidence:
Return ONE URL from the documentation list.

If unsure return Unknown.

Return ONLY valid JSON.
"""

    MAX_RETRIES = 5

    for attempt in range(MAX_RETRIES):

        try:

            print("=" * 60)
            print("MODEL:", MODEL)
            print("=" * 60)

            response = client.chat.completions.create(
                model=MODEL,
                messages=[
                    {
                        "role": "system",
                        "content": "You are a precise API research assistant. Return ONLY valid JSON."
                    },
                    {
                        "role": "user",
                        "content": prompt
                    }
                ],
                temperature=0,
                timeout=60
            )

            output = response.choices[0].message.content.strip()

            if output.startswith("```json"):
                output = output.replace("```json", "").replace("```", "").strip()

            elif output.startswith("```"):
                output = output.replace("```", "").strip()

            return json.loads(output)

        except Exception as e:

            error = str(e)

            print(f"[{app_name}] Retry {attempt + 1}/{MAX_RETRIES}")
            print(error)

            # Timeout
            if "timed out" in error.lower():

                return {
                    "category": "Unknown",
                    "description": "Timeout",
                    "authentication": "Unknown",
                    "self_serve": "Unknown",
                    "api_surface": "Unknown",
                    "mcp": "Unknown",
                    "buildability": "Low",
                    "blocker": "Timeout",
                    "evidence": urls[0]
                }

            # Invalid model
            if (
                "400" in error
                or "404" in error
                or "not a valid model id" in error.lower()
                or "unavailable for free" in error.lower()
            ):
                raise

            wait = (2 ** attempt) + random.randint(1, 5)

            print(f"Waiting {wait} seconds...\n")

            time.sleep(wait)

    return {
        "category": "Unknown",
        "description": "Extraction Failed",
        "authentication": "Unknown",
        "self_serve": "Unknown",
        "api_surface": "Unknown",
        "mcp": "Unknown",
        "buildability": "Low",
        "blocker": "LLM Error",
        "evidence": urls[0]
    }
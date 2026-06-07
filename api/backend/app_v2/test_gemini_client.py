"""
test_gemini_client.py

Purpose:
---------
Validate Gemini connectivity and model
configuration.

Usage:
------
python backend/app_v2/test_gemini_client.py
"""

from gemini_client import GeminiClient


client = GeminiClient()

response = client.generate(
    """
Return exactly:

HELLO
"""
)

print("\n==============================")
print("GEMINI RESPONSE")
print("==============================")
print(response)

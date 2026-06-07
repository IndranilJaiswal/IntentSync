"""
gemini_client.py

Purpose:
---------
Reusable Gemini client for AI Assurance Platform.

Responsibilities:
------------------
- Gemini authentication
- Prompt execution
- Retry handling
- Development fallback mode

Consumers:
----------
claim_discovery_agent.py

Future:
-------
remediation_agent.py
explanation_agent.py

Author:
-------
Indranil Jaiswal
AI Assurance Platform
"""

import os
import time

from dotenv import load_dotenv
from google import genai

load_dotenv()


class GeminiClient:
    """
    Wrapper around Gemini API.

    Provides:
    - Retry handling
    - Configurable model selection
    - Optional fallback mode
    """

    def __init__(self):

        api_key = os.getenv("GEMINI_API_KEY")

        if not api_key:
            raise ValueError(
                "GEMINI_API_KEY not configured"
            )

        self.client = genai.Client(
            api_key=api_key
        )

        self.model = os.getenv(
            "GEMINI_MODEL",
            "gemini-3.1-flash-lite"
        )

    def generate(
        self,
        prompt: str,
        fallback_response: str | None = None,
    ) -> str:
        """
        Execute a Gemini prompt.

        Parameters
        ----------
        prompt:
            Prompt sent to Gemini.

        fallback_response:
            Returned if Gemini is unavailable.
        """

        for attempt in range(3):

            try:

                response = self.client.models.generate_content(
                    model=self.model,
                    contents=prompt,
                )

                return response.text

            except Exception as error:

                print(
                    f"Gemini attempt "
                    f"{attempt + 1}/3 failed: "
                    f"{error}"
                )

                # Invalid model should fail immediately
                if "404" in str(error):
                    raise RuntimeError(
                        f"Configured model "
                        f"'{self.model}' does not exist."
                    )

                time.sleep(5)

        if fallback_response:

            print(
                "Gemini unavailable. "
                "Using fallback response."
            )

            return fallback_response

        raise RuntimeError(
            "Gemini unavailable after retries."
        )

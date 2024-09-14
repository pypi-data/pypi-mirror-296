# geminipro1.py
from .google import Google
from langchain_google_vertexai import ChatVertexAI, HarmBlockThreshold, HarmCategory

class GeminiPro1(Google):
    name = "gemini_pro_1"
    model = "gemini-1.0-pro-002"  # Override class variable

    def __init__(self, temperature=0.2, max_tokens=8192, **model_kwargs):
        super().__init__(**model_kwargs)

        self.temperature=temperature
        self.max_tokens=max_tokens

        safety_settings={
            # https://readthedocs.org/projects/google-auth/downloads/pdf/latest/
            # https://ai.google.dev/docs/safety_setting_gemini
            # Not Present in Gemini
            #HarmCategory.HARM_CATEGORY_DEROGATORY: HarmBlockThreshold.BLOCK_NONE,
            #HarmCategory.HARM_CATEGORY_TOXICITY: HarmBlockThreshold.BLOCK_NONE,
            #HarmCategory.HARM_CATEGORY_VIOLENCE: HarmBlockThreshold.BLOCK_NONE,
            #HarmCategory.HARM_CATEGORY_SEXUAL: HarmBlockThreshold.BLOCK_NONE,
            #HarmCategory.HARM_CATEGORY_MEDICAL: HarmBlockThreshold.BLOCK_NONE,
            #HarmCategory.HARM_CATEGORY_DANGEROUS: HarmBlockThreshold.BLOCK_NONE,
            # Everything bellow present in Gemini
            HarmCategory.HARM_CATEGORY_UNSPECIFIED: HarmBlockThreshold.BLOCK_NONE,
            HarmCategory.HARM_CATEGORY_HARASSMENT: HarmBlockThreshold.BLOCK_NONE,
            HarmCategory.HARM_CATEGORY_HATE_SPEECH: HarmBlockThreshold.BLOCK_NONE,
            HarmCategory.HARM_CATEGORY_SEXUALLY_EXPLICIT: HarmBlockThreshold.BLOCK_NONE,
            HarmCategory.HARM_CATEGORY_DANGEROUS_CONTENT: HarmBlockThreshold.BLOCK_NONE
        }

        self.llm.safety_settings = safety_settings

        # Override AUTHENTICATION per Model
        try:
            self.auth(self.__class__.name.lower())
        except Exception as e:
            print(f"Error during authentication: {e}")

        try:
            self.updateLLM()
        except Exception as e:
            print(f"Error updating LLM in GeminiPro1: {e}")


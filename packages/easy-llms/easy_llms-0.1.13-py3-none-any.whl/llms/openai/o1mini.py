# o1mini.py
from .openai import OpenAI
from langchain_core.prompts import PromptTemplate

class o1Mini(OpenAI):
    name = "o1_mini"
    model = "o1-mini"  # Override class variable

    # NOTE: This model currently ONLY supports a temperature of "1" (as an int)
    def __init__(self, temperature=1, max_tokens=4096, **model_kwargs):
        super().__init__(**model_kwargs)
        self.temperature = temperature
        self.max_completion_tokens = max_tokens

        # Override - Cohere Command R requires a different input template
        try:
            system_message = "You are a helpful assistant. Answer all questions to the best of your ability.\n{messages}"
            self.prompt_template = PromptTemplate(
                input_variables=["messages"],
                template=system_message
            )
        except Exception as e:
            print(f"Error initializing prompt template: {e}")
            sys.exit(1)

        # Override AUTHENTICATION per Model
        try:
            self.auth(self.__class__.name.lower())
        except Exception as e:
            print(f"Error during authentication: {e}")


        try:
            self.updateLLM()
        except Exception as e:
            print(f"Error updating LLM in {self.__class__.__name__}: {e}")


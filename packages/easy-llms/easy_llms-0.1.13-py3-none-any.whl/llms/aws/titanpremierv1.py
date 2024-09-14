# titanlitev1.py
from .aws import AWS

class TitanPremierV1(AWS):
    name = "titan_premier_v1"
    model = "amazon.titan-text-premier-v1:0"  # Override class variable

    def __init__(self, temperature=0.2, max_tokens=3072, **model_kwargs):
        super().__init__(**model_kwargs)

        self.model_kwargs = {
            "temperature": temperature,
            "maxTokenCount": max_tokens,
            **model_kwargs
        }

        # Override AUTHENTICATION - needed due to limited specific Region rollout
        try:
            self.auth(self.__class__.name.lower())
        except Exception as e:
            print(f"Error during authentication: {e}")

        try:
            self.updateLLM()
        except Exception as e:
            print(f"Error updating LLM in {self.__class__.__name__}: {e}")


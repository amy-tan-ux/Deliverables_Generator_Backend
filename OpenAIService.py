from openai import AzureOpenAI
from config import Config
Config = Config()
Temperature= 0.7
Max_tokens= 4096
Top_p= 0.95

class OpenAIService:

    def __init__(self):
        self.client = AzureOpenAI(
            api_key=Config.get_secret("AZURE_OPENAI_KEY"),
            azure_endpoint=Config.get_secret("AZURE_OPENAI_ENDPOINT"),
            api_version="2025-01-01-preview"
    )
    
    def get_response(self, prompt: str, system_message: str = None, deployment_name: str = None) -> str:
        """Generate deliverable from a single prompt string."""
        sys_msg = system_message or "You are an expert proposal generator for consulting and advisory services."
        deployment = deployment_name or Config.get_secret("AZURE_OPENAI_DEPLOYMENT")
        try:
            response = self.client.chat.completions.create(
                model=deployment,
                messages=[
                    {"role": "system", "content": sys_msg},
                    {"role": "user", "content": prompt}
                ],
                temperature=Temperature,
                max_tokens=Max_tokens,
                top_p=Top_p
            )
            return response.choices[0].message.content
        except Exception as e:
            return f"Error generating content: {e}"
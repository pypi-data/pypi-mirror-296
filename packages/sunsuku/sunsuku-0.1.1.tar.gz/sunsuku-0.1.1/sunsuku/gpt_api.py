from typing import Any, Dict
import openai
from .base import BaseAIModel

class GPTAPI(BaseAIModel):

    ALLOWED_MODELS = ['gpt-4o', 'gpt-4o-mini']

    @property
    def client(self):
        return openai.OpenAI(api_key=self.api_key)
    
    def generate_text(self, prompt: str) -> str:
        self.add_message('user', prompt)
        completion = self.client.chat.completions.create(
            model = self.model_name,
            messages=self.message_history
        )
        assistant_message = completion.choices[0].message.content
        self.add_message(completion.choices[0].message.role, assistant_message)
        return assistant_message

    def _format_message(self, role: str, content: str) -> Dict[str, Any]:
        return {'role': role, 'content': content}


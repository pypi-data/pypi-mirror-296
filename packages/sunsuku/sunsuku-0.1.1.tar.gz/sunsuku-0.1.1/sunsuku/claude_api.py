from typing import Any, Dict
import anthropic
from .base import BaseAIModel

class ClaudeAPI(BaseAIModel):

    ALLOWED_MODELS = ["claude-3-5-sonnet-20240620", 'claude-3-haiku-20240307']


    @property
    def client(self):
        return anthropic.Anthropic(api_key=self.api_key)
    
    def generate_text(self, prompt: str) -> str:
        self.add_message('user', prompt)
        completion = self.client.messages.create(
            model=self.model_name,
            messages=self.message_history,
            max_tokens=self.max_tokens
        )
        assistant_message = completion.content[0].text
        self.add_message(completion.role, assistant_message)
        return assistant_message
    

    def _format_message(self, role: str, content: str) -> Dict[str, Any]:
        return {'role': role, 'content': content}

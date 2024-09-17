from typing import Any, Dict
import google.generativeai as genai
from .base import BaseAIModel

class GeminiAPI(BaseAIModel):

    ALLOWED_MODELS = ['gemini-1.5-pro', 'gemini-1.5-flash']

    def __init__(self, api_key: str, model_name: str, system_prompt: str = '', max_tokens: int=1024, temperature: float=0):
        super().__init__(api_key, model_name, system_prompt, max_tokens=max_tokens, temperature=temperature)

    
    @property
    def client(self):
        genai.configure(api_key=self.api_key)
        if self.system_prompt:
            return genai.GenerativeModel(model_name=self.model_name, system_instruction=self.system_prompt)
        else:
            return genai.GenerativeModel(model_name=self.model_name)
    

    def generate_text(self, prompt: str) -> str:
        generation_config = genai.types.GenerationConfig(
            max_output_tokens=self.max_tokens,
            temperature=self.temperature
        )
        self.add_message('user', prompt)
        completion = self.client.generate_content(
            contents=self.message_history,
            generation_config=generation_config
        )
        assistant_message = completion.candidates[0].content.parts[0].text
        self.add_message(completion.candidates[0].content.role, assistant_message)
        return assistant_message
    

    def _format_message(self, role: str, content: str) -> Dict[str, Any]:
        return {'role': role, 'parts': content}

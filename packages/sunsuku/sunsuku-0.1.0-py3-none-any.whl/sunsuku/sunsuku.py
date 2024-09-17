from typing import Dict
from .base import BaseAIModel
from .gpt_api import GPTAPI
from .claude_api import ClaudeAPI
from .gemini_api import GeminiAPI
from .exceptions import InvalidProviderError

class Sunsuku:
    
    def __init__(self):
        self.models: Dict[str, BaseAIModel] = {}
    

    def add_model(self, provider: str, api_key: str, model_name: str, **kwargs):
        if provider == 'openai':
            self.models[provider] = GPTAPI(api_key, model_name, **kwargs)
        elif provider == 'anthropic':
            self.models[provider] = ClaudeAPI(api_key, model_name, **kwargs)
        elif provider == 'google':
            self.models[provider] = GeminiAPI(api_key, model_name, **kwargs)
        else:
            raise InvalidProviderError(f'Unsupported provider: {provider}')
    

    def generate_text(self, provider: str, prompt: str) -> str:
        if provider not in self.models:
            raise InvalidProviderError(f'Provider: {provider} not initialized.')
        return self.models[provider].generate_text(prompt)

    def set_model(self, provider: str, model_name: str):
        if provider not in self.models:
            raise InvalidProviderError(f'Provider')

    def clear_message_history(self, provider: str):
        if provider not in self.models:
            raise InvalidProviderError(f"Provider: {provider} not initialized")
        self.models[provider].clear_message_history()

    def get_allowed_models(self, provider: str) -> list:
        if provider not in self.models:
            raise InvalidProviderError(f'Provider {provider} not initialized')
        return self.models[provider].ALLOWED_MODELS
    
    def configure_mode(self, provider: str, **kwargs):
        if provider not in self.models:
            raise InvalidProviderError(f'Provider {provider} not initialized')
        self.models['provider'].configure(**kwargs)


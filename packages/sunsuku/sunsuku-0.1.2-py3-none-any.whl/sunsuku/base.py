from abc import ABC, abstractmethod
from typing import List, Dict, Any


class BaseAIModel(ABC):

    def __init__(self, api_key: str, model_name: str, system_prompt: str='', max_tokens=1024, **kwargs):
        self.api_key = api_key
        self.system_prompt = system_prompt
        self.max_tokens = max_tokens
        self.set_model(model_name)
        self.message_history :List[Dict[str, str]] = []
        if system_prompt:
            self.add_message('system', system_prompt)
        self.configure(**kwargs)

    
    @property
    @abstractmethod
    def client(self):
        pass

    @property
    @abstractmethod
    def ALLOWED_MODELS(self):
        pass

    def set_model(self, model_name: str):
        if model_name not in self.ALLOWED_MODELS:
            raise ValueError(f'Model name must be one of {self.ALLOWED_MODELS}')
        self.model_name = model_name

    
    def add_message(self, role: str, content: str):
        self.message_history.append(self._format_message(role, content))

    def clear_message_history(self):
        self.message_history.clear()

    @abstractmethod
    def generate_text(self, prompt: str) -> str:
        pass

    @abstractmethod
    def _format_message(self, role: str, content: str) -> Dict[str, Any]:
        pass

    def configure(self, **kwargs):
        for key, value in kwargs.items():
            setattr(self, key, value)

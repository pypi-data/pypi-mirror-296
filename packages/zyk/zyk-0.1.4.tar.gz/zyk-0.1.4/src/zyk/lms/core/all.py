
from src.zyk.lms.vendors.core.anthropic_api import AnthropicAPI
from src.zyk.lms.vendors.core.gemini_api import GeminiAPI
from src.zyk.lms.vendors.core.openai_api import (
    OpenAIPrivate,
)
from src.zyk.lms.vendors.supported.deepseek import DeepSeekAPI
from src.zyk.lms.vendors.supported.together import TogetherAPI


class OpenAIClient(OpenAIPrivate):
    def __init__(self):
        super().__init__()

class AnthropicClient(AnthropicAPI):
    def __init__(self):
        super().__init__()

class GeminiClient(GeminiAPI):
    def __init__(self):
        super().__init__()

class DeepSeekClient(DeepSeekAPI):
    def __init__(self):
        super().__init__()

class TogetherClient(TogetherAPI):
    def __init__(self):
        super().__init__()

    
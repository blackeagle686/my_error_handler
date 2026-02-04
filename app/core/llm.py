
import torch
from transformers import AutoModelForCausalLM, AutoTokenizer
from app.core.config import settings
import logging

logger = logging.getLogger(__name__)

class LLMService:
    _instance = None

    def __new__(cls):
        if cls._instance is None:
            cls._instance = super(LLMService, cls).__new__(cls)
            cls._instance._initialize()
        return cls._instance

    def _initialize(self):
        self.mock_mode = settings.USE_MOCK_LLM
        if self.mock_mode:
            logger.info("Initializing LLM Service in MOCK MODE")
            self.model = None
            self.tokenizer = None
        else:
            logger.info(f"Initializing LLM Service with model: {settings.MODEL_PATH}")
            try:
                self.tokenizer = AutoTokenizer.from_pretrained(settings.MODEL_PATH)
                self.model = AutoModelForCausalLM.from_pretrained(
                    settings.MODEL_PATH, 
                    torch_dtype=torch.float16, 
                    device_map="auto"
                )
            except Exception as e:
                logger.error(f"Failed to load model: {e}. Falling back to Mock Mode.")
                self.mock_mode = True

    def generate_fix(self, code: str, error_message: str, context: str = "") -> str:
        prompt = self._build_prompt(code, error_message, context)
        
        if self.mock_mode:
            return self._mock_generate(prompt)
        
        try:
            inputs = self.tokenizer(prompt, return_tensors="pt").to(self.model.device)
            outputs = self.model.generate(
                **inputs, 
                max_new_tokens=512, 
                temperature=0.2,
                top_p=0.9
            )
            response = self.tokenizer.decode(outputs[0], skip_special_tokens=True)
            # Extract only the AI's response part if necessary, depending on template
            # For simplicity returning full response or stripping prompt might be needed
            return response.replace(prompt, "").strip()
        except Exception as e:
            logger.error(f"Error generating fix: {e}")
            return f"# Error generating fix: {str(e)}"

    def chat(self, message: str, history: list) -> str:
        """
        Handle general chat interactions.
        """
        if self.mock_mode:
            return f"I am in Mock Mode. You said: {message}"
        
        # Simple chat implementation for Qwen
        messages = [{"role": "system", "content": "You are a helpful coding assistant."}]
        for msg in history:
            messages.append({"role": msg.get("role"), "content": msg.get("content")})
        messages.append({"role": "user", "content": message})
        
        text = self.tokenizer.apply_chat_template(
            messages,
            tokenize=False,
            add_generation_prompt=True
        )
        model_inputs = self.tokenizer([text], return_tensors="pt").to(self.model.device)
        
        generated_ids = self.model.generate(
            model_inputs.input_ids,
            max_new_tokens=512,
            temperature=0.4
        )
        generated_ids = [
            output_ids[len(input_ids):] for input_ids, output_ids in zip(model_inputs.input_ids, generated_ids)
        ]
        
        response = self.tokenizer.batch_decode(generated_ids, skip_special_tokens=True)[0]
        return response

    def _build_prompt(self, code: str, error: str, context: str) -> str:
        return f"""
Isolate the error in the following Python code and provide a fix.
CONTEXT: {context}
ERROR: {error}

CODE:
```python
{code}
```

FIX:
"""

    def _mock_generate(self, prompt: str) -> str:
        return """```python
# Fixed code (Mock)
def fixed_function():
    print("This is a mock fix for the error.")
    return True
```
This is a mock explanation. The error was fixed by adding a return statement."""

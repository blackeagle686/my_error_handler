
import logging
from app.core.llm import LLMService
from app.core.sandbox import Sandbox
from app.services.vector_store import VectorStore
from app.api.models import ExecuteResponse

logger = logging.getLogger(__name__)

class AnalysisService:
    def __init__(self):
        self.llm = LLMService()
        self.sandbox = Sandbox()
        self.vector_store = VectorStore()

    async def analyze_and_fix(self, code: str, error_message: str = "", context: str = "") -> dict:
        """
        Orchestrates the fix process:
        1. Search Vector DB for similar errors (optional optimization)
        2. Generate Fix via LLM
        3. Validate Fix via Sandbox
        4. Store result if successful
        """
        
        # Step 1: Generate Fix
        logger.info("Generating fix...")
        fix_response = self.llm.generate_fix(code, error_message, context)
        
        # Extract code from LLM response (simple heuristic)
        fixed_code = self._extract_code(fix_response)
        if not fixed_code:
            # Fallback if no code block found, maybe the response itself is code or failed
            fixed_code = code # No change
            logger.warning("No code block found in LLM response.")

        # Step 2: Validate in Sandbox
        logger.info("Running sandbox validation...")
        execution_result = self.sandbox.execute(fixed_code)

        # Step 3: Store if successful
        if execution_result['success']:
            logger.info("Fix successful, storing in Vector DB.")
            self.vector_store.add_record(error_message, code, fixed_code)
        else:
            logger.warning("Fix failed in sandbox.")

        return {
            "original_code": code,
            "fixed_code": fixed_code,
            "explanation": fix_response.replace(fixed_code, ""), # Basic separation
            "execution_result": execution_result
        }

    def _extract_code(self, text: str) -> str:
        if "```python" in text:
            start = text.find("```python") + 9
            end = text.find("```", start)
            return text[start:end].strip()
        elif "```" in text:
            start = text.find("```") + 3
            end = text.find("```", start)
            return text[start:end].strip()
        return ""

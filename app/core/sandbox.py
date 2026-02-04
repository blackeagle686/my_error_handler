
import subprocess
import tempfile
import os
from typing import Tuple
from app.core.security import validate_code

class Sandbox:
    def __init__(self):
        self.timeout = 5  # seconds

    def execute(self, code: str) -> dict:
        # 1. Static Analysis
        is_safe, security_errors = validate_code(code)
        if not is_safe:
            return {
                "success": False,
                "output": "",
                "error": "Security Violation:\n" + "\n".join(security_errors)
            }

        # 2. Execution in Subprocess
        # We write code to a temp file and run it
        with tempfile.NamedTemporaryFile(mode='w', suffix='.py', delete=False) as tmp_file:
            tmp_file.write(code)
            tmp_path = tmp_file.name

        try:
            # Run code
            # Note: We restrict resource usage ideally, but for basic subprocess:
            result = subprocess.run(
                ["python3", tmp_path],
                capture_output=True,
                text=True,
                timeout=self.timeout
            )
            
            output = result.stdout
            error = result.stderr
            
            if result.returncode == 0:
                return {
                    "success": True,
                    "output": output,
                    "error": None
                }
            else:
                return {
                    "success": False,
                    "output": output,
                    "error": error
                }

        except subprocess.TimeoutExpired:
            return {
                "success": False,
                "output": "",
                "error": "Execution Timed Out (Max 5s)"
            }
        except Exception as e:
            return {
                "success": False,
                "output": "",
                "error": f"Sandbox Error: {str(e)}"
            }
        finally:
            # Cleanup
            if os.path.exists(tmp_path):
                os.remove(tmp_path)

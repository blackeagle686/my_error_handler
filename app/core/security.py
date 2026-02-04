
import ast
from typing import List, Tuple

class SecurityValidator(ast.NodeVisitor):
    def __init__(self):
        self.errors = []
        self.dangerous_imports = {
            'os', 'sys', 'subprocess', 'shutil', 'socket', 'requests', 'urllib', 'http'
        }
        self.dangerous_functions = {
            'eval', 'exec', 'open', 'input', '__import__'
        }

    def visit_Import(self, node):
        for alias in node.names:
            if alias.name.split('.')[0] in self.dangerous_imports:
                self.errors.append(f"Forbidden import: {alias.name} at line {node.lineno}")
        self.generic_visit(node)

    def visit_ImportFrom(self, node):
        if node.module and node.module.split('.')[0] in self.dangerous_imports:
            self.errors.append(f"Forbidden import: {node.module} at line {node.lineno}")
        self.generic_visit(node)

    def visit_Call(self, node):
        if isinstance(node.func, ast.Name):
            if node.func.id in self.dangerous_functions:
                 self.errors.append(f"Forbidden function call: {node.func.id} at line {node.lineno}")
        self.generic_visit(node)

def validate_code(code: str) -> Tuple[bool, List[str]]:
    try:
        tree = ast.parse(code)
    except SyntaxError as e:
        return False, [f"Syntax Error: {e}"]

    validator = SecurityValidator()
    validator.visit(tree)
    
    if validator.errors:
        return False, validator.errors
    
    return True, []

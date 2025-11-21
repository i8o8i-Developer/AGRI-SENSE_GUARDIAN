"""
AgriSenseGuardian Code Execution Tool - Safe Mathematical Expression Evaluator

Provides Secure Evaluation Of Mathematical Expressions For Agricultural Calculations.
Uses AST Parsing And Whitelisting To Allow Only Safe Arithmetic Operations And
Approved Math Functions, Preventing Code Injection And System Compromise.

Designed Specifically For Agronomic Formulae Such As Irrigation Calculations,
Fertilizer Ratios, And Crop Yield Estimations Used In Agricultural Decision Support.
"""

from __future__ import annotations

import ast
import math
from typing import Any, Dict


_ALLOWED_NAMES = {k: getattr(math, k) for k in (
    "ceil", "floor", "sqrt", "log", "log10", "exp", "sin", "cos", "tan",
    "asin", "acos", "atan", "degrees", "radians", "fabs", "pow"
)}
_ALLOWED_NAMES.update({
    "pi": math.pi,
    "e": math.e
})

_ALLOWED_NODES = (
    ast.Expression, ast.BinOp, ast.UnaryOp, ast.Num, ast.Load,
    ast.Add, ast.Sub, ast.Mult, ast.Div, ast.Pow, ast.Mod,
    ast.USub, ast.UAdd, ast.Call, ast.Name, ast.Constant,
    ast.FloorDiv
)


def _validate_ast(node: ast.AST) -> None:
    """
    Validate AST Nodes Against Allowed Operations.
    
    Recursively Checks That All AST Nodes In The Expression Tree Are
    From The Whitelist Of Safe Operations, Preventing Execution Of
    Dangerous Code Constructs.
    
    Args:
        node: Root AST Node To Validate
        
    Raises:
        ValueError: If Any Disallowed AST Node Is Found
    """
    for child in ast.walk(node):
        if not isinstance(child, _ALLOWED_NODES):
            raise ValueError(
                f"Unsafe Operation Detected: {type(child).__name__}. "
                f"Only Mathematical Expressions Are Allowed."
            )


async def CodeExecutionTool(
    Expression: str,
    ToolContextInstance
) -> Dict[str, Any]:
    """
    Safely Evaluate Mathematical Expressions For Agricultural Calculations.
    
    This ADK Tool Provides Secure Evaluation Of Mathematical Formulae Used
    In Agricultural Decision Support, Such As Irrigation Calculations,
    Fertilizer Ratios, Crop Yield Estimations, And Area Measurements.
    
    Uses AST Parsing With Whitelisted Operations To Prevent Code Injection.
    Only Allows Arithmetic Operations And Approved Math Functions.
    
    Args:
        Expression: Mathematical Expression String (e.g., "sqrt(144) * 2.5")
        ToolContextInstance: ADK Tool Context For Session Management
        
    Returns:
        Dictionary With Calculation Result, Status, And Expression Details
    
    Examples:
        - "sqrt(144)" → 12.0
        - "(10 * 15) / 2" → 75.0 (Area Calculation)
        - "pi * pow(5, 2)" → 78.54 (Circle Area)
    """
    try:
        # Parse Expression Into AST
        tree = ast.parse(Expression, mode="eval")
        
        # Validate All Nodes Are Safe
        _validate_ast(tree)
        
        # Compile And Execute In Restricted Namespace
        code = compile(tree, "<string>", "eval")
        result = eval(code, {"__builtins__": {}}, _ALLOWED_NAMES)
        
        return {
            "Status": "Success",
            "Expression": Expression,
            "Result": result,
            "Type": type(result).__name__,
            "DataSource": "CodeExecutor"
        }
        
    except SyntaxError as e:
        return {
            "Status": "Error",
            "Message": f"Syntax Error: {str(e)}",
            "Expression": Expression
        }
    except ValueError as e:
        return {
            "Status": "Error",
            "Message": f"Security Error: {str(e)}",
            "Expression": Expression
        }
    except Exception as e:
        return {
            "Status": "Error",
            "Message": f"Execution Error: {str(e)}",
            "Expression": Expression
        }


__all__ = ["CodeExecutionTool"]
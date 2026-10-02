"""Input sanitization + a safe (AST-whitelisted) arithmetic evaluator."""
from __future__ import annotations

import ast
import operator
import re
import unicodedata

MAX_INPUT_LEN = 500
MAX_EXPR_LEN = 200

_CONTROL = re.compile(r"[\x00-\x08\x0b-\x1f\x7f]")
_INJECTION = re.compile(
    r"(ignore\s+(all\s+|any\s+)?(previous|prior|above)|system\s+prompt|you\s+are\s+now"
    r"|disregard|__\w+__|\bexec\b|\beval\b|\bos\.|subprocess|<\s*script|```)",
    re.IGNORECASE,
)


class InputRejected(ValueError):
    """Raised when user input fails sanitization."""


def sanitize_text(text: str) -> str:
    """Normalise and validate raw user text before it reaches the router/LLM."""
    if not isinstance(text, str):
        raise InputRejected("Input must be a string.")
    t = unicodedata.normalize("NFKC", text)
    t = _CONTROL.sub("", t)
    t = re.sub(r"\s+", " ", t).strip()
    if not t:
        raise InputRejected("Input is empty.")
    if len(t) > MAX_INPUT_LEN:
        raise InputRejected(f"Input exceeds {MAX_INPUT_LEN} characters.")
    if _INJECTION.search(t):
        raise InputRejected("Input contains disallowed patterns.")
    return t


_BIN_OPS = {
    ast.Add: operator.add, ast.Sub: operator.sub, ast.Mult: operator.mul,
    ast.Div: operator.truediv, ast.Mod: operator.mod,
    ast.FloorDiv: operator.floordiv, ast.Pow: operator.pow,
}
_UNARY_OPS = {ast.UAdd: operator.pos, ast.USub: operator.neg}


def safe_eval(expression: str) -> float:
    """Evaluate +, -, *, /, //, %, ** on numeric literals only. No names, calls or attributes."""
    expr = expression.replace("^", "**").replace(",", "").strip()
    if not expr or len(expr) > MAX_EXPR_LEN:
        raise InputRejected("Expression is empty or too long.")
    try:
        tree = ast.parse(expr, mode="eval")
    except SyntaxError as exc:
        raise InputRejected("Invalid arithmetic expression.") from exc

    def ev(node: ast.AST, depth: int = 0) -> float:
        if depth > 20:
            raise InputRejected("Expression is nested too deeply.")
        if isinstance(node, ast.Expression):
            return ev(node.body, depth + 1)
        if isinstance(node, ast.Constant) and type(node.value) in (int, float):
            return node.value
        if isinstance(node, ast.UnaryOp) and type(node.op) in _UNARY_OPS:
            return _UNARY_OPS[type(node.op)](ev(node.operand, depth + 1))
        if isinstance(node, ast.BinOp) and type(node.op) in _BIN_OPS:
            left, right = ev(node.left, depth + 1), ev(node.right, depth + 1)
            if isinstance(node.op, ast.Pow) and (abs(right) > 100 or abs(left) > 1e6):
                raise InputRejected("Exponent too large.")
            try:
                return _BIN_OPS[type(node.op)](left, right)
            except ZeroDivisionError as exc:
                raise InputRejected("Division by zero.") from exc
        raise InputRejected("Only numeric arithmetic is allowed.")

    result = ev(tree)
    if result != result or result in (float("inf"), float("-inf")):
        raise InputRejected("Result is not a finite number.")
    return result
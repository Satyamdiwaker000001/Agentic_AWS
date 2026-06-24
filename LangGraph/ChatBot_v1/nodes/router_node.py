import random
import re

def router_node(state):
    query = state["message"].lower()

    # Precedence checklist
    # 1. Debug keywords
    # 2. Coding keywords
    # 3. Physics keywords
    # 4. Math keywords
    # 5. General / Default

    debug_keywords = [
        "fix", "bug", "error", "exception", "compile", "syntax error", 
        "traceback", "debug", "crash", "issue", "broken", "correct code",
        "doesn't work", "fail", "infinite loop", "undefined", "null pointer"
    ]

    coding_keywords = [
        "python", "react", "javascript", "node", "code", "api", "function", 
        "class", "write a", "create a", "component", "typescript", "html", 
        "css", "tailwind", "framework", "json", "yaml", "sql", "database", 
        "script", "programming", "build", "cdn", "gsap"
    ]

    physics_keywords = [
        "acceleration", "velocity", "gravity", "physics", "speed", 
        "kinetic", "potential", "force", "newton", "friction", "mass", 
        "momentum", "energy", "joule", "displacement", "projectile"
    ]

    math_keywords = [
        "solve", "differentiate", "integrate", "derivative", "integral", 
        "calculus", "algebra", "math", "equation", "limit", "matrix", 
        "determinant", "vector", "trigonometry", "sin", "cos", "tan", 
        "logarithm", "sqrt", "product of", "sum of"
    ]

    def has_match(keywords, text):
        for word in keywords:
            # use word boundaries to avoid matching "sin" inside "using"
            if re.search(rf'\b{re.escape(word)}\b', text):
                return True
            # Special case for operators that might not have word boundaries
            if word in ["x^", "x²"] and word in text:
                return True
        return False

    # Evaluate matches
    if has_match(debug_keywords, query):
        return {
            "task_type": "debug",
            "confidence": round(random.uniform(0.92, 0.98), 2)
        }

    if has_match(coding_keywords, query):
        return {
            "task_type": "coding",
            "confidence": round(random.uniform(0.93, 0.99), 2)
        }

    if has_match(physics_keywords, query):
        return {
            "task_type": "physics",
            "confidence": round(random.uniform(0.91, 0.97), 2)
        }

    if has_match(math_keywords, query):
        return {
            "task_type": "math",
            "confidence": round(random.uniform(0.90, 0.96), 2)
        }

    return {
        "task_type": "general",
        "confidence": round(random.uniform(0.85, 0.90), 2)
    }
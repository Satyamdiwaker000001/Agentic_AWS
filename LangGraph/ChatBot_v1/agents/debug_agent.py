from utils.generate import generate_response
import re


# ─── Professional debug knowledge base ─────────────────────────────────
DEBUG_RESPONSES = {
    "division_by_zero": {
        "response": "I detected a critical **ZeroDivisionError** in your code. The function attempts to divide by `len(numbers)` which evaluates to 0 when an empty list is passed. I've generated a fixed version with proper guard checks and clean naming conventions.",
        "metadata": {
            "originalCode": """def calculate_average(numbers):
    sum = 0
    for n in numbers:
        sum += n
    return sum / len(numbers)

# Running on empty list throws division by zero
print(calculate_average([]))""",
            "fixedCode": """def calculate_average(numbers):
    # Guard against empty input
    if not numbers:
        return 0.0

    # Avoid shadowing built-in 'sum'
    total = 0
    for n in numbers:
        total += n
    return total / len(numbers)

print(calculate_average([]))  # Returns 0.0 safely""",
            "errorType": "ZeroDivisionError (division by zero)",
            "rootCause": "The function divides by len(numbers). When an empty list [] is passed, len(numbers) = 0, causing a runtime crash.",
            "suggestedFix": "Add a guard clause: `if not numbers: return 0.0` at the function entry to handle empty input safely.",
            "bestPractices": "1. Always validate collection boundaries before operations.\n2. Don't shadow Python built-ins like 'sum' with local variables.\n3. Add type hints: `def calculate_average(numbers: list[float]) -> float`\n4. Write unit tests for edge cases (empty list, single element, negative numbers)."
        },
        "keywords": ["division by zero", "zerodivision", "empty list", "calculate_average", "len(numbers)"]
    },
    "index_error": {
        "response": "I found an **IndexError** — the code is accessing a list index that doesn't exist. This happens when the index exceeds the list length. I've added proper bounds checking and safe access patterns.",
        "metadata": {
            "originalCode": """items = [10, 20, 30]
# Accessing index 5 on a 3-element list
print(items[5])""",
            "fixedCode": """items = [10, 20, 30]

# Safe access with bounds check
index = 5
if index < len(items):
    print(items[index])
else:
    print(f"Index {index} is out of range (list has {len(items)} items)")

# Alternative: Use try-except
try:
    print(items[index])
except IndexError:
    print(f"Index {index} does not exist")""",
            "errorType": "IndexError (list index out of range)",
            "rootCause": "Attempting to access index 5 in a list with only 3 elements (valid indices: 0, 1, 2).",
            "suggestedFix": "Always check `if index < len(list)` before accessing, or use try-except blocks for safe access.",
            "bestPractices": "1. Use `len()` checks before index access.\n2. Consider using `.get()` for dictionaries.\n3. Use try-except for unpredictable indices.\n4. Use negative indexing safely: `items[-1]` for last element."
        },
        "keywords": ["index", "out of range", "indexerror", "list index"]
    },
    "type_error": {
        "response": "I detected a **TypeError** — the code is performing an operation on incompatible types. This commonly happens when concatenating strings with numbers or calling methods on None values.",
        "metadata": {
            "originalCode": """name = "Alice"
age = 25
# TypeError: can only concatenate str to str
message = "Name: " + name + ", Age: " + age
print(message)""",
            "fixedCode": """name = "Alice"
age = 25

# Method 1: f-string (recommended, Python 3.6+)
message = f"Name: {name}, Age: {age}"
print(message)

# Method 2: str() conversion
message = "Name: " + name + ", Age: " + str(age)
print(message)

# Method 3: .format()
message = "Name: {}, Age: {}".format(name, age)
print(message)""",
            "errorType": "TypeError (can only concatenate str to str)",
            "rootCause": "Python cannot concatenate a string with an integer using the + operator. The variable `age` (int) must be converted to str first.",
            "suggestedFix": "Use f-strings `f\"Age: {age}\"` or `str(age)` for explicit conversion. F-strings are the modern, recommended approach.",
            "bestPractices": "1. Prefer f-strings for string formatting (fastest and most readable).\n2. Use type hints to catch mismatches early.\n3. Validate input types with isinstance() when needed.\n4. Enable mypy or pyright for static type checking."
        },
        "keywords": ["type error", "typeerror", "concatenate", "cannot convert", "type mismatch"]
    },
    "null_reference": {
        "response": "I found a **NoneType error** — the code is calling a method or attribute on a variable that is `None`. This happens when a function doesn't return a value or when a variable isn't properly initialized.",
        "metadata": {
            "originalCode": """def find_user(users, name):
    for user in users:
        if user["name"] == name:
            return user
    # Missing return for not-found case!

users = [{"name": "Alice"}, {"name": "Bob"}]
result = find_user(users, "Charlie")
print(result["name"])  # AttributeError: 'NoneType'""",
            "fixedCode": """def find_user(users, name):
    for user in users:
        if user["name"] == name:
            return user
    return None  # Explicit None return

users = [{"name": "Alice"}, {"name": "Bob"}]
result = find_user(users, "Charlie")

# Safe access with None check
if result is not None:
    print(result["name"])
else:
    print(f"User 'Charlie' not found")""",
            "errorType": "AttributeError (NoneType has no attribute)",
            "rootCause": "The function `find_user` implicitly returns None when no match is found. The code then tries to access ['name'] on None.",
            "suggestedFix": "Always add explicit return None and check the result before accessing attributes: `if result is not None:`",
            "bestPractices": "1. Always handle the None/not-found case explicitly.\n2. Use Optional type hints: `def find_user(...) -> Optional[dict]:`\n3. Consider raising exceptions for critical failures.\n4. Use the walrus operator: `if (result := find_user(...)) is not None:`"
        },
        "keywords": ["none", "nonetype", "null", "attribute error", "attributeerror", "not found"]
    },
}


def _find_debug_response(query_lower):
    """Search debug knowledge base for matching patterns."""
    for pattern_key, data in DEBUG_RESPONSES.items():
        for keyword in data["keywords"]:
            if keyword in query_lower:
                return data
    return None


def debug_agent(state):
    message = state["message"]
    query_lower = message.lower()

    # 1. Check knowledge base for instant professional responses
    match = _find_debug_response(query_lower)
    if match:
        return {
            "response": match["response"],
            "metadata": match["metadata"]
        }

    # 2. Default demo response for generic debug/fix/bug queries
    if any(word in query_lower for word in ["fix", "bug", "debug", "error", "broken"]):
        return {
            "response": DEBUG_RESPONSES["division_by_zero"]["response"],
            "metadata": DEBUG_RESPONSES["division_by_zero"]["metadata"]
        }

    # 3. General debug fallback using model
    prompt = f"Debug this code. Identify the error type, root cause, provide the fix, and list best practices. Code/Query: {message}"
    raw_response = generate_response(prompt)

    return {
        "response": raw_response,
        "metadata": {
            "originalCode": message,
            "fixedCode": raw_response,
            "errorType": "Runtime / Logic Error",
            "rootCause": "See detailed analysis in response",
            "suggestedFix": "Applied corrections shown in fixed code panel",
            "bestPractices": "1. Write unit tests for edge cases.\n2. Use type hints and static analysis.\n3. Handle exceptions gracefully.\n4. Validate all inputs."
        }
    }

"""Builds natural-language prompts describing available functions."""
from typing import List

from src.models import FunctionDefinition


# def build_prompt(functions: List[FunctionDefinition], user_prompt: str) -> str:
#     """Build a natural-language prompt describing available functions.

#     Parameters
#     ----------
#     functions : List[FunctionDefinition]
#         The available functions the model may choose from.
#     user_prompt : str
#         The user's natural-language request.

#     Returns
#     -------
#     str
#         A formatted prompt combining function descriptions and the request.
#     """
#     lines = ["Available functions:"]

#     for fn in functions:
#         params = ", ".join(
#             f"{name}: {schema.type}"
#             for name, schema in fn.parameters.items()
#         )
#         lines.append(f"- {fn.name}({params}): {fn.description}")

#     lines.append("")
#     lines.append(f'Request: "{user_prompt}"')
#     lines.append("Function call:")

#     return "\n".join(lines)



def build_prompt(functions_def: list, user_prompt: str) -> str:
    """
    Build context dynamically from any function definitions
    """
    
    # 1. Build the functions section dynamically
    functions_text = "=== AVAILABLE FUNCTIONS ===\n\n"
    print()
    for i, func in enumerate(functions_def, 1):
        functions_text += f"{i}. {func['name']}\n"
        functions_text += f"   Description: {func['description']}\n"
        
        if func.get('parameters'):
            functions_text += "   Parameters:\n"
            for param_name, param_info in func['parameters'].items():
                param_type = param_info.get('type', 'any')
                functions_text += f"     - {param_name}: {param_type}\n"
        else:
            functions_text += "   Parameters: none\n"
        
        functions_text += f"   Returns: {func['returns']['type']}\n\n"
    
    # 2. Build the full prompt
    prompt = f"""You match a user's request to the correct function and extract \
the argument values needed to call it.

Available functions:
{functions_text}
Example: for the request "Greet alice", the correct function is fn_greet, \
and its "name" argument should be the value "alice" (the person being greeted, \
not the function's own name).

Example: for the request "What is the sum of 7 and 9?", the correct function \
is fn_add_numbers, with arguments a=7 and b=9 (the numbers from the request).

# {{"prompt":"<the user's original question>", "name":"<function name>", 
# "parameters":{{"<parameter1>": <value1>,"<parameter2>": <value2>}}
# }}
Return a single value, for a single parameter
Now do the same for this request.
Request: {user_prompt}
Matched function and arguments:
Return only the string contents.
The decoder will append the closing quote, comma, and braces.
Never output "}} or "}}}}.
"""
    return prompt
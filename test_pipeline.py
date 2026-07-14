"""End-to-end test of the constrained generation pipeline on real data.

This is a manual verification script, not part of the graded submission.
Run with: uv run python scratch/test_pipeline.py
"""
import sys
import os
import json

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
sys.path.insert(0, "llm_sdk")

from llm_sdk import Small_LLM_Model  # noqa: E402

from src.__main__ import load_function_definitions  # noqa: E402
from src.pipeline import generate_function_call  # noqa: E402
from src.prompt_builder import build_prompt  # noqa: E402
from src.vocabulary import Vocabulary  # noqa: E402
from src.grammar import escape_json_string  # noqa: E402



def load_functions(path: str) -> list:
    """Load function definitions from JSON."""
    try:
        with open(path, "r", encoding="utf-8") as f:
            return json.load(f)
    except FileNotFoundError:
        print(f"Error: File not found: {path}")
        return []
    except json.JSONDecodeError:
        print(f"Error: Invalid JSON in file: {path}")
        return []
    except Exception as e:
        print("Error:", e)
        return []

# def escape_json_string(text):
#     """Escape quotes for JSON."""
#     return prompt.replace("\\", "\\\\").replace('"', '\\"')

def main() -> None:
    """Run the pipeline on a handful of real test prompts."""
    print("Loading model...")
    model = Small_LLM_Model()
    print("Model loaded.\n")

    vocab_path = model.get_path_to_vocab_file()
    vocab = Vocabulary(vocab_path)

    functions_for_temlp = load_function_definitions("data/input/functions_definition.json")
    functions_for_prompt = load_functions("data/input/functions_definition.json")
    
    print(f"Loaded {len(functions_for_temlp)} functions.\n")

    test_prompts = [
        # "What is the sum of 265 and 345?",
        "3.4 is greater than 5",
        # "Greet 'shrek'",
        # "Greet john",
        # 'Reverse the string "world"',
        # "What is the 'square' root of 16?",
        # "Calculate the square root of 144",
        # "Replace all numbers in \"Hello 34 I'm 233 years old\" with NUMBERS",
        # "Replace all vowels in 'Programming is fun' with asterisks",
        # "What is the sum of 2 and 3?",
        # "Substitute the word 'cat' with 'dog' in 'The cat sat on the mat with another cat'"
    ]

    for user_prompt in test_prompts:
        prompt_text = build_prompt(functions_for_prompt, user_prompt)
        user_prompt =  escape_json_string(user_prompt)

        print("=" * 60)
        print(f"PROMPT: {user_prompt}")
        print("=" * 60)

        result = generate_function_call(model, vocab, functions_for_temlp, prompt_text, user_prompt, 10)

        print("RESULT:", result)
        try:
            obj = json.loads(result)
            print("✓ Valid JSON")
        except json.JSONDecodeError as e:
            print("✗ Invalid JSON:", e)
        except Exception as error:
            print("error", error)
               


if __name__ == "__main__":
    main()


# prompt_text = escape_json_string(prompt_text)
# function_name = escape_json_string(function_name)
# string_value = escape_json_string(string_value)

# result = (
#     '{"prompt":"'
#     + prompt_text
#     + '","name":"'
#     + function_name
#     + '","parameters":{"s":"'
#     + string_value
#     + '"}}'
# )
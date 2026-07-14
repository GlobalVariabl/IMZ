"""The main constrained generation pipeline: turns one prompt into a
schema-compliant function-call JSON object."""
from typing import List

import numpy as np

from src.grammar import (
    ValueSlot,
    get_allowed_tokens_for_function_name,
    get_allowed_tokens_for_number,
    get_allowed_tokens_for_string,
    is_function_name_complete,
    mask_string_end_tokens,
    escape_json_string,
    get_allowed_tokens_for_boolean,
)
from src.models import FunctionDefinition
from src.vocabulary import Vocabulary


def mask_logits(logits: List[float], allowed_token_ids: List[int]) -> List[float]:
    """Set every logit not in allowed_token_ids to negative infinity.

    Parameters
    ----------
    logits : List[float]
        The raw logits from the model.
    allowed_token_ids : List[int]
        The token IDs that are valid choices right now.

    Returns
    -------
    List[float]
        The masked logits, safe to pass to argmax.
    """
    allowed_set = set(allowed_token_ids)
    return [
        value if index in allowed_set else float("-inf")
        for index, value in enumerate(logits)
    ]


def generate_function_call(
    model,
    vocab: Vocabulary,
    functions: List[FunctionDefinition],
    prompt_text: str,
    user_prompt: str,
    max_value_tokens: int = 30,
) -> str:
    """Run the full constrained generation pipeline for one prompt.

    Parameters
    ----------
    model : Small_LLM_Model
        The loaded language model.
    vocab : Vocabulary
        The loaded vocabulary wrapper.
    functions : List[FunctionDefinition]
        All available function definitions.
    prompt_text : str
        The natural-language prompt built for this request.
    max_value_tokens : int
        Safety cap on how many tokens a single value may take.

    Returns
    -------
    str
        The generated function-call text (decoded from token IDs).
    """

    input_ids = model.encode(prompt_text)[0].cpu().tolist()
    prompt_length = len(input_ids)

    for literal in ['{', '"', 'prompt', '"', ':', '"']:
        token_ids = model.encode(literal)[0].cpu().tolist()
        input_ids.extend(token_ids)

    
    token_ids = model.encode(user_prompt)[0].cpu().tolist()
    input_ids.extend(token_ids)

    for literal in ['"', ',', '"', 'name', '"', ':', '"']:
        token_ids = model.encode(literal)[0].cpu().tolist()
        input_ids.extend(token_ids)

    known_names = [escape_json_string(fn.name) for fn in functions]
    name_so_far = ''
    while not is_function_name_complete(name_so_far, known_names):
        logits = model.get_logits_from_input_ids(input_ids)
        allowed = get_allowed_tokens_for_function_name(name_so_far, known_names, vocab)
        masked_logits = mask_logits(logits, allowed)
        chosen_id = int(np.argmax(masked_logits))
        input_ids.append(chosen_id)
        name_so_far += vocab.id_to_token(chosen_id)

    selected_function = next(fn for fn in functions if fn.name == name_so_far)

    for literal in ['"', ',', '"', 'parameters', '"', ':', '{']:
        token_ids = model.encode(literal)[0].cpu().tolist()
        input_ids.extend(token_ids)

    param_items = list(selected_function.parameters.items())
    for index, (param_name, param_schema) in enumerate(param_items):
        for literal in ['"', escape_json_string(param_name), '"', ':']:
            token_ids = model.encode(literal)[0].cpu().tolist()
            input_ids.extend(token_ids)
            # print(f"index :{index}, param_name:{param_name}")

        is_last_param = index == len(param_items) - 1
        next_literal = '}' if is_last_param else ','
        # print(next_literal)
        next_token_id = model.encode(next_literal)[0].cpu().tolist()[0]

        if param_schema.type == "number":
            value_ids: List[int] = []
            for _ in range(max_value_tokens):
                logits = model.get_logits_from_input_ids(input_ids + value_ids)
                allowed = get_allowed_tokens_for_number(value_ids, next_token_id, vocab)
                masked_logits = mask_logits(logits, allowed)
                chosen_id = int(np.argmax(masked_logits))
                if chosen_id == next_token_id:
                    break
                value_ids.append(chosen_id)
            input_ids.extend(value_ids)

        elif param_schema.type == "string":
            quote_id = vocab.find_exact_token('"')
            input_ids.extend(model.encode('"')[0].cpu().tolist())
            value_ids = []
            for _ in range(max_value_tokens):
                logits = model.get_logits_from_input_ids(input_ids + value_ids)
                allowed = get_allowed_tokens_for_string(value_ids, quote_id, vocab)
                    
                   
                masked_logits = mask_logits(logits, allowed)

                chosen_id = int(np.argmax(masked_logits))
                candidate_ids = value_ids + [chosen_id]
                candidate_text = vocab.id_to_token(chosen_id)
                
                if '"' in candidate_text:
                    # Keep everything before the quote
                    prefix = candidate_text.split('"', 1)[0]

                    if prefix:
                        prefix_ids = model.encode(prefix)[0].cpu().tolist()
                        value_ids.extend(prefix_ids)

                    break
                if chosen_id == quote_id:
                    break
                value_ids.append(chosen_id)

            input_ids.extend(value_ids)

            # print("ADDING MY OWN QUOTE")

            input_ids.extend(model.encode('"')[0].tolist())

            # print(model.decode(input_ids[prompt_length:]))

        elif param_schema.type == "boolean":
            logits = model.get_logits_from_input_ids(input_ids)
            allowed = get_allowed_tokens_for_boolean(vocab)
            masked_logits = mask_logits(logits, allowed)
            chosen_id = int(np.argmax(masked_logits))
            input_ids.append(chosen_id)

        if not is_last_param:
            input_ids.extend(model.encode(',')[0].cpu().tolist())
    input_ids.extend(model.encode('}')[0].cpu().tolist())
    input_ids.extend(model.encode('}')[0].cpu().tolist())
    generated_ids = input_ids[prompt_length:]
    #print("\nmodel.decode(generated_ids): ",model.decode(generated_ids))
    return model.decode(generated_ids)

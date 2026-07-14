"""Builds the token-level template structure for a function call JSON object."""
from typing import List, Union

from src.models import FunctionDefinition
from src.vocabulary import Vocabulary


class ValueSlot:
    def __init__(self, value_type):
        self.value_type = value_type


TemplateStep = Union[str, ValueSlot]



def get_allowed_tokens_for_number(
    value_tokens_so_far: List[int],
    next_forced_token_id: int,
    vocab: Vocabulary,
) -> List[int]:
    
    text_so_far = "".join(vocab.id_to_token(tid) for tid in value_tokens_so_far)
    has_digit = any(char.isdigit() for char in text_so_far)
    has_decimal_point = "." in text_so_far

    allowed: List[int] = []

    for digit in "0123456789":
        digit_id = vocab.find_exact_token(digit)
        if digit_id is not None:
            allowed.append(digit_id)

    if text_so_far == "":
        minus_id = vocab.find_exact_token("-")
        if minus_id is not None:
            allowed.append(minus_id)

    if has_digit and not has_decimal_point:
        dot_id = vocab.find_exact_token(".")
        if dot_id is not None:
            allowed.append(dot_id)

    if has_digit:
        allowed.append(next_forced_token_id)

    return allowed

def get_allowed_tokens_for_string(
    value_tokens_so_far: List[int],
    closing_quote_token_id: int,
    vocab: Vocabulary,
) -> List[int]:
    """Determine which token IDs are valid at the current step of string generation."""
    allowed = []

    for tid in vocab.all_ids():

        token = vocab.id_to_token(tid)
        # if '"' in token:
        #     print(tid, repr(token))
        # allow only the plain quote token
        if tid == closing_quote_token_id:
            allowed.append(tid)
            continue

        # reject merged tokens beginning with "
        if token.startswith('"'):
            continue

        allowed.append(tid)

    return allowed



def get_allowed_tokens_for_function_name(
    text_so_far: str,
    known_function_names: List[str],
    vocab: Vocabulary,
) -> List[int]:
    still_possible_names = [
        name for name in known_function_names
        if name.startswith(text_so_far)
    ]

    # Step 2: for every token in the vocabulary, check if adding it keeps
    # us on a valid path toward at least one still-possible name.
    allowed_token_ids = []
    for token_id in vocab.all_ids():
        token_text = vocab.id_to_token(token_id)
        text_if_we_add_this_token = text_so_far + token_text

        is_still_valid = False
        for name in still_possible_names:
            if name.startswith(text_if_we_add_this_token):
                is_still_valid = True
                break

        if is_still_valid:
            allowed_token_ids.append(token_id)
    print("text_so_far",text_so_far)
    return allowed_token_ids


def is_function_name_complete(
    text_so_far: str,
    known_function_names: List[str],
) -> bool:
    if text_so_far not in known_function_names:
        return False

    # Second, no OTHER, different name should also start with this text
    # (otherwise we can't be sure the model isn't still mid-way through
    # typing that longer name).
    for name in known_function_names:
        is_a_different_name = (name != text_so_far)
        also_starts_the_same_way = name.startswith(text_so_far)

        if is_a_different_name and also_starts_the_same_way:
            return False

    return True



def mask_string_end_tokens(logits, vocab):
    logits = logits.copy()

    for token_id in vocab.all_ids():
        text = vocab.id_to_token(token_id)

        if text.startswith('"') or text.startswith('}'):
            logits[token_id] = -float("inf")

    return logits

def get_allowed_tokens_for_boolean(vocab):
    return [
        vocab.token_to_id("true"),
        vocab.token_to_id("false"),
    ]


def escape_json_string(s: str) -> str:
    return (
        s.replace("\\", "\\\\")
         .replace('"', '\\"')
         .replace("\n", "\\n")
         .replace("\r", "\\r")
         .replace("\t", "\\t")
    )
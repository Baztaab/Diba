def prompt_text(label: str) -> str:
    return input(f"{label}: ").strip()


def prompt_float(label: str) -> float:
    return float(prompt_text(label))


def prompt_int(label: str) -> int:
    return int(prompt_text(label))


def prompt_choice(label: str, choices, default=None) -> str:
    choice_str = "/".join(choices)
    prompt = f"{label} ({choice_str})"
    if default:
        prompt += f" [{default}]"
    return (input(prompt + ": ").strip() or default).strip()

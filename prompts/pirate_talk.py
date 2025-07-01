def get_pirate_prompt(text: str) -> str:
    template = """Transform the following text to sound like a pirate would speak. Use pirate vocabulary like 'ahoy', 'matey', 'arr', 'ye', 'me hearties', etc. Make it sound authentic but fun.

Text to transform: {text}

Pirate version:"""
    return template.format(text=text)
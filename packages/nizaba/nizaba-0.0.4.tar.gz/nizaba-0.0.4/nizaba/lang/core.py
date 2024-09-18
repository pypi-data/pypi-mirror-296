import ply.lex as lex
from dataclasses import dataclass
from typing import List, Union

@dataclass
class Token:
    original_text: str

@dataclass
class Annotation(Token):
    key: str
    value: str

@dataclass
class VariableStart(Token):
    key: str

@dataclass
class VariableEnd(Token):
    end: bool = True

@dataclass
class TextToken(Token):
    text: str

TokenType = Union[Annotation, TextToken, VariableStart, VariableEnd]

# List of token names
tokens = (
    'VARIABLE_START',
    'VARIABLE_END',
    'ANNOTATION',
    'TEXT',
    'ESCAPED_BRACE',
)

# Regular expression rules for tokens
def t_VARIABLE_START(t):
    r'\{\{\s*([a-zA-Z0-9_+.]+)\s*-\s*\*\*\*\s*\}\}'
    content = t.value[2:-2].strip()
    key, _ = map(str.strip, content.split('-', 1))
    t.value = VariableStart(key=key, original_text=t.value)
    return t

def t_VARIABLE_END(t):
    r'\{\{\s*\*\*\*\s*\}\}'
    t.value = VariableEnd(original_text=t.value)
    return t

def t_ANNOTATION(t):
    r'\{\{\s*([a-zA-Z0-9_+.]+)\s*-\s*([a-zA-Z0-9_+.]+)\s*\}\}'
    content = t.value[2:-2].strip()
    key, value = map(str.strip, content.split('-', 1))
    t.value = Annotation(key=key, value=value, original_text=t.value)
    return t

def t_ESCAPED_BRACE(t):
    r'\\[{}]'
    t.value = TextToken(text=t.value[1], original_text=t.value)
    return t

def t_TEXT(t):
    r'[^{\\]+|\\(?![{}])|{'
    t.value = TextToken(text=t.value, original_text=t.value)
    return t

# Error handling rule
def t_error(t):
    print(f"Illegal character '{t.value[0]}' at position {t.lexpos}")
    t.lexer.skip(1)

# Build the lexer
lexer = lex.lex()

def parse(text: str) -> List[TokenType]:
    lexer.input(text)
    return list(tok.value for tok in lexer)

def escape(text: str) -> str:
    """
    Escapes a string to be safely used as a single text token in our simple language.
    """
    escaped = text.replace('\\', '\\\\')  # Escape backslashes first
    escaped = escaped.replace('{', '\\{').replace('}', '\\}')  # Escape braces
    return escaped

def unescape(text: str) -> str:
    """
    Unescapes a string by reversing the escape process.
    """
    # First, unescape escaped braces
    text = text.replace('\\{', '{').replace('\\}', '}')
    # Then unescape escaped backslashes
    text = text.replace('\\\\', '\\')
    return text

def parse_and_build_specification(text: str):
    tokens = parse(text)
    RawText = ''
    Annotations = {}
    Variables = {}
    variable_stack = []

    for token in tokens:
        if isinstance(token, TextToken):
            RawText += token.text
            if variable_stack:
                variable_stack[-1]['content'] += token.original_text
        elif isinstance(token, Annotation):
            Annotations[token.key] = token.value
            if variable_stack:
                variable_stack[-1]['content'] += token.original_text
        elif isinstance(token, VariableStart):
            if variable_stack:
                raise ValueError('Nested variables are not allowed')
            variable_stack.append({'key': token.key, 'content': ''})
        elif isinstance(token, VariableEnd):
            if not variable_stack:
                raise ValueError('VariableEnd without matching VariableStart')
            variable = variable_stack.pop()
            # Unescape the variable content before adding to Variables
            variable_value = unescape(variable['content'])
            Variables[variable['key']] = variable_value
        else:
            # Should not happen
            pass

    if variable_stack:
        raise ValueError('Unclosed variable sections')

    Specification = {
        'Annotations': Annotations,
        'Variables': Variables
    }

    return RawText, Specification
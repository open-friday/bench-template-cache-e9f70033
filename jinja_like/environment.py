from .compiler import compile_template
from .lexer import tokenize


class Environment:
    def __init__(self, autoescape=False, cache_size=128):
        self.autoescape = autoescape
        self.cache_size = cache_size

    def render(self, source, context=None, filters=None):
        context = context or {}
        tokens = tokenize(source)
        template = compile_template(tokens, autoescape=self.autoescape)
        return template(context, filters=filters)

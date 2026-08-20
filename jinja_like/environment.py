from collections import OrderedDict

from .compiler import compile_template
from .lexer import tokenize


class Environment:
    def __init__(self, autoescape=False, cache_size=128):
        self.autoescape = autoescape
        self.cache_size = cache_size
        self._template_cache = OrderedDict()

    def render(self, source, context=None, filters=None):
        context = context or {}
        if self.cache_size <= 0:
            tokens = tokenize(source)
            template = compile_template(tokens, autoescape=self.autoescape)
            return template(context, filters=filters)

        key = (source, self.autoescape)
        template = self._template_cache.get(key)
        if template is None:
            tokens = tokenize(source)
            template = compile_template(tokens, autoescape=self.autoescape)
            self._template_cache[key] = template
            while len(self._template_cache) > self.cache_size:
                self._template_cache.popitem(last=False)
        else:
            self._template_cache.move_to_end(key)

        return template(context, filters=filters)

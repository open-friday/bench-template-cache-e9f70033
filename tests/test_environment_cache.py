import unittest

from jinja_like import compiler, lexer
from jinja_like.environment import Environment


class EnvironmentCacheTests(unittest.TestCase):
    def setUp(self):
        lexer.reset_stats()
        compiler.reset_stats()

    def test_repeated_source_is_compiled_once(self):
        environment = Environment()

        self.assertEqual(environment.render("Hello {{ name }}", {"name": "Ada"}), "Hello Ada")
        self.assertEqual(environment.render("Hello {{ name }}", {"name": "Grace"}), "Hello Grace")

        self.assertEqual(lexer.get_stats()["tokenize_calls"], 1)
        self.assertEqual(compiler.get_stats()["compile_calls"], 1)

    def test_cached_template_uses_each_calls_context(self):
        environment = Environment()

        first = environment.render("{{ value }}", {"value": "first"})
        second = environment.render("{{ value }}", {"value": "second"})

        self.assertEqual((first, second), ("first", "second"))
        self.assertEqual(compiler.get_stats()["compile_calls"], 1)

    def test_cached_template_uses_each_calls_filters(self):
        environment = Environment()
        source = "{% upper value %}"

        default = environment.render(source, {"value": "hello"})
        custom = environment.render(
            source,
            {"value": "hello"},
            filters={"upper": lambda value: "custom:" + value},
        )

        self.assertEqual((default, custom), ("HELLO", "custom:hello"))
        self.assertEqual(compiler.get_stats()["compile_calls"], 1)

    def test_zero_cache_size_disables_caching(self):
        environment = Environment(cache_size=0)

        environment.render("same source")
        environment.render("same source")

        self.assertEqual(lexer.get_stats()["tokenize_calls"], 2)
        self.assertEqual(compiler.get_stats()["compile_calls"], 2)

    def test_autoescape_is_part_of_the_cache_identity(self):
        environment = Environment(autoescape=False)
        source = "{{ value }}"

        plain = environment.render(source, {"value": "<tag>"})
        environment.autoescape = True
        escaped = environment.render(source, {"value": "<tag>"})

        self.assertEqual((plain, escaped), ("<tag>", "&lt;tag&gt;"))
        self.assertEqual(compiler.get_stats()["compile_calls"], 2)

    def test_cache_evicts_the_least_recently_used_template(self):
        environment = Environment(cache_size=2)

        for source in ("A", "B", "A", "C", "A", "B"):
            environment.render(source)

        self.assertEqual(compiler.get_stats()["compile_calls"], 4)

    def test_negative_cache_size_disables_caching(self):
        environment = Environment(cache_size=-1)

        environment.render("same source")
        environment.render("same source")

        self.assertEqual(lexer.get_stats()["tokenize_calls"], 2)
        self.assertEqual(compiler.get_stats()["compile_calls"], 2)

    def test_plain_text_is_unchanged(self):
        environment = Environment()

        self.assertEqual(environment.render("plain text"), "plain text")

    def test_missing_variable_renders_as_empty_text(self):
        environment = Environment()

        self.assertEqual(environment.render("before {{ missing }} after"), "before  after")

    def test_different_sources_compile_independently(self):
        environment = Environment()

        environment.render("first")
        environment.render("second")
        environment.render("first")

        self.assertEqual(lexer.get_stats()["tokenize_calls"], 2)
        self.assertEqual(compiler.get_stats()["compile_calls"], 2)


if __name__ == "__main__":
    unittest.main()

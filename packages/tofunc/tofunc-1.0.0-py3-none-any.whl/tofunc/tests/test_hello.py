import functools
import unittest

from tofunc import tofunc


class TestHello(unittest.TestCase):
    def test_hello(self):
        def join(self, b="beta", c="gamma"):
            return "%s %s %s" % (self, b, c)

        class Foo: ...

        hello = functools.partial(join, c="hello")
        Foo.greet = hello
        self.assertEqual(Foo().greet("Alice"), "Alice beta hello")
        hello = tofunc(hello)
        Foo.greet = hello
        text = Foo().greet("Bob")
        self.assertTrue(text.endswith("Bob hello"))
        self.assertTrue("Foo" in text)


if __name__ == "__main__":
    unittest.main()

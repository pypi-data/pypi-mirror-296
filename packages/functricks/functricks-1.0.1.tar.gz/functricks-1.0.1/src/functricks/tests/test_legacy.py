import functools
import unittest

from functricks import *


class OverloadBar:
    def __init__(self, addon) -> None:
        self.addon = addon

    @overloadable
    def foo(self, x):
        if type(x) is int:
            return "int"

    @foo.overload("int")
    def foo(self, x):
        return x * x + self.addon

    @foo.overload()  # key=None
    def foo(self, x):
        return str(x)[::-1]


class TestOverloadable(unittest.TestCase):
    def test_overloadable(self):
        bar = OverloadBar(42)
        self.assertEqual(bar.foo(1), 43)
        self.assertEqual(bar.foo(3.14), "41.3")
        self.assertEqual(bar.foo("baz"), "zab")


class TestKeyalias(unittest.TestCase):
    def test_keyalias(self):
        @keyalias(bar=6)
        class Foo:
            def __init__(self):
                self.data = list(range(10))  # Example list with 10 elements

            def __getitem__(self, index):
                return self.data[index]

            def __setitem__(self, index, value):
                self.data[index] = value

            def __delitem__(self, index):
                del self.data[index]

        # Create an instance of Foo
        my_instance = Foo()

        # Use the alias property to access index 6
        self.assertEqual(my_instance.bar, 6)  # Get the value at index 6
        my_instance.bar = 42  # Set the value at index 6
        self.assertEqual(my_instance.bar, 42)  # Check the updated value at index 6
        del my_instance.bar  # Delete the value at index 6
        self.assertEqual(my_instance.bar, 7)  # Check the updated value at index 6


class TestTofunc(unittest.TestCase):
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

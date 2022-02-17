import ast
import sys
import textwrap

from ssort._method_requirements import get_method_requirements


def _method_requirements(source):
    source = textwrap.dedent(source)
    root = ast.parse(source)
    assert len(root.body) == 1
    node = root.body[0]
    if sys.version_info >= (3, 9):
        print(ast.dump(node, include_attributes=True, indent=2))
    else:
        print(ast.dump(node, include_attributes=True))
    return list(get_method_requirements(node))


def test_staticmethod_requirements():
    reqs = _method_requirements(
        """
        @staticmethod
        def function():
            return Class.attr
        """
    )
    assert reqs == []


def test_classmethod_requirements():
    reqs = _method_requirements(
        """
        @classmethod
        def function(cls, arg, **kwargs):
            return cls.attr + arg.argattr
        """
    )
    assert reqs == ["attr"]


def test_method_requirements():
    reqs = _method_requirements(
        """
        def function(self, something):
            return self.a + self.b - something.other
        """
    )
    assert reqs == ["a", "b"]


def test_assign_method_requirements_none():
    """
    ..code:: python

        Assign(expr* targets, expr value, string? type_comment)
    """
    reqs = _method_requirements(
        """
        def fun(self):
            a = b
        """
    )
    assert reqs == []


def test_assign_method_requirements_target():
    """
    ..code:: python

        Assign(expr* targets, expr value, string? type_comment)
    """
    reqs = _method_requirements(
        """
        def fun(self):
            self.a = b
        """
    )
    assert reqs == []


def test_assign_method_requirements_value():
    """
    ..code:: python

        Assign(expr* targets, expr value, string? type_comment)
    """
    reqs = _method_requirements(
        """
        def fun(self):
            a = self.b
        """
    )
    assert reqs == ["b"]


def test_assign_method_attribute_requirements_none():
    reqs = _method_requirements(
        """
        def fun(self):
            a.b = c
        """
    )
    assert reqs == []


def test_assign_method_attribute_requirements():
    reqs = _method_requirements(
        """
        def fun(self):
            self.a.b = c
        """
    )
    assert reqs == ["a"]


def test_assign_method_star_requirements_none():
    reqs = _method_requirements(
        """
        def fun(self):
            *a = c
        """
    )
    assert reqs == []


def test_assign_method_star_requirements():
    reqs = _method_requirements(
        """
        def fun(self):
            *self.a = c
        """
    )
    assert reqs == []


def test_assign_method_star_attribute_requirements_none():
    reqs = _method_requirements(
        """
        def fun(self):
            *a.b = c
        """
    )
    assert reqs == []


def test_assign_method_star_attribute_requirements():
    reqs = _method_requirements(
        """
        def fun(self):
            *self.a.b = c
        """
    )
    assert reqs == ["a"]


def test_assign_method_subscript_requirements_none():
    reqs = _method_requirements(
        """
        def fun(self):
            a[b] = c
        """
    )
    assert reqs == []


def test_assign_method_subscript_requirements_source():
    reqs = _method_requirements(
        """
        def fun(self):
            self.a[b] = c
        """
    )
    assert reqs == ["a"]


def test_assign_method_subscript_requirements_key():
    reqs = _method_requirements(
        """
        def fun(self):
            a[self.b] = c
        """
    )
    assert reqs == ["b"]


def test_assign_method_tuple_requirements_none():
    reqs = _method_requirements(
        """
        def fun(self):
            a, b[c], d.e, *f = g
        """
    )
    assert reqs == []


def test_assign_method_tuple_requirements():
    reqs = _method_requirements(
        """
        def fun(self):
            self.a, self.b[self.c], self.d.e, *self.f = self.g
        """
    )
    assert reqs == ["b", "c", "d", "g"]

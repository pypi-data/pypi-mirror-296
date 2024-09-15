# tests/test_example.py

from example_package import MyClass

def test_public_method():
    obj = MyClass()
    assert obj.public_method() == "Это публичный метод!"

def test_internal_method():
    obj = MyClass()
    assert obj._internal_method() == "Это внутренний метод!"

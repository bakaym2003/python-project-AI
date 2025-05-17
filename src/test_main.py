from main import greet


def test_greet_default():
    """Test the default greeting."""
    assert greet() == "Hello, World!"


def test_greet_custom_name():
    """Test greeting with a custom name."""
    assert greet("Python") == "Hello, Python!" 
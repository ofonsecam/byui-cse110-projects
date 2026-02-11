from names import make_full_name, extract_family_name, extract_given_name
import pytest

def test_make_full_name():
    """Verify that make_full_name returns the correct formatted string."""
    assert make_full_name("John", "Smith") == "Smith; John"
    assert make_full_name("Li", "Wu") == "Wu; Li"
    assert make_full_name("Alice", "") == "; Alice"
    assert make_full_name("Mary-Jane", "Smith-Jones") == "Smith-Jones; Mary-Jane"

def test_extract_family_name():
    """Verify that extract_family_name extracts the family name correctly."""
    assert extract_family_name("Smith; John") == "Smith"
    assert extract_family_name("Wu; Li") == "Wu"
    assert extract_family_name("; Alice") == ""
    assert extract_family_name("Smith-Jones; Mary-Jane") == "Smith-Jones"

def test_extract_given_name():
    """Verify that extract_given_name extracts the given name correctly."""
    assert extract_given_name("Smith; John") == "John"
    assert extract_given_name("Wu; Li") == "Li"
    assert extract_given_name("; Alice") == "Alice"
    assert extract_given_name("Smith-Jones; Mary-Jane") == "Mary-Jane"  

# Main entry point to run the tests with pytest
if __name__ == "__main__":
    pytest.main(["-v", "--tb=line", "-rN", __file__])
from helpers.date_utils import auto_date_parse
import pytest

def test_date_parse_with_time():
    """ Tests if the date parseing helper function can parse an html date with time included"""
    test_date = auto_date_parse("2025-06-11T09:45") # Should be June 11th 2025 at 9:45 AM
    assert test_date.minute == 45
    assert test_date.hour == 9
    assert test_date.day == 11
    assert test_date.month == 6
    assert test_date.year == 2025

def test_date_parse_without_time():
    """ Tests if the date aprsing helper function can pare an html date excluding a timestamp"""
    test_date = auto_date_parse("2027-11-15") # Should be novemeber 15th 2027 at 11:59 PM
    assert test_date.minute == 59
    assert test_date.hour == 23
    assert test_date.day == 15
    assert test_date.month == 11
    assert test_date.year == 2027

def test_date_parse_no_string_given():
    """Makes sure a value error is raised if a string is not given"""
    with pytest.raises(ValueError):
        test_date = auto_date_parse(12345)
    

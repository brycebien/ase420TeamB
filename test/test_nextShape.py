import pytest
import sys
sys.path.append('src')
from next_shape import NextShape

def test_determine_next_shape_initialization():
    determine_next_instance = NextShape()
    assert determine_next_instance.next_shape == None
    assert determine_next_instance.current_shape == None
    assert determine_next_instance.has_been_set == False

def determine_next_first_call():
    determine_next_instance = NextShape()
    res = determine_next_instance.determineNext()
    assert determine_next_instance.current_shape == res
    assert determine_next_instance.next_shape is not None
    assert determine_next_instance.has_been_set is True

def test_determine_next_subsequent_calls():
    determine_next_instance = NextShape()
    determine_next_instance.determineNext()  # First call
    current_shape_before = determine_next_instance.current_shape
    result = determine_next_instance.determineNext()  # Subsequent call
    assert determine_next_instance.current_shape == result
    assert determine_next_instance.next_shape is not None
    assert determine_next_instance.current_shape != current_shape_before
    assert determine_next_instance.has_been_set is True
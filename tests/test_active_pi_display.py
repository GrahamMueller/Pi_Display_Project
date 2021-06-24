import pytest
from active_display.active_pi_display import *


@pytest.mark.parametrize("test_message,test_chars,answer", [("", 1, 1), ("a a", 1, 2), ("aa", 1, 1), ("okay simple test", 6, 3)])
def test_word_wrap_string(test_message, test_chars, answer):
    message_list = word_wrap_string(test_message, test_chars)
    assert (len(message_list) == answer)
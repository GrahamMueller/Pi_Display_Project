import pytest
from active_display.active_pi_display import *

"""Test it can be created"""


def test_logger_display_init():
    pygame.font.init()
    try:
        logger_display = LoggerDisplay()
    except Exception as e:
        pytest.fail("Failed to initialize logger display")
        raise e


"""Test adding messages works"""


def test_add_message():
    pygame.font.init()
    logger_display = LoggerDisplay()
    print("logger_display_dim", logger_display.font_dimension)
    assert len(logger_display.message_list) == 0
    logger_display.add_message("a")
    assert len(logger_display.message_list) > 0


"""Test message limit in logger"""


def test_message_limit():
    pygame.font.init()
    logger_display = LoggerDisplay()

    iter_count = 0
    iter_test_limit = 1000
    last_length = -1
    # Add new lines to the logger until it begins to remove old messages.
    while last_length != len(logger_display.message_list):
        # Test fails if we are allowed to keep adding endless lines to the logger.
        iter_count += 1
        assert iter_count <= iter_test_limit
        # Add new line to logger.
        last_length = len(logger_display.message_list)
        logger_display.add_message("a")

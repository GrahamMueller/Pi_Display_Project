#!/usr/bin/env python3

"""
Create main function.
Create main class?
    How would this structure look?

Can have an overlay that acts to tint the screen / add some vingette to it.
Display information to a log file or multiple for easy access.  Should be able to enter/exit.
"""
import os
import time
import pygame, sys
from pygame.locals import *

from gpiozero import CPUTemperature
from gpiozero import LoadAverage

from typing import NamedTuple


class Size(NamedTuple):
    """Simple dimension sizing"""

    width: int
    height: int


class Color3(NamedTuple):
    """Simple color, no alpha"""

    red: int
    blue: int
    green: int


c_red = Color3(255, 0, 0)
c_green = Color3(0, 0, 255)
c_blue = Color3(0, 255, 0)
c_white = Color3(255, 255, 255)
c_black = Color3(0, 0, 0)
c_background = Color3(10, 25, 5)
c_log_font = Color3(255, 255, 205)

"""
Handles the logger display window.  
The program sends messages to be displayed on the screen.
"""


class LoggerDisplay:
    """
    font_size : Font size height
    font_name : Path to font type.
    dimensions : 2D list or tuple of size of logging area
    position : 2D list or tuple of size of center of display
    """

    def __init__(
        self,
        font_size=16,
        font_name="freesansbold.ttf",
        dimensions=[100, 100],
        position=[0, 0],
    ):
        # verify inputs are correct and useable
        try:
            self.font = pygame.font.Font(font_name, font_size)
        except Exception as e:
            raise e

        self.font_dimension = Size(*self.font.size("a"))
        self.message_list = []
        self.dimensions = Size(*dimensions)
        self.position = Size(*position)

    """Adds a message to be displayed by the log display."""

    def add_message(self, input_message):
        try:
            message = str(input_message)
        except Exception as e:
            raise e

        chars_per_line = int(self.dimensions.width / self.font_dimension.width)
        lines_total = int(self.dimensions.height / self.font_dimension.height)
        print("chars per line : ", chars_per_line)
        print("lines_limit :", lines_total)

        word_wrapped_message = word_wrap_string(message, chars_per_line)

        for m in word_wrapped_message:
            self.message_list.append(m)

        while len(self.message_list) > lines_total:
            self.message_list.pop(0)

    def render_onto_surface(self):
        #Render objects onto a single surface that is provided.
        #title
        #----------
        #Logger window
        #....
        #----------


class ActivePiDisplay(object):
    log_font_size = 16

    def __init__(
        self,
        log_width_perc=0.5,
    ):
        try:
            self.fullscreen_surface = pygame.display.set_mode((0, 0), pygame.FULLSCREEN)
            pygame.mouse.set_visible(False)
            pygame.display.set_allow_screensaver(False)
            pygame.font.init()
        except:
            # Pygame does not have great errors.  If no display is present, this will just fail without an error.
            raise ActivePiDisplayFailedInit()

        fs_s = self.fullscreen_surface.get_size()
        self.fullscreen_size = Size(fs_s[0], fs_s[1])

        # Create log window.
        self.log_surface = pygame.Surface(
            ((self.fullscreen_size.width * log_width_perc), self.fullscreen_size.height)
        )
        # self.log_surface.set_center = (self.fullscreen_size.width * log_width_perc * 0.5, self.fullscreen_size.height * 0.5)
        # self.log_font = pygame.font.Font(
        #     "freesansbold.ttf", ActivePiDisplay.log_font_size
        # )

    # self.log_message_list = []

    #
    def render(self):
        # Fill background
        self.fullscreen_surface.fill(c_background)
        # Render text
        # texttest = self.log_font.render(
        #     "string string string\n stastststst", False, c_log_font
        # )

        # test
        y = 0

        # Move this into its own class.
        test_m = ["one", "two", "three", "four", "five", "six"]
        for m in self.log_message_list:
            texttest = self.log_font.render(m, False, c_log_font)
            # print("m:",y , "  - ",m)
            self.log_surface.blit(texttest, (0, y))
            y += 16
        # Colors thing
        # self.log_surface.fill(c_red)

        # Draw log background onto the window
        # self.fullscreen_surface.blit(self.log_surface, (0, 0))
        # Draw text
        # self.fullscreen_surface.blit(texttest, (0, 0))
        # textRect = text.get_rect()
        pygame.display.update()


def word_wrap_string(message, chars_per_line):
    message_list = [""]
    words = message.split()
    for word in words:
        # Success - If word can be added to current line.
        if len(message_list[-1]) + len(word) <= chars_per_line:
            message_list[-1] += word + " "
        # Mild success - Add to next line instead.
        else:
            if len(message_list[-1]) == 0:
                message_list[-1] += word + " "
            else:
                message_list.append(word + " ")
    # print("m ", message_list)
    return message_list


if __name__ == "__main__":
    active_display = ActivePiDisplay()
    active_display.add_log_message(
        "one two three four five six seven eight nine ten eleven twelve thirteen fourteen fiftheen sixteen seventeen"
    )
    i = 0
    for i in range(1, 80):
        active_display.add_log_message("dah" + str(i))
    while True:
        active_display.render()


class ActivePiDisplayFailedInit(Exception):
    """Exception raised for generic errors with pygame display modes.

    Attributes:
        message -- explanation of the error
    """

    def __init__(
        self, message="Generic error related with pygame failing to set mode."
    ):
        self.message = message
        super().__init__(self.message)


# DISPLAY_FPS = 15


# cpu_temp = CPUTemperature()


# #refresh
# x = 0
# y = 200
# while True:
#     pygame_screen.fill(COLOR_BACKGROUND)

#     x = (x+1)%800
#     pygame.draw.rect(pygame_screen, RED, (x, y, 20, 40),1, 5)
#     pygame.display.update()

#     #Print temperature
#     print("CPU TEMP : ", cpu_temp.temperature)
#     print("CPU % :" + str(int(LoadAverage().load_average*100)))
#         #Now pause to give desired frame rate. Should take into account time to render?
#     time.sleep(1.0/DISPLAY_FPS)
# #
# #font = pygame.font.Font(None, 32)
# font = pygame.font.Font('freesansbold.ttf', 8)

# # create a text surface object,
# # on which text is drawn on it.
# text = font.render('GeeksForGeeks', True, BLUE, WHITE)

# # create a rectangular object for the
# # text surface object
# textRect = text.get_rect()
# # set the center of the rectangular object.
# textRect.center = (322, 320)
# screen_size = pygame_screen.get_rect()
# print(screen_size)

# pygame_screen.fill(BLACK)
# pygame.draw.rect(pygame_screen, RED, (200, 200, 20, 40),1, 5)
# pygame_screen.blit(text, textRect)

# pygame.display.update()

# input("Press any key")

# pygame_screen.fill(BLUE)
# pygame.display.update()
# input("now blue")

# # def BoxOutline(center, size, outline_width, outline_color, inside_color):
# #     pygame.draw.rect(screen, outline_color, (center.width, center.height, size.width, size.height),0)
# #Box outline - render outline color, then background color slightly resized on top.
# #Progresive downward text - continually downshift

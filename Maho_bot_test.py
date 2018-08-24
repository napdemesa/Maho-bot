import unittest
from Maho_bot import on_message
import discord
import asyncio
import random

class TestMahoBot(unittest.TestCase):
    def test_on_message(self):
        self.assertTrue(on_message('$hello'))
        self.assertTrue(on_message('$roll'))

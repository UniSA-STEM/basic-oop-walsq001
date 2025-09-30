"""
File: Hacker.py
Description: This module outlines the Hacker class and its associated methods.
Author: Scott Quinton Walker
ID: 110441860
Username: walsq001
This is my own work as defined by the University's Academic Misconduct Policy.
"""

import random

# Variable and constant declarations

crypto_token = 0
trace_level = 0

"""
Hacker class to be imported into main program.
Each instantiation will pick a random name,
while other attributes meet specifications of the brief.
"""

class Hacker:
    def __init__(self):
        self.name = random.choice(
            ["Alan Turing", "Christopher Strachey", "Edie Windsor",
            "Jon 'Maddog' Hall", "Mary Ann Horton", "Audrey Tang",
             "Tim Cook", "Dr. Mary Gray"]
        )
        self.inventory = [
            (crypto_token + 1),
        ]
        self.trace_level = trace_level
        self._has_rig = False
        self._actions_blocked = False

    def display_details(self):
        print(f"Name: {self.name}")
        print(f"Inventory: {self.inventory}")
        print(f"Trace level: {self.trace_level}")
        print(f"Has rig: {self._has_rig}")

player1 = Hacker()
player2 = Hacker()
player1.display_details()
player2.display_details()
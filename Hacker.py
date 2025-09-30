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
max_trace_level = 5
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
        self.__blocked = False

    def __str__(self):
        return (f"Name: {self.name}\n"
                f"Inventory: {self.inventory}\n"
                f"Trace Level: {self.trace_level}")

    def __actions_blocked(self):
        return self.__blocked == True

    def trace_track(self):
        if self.trace_level >= max_trace_level:
            print("Your actions are blocked")
            return self.__actions_blocked()
        else:
            print("Your actions are not blocked")
            return None

player1 = Hacker()
player2 = Hacker()
print(player1)
player1.trace_track()
player1.trace_level = 6
player1.trace_track()


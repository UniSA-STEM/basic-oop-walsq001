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


"""
Hacker class to be imported into main program.
Each instantiation will pick a random name,
while other attributes meet specifications of the brief.
"""

class Hacker:
    def __init__(self):
        self.__name = random.choice(
            ["Alan Turing", "Christopher Strachey", "Edie Windsor",
            "Jon 'Maddog' Hall", "Mary Ann Horton", "Audrey Tang",
             "Tim Cook", "Dr. Mary Gray"]
        )
        self.__inventory = [
            (crypto_token + 1),
        ]
        self.__max_trace = 5
        self.__trace_level = 0
        self.__has_rig = False
        self.__blocked = False

    def __str__(self):
        return (f"Name: {self.__name}\n"
                f"Inventory: {self.__inventory}\n"
                f"Trace Level: {self.__trace_level}")

    def __actions_blocked(self):
        self.__blocked = True

    def get_trace_track(self):
        if self.__trace_level >= self.__max_trace:
            return self.__actions_blocked()
        else:
            return None

    def set_trace(self, trace_level):
        self.__trace_level += trace_level

player1 = Hacker()
player2 = Hacker()
print(player1)
player1.get_trace_track()
index = 0
while index < 6:
    player1.set_trace(1)
    player1.get_trace_track()
    index += 1
    print(player1)


"""
File: Hacker.py
Description: This module outlines the Hacker class and its associated methods.
Author: Scott Quinton Walker
ID: 110441860
Username: walsq001
This is my own work as defined by the University's Academic Misconduct Policy.
"""
from Asset import CryptoToken
import random

# Variable and constant declarations

MAX_TRACE = 5

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
            CryptoToken(),
        ]
        self.__trace_level = 0
        self.__has_rig = False
        self.__exposed = False

    def __str__(self):
        inventory_str = "\n".join(f"{str(item)}" for item in self.__inventory)
        return (f"Name: {self.__name}\n"
                f"Inventory: {inventory_str}\n"
                f"Trace Level: {self.__trace_level}"
                f"Exposed: {self.__exposed}")

    def __actions_blocked(self):
        self.__exposed = True

    def get_trace_track(self):
        if self.__trace_level >= MAX_TRACE:
            return self.__actions_blocked()
        else:
            return None

    def set_trace(self, trace_level):
        self.__trace_level += trace_level

    def get_rig(self, parameter):
        if parameter is not None:
            self.__has_rig = True
            if self.consume_token():
                return "You have acquired a rig!"
            else:
                return "You have tried to acquire a rig, but no token was available."
        else:
            self.__has_rig = False
            return f"You have not acquired a rig! :("

    def consume_token(self):
        for i, asset in enumerate(self.__inventory):
            if isinstance(asset, CryptoToken) and asset.quantity > 0:
                asset.quantity = -1
                if asset.quantity == 0:
                    del self.__inventory[i]
                return True
        return False


player1 = Hacker()
player2 = Hacker()
print(player1)
player1.get_trace_track()
index = 0
while index < 6:
    player1.set_trace(1)
    print(player1.get_rig(1))
    player1.get_trace_track()
    index += 1
    print(player1)


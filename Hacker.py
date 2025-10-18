"""
File: Hacker.py
Description: This module outlines the Hacker class and its associated methods.
Author: Scott Quinton Walker
ID: 110441860
Username: walsq001
This is my own work as defined by the University's Academic Misconduct Policy.
"""
from Asset import CryptoToken, DataSpike
from Rig import Rig
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
        self.rig = None
        self.__name = random.choice(
            ["Alan Turing", "Christopher Strachey", "Edie Windsor",
            "Jon 'Maddog' Hall", "Mary Ann Horton", "Audrey Tang",
             "Tim Cook", "Dr. Mary Gray"]
        )
        token = CryptoToken()
        token.quantity = 2
        self.__inventory: list = [token]
        self.__trace_level = 0
        self.__has_rig = False
        self.__exposed = False

    def __str__(self):
        inventory_str = "\n".join(f"{str(item)}" for item in self.__inventory)
        return (f"Name: {self.__name}\n"
                f"Inventory: {inventory_str}\n"
                f"Trace Level: {self.__trace_level}\n"
                f"Exposed: {self.__exposed}")

    def __actions_blocked(self):
        self.__exposed = True

    def get_trace(self):
        if self.__trace_level >= MAX_TRACE:
            return self.__actions_blocked()
        return self.__trace_level

    def set_trace(self, value):
        self.__trace_level += value

    def get_rig(self):
        if not self.__has_rig:
            if self.consume_asset(CryptoToken):
                self.__has_rig = True
                self.rig = Rig()
                print("You have acquired a rig!")
                self.__inventory.append(self.rig)
                return self.rig
            else:
                return print("You have tried to acquire a rig, but no token was available.")
        else:
            return print("You already have a rig!")

    def consume_asset(self, asset_type, amount=1):
        for asset in self.__inventory:
            if isinstance(asset, asset_type) and asset.quantity > 0:
                still_has = asset.consume(amount)
                if not still_has:
                    self.__inventory.remove(asset)
                return True
        return False

    trace = property(get_trace, set_trace)
p1 = Hacker()
rig = p1.get_rig()
if rig:
    print("Initial rig state:")
    print(rig)
    spike1 = DataSpike()
    spike1.quantity = 2
    rig.add_to_storage(spike1)

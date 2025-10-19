"""
File: Hacker.py
Description: This module outlines the Hacker class and its associated methods.
Author: Scott Quinton Walker
ID: 110441860
Username: walsq001
This is my own work as defined by the University's Academic Misconduct Policy.
"""
from Asset import CryptoToken
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
        rig_str = str(self.rig) if self.rig else "No rig"
        return (f"Name: {self.__name}\n"
                f"Inventory: {inventory_str}\n"
                f"Trace Level: {self.__trace_level}\n"
                f"{rig_str}")

    def _transfer(self, source, dest, asset_type, amount, capacity=None):
        for asset in source:
            if isinstance(asset, asset_type):
                if asset.quantity < amount:
                    print("Not enough quantity to transfer!")
                    return False

                asset.consume(amount)
                if asset.quantity == 0:
                    source.remove(asset)

                if capacity is not None:
                    current_total = self.rig.capacity
                    if current_total + amount > capacity:
                        print("Destination storage full!")
                        return False

                for d in dest:
                    if isinstance(d, asset_type):
                        d.quantity += amount
                        return True

                new_asset = asset_type()
                new_asset.quantity = amount
                dest.append(new_asset)
                return True
        print(f"No {asset_type.__name__} available to transfer.")
        return False


    def __actions_blocked(self):
        self.__exposed = True
        return self.__trace_level

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

    def store_asset(self, asset_type, amount=1):
        if not self.rig:
            print("No rig available!")
            return False
        return self._transfer(self.__inventory, self.rig.storage, asset_type, amount, capacity=self.rig.capacity)

    def get_asset(self, asset_type, amount=1):
        if not self.rig:
            print("No rig available!")
            return False
        return self._transfer(self.rig.storage, self.__inventory, asset_type, amount)

    trace = property(get_trace, set_trace)
p1 = Hacker()
rig = p1.get_rig()
while p1.trace <= MAX_TRACE:
    print(p1)
    p1.rig.generate_asset()
    p1.rig.dmg = 3
    p1.rig.repair()
    p1.trace = 1

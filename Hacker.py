"""
File: Hacker.py
Description: This module outlines the Hacker class and its associated methods.
Author: Scott Quinton Walker
ID: 110441860
Username: walsq001
This is my own work as defined by the University's Academic Misconduct Policy.
"""
from Asset import CryptoToken, DataSpike, SecurityChip
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

        # Start with two crypto tokens
        token = CryptoToken()
        token.quantity = 2
        self.__inventory = [token]

        # Trace-level tracking
        self.__trace_level = 0
        self.__exposed = False

    """
    String Magic Method
    """
    def __str__(self):
        inventory_str = "\n".join(f"{str(item)}" for item in self.__inventory)
        rig_str = str(self.rig) if self.rig else "No rig"
        return (f"Name: {self.__name}\n"
                f"Inventory: {inventory_str}\n"
                f"Trace Level: {self.__trace_level}\n"
                f"{rig_str}")

    # Trace methods
    def get_trace(self):
        return self.__trace_level

    def increase_trace(self, value=1):
        self.__trace_level += value
        if self.__trace_level >= MAX_TRACE:
            self.__exposed = True
            print("Trace maximum reached - actions blocked!")

    # Rig Acquisition
    def get_rig(self):
        if self.rig:
            print("You already have a rig!")
            return None

        if self.consume_asset(CryptoToken):
            self.rig = Rig()
            print("Rig successfully acquired!")
            return self.rig
        else:
            print("No CryptoToken available to acquire a rig!")
            return None

    # Inventory & Rig storage transfer
    def store_asset(self, asset_type, amount=1):
        if not self.rig:
            print("No rig available!")
            return False
        return self._transfer(
            source=self.__inventory,
            dest=self.rig.storage,
            asset_type=asset_type,
            amount=amount,
            capacity=self.rig.capacity
        )


    def get_asset(self, asset_type, amount=1):
        if not self.rig:
            print("No rig available!")
            return False

        return self._transfer(
            source=self.rig.storage,
            dest=self.__inventory,
            asset_type=asset_type,
            amount=amount
        )

    def _transfer(self, source, dest, asset_type,
                  amount, capacity=None):
        # Find the source asset
        for asset in source:
            if isinstance(asset, asset_type):
                if asset.quantity < amount:
                    print("Not enough quantity to transfer!")
                    return False

                # check capacity for storage
                if capacity is not None:
                    total = self.rig.capacity
                    if total + amount > capacity:
                        print("Destination storage full!")
                        return False

                # consume from source
                asset.consume(amount)
                if asset.quantity == 0:
                    source.remove(asset)
                # merge into destination
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

    # Encrypt/Decrypt logic
    def _toggle_asset_encryption(self, asset_type, encrypt=True):
        if not self.rig:
            print("No rig available!")
            return False

        # find a chip in inventory or storage
        chip, loc = self._find_security_chip()
        if not chip:
            print("No Security Chip available!")
            return False

        for asset in self.rig.storage:
            """
            Only encrypt if currently unencrypted,
            or decrypt if currently encrypted.
            """
            if isinstance(asset, asset_type):
                if encrypt and not asset.encrypted:
                    pass
                elif not encrypt and asset.encrypted:
                    pass
                else:
                    continue
                success = asset.toggle_encrypt(token=chip)
                if success and chip.quantity == 0:
                    self._remove_chip(chip, loc)
                return success

        action = "encrypt" if encrypt else "decrypt"
        print(f"No {asset_type.__name__} available to {action}.")
        return False

    def encrypt_asset(self, asset_type):
        return self._toggle_asset_encryption(asset_type, encrypt=True)
    def decrypt_asset(self, asset_type):
        return self._toggle_asset_encryption(asset_type, encrypt=False)

    def consume_asset(self, asset_type, amount=1):
        for asset in self.__inventory:
            if isinstance(asset, asset_type) and asset.quantity > 0:
                still_has = asset.consume(amount)
                if not still_has:
                    self.__inventory.remove(asset)
                return True
        return False




    def _remove_chip(self, chip, location):
        if location == "inventory":
            try: self.__inventory.remove(chip)
            except: pass
        else:
            try: self.rig.storage.remove(chip)
            except: pass



    def _find_security_chip(self):
        chip = next((a for a in self.__inventory
                     if isinstance(a, SecurityChip) and
                     a.quantity > 0), None)
        if chip:
            return chip, "inventory"

        if self.rig:
            chip = next((a for a in self.rig.storage
                         if isinstance(a, SecurityChip) and
                         a.quantity > 0), None)
            if chip:
                return chip, "storage"
        return None, None


    trace = property(get_trace, increase_trace)


p1 = Hacker()
print(p1)
rig = p1.get_rig()
while p1.trace <= MAX_TRACE:
    print(p1)
    p1.rig.generate_asset()
    p1.rig.dmg = 3
    p1.rig.repair()
    p1.decrypt_asset(DataSpike)
    p1.encrypt_asset(DataSpike)
    p1.trace = 1

"""
File: Hacker.py
Description: This module outlines the Hacker class and its associated methods.
Author: Scott Quinton Walker
ID: 110441860
Username: walsq001
This is my own work as defined by the University's Academic Misconduct Policy.
"""

import random
from Rig import Rig
from Asset import Asset, DataSpike, CryptoToken, RemovableDrive, SecurityChip, HardwarePatch

MAX_TRACE = 5 # Maximum trace level before hacker is exposed

class Hacker:
    def __init__(self):
        """
        Represents a hacker in the simulation.
        Hackers manage an inventory, acquire a rig,
        perform actions such as attacks, encryption, and
        asset transfers. The hacker accumulates
        trace when performing risky actions.
        """
        self.__name = random.choice(
            ["Alan Turing", "Christopher Strachey", "Edie Windsor",
            "Jon 'Maddog' Hall", "Mary Ann Horton", "Audrey Tang",
             "Tim Cook", "Dr. Mary Gray"]
        )
        self.rig = None
        # Start with one crypto token
        token = CryptoToken()
        token.set_unencrypted(1)
        self.__inventory = [token]

        # Trace-level tracking
        self.__trace_level = 0
        self.__exposed = False

    # --- Properties---
    def get_trace(self):
        return self.__trace_level
    def set_trace(self, value=1):
        self.__trace_level += value
        if self.__trace_level >= MAX_TRACE:
            self.__trace_level = MAX_TRACE
            self.__exposed = True
            print("Trace maximum reached, actions blocked!")
    def get_name(self):
        return self.__name
    def get_rig(self):
        """Returns the rig object."""
        if self.rig is not None:
            return self.rig
        consumed = self.consume_asset(CryptoToken, 1)
        if consumed:
            self.rig = Rig()
            print(f"{self.__name} has activated a new rig: {self.rig.name}")
            return self.rig
        return None

    def store_asset(self, asset_type, amount=1):
        if not self.rig:
            return False
        success = self._transfer(self.__inventory, self.rig.storage, asset_type, amount, self.rig.capacity)
        if success:
            self.set_trace()
        return success

    def get_asset(self, asset_type, amount=1):
        if not self.rig:
            return False
        success = self._transfer(self.rig.storage, self.__inventory, asset_type, amount)
        if success:
            self.set_trace()
        return success

    def get_exposed(self):
        return self.__exposed

    name = property(get_name)
    trace = property(set_trace)
    exposed = property(get_exposed)


    def _transfer(self, source, dest, asset_type, amount, capacity=None):
        """
        Move assets between two lists (inventory <--> storage).
        Steps:
        1. Skip items if they are not the requested type.
        2. Block transfer if the asset is encrypted.
        3. Skip if not enough encrypted units available.
        4. Check capacity if moving into rig storage.
        5. Consume requested amount of units.
        6. If the source asset is empty, remove it.
        7. If the destination already has that type, merge into it.
            Otherwise, create a new asset entry.
        Return true if transfer was successful.
        Return false otherwise.
        """
        amount = int(amount)
        if amount <= 0:
            return False
        for item in list(source):
            if not isinstance(item, asset_type):
                continue
            if item.encrypted_count() > 0:
                print("Cannot transfer encrypted assets")
                return False
            if item.unencrypted_count() < amount:
                continue
            if capacity is not None:
                dest_total = sum(d.quantity() for d in dest)
                if dest_total + amount > capacity:
                    return False
            consumed = item.consume(amount)
            if consumed <= 0:
                return False
            if item.quantity() == 0:
                source.remove(item)
            for d in dest:
                if isinstance(d, asset_type):
                    d.set_unencrypted(d.unencrypted_count() + consumed)
                    return True
            new_asset = asset_type()
            new_asset.set_unencrypted(consumed)
            dest.append(new_asset)
            return True
        return False

    def consume_asset(self, asset_type, amount=1):
        amount = int(amount)
        if amount <= 0:
            return 0
        remaining = amount
        total_consumed = 0

        sources = [self.__inventory]
        if self.rig:
            sources.append(self.rig.storage)

        for source in sources:
            for asset in list(source):
                if not isinstance(asset, asset_type):
                    continue

                consumed = asset.consume(remaining)
                total_consumed += consumed
                remaining -= consumed

                if asset.quantity() == 0:
                    source.remove(asset)
                if remaining <= 0:
                    return total_consumed
        return total_consumed

    # Encryption helper
    def _find_instance(self, asset_type):
        """
        Return the first instance of asset type if it exists.
        :param asset_type:
        :return:
        """
        # if a caller passed an instance already, just return it
        if not isinstance(asset_type, type):
            return asset_type

        for a in self.__inventory:
            if isinstance(a, asset_type):
                return a

        if self.rig:
            for a in self.rig.storage:
                if isinstance(a, asset_type):
                    return a
        return None

    def encrypt_assets(self, asset, amount=1):
        """
        Find an asset instance and encrypt it its unencrypted
        units with one security chip.
        :param asset:
        :return: True or False
        """
        asset = self._find_instance(asset)
        if asset is None:
            return False
        chip = self._find_instance(SecurityChip)
        if chip is None:
            return False

        if chip in self.__inventory:
            loc = "inventory"
        elif self.rig and chip in self.rig.storage:
            loc = "storage"
        else:
            loc = None

        encrypted = asset.encrypt(amount, chip)
        if encrypted <= 0:
            return False

        if chip.quantity() == 0 and loc == "inventory":
            if chip in self.__inventory:
                self.__inventory.remove(chip)
        elif chip.quantity() == 0 and loc == "storage":
            if self.rig and chip in self.rig.storage:
                self.rig.storage.remove(chip)
        return True


    def decrypt_assets(self, asset, amount=1):
        asset = self._find_instance(asset)
        if asset is None:
            return False
        chip = self._find_instance(SecurityChip)
        if chip is None:
            return False
        if chip in self.__inventory:
            loc = "inventory"
        elif self.rig and chip in self.rig.storage:
            loc = "storage"
        else:
            loc = None
        decrypted = asset.decrypt(amount, chip)
        if decrypted <= 0:
            return False
        if chip.quantity() == 0 and loc == "inventory":
            if chip in self.__inventory:
                self.__inventory.remove(chip)
        elif chip.quantity() == 0 and loc == "storage":
            if self.rig and chip in self.rig.storage:
                self.rig.storage.remove(chip)
        return True

    # Common actions that consume assets

    def repair_rig(self):
        """Consume one CryptoToken to repair"""
        if not self.rig:
            return False
        consumed = self.consume_asset(CryptoToken)
        if consumed == 0:
            return False
        return self.rig.repair()

    def upgrade_rig(self):
        """Consume one HardwarePatch to upgrade"""
        if not self.rig:
            return False
        if self.__exposed:
            print("Action blocked: hacker is exposed.")
            return False
        consumed = self.consume_asset(HardwarePatch)
        if consumed == 0:
            return False
        self.set_trace()
        return self.rig.upgrade()

    def launch_attack(self, target_hacker, hits=1):
        """
        Attack another Hacker's rig using DataSpike(s) from this hacker's inventory.
        Consumes DataSpike assets from inventory and applies damage to the target rig.
        Returns damage applied (float) or 0 if no damage occurred.
        """
        if target_hacker is None or target_hacker.rig is None:
            print("No valid target to attack.")
            return 0
        if self.__exposed:
            print("Action blocked: hacker is exposed.")
            return 0
        # consume DataSpike(s) from this hacker's inventory
        consumed = self.rig.consume_from_storage(DataSpike, hits)
        if consumed == 0:
            print("No DataSpike available to launch attack")
            return 0
        # each consumed spike counts as one hit against the target rig
        dmg = target_hacker.rig.take_hit(consumed, attacker=self.name)
        self.set_trace()
        return dmg

    def generate(self):
        if not self.rig:
            return None
        return self.rig.generate()

    def extract_assets(self, target_hacker):
        """
        Extract assets from a broken target rig.
        - Requires this hacker to have a RemovableDrive.
        - Consumes one RemovableDrive.
        - Steals all unencrypted assets from targets rig.
        - Adds them into this hacker's inventory (merging if type exists).
        - Increase trace.
        Returns amount of assets extracted.
        """
        # basic checks
        if target_hacker is None:
            return 0
        if target_hacker.rig is None:
            return 0
        if not target_hacker.rig.broken:
            return 0

        # Attacker must have a removable drive
        drive = None
        for a in list(self.rig.storage):
            if isinstance(a, RemovableDrive):
                drive = a
                break
        if drive is None:
            return 0

        consumed_drive = drive.consume(1)
        if consumed_drive <= 0:
            return 0
        if drive.quantity() == 0 and drive in self.rig.storage:
            self.rig.storage.remove(drive)

        total_extracted = 0
        # Helper: Add n unencrypted units of asset_type into this hackers inventory
        def add_to_my_inventory(asset, n):
            if n <= 0:
                return
            # Find existing asset of that type in my inventory
            for inv_item in self.__inventory:
                if isinstance(inv_item, asset):
                    inv_item.set_unencrypted(inv_item.unencrypted_count() + n)
                    return
            # Not found: create a new instance and append
            new_item = asset()
            new_item.set_unencrypted(n)
            self.__inventory.append(new_item)
        # Steal from target rig storage
        for asset in list(target_hacker.rig.storage):
            if not isinstance(asset, Asset):
                continue
            available = asset.unencrypted_count()
            if available <= 0:
                continue
            taken = asset.consume(available)
            if taken > 0:
                total_extracted += taken
                add_to_my_inventory(type(asset), taken)
            if asset.quantity() == 0:
                if asset in target_hacker.rig.storage:
                    target_hacker.rig.storage.remove(asset)
        self.set_trace()
        return total_extracted

    def scan_inventory(self, asset_name: str):
        for asset in self.__inventory:
            if asset.get_name().lower() == asset_name.lower():
                self.__inventory.remove(asset)
                return asset
        return None

    def retrieve_assets(self, asset_type):
        results = []
        for asset in list(self.__inventory):
            if isinstance(asset, asset_type):
                results.append(asset)
                self.__inventory.remove(asset)
        return results

    """
    String Magic Method
    """
    def __str__(self):
        inventory_str = "\n".join(f"{str(item)}" for item in self.__inventory)
        if not inventory_str:
            inventory_str = "No items in inventory."
        rig_str = str(self.rig) if self.rig else "No rig"
        return (f"---Hacker---\n"
                f"Name: {self.__name}\n"
                f"Trace Level: {self.__trace_level}\n"
                f"---Inventory---\n"
                f"{inventory_str}\n"
                f"---Rig---\n"
                f"{rig_str}\n")



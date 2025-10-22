"""
File: Asset.py
Description: This module outlines the asset class and their associated functionality.
Author: Scott Quinton Walker
ID: 110441860
Username: walsq001
This is my own work as defined by the University's Academic Misconduct Policy.
"""
class Asset:
    """
    Base class for all digital assets.
    Tracks separate counts for unencrypted and encrypted assets.
    """
    def __init__(self, name: str, description: str, quantity: int = 1):
        # Each asset has a name, descriptions, and instantiates with some unencrypted units.
        # Encrypted units are tracked separately.
        self.__name = name
        self.__description = description
        self.__unencrypted_quantity = quantity
        self.__encrypted_quantity = 0

    def get_name(self):
        return self.__name

    def get_description(self):
        return self.__description

    def unencrypted_count(self):
        return self.__unencrypted_quantity

    def encrypted_count(self):
        return self.__encrypted_quantity

    def quantity(self):
        return self.__unencrypted_quantity + self.__encrypted_quantity

    def set_unencrypted(self, qty: int):
        self.__unencrypted_quantity = qty

    def _adjust_quantity(self, amount, from_encrypted=False):
        """
        Adjusts the 'amount' of an asset.
        Determines whether the asset is encrypted or not.
        """
        amount = int(amount)
        if amount <= 0:
            return 0
        if from_encrypted:
            available = self.__encrypted_quantity
            if available <= 0:
                return 0
            taken = min(amount, available)
            self.__encrypted_quantity -= taken
            self.__unencrypted_quantity += taken
            return taken
        else:
            available = self.__unencrypted_quantity
            if available <= 0:
                return 0
            taken = min(amount, available)
            self.__unencrypted_quantity -= taken
            return taken

    def encrypt(self, amount, token):
        """
        Encrypts the given amount of units using a SecurityChip token.
        """
        if token is None or not isinstance(token, SecurityChip):
            return 0
        if token.consume(1) <= 0:
            return 0
        amount = int(amount)
        return self._adjust_quantity(amount, from_encrypted=False)

    def decrypt(self, amount, token):
        """
        Decrypts the given amount of units using a SecurityChip token.
        """
        if token is None or not isinstance(token, SecurityChip):
            return 0
        if token.consume(1) <= 0:
            return 0
        return self._adjust_quantity(amount, from_encrypted=True)

    def merge_from(self, other):
        """
        Combines another asset of the same type into this one.
        """
        if other is None:
            return self.quantity()
        # Add other's unencrypted/encrypted amounts into corresponding buckets
        self.__unencrypted_quantity += other.unencrypted_count()
        self.__encrypted_quantity += other.encrypted_count()
        return self.quantity()

    def consume(self, amount=1):
        """
        Consumes up to 'amount' of unencrypted assets.
        Returns the amount actually consumed.
        """
        return self._adjust_quantity(amount, from_encrypted=False)


    def __str__(self):
        """
        String representation of the asset.
        """
        parts = []
        if self.__unencrypted_quantity > 0:
            parts.append(f"{self.__unencrypted_quantity} unencrypted")
        if self.__encrypted_quantity > 0:
            parts.append(f"{self.__encrypted_quantity} encrypted")
        counts = ", ".join(parts) if parts else "Empty"
        return (f"{self.__name} - {self.__description}\n"
                f"({counts})")

"""
Sub-classes for Asset
"""
class CryptoToken(Asset):
    def __init__(self):
        super().__init__("Crypto Token", "Used to acquire or repair rigs.", 1)

class DataSpike(Asset):
    def __init__(self):
        super().__init__("Data Spike", "Used in battles", 1)

class RemovableDrive(Asset):
    def __init__(self):
        super().__init__("Removable Drive", "Found in rigs" +
                         " and used for extraction", 1)

class SecurityChip(Asset):
    def __init__(self):
        super().__init__("Security Chip", "Used to encrypt" +
                         " or decrypt assets", 1)

class HardwarePatch(Asset):
    def __init__(self):
        super().__init__("Hardware Patch", "Used to upgrade rigs", 1)

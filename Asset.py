"""
File: Asset.py
Description: This module outlines the asset class and their associated functionality.
Author: Scott Quinton Walker
ID: 110441860
Username: walsq001
This is my own work as defined by the University's Academic Misconduct Policy.
"""
class Asset:
    def __init__(self, name, description, quantity):
        self.__name = name
        self.__description = description
        self.__quantity = quantity
        self.__encrypted = False

    def __str__(self):
        enc = " [Encrypted]" if self.__encrypted else ""
        return (f"{self.__name} - {self.__description}"
        f"{self.__quantity}{enc}")

    def get_encrypt(self):
        return self.__encrypted

    def set_encrypt(self, encrypted):
        if encrypted == self.__encrypted:
            self.__encrypted = True
        else:
            self.__encrypted = False

    def get_quantity(self):
        return self.__quantity

    def set_quantity(self, value):
        if not isinstance(value, int):
            raise TypeError("Quantity must be an integer")
        self.__quantity = max(0, value)

    def consume(self, amount=1):
        if amount < 0:
            raise ValueError("Quantity cannot be negative")
        if self.__quantity >= amount:
            self.__quantity -= amount
        else:
            self.__quantity = 0
        return self.__quantity > 0

    quantity = property(get_quantity, set_quantity)
    encrypt = property(get_encrypt, set_encrypt)

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

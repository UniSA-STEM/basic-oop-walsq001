"""
File: Asset.py
Description: This module outlines the asset class and their associated functionality.
Author: Scott Quinton Walker
ID: 110441860
Username: walsq001
This is my own work as defined by the University's Academic Misconduct Policy.
"""


class CryptoToken:
    def __init__(self):
        self.__name = "CryptoToken"
        self.__encrypted = False
        self.__quantity = 1

    def __str__(self):
        return f"{self.__name} {self.__quantity}"

    def __get_quantity(self):
        return self.__quantity

    def __set_quantity(self, value):
        if not isinstance(value, int):
            raise TypeError("CryptoToken quantity must be an integer")
        self.__quantity += value
        if self.__quantity <= 0:
            self.__quantity = 0

    quantity = property(__get_quantity, __set_quantity)


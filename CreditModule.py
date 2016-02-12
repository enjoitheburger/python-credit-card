#!/usr/bin/python
import Luhn10


class Customer:

    def __init__(self, name):
        self.name = name
        self.credit_cards_dict = {}

    def add_credit_card(self, card_number, credit_limit):

        if card_number in self.credit_cards_dict:
            return False

        try:
            credit_card = CreditCard(card_number, credit_limit)
            self.credit_cards_dict[card_number] = credit_card
            return True
        except ValueError:
            return False

    def charge_account(self, charge_amount):

        if not self.credit_cards_dict:
            return False

        try:
            # Will charge the first credit card in the dictionary.
            return list(self.credit_cards_dict.values())[0].add_balance(charge_amount)
        except ValueError:
            return False

    def change_credit_limit(self, credit_limit):

        if not self.credit_cards_dict:
            return False

        try:
            # Will change the credit limit for the first credit card in the dictionary.
            return list(self.credit_cards_dict.values())[0].change_credit_limit(credit_limit)
        except ValueError:
            return False

    def get_card(self):
        if self.credit_cards_dict:
            return list(self.credit_cards_dict.values())[0]

    def get_card_balance(self):
        # Get balance of first card in dictionary. If dictionary is empty, return "Error"
        if not self.credit_cards_dict:
            return "error"

        return "$" + str(list(self.credit_cards_dict.values())[0].balance)

    def get_card_credit_limit(self):
        # Get credit limit of first card in dictionary. If dictionary is empty, return "Error"
        if not self.credit_cards_dict:
            return "error"

        return "$" + str(list(self.credit_cards_dict.values())[0].credit_limit)


class CreditCard:

    def __init__(self, card_number, credit_limit):
        if not Luhn10.is_luhn_valid(card_number):
            raise ValueError
        else:
            credit_limit = self._valid_monetary_amount(credit_limit, False)
            self.card_number = card_number;
            self.balance = 0
            self.credit_limit = credit_limit

    def add_balance(self, charge_amount):
        charge_amount = self._valid_monetary_amount(charge_amount, True)
        if charge_amount < 0:
            self.balance += charge_amount
            return True

        new_balance = self.balance + charge_amount
        if self.credit_limit >= new_balance:
            self.balance += charge_amount
            return True
        return False

    def change_credit_limit(self, credit_limit):
        credit_limit = self._valid_monetary_amount(credit_limit, False)
        self.credit_limit = credit_limit
        if self.credit_limit < self.balance:
            self.balance = self.credit_limit - self.balance

        return True

    def _valid_monetary_amount(self, money_string, allow_negative):
        if money_string[0] != '$':
            raise ValueError

        dollar_int = int(money_string[1:])
        if not allow_negative and dollar_int <= 0:
            raise ValueError
        return dollar_int


class CreditSystem:

    def __init__(self):
        self.customers_dict = {}

    def add(self, name, card_number, credit_limit):

        if name in self.customers_dict:
            is_card_added = self.customers_dict[name].add_credit_card(card_number, credit_limit)
            return is_card_added
        else:
            new_customer = Customer(name)
            is_card_added = new_customer.add_credit_card(card_number, credit_limit)
            self.customers_dict[name] = new_customer
            return is_card_added

    def charge(self, name, charge_amount):
        if name not in self.customers_dict:
            return False

        return self.customers_dict[name].charge_account(charge_amount)

    def credit(self, name, credit_limit):
        if name not in self.customers_dict:
            return False

        return self.customers_dict[name].change_credit_limit(credit_limit)

    def get_customer(self, name):
        return self.customers_dict[name]

    def print_customer_accounts(self):
        for customer in self.customers_dict.values():
            print(customer.name + ": " + customer.get_card_balance())

#!/usr/bin/python
import unittest
import CreditModule


class CreditSystem(unittest.TestCase):
    def setUp(self):
        self.credit_system = CreditModule.CreditSystem()

    def tearDown(self):
        self.credit_system = None


class AddTest(CreditSystem):
    def test_add_credit_success(self):
        add_customer = self.credit_system.add("Tom", "79927398713", "$1000")
        self.assertTrue(add_customer)

    def test_add_credit_success_existing_customer(self):
        self.credit_system.add("Tom", "4597384256449462", "$500")
        add_customer = self.credit_system.add("Tom", "79927398713", "$500")
        self.assertTrue(add_customer)

    def test_add_credit_fail_existing_customer_and_card(self):
        self.credit_system.add("Tom", "4597384256449462", "$500")
        add_customer = self.credit_system.add("Tom", "4597384256449462", "$500")
        self.assertFalse(add_customer)

    def test_add_credit_fail_Luhn10(self):
        add_customer = self.credit_system.add("Tom", "12345678910", "$1000")
        self.assertFalse(add_customer)

    def test_add_credit_fail_nonnumeric_creditlimit(self):
        add_customer = self.credit_system.add("Tom", "79927398713", "#D4")
        self.assertFalse(add_customer)

    def test_add_credit_fail_decimal_creditlimit(self):
        add_customer = self.credit_system.add("Tom", "79927398713", "$0.01")
        self.assertFalse(add_customer)


class ChargeTest(CreditSystem):
    def test_charge_success(self):
        self.credit_system.add("Tom", "4597384256449462", "$500")
        charge_customer = self.credit_system.charge("Tom", "$250")
        self.assertTrue(charge_customer)
        credit_limit = self.credit_system.get_customer("Tom").get_card().balance
        self.assertEqual(credit_limit, 250)

    def test_charge_fail_nonexisting_customer(self):
        charge_customer = self.credit_system.charge("Tom", "$250")
        self.assertFalse(charge_customer)

    def test_charge_fail_overdraft(self):
        self.credit_system.add("Tom", "4597384256449462", "$300")
        charge_customer = self.credit_system.charge("Tom", "$301")
        self.assertFalse(charge_customer)
        credit_limit = self.credit_system.get_customer("Tom").get_card().balance
        # Decline charge, balance remains 0
        self.assertEqual(credit_limit, 0)


    def test_charge_fail_negative_charge(self):
        self.credit_system.add("Tom", "4597384256449462", "$300")
        charge_customer = self.credit_system.charge("Tom", "$-20")
        self.assertTrue(charge_customer)


class CreditTest(CreditSystem):

    def test_credit_success(self):
        self.credit_system.add("Tom", "4597384256449462", "$500")
        credit_change = self.credit_system.credit("Tom", "$250")
        self.assertTrue(credit_change)
        credit_limit = self.credit_system.get_customer("Tom").get_card().credit_limit
        self.assertEqual(credit_limit, 250)

    def test_credit_success_negative_credit_to_balance(self):
        self.credit_system.add("Tom", "4597384256449462", "$300")
        self.credit_system.charge("Tom", "$300")
        credit_change = self.credit_system.credit("Tom", "$100")
        self.assertTrue(credit_change)
        credit_limit = self.credit_system.get_customer("Tom").get_card().balance
        self.assertEqual(credit_limit, -200)

    def test_credit_fail_negative_credit(self):
        self.credit_system.add("Tom", "4597384256449462", "$300")
        credit_change = self.credit_system.credit("Tom", "-$250")
        self.assertFalse(credit_change)
        credit_limit = self.credit_system.get_customer("Tom").get_card().credit_limit
        self.assertEqual(credit_limit, 300)

    def test_credit_fail_nonexisting_customer(self):
        self.credit_system.add("Tom", "4597384256449462", "$300")
        credit_change = self.credit_system.credit("Amy", "-$250")
        self.assertFalse(credit_change)


if __name__ == '__main__':
    unittest.main()

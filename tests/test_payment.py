import unittest
from data_model import Member, Transaction, FitnessManagementSystem, MEMBERSHIP_TYPE, FITNESS_GOAL
from datetime import datetime

class TestTransaction(unittest.TestCase):
    def test_payment_creation(self):
        fms = FitnessManagementSystem()
        member = Member(fms, "Ali", 25, MEMBERSHIP_TYPE.BASIC, FITNESS_GOAL.WEIGHT_LOSS)
        payment = Transaction(fms, member, 1000, datetime(2023, 5, 1), MEMBERSHIP_TYPE.BASIC)

        self.assertEqual(payment.amount_paid, 1000)
        self.assertEqual(payment.member, member)
        self.assertEqual(payment.payment_date, datetime(2023, 5, 1))

if __name__ == '__main__':
    unittest.main()
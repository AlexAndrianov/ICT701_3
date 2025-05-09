import unittest
from data_model import *

class TestFitnessClassManagementSystem(unittest.TestCase):

    def test_cancel_nonexistent_booking(self):
        fms = FitnessManagementSystem()
        member = fms.register_member("Ali", 25, MEMBERSHIP_TYPE.BASIC, FITNESS_GOAL.WEIGHT_LOSS)
        trainer = fms.add_trainer("Sara", SPECIALIZATION.YOGA)
        yoga_class = fms.schedule_class("Yoga", trainer, 2, datetime.datetime.now())

        # Cancel without booking
        yoga_class.cancel_booking(member)

        # Member should not be in class
        assert member not in yoga_class.members

    def test_negative_payment_amount(self):
        fms = FitnessManagementSystem()
        member = fms.register_member("Ali", 25, MEMBERSHIP_TYPE.BASIC, FITNESS_GOAL.WEIGHT_LOSS)

        try:
            fms.process_payment(member, -100, MEMBERSHIP_TYPE.BASIC)
            assert False  # Should not reach here
        except ValueError:
            assert True  # Expected outcome

    def test_generate_receipt_output(self):
        fms = FitnessManagementSystem()
        member = fms.register_member("Ali", 25, MEMBERSHIP_TYPE.VIP, FITNESS_GOAL.MUSCLE_GAIN)
        txn = fms.process_payment(member, 2000, MEMBERSHIP_TYPE.VIP)

        receipt = txn.generate_receipt()

        assert f"Transaction #{txn.ID}" in receipt
        assert "Member:" in receipt
        assert "Amount Paid:" in receipt
        assert "VIP" in receipt

    def test_top_class_in_revenue_report(self):
        fms = FitnessManagementSystem()
        m1 = fms.register_member("Ali", 25, MEMBERSHIP_TYPE.BASIC, FITNESS_GOAL.ENDURANCE)
        m2 = fms.register_member("Sara", 27, MEMBERSHIP_TYPE.PREMIUM, FITNESS_GOAL.MUSCLE_GAIN)
        trainer = fms.add_trainer("John", SPECIALIZATION.CARDIO)
        class1 = fms.schedule_class("HIIT", trainer, 5, datetime.datetime.now())
        class2 = fms.schedule_class("Yoga", trainer, 5, datetime.datetime.now())

        m1.book_class(class1)
        m2.book_class(class1)
        m1.book_class(class2)

        fms.process_payment(m1, 500, MEMBERSHIP_TYPE.BASIC)
        fms.process_payment(m2, 1000, MEMBERSHIP_TYPE.PREMIUM)

        assert fms.generate_revenue_report() == 1500

    def test_class_at_capacity_booking_blocked(self):
        fms = FitnessManagementSystem()
        m1 = fms.register_member("Ali", 25, MEMBERSHIP_TYPE.BASIC, FITNESS_GOAL.ENDURANCE)
        m2 = fms.register_member("Sara", 27, MEMBERSHIP_TYPE.PREMIUM, FITNESS_GOAL.MUSCLE_GAIN)
        trainer = fms.add_trainer("Zane", SPECIALIZATION.STRENGTH_TRAINING)
        class1 = fms.schedule_class("Strength Max", trainer, 1, datetime.datetime.now())

        assert m1.book_class(class1) == True
        assert m2.book_class(class1) == False  # Should be blocked



if __name__ == '__main__':
    unittest.main()

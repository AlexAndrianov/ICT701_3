import unittest
from data_model import (
    FitnessManagementSystem, MEMBERSHIP_TYPE, FITNESS_GOAL, SPECIALIZATION
)
import datetime

class TestFitnessManagementSystem(unittest.TestCase):

    def setUp(self):
        self.fms = FitnessManagementSystem()

    def test_register_member(self):
        member = self.fms.register_member("Ali", 25, MEMBERSHIP_TYPE.BASIC, FITNESS_GOAL.WEIGHT_LOSS)
        self.assertEqual(member.Name, "Ali")
        self.assertEqual(member.Age, 25)
        self.assertEqual(member.MembershipType, MEMBERSHIP_TYPE.BASIC)
        self.assertIn(member.ID, self.fms.members)

    def test_add_trainer_and_assign_class(self):
        trainer = self.fms.add_trainer("John", SPECIALIZATION.YOGA)
        scheduled_class = self.fms.schedule_class(
            "Morning Yoga", trainer, 5, datetime.datetime.now()
        )
        self.assertEqual(scheduled_class.Trainer.Name, "John")
        self.assertIn(scheduled_class.ID, self.fms.classes)

    def test_book_class(self):
        member = self.fms.register_member("Ali", 25, MEMBERSHIP_TYPE.BASIC, FITNESS_GOAL.WEIGHT_LOSS)
        trainer = self.fms.add_trainer("John", SPECIALIZATION.YOGA)
        yoga_class = self.fms.schedule_class(
            "Morning Yoga", trainer, 2, datetime.datetime.now()
        )
        booked = member.book_class(yoga_class)
        self.assertTrue(booked)
        self.assertIn(member, yoga_class.members)

    def test_cancel_booking(self):
        member = self.fms.register_member("Ali", 25, MEMBERSHIP_TYPE.BASIC, FITNESS_GOAL.WEIGHT_LOSS)
        trainer = self.fms.add_trainer("John", SPECIALIZATION.YOGA)
        yoga_class = self.fms.schedule_class("Yoga", trainer, 2, datetime.datetime.now())
        member.book_class(yoga_class)
        yoga_class.cancel_booking(member)
        self.assertNotIn(member, yoga_class.members)

    def test_update_membership(self):
        member = self.fms.register_member("Ali", 25, MEMBERSHIP_TYPE.BASIC, FITNESS_GOAL.WEIGHT_LOSS)
        member.update_membership(MEMBERSHIP_TYPE.VIP)
        self.assertEqual(member.MembershipType, MEMBERSHIP_TYPE.VIP)

    def test_track_progress(self):
        member = self.fms.register_member("Ali", 25, MEMBERSHIP_TYPE.BASIC, FITNESS_GOAL.WEIGHT_LOSS)
        member.track_progress("Lost 2kg", FITNESS_GOAL.WEIGHT_LOSS)
        self.assertIn(FITNESS_GOAL.WEIGHT_LOSS, member.progresses)
        self.assertEqual(member.progresses[FITNESS_GOAL.WEIGHT_LOSS][0], "Lost 2kg")

    def test_process_payment(self):
        member = self.fms.register_member("Ali", 25, MEMBERSHIP_TYPE.BASIC, FITNESS_GOAL.WEIGHT_LOSS)
        txn = self.fms.process_payment(member, 1000, MEMBERSHIP_TYPE.BASIC)
        self.assertEqual(txn.amount_paid, 1000)

    def test_generate_revenue_report(self):
        member1 = self.fms.register_member("Ali", 25, MEMBERSHIP_TYPE.BASIC, FITNESS_GOAL.WEIGHT_LOSS)
        member2 = self.fms.register_member("Sara", 30, MEMBERSHIP_TYPE.VIP, FITNESS_GOAL.MUSCLE_GAIN)
        self.fms.process_payment(member1, 1000, MEMBERSHIP_TYPE.BASIC)
        self.fms.process_payment(member2, 2000, MEMBERSHIP_TYPE.VIP)
        total = self.fms.generate_revenue_report()
        self.assertEqual(total, 3000)

    def test_cancel_membership(self):
        member = self.fms.register_member("Ali", 25, MEMBERSHIP_TYPE.BASIC, FITNESS_GOAL.WEIGHT_LOSS)
        self.fms.cancel_membership(member)
        self.assertNotIn(member.ID, self.fms.members)

if __name__ == '__main__':
    unittest.main()
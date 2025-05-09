
from data_model import FitnessManagementSystem, Member, MEMBERSHIP_TYPE, FITNESS_GOAL
import unittest

class TestFitnessMemberSystem(unittest.TestCase):
    def test_member_registration(self):
        fms = FitnessManagementSystem()
        member = fms.register_member("John Doe", 30, MEMBERSHIP_TYPE.BASIC, FITNESS_GOAL.WEIGHT_LOSS)

        assert member.Name == "John Doe"
        assert member.Age == 30
        assert member.MembershipType == MEMBERSHIP_TYPE.BASIC
        assert member.FitnessGoals == FITNESS_GOAL.WEIGHT_LOSS
        assert member.ID in fms.Members


    def test_member_membership_update(self):
        fms = FitnessManagementSystem()
        member = fms.register_member("Alice", 25, MEMBERSHIP_TYPE.BASIC, FITNESS_GOAL.ENDURANCE)
        
        member.update_membership(MEMBERSHIP_TYPE.VIP)
        assert member.MembershipType == MEMBERSHIP_TYPE.VIP


    def test_member_class_booking(self):
        from datetime import datetime
        from data_model import Trainer, SPECIALIZATION

        fms = FitnessManagementSystem()
        member = fms.register_member("Bob", 28, MEMBERSHIP_TYPE.PREMIUM, FITNESS_GOAL.MUSCLE_GAIN)
        trainer = fms.add_trainer("Sam", SPECIALIZATION.STRENGTH_TRAINING)
        class_time = datetime.now()
        fit_class = fms.schedule_class("Strength 101", trainer, 10, class_time)

        result = member.book_class(fit_class)

        assert result is True
        assert member in fit_class.members
        assert fit_class in member.ClassBooking


    def test_member_track_progress(self):
        fms = FitnessManagementSystem()
        member = fms.register_member("Carol", 32, MEMBERSHIP_TYPE.BASIC, FITNESS_GOAL.WEIGHT_LOSS)

        member.track_progress({"date": "2025-05-01", "weight": 70}, FITNESS_GOAL.WEIGHT_LOSS)
        member.track_progress({"date": "2025-05-02", "weight": 69}, FITNESS_GOAL.WEIGHT_LOSS)

        assert FITNESS_GOAL.WEIGHT_LOSS in member.progresses
        assert len(member.progresses[FITNESS_GOAL.WEIGHT_LOSS]) == 2
        assert member.progresses[FITNESS_GOAL.WEIGHT_LOSS][0]["weight"] == 70


if __name__ == '__main__':
    unittest.main()
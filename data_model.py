from enum import Enum
import datetime
from id_generator import next_id

# ------------------------- Enums section --------------------------------------

class MEMBERSHIP_TYPE(Enum):
    BASIC = 1
    PREMIUM = 2
    VIP = 3

    def __str__(self):
        names = {
            MEMBERSHIP_TYPE.BASIC: "Basic",
            MEMBERSHIP_TYPE.PREMIUM: "Premium",
            MEMBERSHIP_TYPE.VIP: "Vip"
        }
        return names[self]


class FITNESS_GOAL(Enum):
    WEIGHT_LOSS = 1
    MUSCLE_GAIN = 2
    ENDURANCE = 3

    def __str__(self):
        names = {
            FITNESS_GOAL.WEIGHT_LOSS: "WeightLoss",
            FITNESS_GOAL.MUSCLE_GAIN: "MuscleGain",
            FITNESS_GOAL.ENDURANCE: "Endurance"
        }
        return names[self]
    

class SPECIALIZATION(Enum):
    YOGA = 1
    STRENGTH_TRAINING = 2
    CARDIO = 3

    def __str__(self):
        names = {
            SPECIALIZATION.YOGA: "Yoga",
            SPECIALIZATION.STRENGTH_TRAINING: "Strength Training",
            SPECIALIZATION.CARDIO: "Cardio"
        }
        return names[self]
    
# ------------------------- Classes section --------------------------------------

class Base:
    """Base class for common ID and system reference."""
    def __init__(self, fms: "FitnessManagementSystem"):
        self.uuid = next_id()
        self.fms = fms
    
    def __eq__(self, other):
        return isinstance(other, Base) and self.uuid == other.uuid

    def __hash__(self):
        return hash(self.uuid)

    @property
    def ID(self):
        return self.uuid


class Member(Base):
    """Represents a fitness club member."""
    def __init__(self, fms: "FitnessManagementSystem", name: str,  age: int, 
                 membership_type: MEMBERSHIP_TYPE, fitness_goals: FITNESS_GOAL):  
        super().__init__(fms)   
        self.name = name
        self.age = age
        self.membership_type = membership_type
        self.fitness_goals = fitness_goals
        self.progresses = {}

    @property
    def Name(self):
        return self.name
    
    @property
    def Age(self):
        return self.age
    
    @property
    def MembershipType(self):
        return self.membership_type
    
    @property
    def FitnessGoals(self):
        return self.fitness_goals

    @property
    def ClassBooking(self):
        return [cl for cl in self.fms.classes.values() if self in cl.members]
    
    def update_membership(self, new_type): 
        self.membership_type = new_type
    
    def book_class(self, class_obj: "FitnessClass"):
        return class_obj.enroll_member(self)

    def track_progress(self, progress_data, goals: FITNESS_GOAL):
        if goals not in self.progresses:
            self.progresses[goals] = []
        self.progresses[goals].append(progress_data)


class Trainer(Base):
    """Represents a fitness trainer."""
    def __init__(self, fms: "FitnessManagementSystem", name: str, specialization: SPECIALIZATION):
        super().__init__(fms)
        self.name = name
        self.specialization = specialization
    
    @property
    def Name(self):
        return self.name
    
    @property
    def Specialization(self):
        return self.specialization
    
    @property
    def AssignedClasses(self):
        return [cl for cl in self.fms.classes.values() if cl.trainer == self]
    
    def assign_class(self, class_obj: "FitnessClass"):
        class_obj.trainer = self


class FitnessClass(Base):
    """Represents a scheduled fitness class."""
    def __init__(self, fms: "FitnessManagementSystem", name: str, trainer: Trainer, 
                 capacity: int, schedule: datetime):
        super().__init__(fms)
        self.name = name
        self.trainer = trainer
        self.capacity = capacity
        self.schedule = schedule
        self.members = set()
    
    @property
    def Name(self):
        return self.name
    
    @property
    def Trainer(self):
        return self.trainer
    
    @Trainer.setter
    def Trainer(self, value):
        self.trainer = value
       
    @property
    def Capacity(self):
        return self.capacity
    
    @property
    def CurrentEnrollments(self):
        return len(self.members)
    
    @property
    def Schedule(self):
        return self.schedule
    
    def enroll_member(self, member: Member):
        if len(self.members) + 1 > self.capacity:
            return False
        
        self.members.add(member)
        return True
    
    def cancel_booking(self, member: Member):
        self.members.discard(member)
 

class Transaction(Base):
    """Represents a payment transaction."""
    def __init__(self, fms: "FitnessManagementSystem", member: Member, amount_paid: float, 
                 paymant_date: datetime, membership_type: MEMBERSHIP_TYPE):
        super().__init__(fms)
        self.member = member

        if amount_paid <= 0:
            raise ValueError(f"The paiment should be positive value")

        self.amount_paid = amount_paid
        self.payment_date = paymant_date
        self.membership_type = membership_type
    
    def generate_receipt(self):
        return (
            f"Receipt for Transaction #{self.ID}\n"
            f"Member: {self.member.Name}\n"
            f"Membership: {self.membership_type.name} (${self.amount_paid})\n"
            f"Date: {self.payment_date.strftime('%Y-%m-%d')}\n"
            f"Amount Paid: ${self.amount_paid}"
        )
    
    @property
    def Member(self):
        return self.member
    
    @property
    def Member(self):
        return self.amount_paid
    
    @property
    def PaymantDate(self):
        return self.paymant_date
    
    @property
    def MembershipType(self):
        return self.membership_type


class FitnessManagementSystem:
    """Central management class for all members, trainers, classes, and transactions."""
    def __init__(self):
        self.members = {}
        self.trainers = {}
        self.classes = {}
        self.transatcions = {}
    
    # ----- Member Management -----
    @property
    def Members(self):
        return self.members

    def view_members(self):
        return list(self.members.values())
    
    def register_member(self, name: str,  age: int, 
                 membership_type: MEMBERSHIP_TYPE, fitness_goals: FITNESS_GOAL): 
        new_member = Member(self, name, age, membership_type, fitness_goals)
        self.members[new_member.ID] = new_member
        return new_member
    
    def cancel_membership(self, member: Member):
        self.members.pop(member.ID)
        for cls in self.classes.values():
            cls.cancel_booking(member)
    
    def view_member_progress(self, member_id):
        member = self.members.get(member_id)
        if not member:
            return None
        return member.progresses
    
    # ----- Trainer Management -----
    @property
    def Trainers(self):
        return self.trainers

    def add_trainer(self, name: str, specialization: SPECIALIZATION):
        new_trainer = Trainer(self, name, specialization)
        self.trainers[new_trainer.ID] = new_trainer
        return new_trainer
    
    def remove_trainer(self, trainer: Trainer):
        self.trainers.pop(trainer.ID)
        for cls in self.classes.values():
            if cls.trainer == trainer:
                 cls.trainer = None
    
    # ----- Class Management -----
    @property
    def Classes(self):
        return self.classes

    def schedule_class(self, name: str, trainer: Trainer, 
                 capacity: int, schedule: datetime):
        new_class = FitnessClass(self, name, trainer, capacity, schedule)
        self.classes[new_class.ID] = new_class
        return new_class
    
    # ----- Transactions -----
    def Transactions(self):
        return self.transatcions

    def process_payment(self, member: Member, amount_paid: float, service: MEMBERSHIP_TYPE): 
        new_transaction = Transaction(self, member, amount_paid, datetime.datetime.now(), service)
        self.transatcions[new_transaction.ID] = new_transaction
        return new_transaction
    
    # Summarizes total earnings from memberships and bookings
    def generate_revenue_report(self): 
        return sum([transaction.amount_paid for transaction in self.transatcions.values()])

        
    

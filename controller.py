from data_model import *
from view import *


class SystemController:
    def __init__(self):
        self.system = FitnessManagementSystem()

    def register_member(self):
        name = SystemView.get_non_empty_string("Enter a member name")     
        age = SystemView.get_int_input(1, 120, "Enter age (1-120)")
        mem_type = SystemView.get_enum_input(MEMBERSHIP_TYPE, "Enter the membership type:")
        f_goal = SystemView.get_enum_input(FITNESS_GOAL, "Enter the goal:")

        new_member = self.system.register_member(name, age, mem_type, f_goal)
        print(f"Member {name} registered successfully with ID {new_member.ID}")


    def view_members(self):
        print("Registered Members:")
        for member in self.system.view_members():
            print(f"ID: {member.ID}, Name: {member.Name}")


    def register_new_trainer(self):
        name = SystemView.get_non_empty_string("Enter a trainer name")     
        spec = SystemView.get_enum_input(SPECIALIZATION, "Enter the trainer specialization:")

        new_trainer = self.system.add_trainer(name, spec)
        print(f"Trainer {name} added successfully with ID {new_trainer.ID}")


    def schedule_new_class(self):
        name = SystemView.get_non_empty_string("Enter a class name")     
        date = SystemView.get_date_input("Enter a class date")
        trainer = SystemView.get_trainer(self.system)
        capacity = SystemView.get_int_input(0, 30, "Enter the class capacity")

        fitness_class = self.system.schedule_class(name, trainer, capacity, date)
        print(f"Fitness class {name} added successfully with ID {fitness_class.ID}")


    def assign_member_to_class(self):
        member = SystemView.get_member(self.system)
        cls = SystemView.get_class(self.system)
        if cls.enroll_member(member) == True:
            print(f"Success. You have added the member {member.ID} to class {cls.ID}")
        else:
            print(f"Fail. Selected class is full")


    def main_interface(self):
        commands = [
            {'descr': "Register New Member", 'method': self.register_member},
            {'descr': "View All Members", 'method': self.view_members},
            {'descr': "Register new trainer'", 'method': self.register_new_trainer},
            {'descr': "Schedule new class'", 'method': self.schedule_new_class},
            {'descr': "Assign member to class'", 'method': self.assign_member_to_class}
            ]

        print("Smart Fitness Management System")
        
        while True:
            exit_number = len(commands) + 1

            for idx, cmd in enumerate(commands, start=1):
                print(f"{idx}. {cmd['descr']}")
            
            print(f"To exit print: {exit_number}")
            comm_number = SystemView.get_int_input(1, exit_number, "Enter a command number")
            
            if comm_number == exit_number:
                print("Good bye!")
                return
            
            try:
                selected_cmd = commands[comm_number - 1]
                selected_cmd['method']()
            except IndexError:
                print("Invalid command number. Try again.")
            except Exception as e:
                print(f"Error executing command: {e}")
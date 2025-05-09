from data_model import *
import datetime


class SystemView:
    @staticmethod
    def get_non_empty_string(prompt: str):
        """Prompts the user to enter a non-empty string."""
        print(prompt)
        while True:
            res_str = input(f"Input non empty string: ")
            if len(res_str) > 0:
                return res_str
    
    @staticmethod
    def get_int_input(min_v: int, max_v: int, prompt: str):
        """Prompts the user for an integer input within a specified range."""
        print(prompt)
        
        while True:
            try:
                vl = int(input(f"Enter a number from {min_v} to {max_v}: "))                            
                if min_v <= vl <= max_v:
                    return vl
            except ValueError:
                print("Invalid input! Please enter a valid int number.")

    @staticmethod
    def get_enum_input(enum_cls, prompt: str):
        """Displays enum options and lets user pick one."""
        print(prompt)
        for item in enum_cls:
            print(f"{item.value}: {item.name}")

        enum_v_list = [e.value for e in enum_cls] 
        min_e = min(enum_v_list)
        max_e = max(enum_v_list)
        
        while True:
            try:
                choice = int(input(f"Enter a number from {min_e} to {max_e}: "))
                return enum_cls(choice)
                
            except ValueError:
                print("Invalid input! Please enter a valid enum number.")
            except KeyError:
                print("Number out of range! Please enter a valid enum number.")

    @staticmethod
    def get_date_input(prompt: str):
        """Prompts the user for a valid date input in YYYY-MM-DD format."""
        print(prompt)
        while True:
            date_str = input("Enter date (YYYY-MM-DD): ")
            try:
                return datetime.datetime.strptime(date_str, "%Y-%m-%d").date()
                break
            except ValueError:
                print("Invalid date format. Please use YYYY-MM-DD")

    @staticmethod
    def get_uuid():
        """Prompts for an integer ID."""
        while True:
            try:
                return int(input(f"Enter an int id: "))         
            except ValueError:
                print("Invalid input! Please enter a valid int number.")

    @staticmethod
    def get_trainer(system: FitnessManagementSystem):
        """Fetches a trainer by ID from the system."""
        print("Enter a trainer ID")

        while True:
            id = SystemView.get_uuid()
            trainer = system.Trainers.get(id)
            if trainer != None:
                return trainer

            print(f"Trainer with id: {id} doesn't exist")
    
    @staticmethod
    def get_member(system: FitnessManagementSystem):
        """Fetches a member by ID from the system."""
        print("Enter a member ID")

        while True:
            id = SystemView.get_uuid()
            member = system.Members.get(id)
            if member != None:
                return member
            
            print(f"Member with id: {id} doesn't exist")

    @staticmethod
    def get_class(system: FitnessManagementSystem):
        """Fetches a fitness class by ID from the system."""
        print("Enter a class ID")

        while True:
            id = SystemView.get_uuid()
            cls = system.Classes.get(id)
            if cls != None:
                return cls
            
            print(f"Class with id: {id} doesn't exist")



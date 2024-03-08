import json
from datetime import datetime
my_datetime_format ='%d/%m/%Y - %H:%M:%S'
class Habit():
    def __init__(self, name, period):
        """initializing the object with the values assigned to it"""
        self.name = name
        self.checked_off = False
        self.broken = False
        self.day_created = datetime.now()
        self.period = period
        self.streak = 0
        self.longest_streak = 0
        self.times_of_completion = []

    def break_off_a_habit(self, day, month, year):
        """breaking off a habit"""
        self.broken = True
        self.checked_off = False
        self.streak = 0

    def making_the_habit_checked_off(self):
        """ checking off a habit"""
        self.broken = False
        self.checked_off = True
        self.times_of_completion.append(datetime.now())
        self.streak += 1
        self.longest_streak = max(self.streak, self.longest_streak)

    def check_for_break(self,year=datetime.today().year, month=datetime.today().month, day=datetime.today().day):
        """checks if the habit exceeds the limited time and breaks off with respect to the time"""
        if len(self.times_of_completion) > 0:
            comp_year = (self.times_of_completion[len(self.times_of_completion)- 1]).year
            comp_month = (self.times_of_completion[len(self.times_of_completion)- 1]).month
            comp_day = (self.times_of_completion[len(self.times_of_completion)-1]).day

            if self.period == "d" and abs(
                    datetime(year, month ,day, 23, 59, 0, 0)
                    - datetime(comp_year, comp_month, comp_day , 23, 59, 0, 0)).days > 1:
                # calculates the difference between the last day it was checked off and today
                self.break_off_a_habit(year, month, day)
                return

            elif self.period == "w" and abs(
                    datetime(  year, month,day, 23, 59, 0, 0)
                    - datetime(comp_year, comp_month, comp_day, 23, 59, 0, 0)).days > 7:
                # calculates the difference between the last week it was checked off and this week
                self.break_off_a_habit( year, month,day)
                return

    def print_habit_info(self):
        """the format for the habit attributes"""
        print(f"0 - Name: {self.name}")
        print(f"1 - Checked off: {self.checked_off}")
        print(f"2 - Broken: {self.broken}")
        print(f"3 - Day Created: {self.day_created.strftime(my_datetime_format)}")
        print(f"4 - Period: {self.period}")
        print(f"5 - Streak: {self.streak}")
        print(f"6 - times_of_completion: {self.times_of_completion}")

    def print_habit_info_user_can_edit(self):
        """the format for the habit attributes when it is done or created by the user"""
        print(f"0 - Name: {self.name}")
        print(f"1 - Day Created: {self.day_created.strftime(my_datetime_format)}")
        print(f"2 - Period: {self.period}")
        print(f"3 - Streak: {self.streak}")
        print(f"6 - times_of_completion: {self.times_of_completion}")


class HabitList():
    def __init__(self):
        self.list_of_all_habits = []
        """ Initialize a list that will contain Habit class."""
        self.import_from_json()
        """ Import the saved habit data."""

    def import_from_json(self):
        """Gets the predefined habits from json file."""
        file = open("list_of_habits.json", 'r')
        read_dict = json.load(file)
        file.close()
        self.habit_dict_to_list(read_dict)

    def export_json_file(self):
        """Updates the JSON file with the new list of habits."""
        my_dict = self.habit_list_to_dict()
        json_file = json.dumps(my_dict, indent=2)
        # Writing to sample.json
        try:
            f = open("list_of_habits.json", "w")
            f.write(json_file)
            f.close()
        except Exception:
            print("Failed to write to file didn't exist, the file is now created")

    def habit_dict_to_list(self, read_dict):
        """changes the dictionary to the list"""
        self.list_of_all_habits = []
        for habit_read in read_dict.values():
            my_habit = Habit(habit_read['name'], habit_read['period'])
            my_habit.day_created = datetime.strptime(habit_read['day_created'], my_datetime_format)
            my_habit.streak = habit_read['streak']
            for time_completion_element in habit_read['times_of_completion']:
                my_habit.times_of_completion.append(datetime.strptime(time_completion_element, my_datetime_format))
            self.list_of_all_habits.append(my_habit)

    def convert_datetime_list_to_string(self, list_to_convert):
        """converts the datetime to string format"""
        converted_list = []
        for e in list_to_convert:
            converted_list.append(e.strftime(my_datetime_format))
        return converted_list

    def habit_list_to_dict(self):
        """converts the list to the dictionary"""
        my_dict = {}
        # dictionary
        i = 0
        for habit in self.list_of_all_habits:
            my_dict[i] = {
                "name": habit.name,
                "period": habit.period,
                "day_created": habit.day_created.strftime(my_datetime_format),
                "streak": habit.streak,
                "times_of_completion": self.convert_datetime_list_to_string(habit.times_of_completion)
            }
            i += 1
        return my_dict

    def print_habit_list(self):
        # called every time the list of habits need to be presented to user
        """prints the list of habits"""
        print("Habits Available:\n")
        for i in range(len(self.list_of_all_habits)):
            print(f"{i}, {self.list_of_all_habits[i].name}")

    def delete_habit(self):
        """Deletes a Habit chosen by user"""
        self.print_habit_list()
        habit_index = int(input(("Type the habit index number you want to delete: ")))
        removed_habit = self.list_of_all_habits.pop(habit_index)
        print(f"Removed Habit: {removed_habit.name}")
        self.print_habit_list()

    def create_new_habit(self):
        """creates a new habit to track"""
        name = input("To create habit, write name: ")
        # print(" Input the date that it is created: day/month/year")
        # day_created = datetime.datetime(day=int(input()), month=int(input()), year=int(input())).now()
        exit = False
        period = ""

        while not exit:
            print("How often do you want to do the habit? \n1. Daily\n 2. Weekly\n Input number of choice: ")
            period_choice = str(input())

            if period_choice == "1":
                period = "d"
                exit = True

            elif period_choice == "2":
                period = "w"
                exit = True

            else:
                print("Invalid input.")
                exit = False

        self.list_of_all_habits.append(Habit(name, period))

    def edit_habit(self):
        """allows user to edit habit"""
        print("Please note that editing the 'day created' and the 'streak'  and 'times of completion'"
              "are not possible due to admin rights")
        self.print_habit_list()
        print(f"Choose which habit to change:\n Enter a number between 0 - {len(self.list_of_all_habits)}")
        user_habit_index = int(input())
        print("Choose what you want to edit:")
        chosen_habit = self.list_of_all_habits[user_habit_index]
        chosen_habit.print_habit_info_user_can_edit()
        print("Enter the number 0 to change the name of the habit or enter 1 to change the period of the habit")
        user_decision = int(input())
        if user_decision == 0:
            print("Enter the new name for the habit selected:")
            user_name = input()
            self.list_of_all_habits[user_habit_index].name = user_name
            print("Habit name changed to:", self.list_of_all_habits[user_habit_index].name)

        if user_decision == 1:
            print("edit the period of the habit by typing the letter:\n 'd' for Daily\n 'w' for Weekly:")
            edited_period = input()
            self.list_of_all_habits[user_habit_index].period = edited_period
            print(self.list_of_all_habits[user_habit_index].period)

    def idle_check_for_break(self):
        """automatically checks if the habit needs to be broken and calls the function that may break it"""
        for habit in self.list_of_all_habits:
            habit.check_for_break()

    def check_off_habit(self):
        """allows user to check-off completed habit.
        Also checks for breaking of the streak"""
        self.print_habit_list()
        print("Enter number of your choice: ")
        choice = int(input())
        chosen_habit = self.list_of_all_habits[choice]

        if chosen_habit.times_of_completion == []:
           chosen_habit.making_the_habit_checked_off()

        else:
            chosen_habit.check_for_break()
            chosen_habit.making_the_habit_checked_off()

def list_all_currently_tracked_habits(list_of_habits):
    """displays the list of all currently tracked habits for the analytics module"""
    for habit in list_of_habits:
        print(habit.name)

def habits_same_periodicity(list_of_habits):
    """ displays the habits with the same periodicity in the analytics module """
    print("Input 1 to display list of daily habits, Input 2 to display list of weekly habits")
    user_decision = int(input())
    if user_decision == 1:
        for i in range(len(list_of_habits)):
            if list_of_habits[i].period == "d":
                print(list_of_habits[i].name)
    elif user_decision == 2:
        for i in range(len(list_of_habits)):
            if list_of_habits[i].period == "w":
                print(list_of_habits[i].name)


def streak_of_all_habits(list_of_habits):
    """gets the streak of all habits"""
    """The longest streak is displayed after the habit has been checked by the user"""
    for i in range(len(list_of_habits)):
        print(list_of_habits[i].longest_streak)

def streak_of_a_given_habit(given_name):
     """gets the streak of one habit"""
     """The longest streak is displayed after the habit has been checked by the user"""
     print(given_name.longest_streak)

def analysis(list_of_habits):
    """display analysis options"""
    print("Choose by typing the number:"
          "\nInput 1 to display a list of all currently tracked habits"
          "\nInput 2 to display a list of all habits with the same periodicity,"
          "\nInput 3 to display the longest run streak of all defined habits"
          "\nInput 4 to display the longest run streak for a given habit"
          )
    decision = int(input())
    # list all current tracked habits
    if decision == 1:
        list_all_currently_tracked_habits(list_of_habits)

    elif decision == 2:
    # return a list of all habits with the same periodicity,
        habits_same_periodicity(list_of_habits)


    elif decision == 3:
    # return the longest run streak of all defined habits,
        streak_of_all_habits(list_of_habits)

    elif decision == 4:
        # return the longest run streak for a given habit.
        h1 = HabitList()
        h1.print_habit_list()
        print(f"type the number of habit you wish "
            f"to display the longest streak for:\n Enter a number between 0 - {len(list_of_habits)}")
        i = int(input())
        streak_of_a_given_habit(list_of_habits[i])

def display_main_options(h):
    """ This is the menu to decide what the user wants to do in the Habit tracker app """
    while True:
        """ This is a loop that will keep putting this menu over and over again until the user
         decides to exit by inputting the number 9 """
        print(
            "Decide what to do:"
            "\nInput 1 if you want to create habit"
            "\nInput 2 if you want to delete habit"
            "\nInput 3 if you want to edit a habit:"
            "\nInput 4 if you want to check-off a habit"
            "\nInput 5 if you want to display the list of habits:"
            "\nInput 6 if you to import to the json file"
            "\nInput 7 if you to export from the json file"
            "\nInput 8 if you want to analyze a habit"
            "\nInput 9 if you want to exit"
        )
        user_decision = int(input())
        h.idle_check_for_break()
        if user_decision == 1:
            print("calling the function that will allow user to create habit")
            h.create_new_habit()
            h.export_json_file()
        elif user_decision == 2:
            print("calling the function that will delete a habit from the list")
            h.delete_habit()
            h.export_json_file()

        elif user_decision == 3:
            print("calling the function that will edit a habit from the list")
            h.edit_habit()
            h.export_json_file()

        elif user_decision == 4:
            print("calling the function that will check-off a habit")
            h.check_off_habit()
            h.export_json_file()

        elif user_decision == 5:
            print("display list of habits")
            my_habits.print_habit_list()

        elif user_decision == 6:
            print("calling function to import to json file")
            h.import_from_json()


        elif user_decision == 7:
            print("calling function to export from json file")
            h.export_json_file()

        elif user_decision == 8:
             print("Displaying the habit analysis")
             analysis(h.list_of_all_habits)

        elif user_decision == 9:
            print("exiting app...")
            break


if __name__ == "__main__":
    """this is where the program will start executing the commands"""
    my_habits = HabitList()
    my_habits.import_from_json()
    display_main_options(my_habits)


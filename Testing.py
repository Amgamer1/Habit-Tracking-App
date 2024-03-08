
import unittest
from main import Habit, HabitList, analysis

class Test_Habits(unittest.TestCase):

    def test_break_off_a_habit(self):
        h1 = Habit("Laundry", "w")
        h1.break_off_a_habit(12, 8, 2020)
        self.assertEqual(h1.broken, True)
        self.assertEqual(h1.checked_off, False)
        self.assertEqual(h1.streak, 0)

    def test_making_the_habit_checked_off(self):
        h1 = Habit("Laundry", "w")
        h1.making_the_habit_checked_off()
        self.assertEqual(h1.broken, False)
        self.assertEqual(h1.checked_off, True)
        self.assertEqual(len(h1.times_of_completion) > 0, True)
        self.assertEqual(h1.streak > 0, True)

    def test_check_for_break(self):
        h1 = Habit("Laundry", "w")
        h1.making_the_habit_checked_off()
        h1.check_for_break(
           year=2000,
           month=10,
           day=13
        )
        self.assertEqual(h1.broken, True)

    def test_to_import_from_json(self):
        # The import json function is getting called from the HabitList() class when we call it here
        self.assertEqual(len(HabitList().list_of_all_habits) > 1 , True )

    def test_to_export_json_file(self):
        h1 = HabitList()
        h1.export_json_file()
        h1.import_from_json() #checking the data after the file got updated
        self.assertEqual(len(h1.list_of_all_habits) > 1, True)


    def test_delete_habit(self):
        h1 = HabitList()
        num_habit = len(h1.list_of_all_habits)
        h1.delete_habit()
        self.assertEqual(len(h1.list_of_all_habits) < num_habit, True)

# to do: habit analysis functions

    def test_habit_analysis_option_1(self):
        h1 = HabitList()
        print("please select option 1")
        analysis(h1.list_of_all_habits)
        print(f"Did all {len(h1.list_of_all_habits)} current tracked habits got displayed?\n reply with Y/N")
        user_input = input()
        self.assertTrue(user_input.upper() == "Y")

    def test_habit_analysis_option_2_input_1(self):
        h1 = HabitList()
        print("please select option 2 and select daily")
        analysis(h1.list_of_all_habits)
        print("Did the habits got displayed as daily?\n reply with Y/N")
        user_input = input()
        self.assertTrue(user_input.upper() == "Y")

    def test_habit_analysis_option_2_input_2(self):
        h1 = HabitList()
        print("please select option 2 and select weekly ")
        analysis(h1.list_of_all_habits)
        print("Did the habits got displayed as weekly?\n reply with Y/N")
        user_input = input()
        self.assertTrue(user_input.upper() == "Y")

    def test_habit_analysis_option_3(self):
        h1 = HabitList()
        print("please select option 3")
        analysis(h1.list_of_all_habits)
        print(f"Did the longest streak of all habits got displayed?\n reply with Y/N")
        user_input = input()
        self.assertTrue(user_input.upper() == "Y")

    def test_habit_analysis_option_4(self):
        h1 = HabitList()
        print("please select option 4")
        analysis(h1.list_of_all_habits)
        print(f"Did a given streak of a habit got displayed?\n reply with Y/N")
        user_input = input()
        self.assertTrue(user_input.upper() == "Y")

if __name__ == '__main__':
    unittest.main()






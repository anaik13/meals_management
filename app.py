import pandas as pd
import os
import json

os.chdir(r'C:\Users\anaik\Desktop\data_science_nauka\python\python_projects\meals_management\data')

class MealsManager():

    MEAL_TYPES = ['breakfast', 'supper', 'lunch', 'snacks', 'for parties']


    def __init__(self):
        pass


    def __read_file(self, file_name):
        with open(file_name) as file:
            data = json.load(file)
        return data


    def __collect_meals(self):
        meals = list()
        for file_name in os.listdir():
            tmp_meal = self.__read_file(file_name)
            meals.append(tmp_meal)
        return meals


    def list_meals(self, meal_type=None): # !
        meals = self.__collect_meals()
        meal_names = list()
        if meal_type:
            for meal in meals:
                if meal['meal_type'] == meal_type:
                    meal_names.append(meal['meal_name'])
            return meal_names
        else:
            for meal in meals:
                meal_names.append(meal['meal_name'])
            return meal_names


    def __save_new_meal(self, new_meal):
        file_name = new_meal['meal_name'].lower().replace(' ', '_') + '.json'
        with open(file_name, 'w') as file:
            json.dump(new_meal, file)


    def add_new_meal(self, meal_name, meal_type, ingredients, url):
        new_meal = {'meal_name': meal_name, 'meal_type': meal_type, 'ingredients': ingredients, 'url': url}
        self.__save_new_meal(new_meal)


meals_12032022 = MealsManager()

print(meals_12032022.list_meals())
print(meals_12032022.list_meals('snack'))
meals_12032022.add_new_meal('meal_name', 'meal_type', 'ingredients', 'url')
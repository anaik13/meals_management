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
        new_meal = {'meal_name': meal_name, 'meal_type': meal_type, 'ingredients': ingredients, 'url': url} #  TODO: ingredients should be a list
        self.__save_new_meal(new_meal)

    def __intersect_lists(self, list1, list2):
        return list(set(list1) & set(list2))


    def search_by_ingredients(self, specified_ingredients):
        meals = self.__collect_meals()
        meals_with_specified_ingredients = list()

        for meal in meals:
            intersected_ingredients = self.__intersect_lists(meal['ingredients'], specified_ingredients)
            if len(intersected_ingredients) == len(specified_ingredients):
                meals_with_specified_ingredients.append({'meal_name': meal['meal_name'], 'ingredients': meal['ingredients']})
        if meals_with_specified_ingredients:
            return meals_with_specified_ingredients
        else:
            return 'No meals with specified ingredients found.'


meals_12032022 = MealsManager()

# print(meals_12032022.list_meals())
# print(meals_12032022.list_meals('snack'))
# meals_12032022.add_new_meal('meal_name', 'meal_type', 'ingredients', 'url')

print(meals_12032022.search_by_ingredients(['szczypiorek']))

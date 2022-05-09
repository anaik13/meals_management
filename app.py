import pandas as pd
import os
import json

os.chdir(r'C:\Users\anaik\Desktop\data_science_nauka\python\python_projects\meals_management')

class MealsManager():

    MEAL_TYPES = ['breakfast', 'supper', 'lunch', 'snacks', 'for parties'] # TODO


    def __init__(self, report_start_date, report_end_date):
        self.report_start_date = report_start_date
        self.report_end_date = report_end_date

    @staticmethod
    def __read_file(file_name, folder_name):
        with open(folder_name + '/' + file_name) as file:
            data = json.load(file)
        return data


    @staticmethod
    def __collect_meals():
        meals = list()
        for file_name in os.listdir('data'):
            tmp_meal = MealsManager.__read_file(file_name, 'data')
            meals.append(tmp_meal)
        return meals

    @staticmethod
    def list_meals(meal_type=None): # !
        meals = MealsManager.__collect_meals()
        meal_names = list()
        if meal_type:
            for meal in meals:
                if meal['suggested_meal_type'] == meal_type:
                    meal_names.append(meal['meal_name'])
            return meal_names
        else:
            for meal in meals:
                meal_names.append(meal['meal_name'])
            return meal_names


    @staticmethod
    def __write_json_file(data, file_name, file_mode, folder_name):
        with open(folder_name + '/' + file_name, file_mode) as file:
            json.dump(data, file)


    @staticmethod
    def add_new_meal(meal_name, suggested_meal_type, ingredients, url):
        new_meal = {'meal_name': meal_name, 'suggested_meal_type': suggested_meal_type, 'ingredients': ingredients, 'url': url} #  TODO: ingredients should be a list
        file_name = new_meal['meal_name'].lower().replace(' ', '_') + '.json'
        MealsManager.__write_json_file(new_meal, file_name, 'w', 'data')

    @staticmethod
    def __intersect_lists(list1, list2):
        return list(set(list1) & set(list2))

    @staticmethod
    def search_by_ingredients(specified_ingredients):
        meals = MealsManager.__collect_meals()
        meals_with_specified_ingredients = list()

        for meal in meals:
            intersected_ingredients = MealsManager.__intersect_lists(meal['ingredients'], specified_ingredients)
            if len(intersected_ingredients) == len(specified_ingredients):
                meals_with_specified_ingredients.append({'meal_name': meal['meal_name'], 'ingredients': meal['ingredients']})
        if meals_with_specified_ingredients:
            return meals_with_specified_ingredients
        else:
            return 'No meals with specified ingredients found.'


    @staticmethod
    def __return_meal_by_name(meal_name):
        meal_name_formatted = meal_name.lower().replace(' ', '_')
        meal = MealsManager.__read_file(meal_name_formatted + '.json', 'data')
        return meal


    def add_meal_to_report(self, meal_name, meal_date, meal_type, portion):
        meal = MealsManager.__return_meal_by_name(meal_name)

        try:
            added_meals = MealsManager.__read_file(self.report_start_date + '_' + self.report_end_date + '.json', 'meal_reports')
            report_exists = 1
        except FileNotFoundError:
            report_exists = 0

        file_name = self.report_start_date + '_' + self.report_end_date + '.json'

        # Increase portion number instead of adding new meal in case of adding a repeated meal
        if report_exists:
            meal_added_earlier = 0
            meal_name_formatted = meal_name.lower().replace(' ', '_')
            for idx, added_meal in enumerate(added_meals):

                if added_meal['meal_name'] == meal_name_formatted:
                    added_meals[idx]['portion'] += portion
                    added_meal['meal_date'].append(meal_date)
                    meal_added_earlier = 1

            if meal_added_earlier:
                MealsManager.__write_json_file(added_meals, file_name, 'w', 'meal_reports')
            else:
                del meal['suggested_meal_type']
                meal['meal_date'] = [meal_date]
                meal['meal_type'] = meal_type
                meal['portion'] = portion
                added_meals.append(meal)
                MealsManager.__write_json_file(added_meals, file_name, 'w', 'meal_reports')

        else: # Add new meal to report
            # Add additional information about meal
            del meal['suggested_meal_type']
            meal['meal_date'] = [meal_date]
            meal['meal_type'] = meal_type
            meal['portion'] = portion
            added_meals = [meal]

            MealsManager.__write_json_file(added_meals, file_name, 'w', 'meal_reports')


    def create_meals_summary(self):
        try:
            meals = MealsManager.__read_file(self.report_start_date + '_' + self.report_end_date + '.json', 'meal_reports')
            report_exists = 1
        except FileNotFoundError:
            report_exists = 0

        if report_exists:
            meal_dates = dict()
            for meal in meals:
                if meal['date'] in meal_dates:
                    meal_dates[meal['meal_names']].append(meal['meal_name'])
                else:
                    meal_dates[meal['meal_names']] = meal['meal_name']

            # Sort meals by dates
                sorted(meal_dates)

        else:
            print(f'There is no added meals for date {self.report_start_date} - {self.report_end_date}.')

    def create_shopping_list(self):
        try:
            meals = MealsManager.__read_file(self.report_start_date + '_' + self.report_end_date + '.json', 'meal_reports')
            report_exists = 1
        except FileNotFoundError:
            report_exists = 0

        if report_exists:
            ingredients = dict()
            for meal in meals:
                for ingredient in meal['ingredients']:
                    ingredients[ingredient] =+ meal['portion'] #  TODO: Currently there is an assumption that for every meal we need 1 portion of each ingredient
            # Save shopping list to file
            file_name = self.report_start_date + '_' + self.report_end_date + '.json'
            MealsManager.__write_json_file(ingredients, file_name, 'w', 'shopping_lists')
        else:
            print(f'There is no added meals for date {self.report_start_date} - {self.report_end_date}.')


meals_12032022 = MealsManager('20220321', '20210327')

# print(meals_12032022.list_meals())
# print(meals_12032022.list_meals('snack'))
# meals_12032022.add_new_meal('meal_name', 'suggested_meal_type', ['ingredients', 'szczypiorek'], 'url')
# print(meals_12032022.search_by_ingredients(['szczypiorek']))

meals_12032022.add_meal_to_report('Koktajl truskawkowy', '2022-03-26', 'snack', 1)
meals_12032022.add_meal_to_report('Bułka zapiekana z jajkiem', '2022-03-26', 'breakfast', 1)
meals_12032022.add_meal_to_report('Koktajl truskawkowy', '2022-03-27', 'snack', 1)

# meals_12032022.create_shopping_list()



# # TODO:
# - zestawienie tygodniowe (jakie dania oraz ile danych produktow do kupienia)
# - dodanie potraw na dany tydzien
# - wylistowanie potraw z zestawienia
# - dodanie/usuniecie dania z zestawienia
# + wygenerowanie pdf z lista zakupow
#
# - dodanie kategorii skladnikow (np. nabial, pieczywo, itp.)
# - sortowanie listy zakupow zgodnie z konkretna kolejnoscia





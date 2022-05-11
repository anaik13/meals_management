import json
import os

os.chdir(r'C:\Users\anaik\Desktop\praca_nauka\python\python_projects\meals_management')


class MealsManager():

    MEAL_TYPES_IN_ORDER = ['breakfast', 'lunch', 'supper', 'snack', 'for parties']

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
            meal = MealsManager.__read_file(file_name, 'data')
            meals.append(meal)
        return meals

    @staticmethod
    def __write_json_file(data, file_name, file_mode, folder_name):
        with open(folder_name + '/' + file_name, file_mode) as file:
            json.dump(data, file)

    @staticmethod
    def __intersect_lists(list1, list2):
        return list(set(list1) & set(list2))

    @staticmethod
    def __return_meal_by_name(meal_name):
        meal_name_formatted = meal_name.lower().replace(' ', '_')
        meal = MealsManager.__read_file(meal_name_formatted + '.json', 'data')
        return meal

    @staticmethod
    def list_meals(meal_type=None):
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
    def add_new_meal(meal_name, suggested_meal_type, ingredients, url):
        new_meal = {
            'meal_name': meal_name,
            'suggested_meal_type': suggested_meal_type,
            'ingredients': ingredients,
            'url': url
        }
        file_name = new_meal['meal_name'].lower().replace(' ', '_') + '.json'
        MealsManager.__write_json_file(new_meal, file_name, 'w', 'data')

    @staticmethod
    def search_by_ingredients(specified_ingredients):
        meals = MealsManager.__collect_meals()
        meals_with_specified_ingredients = list()

        for meal in meals:
            intersected_ingredients = MealsManager.__intersect_lists(list(meal['ingredients'].keys()), specified_ingredients)
            if len(intersected_ingredients) == len(specified_ingredients):
                meals_with_specified_ingredients.append({'meal_name': meal['meal_name'], 'ingredients': meal['ingredients']})
        if meals_with_specified_ingredients:
            return meals_with_specified_ingredients
        else:
            return 'No meals with specified ingredients found.'

    def add_meal_to_report(self, meal_name, meal_date, meal_type, portion):
        meal = MealsManager.__return_meal_by_name(meal_name)

        if meal_type not in self.MEAL_TYPES_IN_ORDER:
            print(f'You specified unknown meal type. Available meal types: {self.MEAL_TYPES_IN_ORDER}')

        try:
            file_name = self.report_start_date + '_' + self.report_end_date + '.json'
            added_meals = MealsManager.__read_file(file_name, 'meal_reports')
            report_exists = 1
        except FileNotFoundError:
            report_exists = 0


        meal['meal_date'] = meal_date
        meal['meal_type'] = meal_type
        meal['portion'] = portion
        del meal['suggested_meal_type']

        if report_exists:
            added_meals.append(meal)
        else:
            added_meals = [meal]

        MealsManager.__write_json_file(added_meals, file_name, 'w', 'meal_reports')


    def delete_meal_from_report(self, meal_date, meal_name, meal_type):
        try:
            file_name = self.report_start_date + '_' + self.report_end_date + '.json'
            meals = MealsManager.__read_file(file_name, 'meal_reports')
        except FileNotFoundError:
            print(f'There is no added meals for date {self.report_start_date} - {self.report_end_date}.')
            return

        meal_deleted = 0
        for meal_idx, meal in enumerate(meals.copy()):
            if meal['meal_date'] == meal_date and meal['meal_name'] == meal_name:
                meals.pop(meal_idx)
                meal_deleted = 1

        if meal_deleted:
            MealsManager.__write_json_file(meals, file_name, 'w', 'meal_reports')
        else:
            print('There is NO meals in report which you specified.')

    def create_report_summary(self):
        try:
            file_name = self.report_start_date + '_' + self.report_end_date + '.json'
            meals = MealsManager.__read_file(file_name, 'meal_reports')
        except FileNotFoundError:
            print(f'There is no added meals for date {self.report_start_date} - {self.report_end_date}.')
            return

        # Sort meals by date and meal_type
        meal_type_order = {key: i for i, key in enumerate(self.MEAL_TYPES_IN_ORDER)}
        meals = sorted(meals, key=lambda x: meal_type_order[x['meal_type']])
        meals = sorted(meals, key=lambda x: x['meal_date'])

        # Print meals after sorting
        print('Meals sorted by day and meal type:')
        analysed_date = meals[0]['meal_date']
        print(analysed_date)
        for meal in meals:
            if analysed_date == meal['meal_date']:
                print(meal)
            else:
                analysed_date = meal['meal_date']
                print(analysed_date)
                print(meal)


        # Aggregate meals by name - calculate quantity of meals
        meals_quantity = dict()
        for meal in meals:
            meal_name = meal['meal_name']
            meal_portion = meal['portion']
            if meal_name in meals_quantity:
                meals_quantity[meal_name] += meal_portion
            else:
                meals_quantity[meal_name] = meal_portion

        # Print meals after aggregating
        print('Meals aggregated by meal name:')
        print(meals_quantity)

    def create_shopping_list(self):
        try:
            file_name = self.report_start_date + '_' + self.report_end_date + '.json'
            meals = MealsManager.__read_file(file_name, 'meal_reports')
        except FileNotFoundError:
            print(f'There is no added meals for date {self.report_start_date} - {self.report_end_date}.')
            return

        shopping_list = dict()
        for meal in meals:
            for ingredient in meal['ingredients']:
                if ingredient in shopping_list:
                    shopping_list[ingredient]['quantity'] += meal['portion'] * meal['ingredients'][ingredient]['quantity']
                else:
                    shopping_list[ingredient] = dict()
                    shopping_list[ingredient]['quantity'] = meal['portion'] * meal['ingredients'][ingredient]['quantity']
                    shopping_list[ingredient]['unit'] = meal['ingredients'][ingredient]['unit']

        # Save shopping list to file
        MealsManager.__write_json_file(shopping_list, file_name, 'w', 'shopping_lists')


meals_12032022 = MealsManager('20220321', '20210327')

# print(meals_12032022.list_meals())
# print(meals_12032022.list_meals('snack'))
# meals_12032022.add_new_meal('meal_name', 'suggested_meal_type', {'wanilia': {'quantity': 2, 'unit': 'peace'}}, 'url')
# print(meals_12032022.search_by_ingredients(['szczypiorek']))

# meals_12032022.add_meal_to_report('Koktajl truskawkowy', '2022-03-26', 'snack', 1)
# meals_12032022.add_meal_to_report('Bułka zapiekana z jajkiem', '2022-03-26', 'breakfast', 1)
# meals_12032022.add_meal_to_report('Koktajl truskawkowy', '2022-03-27', 'snack', 1)

# meals_12032022.create_report_summary()
# meals_12032022.create_shopping_list()
#
# meals_12032022.delete_meal_from_report('2022-03-27', 'koktajl_truskawkowy', 'snack')



# # TODO:
# - wygenerowanie podsumowania i listy zakupow jako pdf/word
# - dodanie kategorii skladnikow (np. nabial, pieczywo, itp.)
# - sortowanie listy zakupow zgodnie z konkretna kolejnoscia





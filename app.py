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
        """
        List all meals with specified meal type or all meals added to data folder.
        :param meal_type str
        :return: list
        """
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
        """
        Add new meal to data folder.
        :param meal_name str
        :param suggested_meal_type str
        :param ingredients list(str)
        :param url str
        """
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
        """
        List meals which contain specified ingredients.
        :param specified_ingredients list
        :return: list(dict)
        """
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
        """Add meal to report for specified date, with meal type and meal portion."""
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
        """
        Delete specified meal from report. Define meal date, name and type to find a particular meal in report.
        :param meal_date str
        :param meal_name str
        :param meal_type str
        """
        try:
            file_name = self.report_start_date + '_' + self.report_end_date + '.json'
            meals = MealsManager.__read_file(file_name, 'meal_reports')
        except FileNotFoundError:
            print(f'There is no added meals for date {self.report_start_date} - {self.report_end_date}.')
            return

        meal_deleted = 0
        for meal_idx, meal in enumerate(meals.copy()):
            if meal['meal_date'] == meal_date and meal['meal_name'] == meal_name and meal['meal_type'] == meal_type:
                meals.pop(meal_idx)
                meal_deleted = 1

        if meal_deleted:
            MealsManager.__write_json_file(meals, file_name, 'w', 'meal_reports')
        else:
            print('There is NO meals in report which you specified.')

    def create_report_summary(self):
        """
        Create summary of report - sorted by date and meal type list of meals as well as a quantitative summary of meals.
        """
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
        """
        Create a shopping list based on meals report.
        """
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






# Example


meals_20220321 = MealsManager('20220321', '20220327')

print(meals_20220321.list_meals())

print(meals_20220321.list_meals(meal_type='snack'))

meals_20220321.add_new_meal(
    meal_name='meal_name',
    suggested_meal_type='suggested_meal_type',
    ingredients={'wanilia': {'quantity': 2, 'unit': 'peace'}},
    url='url'
)
print(meals_20220321.search_by_ingredients(
    specified_ingredients=['szczypiorek'])
)

meals_20220321.add_meal_to_report(
    meal_name='Koktajl truskawkowy',
    meal_date='2022-03-26',
    meal_type='snack',
    portion=1
)
meals_20220321.add_meal_to_report(
    meal_name='Bułka zapiekana z jajkiem',
    meal_date='2022-03-26',
    meal_type='breakfast',
    portion=1
)
meals_20220321.add_meal_to_report(
    meal_name='Koktajl truskawkowy',
    meal_date='2022-03-27',
    meal_type='snack',
    portion=1
)

meals_20220321.delete_meal_from_report(
    meal_date='2022-03-27',
    meal_name='koktajl_truskawkowy',
    meal_type='snack'
)

meals_20220321.create_report_summary()

meals_20220321.create_shopping_list()

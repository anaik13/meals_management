# Meals management app

This application can be used to plan meals.


### Available functionalities

- list_meals() - List all meals with specified meal type or all meals added to data folder.
- add_new_meal() - Add new meal to data folder.
- search_by_ingredients() - List meals which contain specified ingredients.
---
- add_meal_to_report() - Add meal to report for specified date, with meal type and meal portion.
- delete_meal_from_report() - Delete specified meal from report. Define meal date, name and type to find a particular meal in report.
---
- create_report_summary() - Create summary of report - sorted by date and meal type list of meals as well as a quantitative summary of meals.
- create_shopping_list() - Create a shopping list based on meals report
---


### Example of use

```python
meals_20220321 = MealsManager('20220321', '20220327')
```

```python
print(meals_12032022.list_meals())

print(meals_12032022.list_meals(meal_type='snack'))

meals_12032022.add_new_meal(
    meal_name='meal_name',
    suggested_meal_type='suggested_meal_type',
    ingredients={'wanilia': {'quantity': 2, 'unit': 'peace'}},
    url='url'
)
print(meals_12032022.search_by_ingredients(
    specified_ingredients=['szczypiorek'])
)
```

```python
meals_12032022.add_meal_to_report(
    meal_name='Koktajl truskawkowy',
    meal_date='2022-03-26',
    meal_type='snack',
    portion=1
)
meals_12032022.add_meal_to_report(
    meal_name='Bułka zapiekana z jajkiem',
    meal_date='2022-03-26',
    meal_type='breakfast',
    portion=1
)
meals_12032022.add_meal_to_report(
    meal_name='Koktajl truskawkowy',
    meal_date='2022-03-27',
    meal_type='snack',
    portion=1
)

meals_12032022.delete_meal_from_report(
    meal_date='2022-03-27',
    meal_name='koktajl_truskawkowy',
    meal_type='snack'
)
```

```python
meals_12032022.create_report_summary()

meals_12032022.create_shopping_list()
```
ing = ['aa', 'bb', 'cc']
ing_input = ['aa', 'bb']


def intersection(list1, list2):
    return list(set(list1) & set(list2))

intersected_ingredients = intersection(ing, ing_input)

if len(intersected_ingredients) == len(ing_input):
    print(ing_input)
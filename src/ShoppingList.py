from src.Ingredient import Ingredient


class ShoppingList:
    def __init__(self):
        self._items = []  # список кортежей (ingredient, recipe_title)

    def add_recipe(self, recipe, portions):
        if portions <= 0:
            raise ValueError("Количество порций должно быть положительным")
        scaled_recipe = recipe.scale(portions)
        for ing in scaled_recipe.ingredients:
            self._items.append((ing, recipe.title))

    def remove_recipe(self, title):
        self._items = [item for item in self._items if item[1] != title]

    def get_list(self):
        temp = {}
        for ing, recipe_title in self._items:
            key = (ing.name, ing.unit)
            if key in temp:
                temp[key] += ing.quantity
            else:
                temp[key] = ing.quantity
        result = [Ingredient(name, quantity, unit) for (name, unit), quantity in temp.items()]
        result.sort(key=lambda ing: ing.name)
        return result

    def __add__(self, other):
        new_list = ShoppingList()
        new_list._items = self._items + other._items
        return new_list
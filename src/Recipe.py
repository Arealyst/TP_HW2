from src.Ingredient import Ingredient


class Recipe:
    def __init__(self, title, ingredients):
        self.title = title
        self.ingredients = ingredients

    def add_ingredient(self, ingredient):
        for ing in self.ingredients:
            if ing == ingredient:   # используем __eq__ из Ingredient
                ing.quantity += ingredient.quantity
                return
        self.ingredients.append(ingredient)

    @staticmethod
    def is_valid_ratio(ratio):
        try:
            return ratio > 0
        except:
            return False

    def scale(self, ratio):
        if not self.is_valid_ratio(ratio):
            raise ValueError("ratio должно быть положительным числом")
        new_ingredients = []
        for ing in self.ingredients:
            new_quantity = ing.quantity * ratio
            new_ing = Ingredient(ing.name, new_quantity, ing.unit)
            new_ingredients.append(new_ing)
        return Recipe(self.title, new_ingredients)

    def __len__(self):
        return len(self.ingredients)

    def __str__(self):
        line = f"{self.title}:"
        for ing in self.ingredients:
            line += f" {ing},"
        line = line[:-1]
        return line
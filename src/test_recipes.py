import pytest

from src.Ingredient import Ingredient
from src.Recipe import Recipe
from src.ShoppingList import ShoppingList


class TestIngredient:
    def test_creation(self):
        ing = Ingredient("Мука", 500.0, "г")
        assert ing.name == "Мука"
        assert ing.quantity == 500.0
        assert ing.unit == "г"

    def test_str(self):
        ing = Ingredient("Мука", 500.0, "г")
        assert str(ing) == "Мука: 500.0 г"

    def test_eq_same_name_unit(self):
        ing1 = Ingredient("Мука", 500, "г")
        ing2 = Ingredient("Мука", 1000, "г")
        assert ing1 == ing2

    def test_eq_different_name(self):
        ing1 = Ingredient("Мука", 500, "г")
        ing2 = Ingredient("Соль", 500, "г")
        assert ing1 != ing2

    def test_eq_different_unit(self):
        ing1 = Ingredient("Мука", 500, "г")
        ing2 = Ingredient("Мука", 500, "кг")
        assert ing1 != ing2


class TestRecipe:
    def test_creation(self):
        r = Recipe("Омлет", [Ingredient("Яйцо", 3, "шт"), Ingredient("Молоко", 50, "мл")])
        assert r.title == "Омлет"
        assert r.ingredients == [Ingredient("Яйцо", 3, "шт"), Ingredient("Молоко", 50, "мл")]

    def test_add_ingredient_new(self):
        r = Recipe("Омлет", [Ingredient("Яйцо", 3, "шт")])
        ing = Ingredient("Молоко", 50, "мл")
        r.add_ingredient(ing)
        assert r.ingredients[1] is ing

    def test_add_ingredient_existing(self):
        r = Recipe("Омлет", [Ingredient("Яйцо", 2, "шт")])
        ing = Ingredient("Яйцо", 1, "шт")
        r.add_ingredient(ing)
        assert r.ingredients[0].quantity == 3

    def test_scale(self):
        r = Recipe("Омлет", [Ingredient("Яйцо", 3, "шт"), Ingredient("Молоко", 50, "мл")])
        scaled = r.scale(3)
        assert scaled is not r
        assert len(scaled.ingredients) == 2
        assert scaled.ingredients[0].quantity == 9
        assert scaled.ingredients[1].quantity == 150
        assert scaled.title == r.title

    def test_scale_invalid_ratio(self):
        r = Recipe("Омлет", [Ingredient("Яйцо", 3, "шт"), Ingredient("Молоко", 50, "мл")])
        with pytest.raises(ValueError, match="ratio должно быть положительным числом"):
            r.scale(-1)

    def test_len(self):
        r = Recipe("Омлет", [Ingredient("Яйцо", 3, "шт"), Ingredient("Молоко", 50, "мл")])
        assert len(r) == 2


class TestShoppingList:
    def test_add_recipe(self):
        r = Recipe("Омлет", [Ingredient("Яйцо", 3, "шт")])
        sl = ShoppingList()
        sl.add_recipe(r, 2)
        assert len(sl._items) == 1
        ing, title = sl._items[0]
        assert ing.name == "Яйцо"
        assert ing.quantity == 6
        assert title == "Омлет"

    def test_add_recipe_invalid_portions(self):
        r = Recipe("Омлет", [Ingredient("Яйцо", 3, "шт")])
        sl = ShoppingList()
        with pytest.raises(ValueError, match="Количество порций должно быть положительным"):
            sl.add_recipe(r, -1)

    def test_remove_recipe(self):
        r1 = Recipe("Омлет", [Ingredient("Яйцо", 3, "шт")])
        r2 = Recipe("Салат", [Ingredient("Огурец", 1, "шт")])
        sl = ShoppingList()
        sl.add_recipe(r1, 1)
        sl.add_recipe(r2, 1)
        assert len(sl._items) == 2
        sl.remove_recipe("Омлет")
        assert len(sl._items) == 1
        assert sl._items[0][1] == "Салат"
        sl.remove_recipe("")

    def test_get_list(self):
        r1 = Recipe("Омлет", [Ingredient("Яйцо", 3, "шт")])
        r2 = Recipe("Салат", [Ingredient("Огурец", 1, "шт"), Ingredient("Яйцо", 2, "шт")])
        sl = ShoppingList()
        sl.add_recipe(r1, 1)
        sl.add_recipe(r2, 2)
        result = sl.get_list()
        assert len(result) == 2
        assert result[0].name == "Огурец"
        assert result[0].quantity == 2
        assert result[1].name == "Яйцо"
        assert result[1].quantity == 7

    def test_add(self):
        sl1 = ShoppingList()
        r1 = Recipe("Омлет", [Ingredient("Яйцо", 2, "шт")])
        sl1.add_recipe(r1, 1)

        sl2 = ShoppingList()
        r2 = Recipe("Салат", [Ingredient("Огурец", 1, "шт")])
        sl2.add_recipe(r2, 1)

        sl3 = sl1 + sl2
        assert sl3 is not sl1
        assert sl3 is not sl2
        assert len(sl3._items) == 2
        assert len(sl1._items) == 1
        assert len(sl2._items) == 1

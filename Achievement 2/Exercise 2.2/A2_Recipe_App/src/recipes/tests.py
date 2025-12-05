from django.test import TestCase
from .models import Recipe

class RecipeModelTest(TestCase):
    def setUpTestData():
        Recipe.objects.create(
            name='Coffee', 
            ingredients='Water, Coffee Beans, Cream, Sugar',
            cooking_time=5
        )

    # Name field label
    def test_recipe_name(self):
        recipe = Recipe.objects.get(id=1)
        label = recipe._meta.get_field("name").verbose_name

        self.assertEqual(label, "name")

    # Max length for Name field
    def test_recipe_name_max_length(self):
        recipe = Recipe.objects.get(id=1)
        max_length = recipe._meta.get_field("name").max_length

        self.assertEqual(max_length, 50)

    # Ingredients max length
    def test_ingredients_max_length(self):
        recipe = Recipe.objects.get(id=1)
        max_length = recipe._meta.get_field("ingredients").max_length

        self.assertEqual(max_length, 225)

    # Type value for cooking_time
    def test_cooking_time_type(self):
        recipe = Recipe.objects.get(id=1)
        self.assertIsInstance(recipe.cooking_time, int)

    # Test difficulty calculation
    def test_calculate_difficulty(self):
        recipe = Recipe.objects.get(id=1)
        self.assertEqual(recipe.calculate_difficulty, "Medium")

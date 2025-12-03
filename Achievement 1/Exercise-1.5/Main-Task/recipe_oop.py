class Recipe:
    all_ingredients = set()

    def __init__ (self, name, ingredients, cooking_time):
        self.name = name
        self.ingredients = set(ingredient.strip().lower() for ingredient in ingredients)
        self.cooking_time = cooking_time
        self.difficulty = None
        self.difficulty = self.calculate_difficulty(cooking_time, self.ingredients)
        self.update_all_ingredients()

    # Calculate recipe difficulty
    def calculate_difficulty(self, cooking_time, ingredients):
        num_ingredients = len(ingredients)

        if cooking_time < 10 and num_ingredients < 4:
            difficulty = "Easy"
        elif cooking_time < 10 and num_ingredients >= 4:
            difficulty = "Medium"
        elif cooking_time >= 10 and num_ingredients < 4:
            difficulty = "Intermediate"
        else:
            difficulty = "Hard"
    
        return difficulty

    def get_difficulty(self):
        if self.difficulty is None:
            self.calculate_difficulty()

        return self.difficulty

    # Name
    def get_name(self):
        return self.name

    def set_name(self, name):
        self.name = name

    # Cooking time
    def get_cooking_time(self):
        return self.cooking_time

    def set_cooking_time(self, cooking_time):
        try:
            cooking_time = int(cooking_time)
            if cooking_time <= 0:
                raise ValueError("Cooking time must be a positive number")

            self.cooking_time = cooking_time
            self.difficulty = self.calculate_difficulty(self.cooking_time, self.ingredients)
        except ValueError as e:
            print(f"Invalid cooking time: {e}")

    # Ingredients
    def add_ingredients(self, *ingredients):
        normalized_ingredients = set(ingredient.strip().lower() for ingredient in ingredients)

        self.ingredients.update(normalized_ingredients)
        self.update_all_ingredients()
        self.difficulty = self.calculate_difficulty(self.cooking_time, self.ingredients)

    def get_ingredients(self):
        return self.ingredients

    def search_ingredient(self, ingredient):
        normalized_ingredient = ingredient.strip().lower()
        return normalized_ingredient in self.ingredients

    def update_all_ingredients(self):
        Recipe.all_ingredients.update(self.ingredients)

    def __str__(self):
        ingredients_display = ', '.join(sorted(self.ingredients))
        return f"Recipe: {self.name}\nIngredients: {ingredients_display}\nCooking Time: {self.cooking_time} minutes\nDifficulty: {self.difficulty}"

    # Recipe search method
    @staticmethod
    def recipe_search(recipes_list, ingredient):
        for recipe in recipes_list:
            if recipe.search_ingredient(ingredient):
                print(recipe)
                print("\n==================================================")


# Recipes
tea = Recipe("Tea", ["Tea Leaves", "Sugar", "Water"], 5)
coffee = Recipe("Coffee", ["Coffee Powder", "Sugar", "Water"], 5)
cake = Recipe("Cake", ["Sugar", "Butter", "Eggs", "Vanilla Essence", "Flour", "Baking Powder", "Milk"], 50)
banana_smoothie = Recipe("Banana Smoothie", ["Bananas", "Milk", "Peanut Butter", "Sugar", "Ice Cubes"], 5)

# Wrap the recipes into a list called 'recipes_list'
recipes_list = [tea, coffee, cake, banana_smoothie]

# Print each recipe in the list
for recipe in recipes_list:
    print(f"\n{recipe}\n\n==================================================")

# Recipes containing water
print("\nRecipes containing 'Water':")
Recipe.recipe_search(recipes_list, 'Water')

# Recipes containing sugar
print("\nRecipes containing 'Sugar':")
Recipe.recipe_search(recipes_list, 'Sugar')

# Recipes containing bananas
print("\nRecipes containing 'Bananas':")
Recipe.recipe_search(recipes_list, 'Bananas')

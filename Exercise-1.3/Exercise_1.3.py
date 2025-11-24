recipe_list = []
ingredients_list = []

while True:
    n = int(input("Please enter the number of recipes: "))

    if n <= 0:
        print("Please enter a valid number.")
    else:
        break

def take_recipe(i):
    print(f"\nRecipe {i + 1}: ")
    
    name = str(input("Recipe name: "))

    while True:
        cooking_time = int(input("Cooking time, in minutes: "))

        if cooking_time <= 0:
            print("Please enter a valid number.")
        else:
            break

    ingredients = [ingredient.strip() for ingredient in input("Enter ingredients (comma separated): ").split(",")]

    recipe = {
        "name": name,
        "cooking_time": cooking_time,
        "ingredients": [ingredient.strip() for ingredient in ingredients]
    }
    
    return recipe

for i in range(n):
    recipe = take_recipe(i)

    for ingredient in recipe["ingredients"]:
        if ingredient not in ingredients_list:
            ingredients_list.append(ingredient)
    
    recipe_list.append(recipe)

print(f"\n\nRecipes list:\n-------------------------")

for recipe in recipe_list:
    cooking_time = recipe["cooking_time"]
    number_of_ingredients = len(recipe["ingredients"])

    if cooking_time < 10 and number_of_ingredients < 4:
        difficulty = "Easy"
    elif cooking_time < 10 and number_of_ingredients >= 4:
        difficulty = "Medium"
    elif cooking_time >= 10 and number_of_ingredients > 4:
        difficulty = "Intermediate"
    else:
        difficulty = "Hard"

    print("\n")
    print(f"Recipe: {recipe['name']}")
    print(f"Cooking time: {cooking_time} minutes")
    print(f"Difficulty: {difficulty}")
    print(f"Ingredients: ")

    for ingredient in recipe['ingredients']:
        print(f"- {ingredient}")

print(f"\n\nIngredients available across all recipes\n-------------------------\n")

ingredients_list.sort()

for ingredient in ingredients_list:
    print(f"- {ingredient}")

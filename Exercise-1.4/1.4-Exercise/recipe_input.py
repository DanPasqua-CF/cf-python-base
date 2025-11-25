import pickle

# Calculate recipe difficulty
def calc_difficulty(cooking_time, num_ingredients):
    if cooking_time < 10 and num_ingredients < 4:
        difficulty = "Easy"
    elif cooking_time < 10 and num_ingredients >= 4:
        difficulty = "Medium"
    elif cooking_time >= 10 and num_ingredients < 4:
        difficulty = "Intermediate"
    else:
        difficulty = "Hard"
    
    return difficulty

# Take recipes from user
def take_recipe():
    name = input("Recipe name: ")
    cooking_time = int(input("Cooking time (in minutes): "))
    ingredients = input("Enter ingredients (comma separated): ").split(",")
    ingredients = [ingredient.strip() for ingredient in ingredients]    
    difficulty = calc_difficulty(cooking_time, len(ingredients))
    
    recipe = {
        "name": name,
        "cooking_time": cooking_time,
        "ingredients": ingredients,
        "difficulty": difficulty
    }
    
    return recipe

# Main code
filename = input("Enter the filename to store recipes: ")

# Open file and load contents
try:
    with open(filename, "rb") as file:
        data = pickle.load(file)
        
    print("File loaded successfully!\n")
except FileNotFoundError:
    print("File not found. Creating new file.\n")

    data = {
        "recipes_list": [],
        "all_ingredients": []
    }
except Exception as e:
    print(f"An error occurred: {e}")
    print("Creating new recipe file.\n")

    data = {
        "recipes_list": [],
        "all_ingredients": []
    }
else:
    pass

finally:
    recipes_list = data["recipes_list"]
    all_ingredients = data["all_ingredients"]

n = int(input("How many recipes would you like to enter? "))

for i in range(n):
    print(f"\n------------------------- Recipe {i + 1} -------------------------")

    recipe = take_recipe()
    recipes_list.append(recipe)
    
    for ingredient in recipe["ingredients"]:
        if ingredient not in all_ingredients:
            all_ingredients.append(ingredient)

data = {
    "recipes_list": recipes_list,
    "all_ingredients": all_ingredients
}

# Save data to binary file
with open(filename, "wb") as file:
    pickle.dump(data, file)

print(f"\nRecipes saved to '{filename}'!")
print(f"Total recipes: {len(recipes_list)}")
print(f"Total unique ingredients: {len(all_ingredients)}")

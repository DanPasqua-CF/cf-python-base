import pickle

recipe = {
    'name': 'Tea', 
    'ingredients': ['Tea Leaves', 'Water', 'Sugar'], 
    'cooking_time': 5, 
    'difficulty': 'Easy'
}

my_file = open('recipe_binary.bin', 'wb')
pickle.dump(recipe, my_file)
my_file.close()

with open('recipe_binary.bin', 'rb') as my_file:
    recipe = pickle.load(my_file)

print("Recipe details - ")
print("Ingredient name: " + recipe['name'])
print("Ingredients: " + ", ".join(recipe['ingredients']))
print("Cooking time in minutes: " + str(recipe['cooking_time']))
print("Difficulty: " + recipe['difficulty'])

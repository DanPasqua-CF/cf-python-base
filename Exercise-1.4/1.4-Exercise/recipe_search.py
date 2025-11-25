import pickle

# Display the recipe
def display_recipe(recipe):
    print("\n" + "="*50)
    print(f"Recipe: {recipe['name']}")
    print("="*50)
    print(f"Cooking Time: {recipe['cooking_time']} minutes")
    print(f"Difficulty: {recipe['difficulty']}")
    print(f"Ingredients:")

    for ingredient in recipe['ingredients']:
        print(f"  - {ingredient}")

    print("="*50)

# Search for ingredients
def search_ingredient(data):
    print("\nAvailable ingredients:")
    print("-" * 30)

    all_ingredients = data['all_ingredients']
    
    for index, ingredient in enumerate(all_ingredients):
        print(f"{index}. {ingredient}")
    
    print("-" * 30)
    
    try:
        choice = int(input("\nEnter the number of the ingredient you want to search: "))
        ingredient_searched = all_ingredients[choice]
    except (ValueError, IndexError):
        print("Invalid input. Please enter a valid number from the list.")
    else:
        print(f"\nRecipes containing '{ingredient_searched}':")
        print("="*50)
        
        recipes_list = data['recipes_list']
        found = False
        
        for recipe in recipes_list:
            if ingredient_searched in recipe['ingredients']:
                display_recipe(recipe)
                found = True
        
        if not found:
            print(f"No recipes found with {ingredient_searched}.")

# Main code
def main():
    filename = input("Enter the filename containing the recipe data: ")
    
    try:
        with open(filename, 'rb') as file:
            data = pickle.load(file)
    except FileNotFoundError:
        print(f"{filename} not found.")
        return
    except Exception as e:
        print(f"Error: {e}")
        return
    else:
        # Call the search_ingredient function
        search_ingredient(data)

if __name__ == "__main__":
    main()

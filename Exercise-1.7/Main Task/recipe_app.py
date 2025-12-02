import os
from sqlalchemy import create_engine, Column
from sqlalchemy.orm import sessionmaker, declarative_base
from sqlalchemy.types import Integer, String

engine = create_engine("mysql://cf-python:NewPassword123@localhost/task_database")

Base = declarative_base()

class Recipe(Base):
    __tablename__ = "final_recipes"

    id = Column(Integer, primary_key=True, autoincrement=True)
    name = Column(String(50))
    ingredients = Column(String(255))
    cooking_time = Column(Integer)
    difficulty = Column(String(20))

    def __repr__(self):
        return f"<Recipe ID: {self.id} - {self.name.title()} - Difficulty: {self.difficulty}>"

    def __str__(self):
        return (
            f"{'-'*50}\n"
            f"Recipe ID: {self.id}\n"
            f"Name: {self.name}\n"
            f"Ingredients: {self.ingredients}\n"
            f"Cooking Time: {self.cooking_time} minutes\n"
            f"Difficulty: {self.difficulty}\n"
            f"{'-'*50}"
        )

    def return_ingredients_as_list(self):
        if self.ingredients:
            return self.ingredients.split(", ")
        else:
            return []
    
    def calculate_difficulty(self):
        num_ingredients = len(self.ingredients.split(", "))
        
        if self.cooking_time < 10 and num_ingredients < 4:
            self.difficulty = "Easy"
        elif self.cooking_time < 10 and num_ingredients >= 4:
            self.difficulty = "Medium"
        elif self.cooking_time >= 10 and num_ingredients < 4:
            self.difficulty = "Intermediate"
        else:
            self.difficulty = "Hard"

# Create the table
Base.metadata.create_all(engine)

# Create the session class and bind it to the engine
Session = sessionmaker(bind=engine)
session = Session()

# Function 1: create_recipe()
def create_recipe():
    try:
        print("\n" + "=" * 50)
        print("Add recipe".center(50))
        print("=" * 50 + "\n")
        
        # Recipe name
        while True:
            name = input("Enter recipe name: ").strip()
            
            # Input validation
            if not name:
                print("Recipe name cannot be empty\n")
                continue
            elif len(name) > 50:
                print("Recipe name cannot exceed 50 characters\n")
                continue
            elif name.isnumeric():
                print("Name must be a string")
                continue
            break
        
        # Cooking time
        while True:
            cooking_time = input("Enter cooking time in minutes: ").strip()
            
            # Input validation
            if not cooking_time.isnumeric():
                print("Cooking time must be a number\n")
                continue
            
            cooking_time = int(cooking_time)
            
            if cooking_time <= 0:
                print("Cooking time must be greater than 0\n")
                continue
            
            break
        
        # Ingredients
        ingredients = []
        
        while True:
            num_ingredients_input = input("How many ingredients would you like to add? ").strip()
            
            # Input validation
            if not num_ingredients_input.isnumeric():
                print("Please enter a valid number\n")
                continue
            
            num_ingredients = int(num_ingredients_input)
            
            if num_ingredients <= 0:
                print("You must enter at least one ingredient\n")
                continue
            
            break
        
        print()
        
        # Ingredients for loop
        for i in range(num_ingredients):
            while True:
                ingredient = input(f"Enter ingredient {i + 1}: ").strip()
                
                if not ingredient:
                    print("Error: Ingredient cannot be empty, please add some\n")
                    continue
                
                ingredients.append(ingredient)
                break
        
        # Ingredient list-to-string conversion
        ingredients_str = ", ".join(ingredients)
        
        # New Recipe object
        recipe_entry = Recipe(
            name=name,
            ingredients=ingredients_str,
            cooking_time=cooking_time
        )
        
        # Calculate difficulty
        recipe_entry.calculate_difficulty()
        
        # Add to database
        session.add(recipe_entry)
        session.commit()
        
        # Success message
        print("-" * 50)
        print("Recipe created".center(50))
        print("-" * 50)
        
    except ValueError as e:
        print(f"Invalid input: {e}")
        session.rollback()
    except Exception as e:
        print(f"Database error: {e}")
        session.rollback()


# Function 2: view_all_recipes()
def view_all_recipes():
    try:
        print("\n" + "=" * 50)
        print("All recipes".center(50))
        print("=" * 50 + "\n")
        
        # Retrieve all recipes as a list
        recipes = session.query(Recipe).all()
        
        # Check for recipes
        if not recipes:
            print("No recipes found, please add some")
            return None
        
        # Loop through recipes
        for recipe in recipes:
            print(recipe)
            print()
        
        print(f"Total: {len(recipes)} recipes found\n")
        print("=" * 50 + "\n")
        
    except Exception as e:
        print(f"Error retrieving recipes: {e}")
        return None


# Function 3: search_by_ingredients()
def search_by_ingredients():
    try:
        print("\n" + "=" * 50)
        print("Search recipes by ingredient".center(50))
        print("=" * 50 + "\n")
        
        # Check for entries
        recipe_count = session.query(Recipe).count()
        
        if recipe_count == 0:
            print("No recipes found\n")
            return
        
        # Retrieve ingredients
        results = session.query(Recipe.ingredients).all()
        
        all_ingredients = []
        
        # Split ingredients, and add to all_ingredients
        for row in results:
            if row[0]:
                ingredients = row[0].split(", ")
                
                for ingredient in ingredients:
                    ingredient = ingredient.strip()
                    
                    if ingredient and ingredient not in all_ingredients:
                        all_ingredients.append(ingredient)
        
        if not all_ingredients:
            print("No ingredients found")
            return
        
        all_ingredients = sorted(all_ingredients)
        
        # Display ingredients
        print("Available ingredients:")
        print("-" * 50)

        for i, ingredient in enumerate(all_ingredients, 1):
            print(f"{i}. {ingredient}")
        
        print("-" * 50)
        
        # Search for ingredients
        choice_input = input("\nEnter the numbers of ingredients to search for (separated by spaces), or 'cancel' to abort: ").strip()
        
        if choice_input.lower() == 'cancel':
            print("Search cancelled\n")
            return
        
        try:
            choices = [int(num) for num in choice_input.split()]
        except ValueError:
            print("Invalid input, please enter numbers only.")
            return
        
        # Validation
        for choice in choices:
            if choice < 1 or choice > len(all_ingredients):
                print(f"Invalid choice: {choice}. Please enter numbers between 1 and {len(all_ingredients)}.")
                return
        
        search_ingredients = [all_ingredients[choice - 1] for choice in choices]
        
        conditions = []
        
        # Loop through search_ingredients
        for ingredient in search_ingredients:
            like_term = f"%{ingredient}%"
            
            conditions.append(Recipe.ingredients.like(like_term))
        
        # Retrieve filtered recipes
        recipes = session.query(Recipe).filter(*conditions).all()
        
        if recipes:
            print(f"\n{'=' * 50}")
            print(f"Recipes containing: {', '.join(search_ingredients)}".center(50))
            print("=" * 50 + "\n")
            
            for recipe in recipes:
                print(f"{recipe}\n")
            
            print(f"Total: {len(recipes)} recipe(s) found\n")
        else:
            print(f"\nNo recipes found containing: {', '.join(search_ingredients)}\n")
    
    except Exception as e:
        print(f"Error searching recipes: {e}")
        return


# Function 4: edit_recipe()
def edit_recipe():
    try:
        print("\n" + "=" * 50)
        print("Edit recipe".center(50))
        print("=" * 50 + "\n")
        
        # Search for recipes
        recipe_count = session.query(Recipe).count()
        
        if recipe_count == 0:
            print("No recipes found, please add some")
            return
        
        # Get ID and name
        results = session.query(Recipe.id, Recipe.name).all()
        
        # Display recipes
        print("Available recipes")
        print("-" * 50)

        for recipe_id, recipe_name in results:
            print(f"ID {recipe_id}: {recipe_name}")
        print("-" * 50)
        
        recipe_id = input("\nEnter the ID of the recipe you want to edit (or 'cancel' to abort): ").strip()
        
        if recipe_id.lower() == 'cancel':
            print("Edit cancelled\n")
            return
        
        # Input validation
        if not recipe_id.isnumeric():
            print("Invalid input, please enter a valid recipe ID.")
            return
        
        recipe_id = int(recipe_id)
        
        # Check if the chosen id exists
        valid_ids = [recipe[0] for recipe in results]
        if recipe_id not in valid_ids:
            print(f"Recipe with ID {recipe_id} does not exist.")
            return
        
        # Retrieve recipe
        recipe_to_edit = session.query(Recipe).filter(Recipe.id == recipe_id).one()
        
        # Display recipe
        print(f"\n{'=' * 50}")
        print(f"Editing recipe: {recipe_to_edit.name}".center(50))
        print("=" * 50)
        print("\nCurrent details:")
        print(f"1. Name: {recipe_to_edit.name}")
        print(f"2. Ingredients: {recipe_to_edit.ingredients}")
        print(f"3. Cooking time: {recipe_to_edit.cooking_time} minutes")
        print(f"4. Difficulty: {recipe_to_edit.difficulty}")
        print("-" * 50)
        
        attribute_choice = input("\nWhich attribute would you like to edit? Enter the number (1-3), or 'cancel' to abort: ").strip()
        
        if attribute_choice.lower() == 'cancel':
            print("Edit cancelled\n")
            return
        
        if not attribute_choice.isnumeric() or int(attribute_choice) not in [1, 2, 3]:
            print("Invalid choice, please enter a number between 1 and 3")
            return
        
        attribute_choice = int(attribute_choice)
        
        if attribute_choice == 1:
            # Edit name
            while True:
                new_name = input("Enter new recipe name: ").strip()
                
                if not new_name:
                    print("Recipe name cannot be empty\n")
                    continue
                elif len(new_name) > 50:
                    print("Recipe name cannot exceed 50 characters.\n")
                    continue
                
                recipe_to_edit.name = new_name
                print(f"Recipe name updated to: {new_name}")
                break
        
        elif attribute_choice == 2:
            # Edit ingredients
            ingredients = []
            
            while True:
                num_ingredients_input = input("How many ingredients would you like to add?").strip()
                
                if not num_ingredients_input.isnumeric():
                    print("Please enter a valid number\n")
                    continue
                
                num_ingredients = int(num_ingredients_input)
                
                if num_ingredients <= 0:
                    print("You must enter at least one ingredient\n")
                    continue
                
                break
            
            print()
            for i in range(num_ingredients):
                while True:
                    ingredient = input(f"Enter ingredient {i + 1}: ").strip()
                    
                    if not ingredient:
                        print("Ingredients cannot be empty, please add some\n")
                        continue
                    
                    ingredients.append(ingredient)
                    break
            
            new_ingredients = ", ".join(ingredients)
            recipe_to_edit.ingredients = new_ingredients
            print(f"Ingredients updated to: {new_ingredients}")
        
        elif attribute_choice == 3:
            # Edit cooking time
            while True:
                cooking_time_input = input("Enter new cooking time (in minutes): ").strip()
                
                if not cooking_time_input.isnumeric():
                    print("Cooking time must be a number\n")
                    continue
                
                cooking_time = int(cooking_time_input)
                
                if cooking_time <= 0:
                    print("Cooking time must be greater than 0\n")
                    continue
                
                recipe_to_edit.cooking_time = cooking_time
                print(f"Cooking time updated to: {cooking_time} minutes")
                
                break
        
        # Recalculate difficulty
        recipe_to_edit.calculate_difficulty()
        
        session.commit()
        
        print("\n" + "=" * 50)
        print("Recipe updated".center(50))
        print("=" * 50)
        print("\nUpdated Recipe:")
        print(recipe_to_edit)
        print("=" * 50 + "\n")
        
    except Exception as e:
        print(f"Error editing recipe: {e}")
        session.rollback()
        return


# Function 5: delete_recipe()
def delete_recipe():
    try:
        print("\n" + "=" * 50)
        print("Delete recipe".center(50))
        print("=" * 50 + "\n")
        
        # Check for recipes
        recipe_count = session.query(Recipe).count()
        
        if recipe_count == 0:
            print("No recipes found, please add some")
            return
        
        # Get ID and name
        results = session.query(Recipe.id, Recipe.name).all()
        
        # Display recipes
        print("Available recipes:")
        print("-" * 50)

        for recipe_id, recipe_name in results:
            print(f"ID {recipe_id}: {recipe_name}")
        
        print("-" * 50)
        
        recipe_id_input = input("\nEnter the ID of the recipe you want to delete (or 'cancel' to abort): ").strip()
        
        if recipe_id_input.lower() == 'cancel':
            print("Delete cancelled\n")
            return
        
        # Input validation
        if not recipe_id_input.isnumeric():
            print("Invalid input, please enter a valid ID")
            return
        
        recipe_id = int(recipe_id_input)
        
        # Check if ID exists
        valid_ids = [recipe[0] for recipe in results]
        if recipe_id not in valid_ids:
            print(f"Recipe with ID {recipe_id} does not exist")
            return
        
        # Retrieve recipe
        recipe_to_delete = session.query(Recipe).filter(Recipe.id == recipe_id).one()
        
        # Confirm deletion
        print(f"\nYou are about to delete: {recipe_to_delete}")        
        confirm = input("\nAre you sure you want to delete this recipe? (yes/no): ").strip().lower()
        
        if confirm == 'yes':
            session.delete(recipe_to_delete)
            session.commit()
            
            print("\n" + "=" * 50)
            print("Recipe deleted".center(50))
            print("=" * 50 + "\n")
        else:
            print("Delete cancelled.\n")
        
    except Exception as e:
        print(f"Error deleting recipe: {e}")
        session.rollback()
        return


def main_menu():
    while True:
        print("\nWhat would you like to do?")
        print("1. Add a recipe")
        print("2. View all recipes")
        print("3. Search for recipes by ingredient")
        print("4. Edit a recipe")
        print("5. Delete a recipe")
        print("6. Exit program")
        print("-" * 50)
        
        choice = input("\nEnter your choice (1-6): ").strip()
        
        if choice == "1":
            create_recipe()
        elif choice == "2":
            view_all_recipes()
        elif choice == "3":
            search_by_ingredients()
        elif choice == "4":
            edit_recipe()
        elif choice == "5":
            delete_recipe()
        elif choice in ("6", "quit", "cancel"):
            print('\n' + "=" * 50)
            print('Exiting Recipe App'.center(50))
            print("=" * 50 + '\n')
            
            session.close()
            engine.dispose()
            
            break
        else:
            print("\nInvalid choice, please enter a number between 1 and 6.")


# MAIN EXECUTION
if __name__ == "__main__":
    try:
        print("\n" + "=" * 50)
        print("Recipe App".center(50))
        print("=" * 50)
        main_menu()
    except KeyboardInterrupt:
        print("\n\nProgram interrupted by user.")
        session.close()
        engine.dispose()
    except Exception as e:
        print(f"\nAn error occurred: {e}")
        session.close()
        engine.dispose()

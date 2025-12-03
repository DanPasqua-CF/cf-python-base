import mysql.connector
from mysql.connector import Error

def create_connection():
    try:
        conn = mysql.connector.connect(
            host="localhost",
            user="cf-python",
            password="password"
        )
        cursor = conn.cursor()
        cursor.execute("CREATE DATABASE IF NOT EXISTS task_database")
        cursor.execute("USE task_database")
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS Recipes (
                id INT AUTO_INCREMENT PRIMARY KEY,
                name VARCHAR(50),
                ingredients VARCHAR(255),
                cooking_time INT,
                difficulty VARCHAR(20)
            )
        """)
        conn.commit()
        
        print("Database connection established\n")
        return conn, cursor
        
    except Error as e:
        print(f"Error connecting to database: {e}")
        return None, None

def calculate_difficulty(cooking_time, ingredients):
    num_ingredients = len(ingredients)
    
    if cooking_time < 10 and num_ingredients < 4:
        return "Easy"
    elif cooking_time < 10 and num_ingredients >= 4:
        return "Medium"
    elif cooking_time >= 10 and num_ingredients < 4:
        return "Intermediate"
    else:
        return "Hard"

def create_recipe(conn, cursor):
    try:
        print("\n===== Add New Recipe =====")
        
        name = input("Enter recipe name: ").strip()

        if not name:
            print("Recipe name cannot be empty.")
            return
        
        cooking_time_input = input("Enter cooking time (in minutes): ").strip()
        
        if not cooking_time_input.isdigit():
            print("Cooking time must be a positive number.")
            return

        cooking_time = int(cooking_time_input)
        ingredients_input = input("Enter ingredients (comma separated): ").strip()
        
        if not ingredients_input:
            print("Ingredients cannot be empty.")
            return
        
        ingredients = [ing.strip() for ing in ingredients_input.split(',') if ing.strip()]
        
        if not ingredients:
            print("Please enter at least one ingredient.")
            return
        
        # Calculate difficulty
        difficulty = calculate_difficulty(cooking_time, ingredients)
        
        # Insert into database (parameterized query)
        sql = "INSERT INTO Recipes (name, ingredients, cooking_time, difficulty) VALUES (%s, %s, %s, %s)"
        val = (name, ', '.join(ingredients), cooking_time, difficulty)
        cursor.execute(sql, val)
        conn.commit()
        
        print(f"\nRecipe '{name}' added successfully!")
        print(f"Difficulty: {difficulty}")
        
    except ValueError:
        print("Invalid input. Please enter valid values.")
    except Error as e:
        print(f"Database error: {e}")
        conn.rollback()


def search_recipe(conn, cursor):
    try:
        print("\n===== Search Recipes by Ingredient =====")
        
        sql = "SELECT ingredients FROM Recipes"
        cursor.execute(sql)
        results = cursor.fetchall()
        
        if not results:
            print("No recipes found in the database.")
            return
        
        all_ingredients = set()
        for row in results:
            if row[0]:
                ingredients = row[0].split(", ")
                
                for ingredient in ingredients:
                    ingredient = ingredient.strip()
                    
                    if ingredient:
                        all_ingredients.add(ingredient)
        
        if not all_ingredients:
            print("No ingredients found in the database.")
            return
        
        all_ingredients = sorted(all_ingredients)
        
        print("\n===== Available Ingredients =====")
        for i, ingredient in enumerate(all_ingredients, 1):
            print(f"{i}. {ingredient}")
        print("=" * 30)
        
        choice_input = input("\nEnter the number of the ingredient to search for (or 'cancel' to abort): ").strip()
        
        if choice_input.lower() == 'cancel':
            print("Search cancelled.")
            return
        
        if not choice_input.isdigit():
            print("Invalid input. Please enter a number.")
            return
        
        choice = int(choice_input)
        
        if choice < 1 or choice > len(all_ingredients):
            print(f"Invalid choice. Please enter a number between 1 and {len(all_ingredients)}.")
            return
        
        search_ingredient = all_ingredients[choice - 1]
        
        sql = """
            SELECT name, ingredients, cooking_time, difficulty
            FROM Recipes
            WHERE ingredients LIKE %s
        """
        search_pattern = f"%{search_ingredient}%"
        cursor.execute(sql, (search_pattern,))
        search_results = cursor.fetchall()
        
        if search_results:
            print(f"\n=== Recipes containing '{search_ingredient}' ===")

            for recipe in search_results:
                print(f"\nName: {recipe[0]}")
                print(f"Ingredients: {recipe[1]}")
                print(f"Cooking Time: {recipe[2]} minutes")
                print(f"Difficulty: {recipe[3]}")
                print("-" * 40)
            print(f"\nTotal: {len(search_results)} recipe(s) found.")
        else:
            print(f"\nNo recipes found containing '{search_ingredient}'.")
    
    except ValueError:
        print("Invalid input. Please enter a valid number.")
    except Error as e:
        print(f"Database error: {e}")


def update_recipe(conn, cursor):
    try:
        print("\n=== Update Recipe ===")
        
        sql = "SELECT id, name, ingredients, cooking_time, difficulty FROM Recipes"
        cursor.execute(sql)
        results = cursor.fetchall()
        
        if not results:
            print("No recipes found in the database.")
            return
        
        print("\n===== Available Recipes =====")
        for row in results:
            print(f"\nID: {row[0]}")
            print(f"Name: {row[1]}")
            print(f"Ingredients: {row[2]}")
            print(f"Cooking Time: {row[3]} mins")
            print(f"Difficulty: {row[4]}")
        
        recipe_id_input = input("\nEnter the ID of the recipe to update: ").strip()
        
        if not recipe_id_input.isdigit():
            print("Invalid input. Please enter a numeric recipe ID.")
            return
        
        recipe_id = int(recipe_id_input)
        
        print("\nWhich column would you like to update?")
        print("1. name")
        print("2. cooking_time")
        print("3. ingredients")
        
        column_choice = input("Enter your choice (1-3): ").strip()
        
        if column_choice == "1":
            new_value = input("Enter new recipe name: ").strip()
            
            if not new_value:
                print("Name cannot be empty.")
                return
            
            sql = "UPDATE Recipes SET name = %s WHERE id = %s"
            cursor.execute(sql, (new_value, recipe_id))
            conn.commit()
            
            print("Recipe name updated successfully.")
            
        elif column_choice == "2":
            new_value = input("Enter new cooking time (in minutes): ").strip()
            
            if not new_value.isdigit():
                print("Cooking time must be a positive number.")
                return
            
            new_cooking_time = int(new_value)
            
            sql = "UPDATE Recipes SET cooking_time = %s WHERE id = %s"
            cursor.execute(sql, (new_cooking_time, recipe_id))
            conn.commit()
            
            sql = "SELECT ingredients FROM Recipes WHERE id = %s"
            cursor.execute(sql, (recipe_id,))
            current_ingredients = cursor.fetchone()[0].split(', ')
            
            new_difficulty = calculate_difficulty(new_cooking_time, current_ingredients)
            
            sql = "UPDATE Recipes SET difficulty = %s WHERE id = %s"
            cursor.execute(sql, (new_difficulty, recipe_id))
            conn.commit()
            
            print(f"Cooking time updated successfully. Difficulty recalculated to: {new_difficulty}")
            
        elif column_choice == "3":
            new_value = input("Enter new ingredients (comma separated): ").strip()
            
            if not new_value:
                print("Ingredients cannot be empty.")
                return
            
            new_ingredients = [ing.strip() for ing in new_value.split(',') if ing.strip()]
            
            if not new_ingredients:
                print("Please enter at least one ingredient.")
                return
            
            ingredients_string = ', '.join(new_ingredients)
            
            sql = "UPDATE Recipes SET ingredients = %s WHERE id = %s"
            cursor.execute(sql, (ingredients_string, recipe_id))
            conn.commit()
            
            sql = "SELECT cooking_time FROM Recipes WHERE id = %s"
            cursor.execute(sql, (recipe_id,))
            current_cooking_time = cursor.fetchone()[0]
            
            new_difficulty = calculate_difficulty(current_cooking_time, new_ingredients)
            
            sql = "UPDATE Recipes SET difficulty = %s WHERE id = %s"
            cursor.execute(sql, (new_difficulty, recipe_id))
            conn.commit()
            
            print(f"Ingredients updated successfully. Difficulty recalculated to: {new_difficulty}")
            
        else:
            print("Invalid choice. Please enter 1, 2, or 3.")
            return
        
    except ValueError:
        print("Invalid input.")
    except Error as e:
        print(f"Database error: {e}")
        conn.rollback()


def delete_recipe(conn, cursor):
    try:
        print("\n=== Delete Recipe ===")
        
        sql = "SELECT id, name, ingredients, cooking_time, difficulty FROM Recipes"
        cursor.execute(sql)
        results = cursor.fetchall()
        
        if not results:
            print("No recipes found in the database.")
            return
        
        print("\n===== Available Recipes =====")
        
        for row in results:
            print(f"\nID: {row[0]}")
            print(f"Name: {row[1]}")
            print(f"Ingredients: {row[2]}")
            print(f"Cooking Time: {row[3]} mins")
            print(f"Difficulty: {row[4]}")
        
        chosen_recipe_id = input("\nEnter the ID of the recipe you want to delete: ").strip()
        
        if not chosen_recipe_id.isdigit():
            print("Invalid input. Please enter a numeric recipe ID.")
            return
        
        recipe_id = int(chosen_recipe_id)
        
        sql = "DELETE FROM Recipes WHERE id = %s"
        cursor.execute(sql, (recipe_id,))
        conn.commit()
        
        if cursor.rowcount > 0:
            print(f"\nRecipe with ID {recipe_id} deleted successfully.")
        else:
            print(f"\nNo recipe found with ID {recipe_id}.")
        
    except ValueError:
        print("Invalid input.")
    except Error as e:
        print(f"Database error: {e}")
        conn.rollback()

def main_menu(conn, cursor):
    while True:
        print("What would you like to do?")
        print("1. Add a recipe")
        print("2. Search for a recipe")
        print("3. Update a recipe")
        print("4. Delete a recipe")
        
        choice = input("Enter your choice (1-4): ").strip()
        
        if choice == "1":
            create_recipe(conn, cursor)
        elif choice == "2":
            search_recipe(conn, cursor)
        elif choice == "3":
            update_recipe(conn, cursor)
        elif choice == "4":
            delete_recipe(conn, cursor)
        else:
            print("Please enter a valid option")

def main():
    conn, cursor = create_connection()
    
    if conn is None or cursor is None:
        print("Failed to connect to database. Exiting...")
        return
    
    try:
        main_menu(conn, cursor)
    except Exception as e:
        print(f"\nAn unexpected error occurred: {e}")
    finally:
        if cursor:
            cursor.close()
        if conn and conn.is_connected():
            conn.close()
            print("Database connection closed")

if __name__ == "__main__":
    main()

class ShoppingList(object):
    def __init__(self, list_name):
        self.list_name = list_name
        self.shopping_list = []

    def add_item(self, item):
        if item not in self.shopping_list:
            self.shopping_list.append(item)

    def remove_item(self, item):
        if item in self.shopping_list:
            self.shopping_list.remove(item)

    def view_list(self):
        print(f"Shopping list: {self.list_name}")

        for item in self.shopping_list:
            print(f"- {item}")

    def merge_lists(self, obj):
        merged_lists_name = 'Merged List - ' + str(self.list_name) + " + " + str(obj.list_name)
        
        merged_lists_obj = ShoppingList(merged_lists_name)
        merged_lists_obj.shopping_list = self.shopping_list.copy()

        for item in obj.shopping_list:
            if not item in merged_lists_obj.shopping_list:
              merged_lists_obj.shopping_list.append(item)

        return merged_lists_obj

pet_store_list = ShoppingList('Pet Store List')
grocery_store_list = ShoppingList('Grocery Store List')

for item in ['dog food', 'frisbee', 'bowl', 'collars', 'flea collars']:
    pet_store_list.add_item(item)

for item in ['fruits' ,'vegetables', 'bowl', 'ice cream']:
    grocery_store_list.add_item(item)

# Add items
pet_store_list.add_item("dog food")
pet_store_list.add_item("frisbee")
pet_store_list.add_item("bowl")
pet_store_list.add_item("collars")
pet_store_list.add_item("flea collars")

# Remove item
# pet_store_list.remove_item("flea collars")

# Add item
pet_store_list.add_item("frisbee")

# View list
pet_store_list.view_list()

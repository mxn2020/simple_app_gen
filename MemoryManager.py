import json

class MemoryManager:
    def __init__(self):
        self.memory = {
            "initial_setup": {}, "author_persona": {}, "book": {},
            "recipe_chapters": {}, "detailed_content": {}, "recipe_variations": {},
            "compilation": {}, "final_memory": {}, "metadata": {}, "project": {}
        }
    
    def update_memory(self, section, keys, value):
        # Navigate through the keys to find the right place to update
        current = self.memory[section]
        for key in keys[:-1]:  # All keys except the last
            if key not in current or not isinstance(current[key], dict):
                current[key] = {}  # Initialize a new dictionary if the key doesn't exist
            current = current[key]
        current[keys[-1]] = value  # Set the value at the final key

    def get_memory(self, section, keys):
        # Retrieve value using nested keys
        current = self.memory[section]
        for key in keys:
            if key not in current:
                return None  # Key not found
            current = current[key]
        return current

    def delete_memory(self, section, keys):
        # Delete value using nested keys
        current = self.memory[section]
        for key in keys[:-1]:
            if key not in current:
                return  # Key not found
            current = current[key]
        del current[keys[-1]]

    def get_all_memory(self, section):
        # Get all memory in a section
        return self.memory[section]
    
    def get_response(self):
        # Get the response from memory.
        return self.get_memory("response", [])
    
    def save_response(self, response):
        # Save the response from OpenAI to memory.
        self.update_memory("response", [], response)

    def get_role(self):
        #        self.memory_manager.update_memory("author_persona", ["persona"], author_persona)
        role = self.get_memory("author_persona", ["persona"])
        return role

    def exists(self, section, keys):
        # Check if the value exists in memory
        return self.get_memory(section, keys) is not None
    
    def get_all_keys(self):
        # Get all keys in memory
        return list(self.memory.keys())

    def save_to_file(self, filename):
        with open(filename, 'w') as file:
            json.dump(self.memory, file, indent=4)

    def load_from_file(self, filename):
        with open(filename, 'r') as file:
            self.memory = json.load(file)
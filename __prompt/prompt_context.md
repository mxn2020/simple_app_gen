## initial information:
please check all provided data

- I am providing you with the project description
- I am providing you with the module json file structure
- I am providing you with initial implementations for a few classes


## instructions:
- please study the provided information and data very well. respond only with YES after the review.

## process.md:

lets create a symple python app using this library.

- setup memory_string
- send project name and description to nlp and request feature list
- add feature list to memory_string
- send memory_string to nlp and request file and folder structure
- add file and folder structure to memory_string
- send memory_string to nlp and request plan for implementation
- add plan for implementation to memory_string
- add memory_string as context to prompt_string with attributes: instructions, context, tech_stack
- send prompt_string to nlp and request implementation of the first file, with response structure {"response": str, "file_path": str}
- add file_path and response to prompt_string
- check if folder of file_path exist, if not, create folder (folders can contain multiple sub folders, create all subfolders)
- check if file exists, if file does not exist create it and save response text inside it
- if the file exists, create a new  file with the same name and a suffix "_updated", (check if that exists too and add numbers to suffix until it does not exist)

LOOP BEGIN
- send prompt_string to nlp and request implementation of the next file, with response structure {"response": str, "file_path": str}
- add file_path and response to prompt_string
- check if folder of file_path exist, if not, create folder (folders can contain multiple sub folders, create all subfolders)
- check if file exists, if file does not exist create it and save response text inside it
- if the file exists, create a new  file with the same name and a suffix "_updated", (check if that exists too and add numbers to suffix until it does not exist)
LOOP END

repeat LOOP until nlp response contains "FINISHED WITH SCRIPT"

## MemoryManager.py:

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

## ProjectFolderCreator.py:

import os
import json
from datetime import datetime
from maldinio_ai import ModuleMemory

class ProjectFolderCreator:
    def __init__(self, memory: ModuleMemory):
        self.main_key = "project"
        self.key = "files"
        self.sub_key = "project_folder"
        self.memory = memory
        self.root_folder = "__temp_project"
        self.project_name = "project_" + datetime.now().strftime("%Y%m%d_%H%M%S")
        self.full_path = os.path.join(self.root_folder, self.project_name)
        self.full_path_prompts = os.path.join(self.root_folder, self.project_name, "prompts")
        self.full_path_responses = os.path.join(self.root_folder, self.project_name, "responses")
        self.full_path_output = os.path.join(self.root_folder, self.project_name, "output")

    def get_key(self):
        return self.key
    
    def get_main_key(self):
        return self.main_key
    
    def get_sub_key(self):
        return self.sub_key

    def execute(self):
        self.create_project_directory()

    def create_project_directory(self):
        if not os.path.exists(self.full_path):
            os.makedirs(self.full_path)
            print(f"Created project directory: {self.full_path}")
        else:
            print(f"Project directory already exists: {self.full_path}")
                
        if not os.path.exists(self.full_path_prompts):
            os.makedirs(self.full_path_prompts)
            print(f"Created prompts directory: {self.full_path_prompts}")
        else:
            print(f"Prompts directory already exists: {self.full_path_prompts}")
            
        if not os.path.exists(self.full_path_responses):
            os.makedirs(self.full_path_responses)
            print(f"Created responses directory: {self.full_path_responses}")
        else:
            print(f"Responses directory already exists: {self.full_path_responses}")
            
        if not os.path.exists(self.full_path_output):
            os.makedirs(self.full_path_output)
            print(f"Created output directory: {self.full_path_output}")
        else:
            print(f"Output directory already exists: {self.full_path_output}")
            
                                 
        self.memory.create([self.main_key, self.key, self.sub_key], self.full_path)
        self.memory.create([self.main_key, self.key, "prompt_folder"], self.full_path_prompts)
        self.memory.create([self.main_key, self.key, "response_folder"], self.full_path_responses)
        self.memory.create([self.main_key, self.key, "output_folder"], self.full_path_output)


## test.py:

import os
import json
from maldinio_ai import NLPClient, PromptContext, PromptGenerator, OpenAIKeyLoader, NLPProcessor, ModuleMemory
from ProjectFolderCreator import ProjectFolderCreator
from MemoryManager import MemoryManager

def parse_response(response):
    try:
        # Try parsing the response as is
        return json.loads(response)
    except json.decoder.JSONDecodeError as e:
        # If a JSONDecodeError is encountered, try fixing the quotes
        try:
            corrected_response = response.replace("'", '"')
            return json.loads(corrected_response)
        except Exception as e:
            # Log the error, raise an exception, or handle it as needed
            print(f"Failed to parse the response even after quote correction: {e}")
            raise

# Simulated NLP client using the PromptContext and PromptGenerator
class MockNLPClient:
    def process(self, prompt):
        print(f"Sending prompt to NLP model: {prompt}")
        # This is where you'd send the prompt to the actual NLP model. For now, it returns mocked responses.
        if "feature list" in prompt:
            return json.dumps(["Login system", "Data visualization", "API integration"])
        elif "file and folder structure" in prompt:
            return json.dumps({
                "folders": ["src", "docs", "tests"],
                "files": ["src/app.py", "src/utils.py", "README.md"]
            })
        elif "implementation plan" in prompt:
            return "Setup project structure -> Implement login system -> Add data visualization -> Integrate external API"
        elif "implementation" in prompt:
            return json.dumps({"response": "def main():\n    print('Hello, world!')", "file_path": "src/app.py"})
        else:
            return "FINISHED WITH SCRIPT"

def ensure_directory_exists(path):
    os.makedirs(path, exist_ok=True)

def write_or_update_file(file_path, content):
    if os.path.exists(file_path):
        base, extension = os.path.splitext(file_path)
        version = 1
        new_file_path = f"{base}_updated{version}{extension}"
        while os.path.exists(new_file_path):
            version += 1
            new_file_path = f"{base}_updated{version}{extension}"
        file_path = new_file_path
    with open(file_path, 'w') as file:
        file.write(content)

def main():
    dotenv_path = os.path.join(os.path.dirname(__file__), 'config', '.env')
    openAI = OpenAIKeyLoader(dotenv_path)
    nlp_client = NLPClient()
    memory_manager = ModuleMemory()
    project_folder_creator = ProjectFolderCreator(memory_manager)
    project_folder_creator.create_project_directory()
    nlp_processor = NLPProcessor(memory_manager)
    generator = PromptGenerator()
    prompt_context = []

    project_name = input("Enter project name: ")
    project_description = input("Enter project description: ")

    prompt_context.append(project_name)
    prompt_context.append(project_description)
    role = "You are a great App Developer"
    messages = []
    messages.append({"role": "system", "content": role})

    # Generate prompt and get feature list
    feature_list_context = PromptContext(
        role="You are a great App Developer",
        simple_prompt="Based on the given project title and description, provide a comprehensive feature and functionality list.",
        context_items={"project_name": project_name, "project_description": project_description},
        response_format="json",
        response_structure={"features" : [{ "name": str, "description": str}]},
        instructions=["Prepare a list of features and functionalities for the project.",
                      "Include all the necessary features for a complete application."],
    )
    generator.set_context(feature_list_context)
    prompt = generator.generate_prompt()
    messages.append({"role": "user", "content": prompt})
    response = nlp_processor.process(messages, feature_list_context)
    parsed_response = parse_response(response)
    features = parsed_response
    messages.append({"role": "assistant", "content": response})
    print("Features:", features)

    # Generate prompt and get file and folder structure
    structure_context = PromptContext(
        role="You are a great App Developer",
        simple_prompt="Based on the feature list, provide the file and folder structure for the project.",
        # context_items={"feature_list": features},
        response_format="json",
        response_structure={ "files" : [ { "name": str, "file_path": str, "description": str } ], "folders" : [ { "name": str, "description": str } ] },
        instructions=["Prepare a file and folder structure for the project.",
                      "Include all the necessary files and folders for a complete application."],
    )
    generator.set_context(structure_context)
    prompt = generator.generate_prompt()
    messages.append({"role": "user", "content": prompt})
    response = nlp_processor.process(messages, structure_context)
    parsed_response = parse_response(response)
    structure = parsed_response
    file_list = structure["files"]
    messages.append({"role": "assistant", "content": response})
    print("Structure:", structure)


    # Generate Implementation Plan
    plan_context = PromptContext(
        role="You are a great App Developer",
        simple_prompt="Based on the file and folder structure, provide a plan for implementation.",
        # context_items={"structure": structure},
        response_format="json",
        response_structure={"plan": str},
        instructions=["Prepare a plan for implementing the project.",
                      "Include all the necessary steps for a complete application."],
    )
    generator.set_context(plan_context)
    prompt = generator.generate_prompt()
    messages.append({"role": "user", "content": prompt})
    response = nlp_processor.process(messages, plan_context)
    parsed_response = parse_response(response)
    plan = parsed_response
    messages.append({"role": "assistant", "content": response})
    print("Plan:", plan)


    # Iterate through the files and implement the project
    for file in file_list:
        file_name = file["name"]
        file_description = file["description"]
        file_path = file["file_path"]

        # Generate prompt and get feature list for the file as well as file_path in array format
        feature_list_context = PromptContext(
            role="You are a great App Developer",
            simple_prompt="Based on the given project title and description, provide a comprehensive feature and functionality list.",
            context_items={"file_name": file_name, "file_description": file_description, "file_path": file_path},
            response_format="json",
            response_structure={"features" : [{ "name": str, "description": str}], "file_path_array": [str]},
            instructions=["Prepare a list of features and functionalities for the project.",
                          "Include all the necessary features for a complete application."],
        )
        generator.set_context(feature_list_context)
        prompt = generator.generate_prompt()
        messages.append({"role": "user", "content": prompt})
        response = nlp_processor.process(messages, feature_list_context)
        parsed_response = parse_response(response)
        features = parsed_response
        file["features"] = features
        file["file_path_array"] = parsed_response["file_path_array"]
        messages.append({"role": "assistant", "content": response})
        print("Features:", features)


        # Generate prompt and get code implementation
        implementation_context = PromptContext(
            role="You are a great App Developer",
            simple_prompt="Lets start implementing the project step by step and generate the code for an initial file, then improve file by file the codebase.",
            context_items={"file_name": file_name, "file_description": file_description, "file_path": file_path, "features": features},
            response_format="json",
            response_structure={"file_path": str, "code": str, "file_instruction": str},
            instructions=["Generate the code for the initial file.",
                          "Generate a comprehensive and well coded implementation code for the current file.",
                          "Also generate brief instruction on how to use the file and what it does.",
                          "Provide the response in the given response format and structure."],
        )
        generator.set_context(implementation_context)
        prompt = generator.generate_prompt()
        messages.append({"role": "user", "content": prompt})
        response = nlp_processor.process(messages, implementation_context)
        parsed_response = parse_response(response)
        coded_file = parsed_response
        file["code"] = coded_file
        file["file_instruction"] = parsed_response["file_instruction"]
        messages.append({"role": "assistant", "content": response})
        print("Coded File:", coded_file)

        # Check and create folder structure
        # ensure_directory_exists(os.path.dirname(file_path))
        # write_or_update_file(file_path, implementation["code"])
        # print("File created at:", file_path)
  

    memory_manager.save_to_file("memory.json")


if __name__ == "__main__":
    main()


## test2.py:

import os

class NLPClient:
    def __init__(self, gpt_model="GPT_MODEL"):
        self.gpt_model = gpt_model
        # This client is a placeholder. In a real scenario, this would interface with OpenAI's API.
    
    def process(self, messages, role, use_json_completion=False):
        # This is a mockup function. You should replace this with actual calls to the NLP API.
        # For demonstration, it returns predefined responses based on the role.
        if role == "request_features":
            return ["Login system", "Data visualization", "API integration"]
        elif role == "request_structure":
            return {
                "folders": ["src", "docs", "tests"],
                "files": ["src/app.py", "src/utils.py", "README.md"]
            }
        elif role == "request_implementation_plan":
            return "1. Setup project structure. 2. Implement login system. 3. Add data visualization. 4. Integrate external API."
        elif role == "request_implementation":
            return {"response": "def main():\n    print('Hello, world!')", "file_path": "src/app.py"}
        elif role == "finish_script":
            return "FINISHED WITH SCRIPT"
        else:
            return "Unknown role"

def ensure_directory_exists(path):
    if not os.path.exists(path):
        os.makedirs(path)

def write_or_update_file(file_path, content):
    if os.path.exists(file_path):
        base, extension = os.path.splitext(file_path)
        version = 1
        new_file_path = f"{base}_updated{version}{extension}"
        while os.path.exists(new_file_path):
            version += 1
            new_file_path = f"{base}_updated{version}{extension}"
        file_path = new_file_path
    
    with open(file_path, 'w') as file:
        file.write(content)

def main():
    nlp_client = NLPClient()
    memory_string = ""
    prompt_string = {"instructions": "", "context": "", "tech_stack": ""}
    
    # Setup process
    project_name = "MyProject"
    project_description = "A project to demonstrate NLP-driven development."
    
    # Request feature list
    features = nlp_client.process([project_name, project_description], "request_features")
    memory_string += f"Features: {features}\n"
    
    # Request file and folder structure
    structure = nlp_client.process(memory_string, "request_structure")
    memory_string += f"Structure: {structure}\n"
    
    # Request plan for implementation
    plan = nlp_client.process(memory_string, "request_implementation_plan")
    memory_string += f"Plan: {plan}\n"
    
    # Add memory_string to prompt_string
    prompt_string["context"] = memory_string
    
    # Implement the first file
    implementation_response = nlp_client.process(prompt_string, "request_implementation")
    prompt_string["instructions"] = implementation_response["response"]
    file_path = implementation_response["file_path"]
    
    # Check and handle file and folder creation
    folder_path = os.path.dirname(file_path)
    ensure_directory_exists(folder_path)
    write_or_update_file(file_path, prompt_string["instructions"])
    
    while "FINISHED WITH SCRIPT" not in prompt_string["instructions"]:
        implementation_response = nlp_client.process(prompt_string, "request_implementation")
        prompt_string["instructions"] = implementation_response["response"]
        file_path = implementation_response["file_path"]
        
        folder_path = os.path.dirname(file_path)
        ensure_directory_exists(folder_path)
        write_or_update_file(file_path, prompt_string["instructions"])

if __name__ == "__main__":
    main()


## test BACKUP.py:

import os
import json
from maldinio_ai import NLPClient, PromptContext, PromptGenerator, OpenAIKeyLoader, NLPProcessor, ModuleMemory
from ProjectFolderCreator import ProjectFolderCreator
from MemoryManager import MemoryManager

def parse_response(response):
    try:
        # Try parsing the response as is
        return json.loads(response)
    except json.decoder.JSONDecodeError as e:
        # If a JSONDecodeError is encountered, try fixing the quotes
        try:
            corrected_response = response.replace("'", '"')
            return json.loads(corrected_response)
        except Exception as e:
            # Log the error, raise an exception, or handle it as needed
            print(f"Failed to parse the response even after quote correction: {e}")
            raise

# Simulated NLP client using the PromptContext and PromptGenerator
class MockNLPClient:
    def process(self, prompt):
        print(f"Sending prompt to NLP model: {prompt}")
        # This is where you'd send the prompt to the actual NLP model. For now, it returns mocked responses.
        if "feature list" in prompt:
            return json.dumps(["Login system", "Data visualization", "API integration"])
        elif "file and folder structure" in prompt:
            return json.dumps({
                "folders": ["src", "docs", "tests"],
                "files": ["src/app.py", "src/utils.py", "README.md"]
            })
        elif "implementation plan" in prompt:
            return "Setup project structure -> Implement login system -> Add data visualization -> Integrate external API"
        elif "implementation" in prompt:
            return json.dumps({"response": "def main():\n    print('Hello, world!')", "file_path": "src/app.py"})
        else:
            return "FINISHED WITH SCRIPT"

def ensure_directory_exists(path):
    os.makedirs(path, exist_ok=True)

def write_or_update_file(file_path, content):
    if os.path.exists(file_path):
        base, extension = os.path.splitext(file_path)
        version = 1
        new_file_path = f"{base}_updated{version}{extension}"
        while os.path.exists(new_file_path):
            version += 1
            new_file_path = f"{base}_updated{version}{extension}"
        file_path = new_file_path
    with open(file_path, 'w') as file:
        file.write(content)

def main():
    dotenv_path = os.path.join(os.path.dirname(__file__), 'config', '.env')
    openAI = OpenAIKeyLoader(dotenv_path)
    nlp_client = NLPClient()
    memory_manager = ModuleMemory()
    project_folder_creator = ProjectFolderCreator(memory_manager)
    project_folder_creator.create_project_directory()
    nlp_processor = NLPProcessor(memory_manager)
    generator = PromptGenerator()
    prompt_context = []

    project_name = input("Enter project name: ")
    project_description = input("Enter project description: ")

    prompt_context.append(project_name)
    prompt_context.append(project_description)
    role = "You are a great App Developer"
    messages = []
    messages.append({"role": "system", "content": role})

    # Generate prompt and get feature list
    feature_list_context = PromptContext(
        role="You are a great App Developer",
        simple_prompt="Based on the given project title and description, provide a comprehensive feature and functionality list.",
        context_items={"project_name": project_name, "project_description": project_description},
        response_format="json",
        response_structure={"features" : [{ "name": str, "description": str}]},
        instructions=["Prepare a list of features and functionalities for the project.",
                      "Include all the necessary features for a complete application."],
    )
    generator.set_context(feature_list_context)
    prompt = generator.generate_prompt()
    messages.append({"role": "user", "content": prompt})
    response = nlp_processor.process(messages, feature_list_context)
    parsed_response = parse_response(response)
    features = parsed_response
    messages.append({"role": "assistant", "content": response})
    print("Features:", features)

    # Generate prompt and get file and folder structure
    structure_context = PromptContext(
        role="You are a great App Developer",
        simple_prompt="Based on the feature list, provide the file and folder structure for the project.",
        # context_items={"feature_list": features},
        response_format="json",
        response_structure={ "files" : [ { "name": str, "file_path": str, "description": str } ], "folders" : [ { "name": str, "description": str } ] },
        instructions=["Prepare a file and folder structure for the project.",
                      "Include all the necessary files and folders for a complete application."],
    )
    generator.set_context(structure_context)
    prompt = generator.generate_prompt()
    messages.append({"role": "user", "content": prompt})
    response = nlp_processor.process(messages, structure_context)
    parsed_response = parse_response(response)
    structure = parsed_response
    file_list = structure["files"]
    messages.append({"role": "assistant", "content": response})
    print("Structure:", structure)


    # Generate Implementation Plan
    plan_context = PromptContext(
        role="You are a great App Developer",
        simple_prompt="Based on the file and folder structure, provide a plan for implementation.",
        # context_items={"structure": structure},
        response_format="json",
        response_structure={"plan": str},
        instructions=["Prepare a plan for implementing the project.",
                      "Include all the necessary steps for a complete application."],
    )
    generator.set_context(plan_context)
    prompt = generator.generate_prompt()
    messages.append({"role": "user", "content": prompt})
    response = nlp_processor.process(messages, plan_context)
    parsed_response = parse_response(response)
    plan = parsed_response
    messages.append({"role": "assistant", "content": response})
    print("Plan:", plan)


    # Iterate through the files and implement the project
    for file in file_list:
        file_name = file["name"]
        file_description = file["description"]
        file_path = file["file_path"]

        # Generate prompt and get feature list for the file as well as file_path in array format
        feature_list_context = PromptContext(
            role="You are a great App Developer",
            simple_prompt="Based on the given project title and description, provide a comprehensive feature and functionality list.",
            context_items={"file_name": file_name, "file_description": file_description, "file_path": file_path},
            response_format="json",
            response_structure={"features" : [{ "name": str, "description": str}], "file_path_array": [str]},
            instructions=["Prepare a list of features and functionalities for the project.",
                          "Include all the necessary features for a complete application."],
        )
        generator.set_context(feature_list_context)
        prompt = generator.generate_prompt()
        messages.append({"role": "user", "content": prompt})
        response = nlp_processor.process(messages, feature_list_context)
        parsed_response = parse_response(response)
        features = parsed_response
        file["features"] = features
        file["file_path_array"] = parsed_response["file_path_array"]
        messages.append({"role": "assistant", "content": response})
        print("Features:", features)


        # Generate prompt and get code implementation
        implementation_context = PromptContext(
            role="You are a great App Developer",
            simple_prompt="Lets start implementing the project step by step and generate the code for an initial file, then improve file by file the codebase.",
            context_items={"file_name": file_name, "file_description": file_description, "file_path": file_path, "features": features},
            response_format="json",
            response_structure={"file_path": str, "code": str, "file_instruction": str},
            instructions=["Generate the code for the initial file.",
                          "Generate a comprehensive and well coded implementation code for the current file.",
                          "Also generate brief instruction on how to use the file and what it does.",
                          "Provide the response in the given response format and structure."],
        )
        generator.set_context(implementation_context)
        prompt = generator.generate_prompt()
        messages.append({"role": "user", "content": prompt})
        response = nlp_processor.process(messages, implementation_context)
        parsed_response = parse_response(response)
        coded_file = parsed_response
        file["code"] = coded_file
        file["file_instruction"] = parsed_response["file_instruction"]
        messages.append({"role": "assistant", "content": response})
        print("Implementation:", implementation)

        # Check and create folder structure
        # ensure_directory_exists(os.path.dirname(file_path))
        # write_or_update_file(file_path, implementation["code"])
        # print("File created at:", file_path)
   



    # Generate prompt and get implementation
    initial_implementation_context = PromptContext(
        role="You are a great App Developer",
        simple_prompt="Lets start implementing the project step by step and generate the code for an initial file, then improve file by file the codebase.",
        # context_items={"plan": plan},
        response_format="json",
        response_structure={"file_path": str, "code": str},
        instructions=["Generate the code for the initial file.",
                      "Please generate a comprehensive and well coded implementation code for an initial file."],
                      # "Provide the response in the given response format and structure."
    )
    generator.set_context(initial_implementation_context)
    prompt = generator.generate_prompt()
    messages.append({"role": "user", "content": prompt})
    response = nlp_processor.process(messages, initial_implementation_context)
    # parsed_response = parse_response(response)
    # implementation = json.loads(response)
    implementation = response
    # file_path = implementation["file_path"]
    # file_content = implementation["code"]
    messages.append({"role": "assistant", "content": response})
    # print("Implementation:", file_content)
    print("Implementation:", implementation)


    # Check and create folder structure
    # ensure_directory_exists(os.path.dirname(file_path))
    # write_or_update_file(file_path, file_content)
    # print("File created at:", file_path)

    # Loop for file implementation
    while "FINISHED WITH SCRIPT" not in implementation:
        implementation_context = PromptContext(
            role="You are a great App Developer",
            simple_prompt="Great! Lets continue with the next file. Please generate a comprehensive and well coded implementation code for the next file.",
            # response_format="json",
            # response_structure={"file_path": str, "code": str},
            instructions=["Generate the code for the next file.", 
                          "Please generate a comprehensive and well coded implementation code for the next file.",
                          "We will develop the app file by file.",
                          "Once you finished all files and did several iterations to improve them and you believe the project is finished, please respond simply with [FINISHED WITH SCRIPT]" ] #, "Provide the response in the given response format and structure."],
        )
        generator.set_context(implementation_context)
        prompt = generator.generate_prompt()
        print()
        print ("prompt:", prompt)
        print()
        print ("messages:", messages)
        print()
        messages.append({"role": "user", "content": prompt})
        response = nlp_processor.process(messages, implementation_context)
        # parsed_response = parse_response(response)
        # implementation = json.loads(response)
        implementation = response
        # file_path = implementation["file_path"]
        # file_content = implementation["code"]
        messages.append({"role": "assistant", "content": response})
        # print("Implementation:", file_content)
        print("Implementation:", implementation)

        # Check and create folder structure
        # ensure_directory_exists(os.path.dirname(file_path))
        # write_or_update_file(file_path, file_content)
        # print("File created at:", file_path)

    memory_manager.save_to_file("memory.json")


if __name__ == "__main__":
    main()


## test_json.py:

import os
import json
from maldinio_ai import NLPClient, PromptContext, PromptGenerator, OpenAIKeyLoader, NLPProcessor, ModuleMemory
from ProjectFolderCreator import ProjectFolderCreator
from MemoryManager import MemoryManager

# Simulated NLP client using the PromptContext and PromptGenerator
class MockNLPClient:
    def process(self, prompt):
        print(f"Sending prompt to NLP model: {prompt}")
        # This is where you'd send the prompt to the actual NLP model. For now, it returns mocked responses.
        if "feature list" in prompt:
            return json.dumps(["Login system", "Data visualization", "API integration"])
        elif "file and folder structure" in prompt:
            return json.dumps({
                "folders": ["src", "docs", "tests"],
                "files": ["src/app.py", "src/utils.py", "README.md"]
            })
        elif "implementation plan" in prompt:
            return "Setup project structure -> Implement login system -> Add data visualization -> Integrate external API"
        elif "implementation" in prompt:
            return json.dumps({"response": "def main():\n    print('Hello, world!')", "file_path": "src/app.py"})
        else:
            return "FINISHED WITH SCRIPT"

def ensure_directory_exists(path):
    os.makedirs(path, exist_ok=True)

def write_or_update_file(file_path, content):
    if os.path.exists(file_path):
        base, extension = os.path.splitext(file_path)
        version = 1
        new_file_path = f"{base}_updated{version}{extension}"
        while os.path.exists(new_file_path):
            version += 1
            new_file_path = f"{base}_updated{version}{extension}"
        file_path = new_file_path
    with open(file_path, 'w') as file:
        file.write(content)

def main():
    dotenv_path = os.path.join(os.path.dirname(__file__), 'config', '.env')
    openAI = OpenAIKeyLoader(dotenv_path)
    nlp_client = NLPClient()
    memory_manager = ModuleMemory()
    project_folder_creator = ProjectFolderCreator(memory_manager)
    project_folder_creator.create_project_directory()
    nlp_processor = NLPProcessor(memory_manager)
    generator = PromptGenerator()
    prompt_context = []

    project_name = input("Enter project name: ")
    project_description = input("Enter project description: ")

    prompt_context.append(project_name)
    prompt_context.append(project_description)
    role = "You are a great App Developer"
    messages = []
    messages.append({"role": "system", "content": role})

    # Generate prompt and get feature list
    feature_list_context = PromptContext(
        role="You are a great App Developer",
        simple_prompt="Based on the given project title and description, provide a comprehensive feature and functionality list.",
        context_items={"project_name": project_name, "project_description": project_description},
        instructions=["Prepare a list of features and functionalities for the project.",
                      "Include all the necessary features for a complete application."],
    )
    generator.set_context(feature_list_context)
    prompt = generator.generate_prompt()
    messages.append({"role": "user", "content": prompt})
    response = nlp_processor.process(messages, feature_list_context)
    features = response
    messages.append({"role": "assistant", "content": features})
    print("Features:", features)

    # Generate prompt and get file and folder structure
    structure_context = PromptContext(
        role="You are a great App Developer",
        simple_prompt="Based on the feature list, provide the file and folder structure for the project.",
        # context_items={"feature_list": features},
        instructions=["Prepare a file and folder structure for the project.",
                      "Include all the necessary files and folders for a complete application."],
    )
    generator.set_context(structure_context)
    prompt = generator.generate_prompt()
    messages.append({"role": "user", "content": prompt})
    response = nlp_processor.process(messages, structure_context)
    structure = response
    messages.append({"role": "assistant", "content": structure})
    print("Structure:", structure)


    # Generate Implementation Plan
    plan_context = PromptContext(
        role="You are a great App Developer",
        simple_prompt="Based on the file and folder structure, provide a plan for implementation.",
        # context_items={"structure": structure},
        instructions=["Prepare a plan for implementing the project.",
                      "Include all the necessary steps for a complete application."],
    )
    generator.set_context(plan_context)
    prompt = generator.generate_prompt()
    messages.append({"role": "user", "content": prompt})
    response = nlp_processor.process(messages, plan_context)
    plan = response
    messages.append({"role": "assistant", "content": plan})
    print("Plan:", plan)


    def parse_response(response):
        try:
            # Try parsing the response as is
            return json.loads(response)
        except json.decoder.JSONDecodeError as e:
            # If a JSONDecodeError is encountered, try fixing the quotes
            try:
                corrected_response = response.replace("'", '"')
                return json.loads(corrected_response)
            except Exception as e:
                # Log the error, raise an exception, or handle it as needed
                print(f"Failed to parse the response even after quote correction: {e}")
                raise


    # Generate prompt and get implementation
    initial_implementation_context = PromptContext(
        role="You are a great App Developer",
        simple_prompt="Lets start implementing the project. Please generate a comprehensive and well coded implementation code for an initial file.",
        # context_items={"plan": plan},
        response_format="json",
        response_structure={"file_path": str, "code": str},
        instructions=["Generate the code for the initial file.",
                      "Follow the plan for implementation.",
                      "Provide the response in the given response format and structure."],
    )
    generator.set_context(initial_implementation_context)
    prompt = generator.generate_prompt()
    messages.append({"role": "user", "content": prompt})
    response = nlp_processor.process(messages, initial_implementation_context)
    parsed_response = parse_response(response)
    implementation = json.loads(response)
    file_path = implementation["file_path"]
    file_content = implementation["code"]
    messages.append({"role": "assistant", "content": response})
    print("Implementation:", file_content)


    # Check and create folder structure
    # ensure_directory_exists(os.path.dirname(file_path))
    # write_or_update_file(file_path, file_content)
    # print("File created at:", file_path)

    # Loop for file implementation
    while "FINISHED WITH SCRIPT" not in file_content:
        implementation_context = PromptContext(
            role="You are a great App Developer",
            simple_prompt="Great! Lets continue with the next file. Please generate a comprehensive and well coded implementation code for the next file.",
            response_format="json",
            response_structure={"file_path": str, "code": str},
            instructions=["Generate the code for the next file.", "Provide the response in the given response format and structure."],
        )
        generator.set_context(implementation_context)
        prompt = generator.generate_prompt()
        print()
        print ("prompt:", prompt)
        print()
        print ("messages:", messages)
        print()
        messages.append({"role": "user", "content": prompt})
        response = nlp_processor.process(messages, implementation_context)
        parsed_response = parse_response(response)
        implementation = parsed_response
        file_path = implementation["file_path"]
        file_content = implementation["code"]
        messages.append({"role": "assistant", "content": response})
        print("Implementation:", file_content)

        # Check and create folder structure
        # ensure_directory_exists(os.path.dirname(file_path))
        # write_or_update_file(file_path, file_content)
        # print("File created at:", file_path)

    memory_manager.save_to_file("memory.json")


if __name__ == "__main__":
    main()


## simple_generator.py:

import os

# Function to interact with NLP model (mockup, replace with actual API calls)
def interact_with_nlp(prompt):
    # This function should be replaced with actual API calls to an NLP service
    # For demonstration, we'll return a placeholder response
    return {"response": "Placeholder response", "file_path": "placeholder/path/to/file.py"}

# Function to check and create folder structure
def ensure_folder_structure(path):
    folder_path = os.path.dirname(path)
    if not os.path.exists(folder_path):
        os.makedirs(folder_path)

# Function to handle file creation and updates
def create_or_update_file(file_path, content):
    if os.path.exists(file_path):
        base, extension = os.path.splitext(file_path)
        i = 1
        new_file_path = f"{base}_updated{i}{extension}"
        while os.path.exists(new_file_path):
            i += 1
            new_file_path = f"{base}_updated{i}{extension}"
        file_path = new_file_path

    with open(file_path, 'w') as file:
        file.write(content)
    return file_path

# Main process
def main():
    memory_string = ""

    # Step 1: Request feature list
    project_name_and_description = "Project Name: Example Project, Description: This is an example project description."
    response = interact_with_nlp(project_name_and_description)
    memory_string += "\n" + response["response"]

    # Step 2: Request file and folder structure
    response = interact_with_nlp(memory_string)
    memory_string += "\n" + response["response"]

    # Step 3: Request plan for implementation
    response = interact_with_nlp(memory_string)
    memory_string += "\n" + response["response"]

    # Initialize prompt string with attributes
    prompt_string = f"Instructions: Implement the first file.\nContext: {memory_string}\nTech Stack: Python"

    # Begin loop for file implementation
    while True:
        response = interact_with_nlp(prompt_string)
        file_path = response["file_path"]
        file_content = response["response"]

        if "FINISHED WITH SCRIPT" in file_content:
            break

        # Check and create folder structure
        ensure_folder_structure(file_path)

        # Create or update the file
        actual_file_path = create_or_update_file(file_path, file_content)

        # Update prompt_string for the next iteration
        prompt_string += f"\nFile Path: {actual_file_path}\nResponse: {file_content}"

if __name__ == "__main__":
    main()


## File and Folder Structure:

{
    "": [
        "process.md",
        "MemoryManager.py",
        "ProjectFolderCreator.py",
        "test.py",
        "test2.py",
        "test BACKUP.py",
        "test_json.py",
        "simple_generator.py"
    ]
}
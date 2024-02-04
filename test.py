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
    print ("Creating directory at:", path)
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

    codebase = []

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
            instructions=["Prepare a list of features and functionalities for the project.",
                          "Include all the necessary features for a complete application.",
                          "Also provide the file path in array format like this ['app', 'src'] as file_path_as_array and 'app.py' as file_name for the file app.py in the src folder."],
        )
        generator.set_context(feature_list_context)
        prompt = generator.generate_prompt()
        messages.append({"role": "user", "content": prompt})
        response = nlp_processor.process(messages, feature_list_context)
        features = response
        messages.append({"role": "assistant", "content": response})
        print("Features:", features)

        # Generate prompt and get feature list for the file as well as file_path in array format
        feature_list_context = PromptContext(
            role="You are a great App Developer",
            simple_prompt="Transform the given data into json format.",
            context_items={"<context_information>": features},
            response_format="json",
            response_structure={"features" : [{ "name": str, "description": str}], "file_path_as_array": [str], "file_name": str},
            instructions=["Please return the given <context_information> in json format.",
                          "Also provide the file path in array format like this ['app', 'src'] as file_path_as_array and 'app.py' as file_name for the file app.py in the src folder."],
        )
        generator.set_context(feature_list_context)
        prompt = generator.generate_prompt()
        messages.append({"role": "user", "content": prompt})
        response = nlp_processor.process(messages, feature_list_context)
        parsed_response = parse_response(response)
        features_dict = parsed_response
        file["features"] = features_dict["features"]
        file["file_path_as_array"] = features_dict["file_path_as_array"]
        file["file_name"] = features_dict["file_name"]
        print("Features Dict:", features_dict)


        # Generate prompt and get code implementation
        implementation_context = PromptContext(
            role="You are a great App Developer",
            simple_prompt="Lets start implementing the project step by step and generate the code for the file with the given file_name and file_description and file_features, then improve file by file the codebase.",
            context_items={"file_name": file_name, "file_description": file_description, "file_path": file_path, "file_features": features},
            instructions=["Generate a comprehensive and well coded implementation code for the current file.",
                          "Also generate brief instruction on how to use the file and what it does."],
        )
        generator.set_context(implementation_context)
        prompt = generator.generate_prompt()
        messages.append({"role": "user", "content": prompt})
        response = nlp_processor.process(messages, implementation_context)
        # parsed_response = parse_response(response)
        coded_file = response
        messages.append({"role": "assistant", "content": response})
        print("Coded File:", coded_file)

        # Generate prompt and get code implementation
        implementation_context = PromptContext(
            role="You are a great App Developer",
            simple_prompt="Lets start implementing the project step by step and generate the code for the file with the given file_name and file_description and file_features, then improve file by file the codebase.",
            context_items={"<context_information>": coded_file},
            response_format="json",
            response_structure={"file_path": str, "code": str, "file_instruction": str},
            instructions=["Please return the given <context_information> in json format.",
                          "Place the code in the given file path.",
                          "Also generate brief instruction on how to use the file and what it does.",
                          "Provide the response in the given response format and structure."],
        )
        generator.set_context(implementation_context)
        prompt = generator.generate_prompt()
        messages.append({"role": "user", "content": prompt})
        response = nlp_processor.process(messages, implementation_context)
        parsed_response = parse_response(response)
        coded_file_dict = parsed_response
        file["code"] = coded_file_dict["code"]
        file["file_instruction"] = coded_file_dict["file_instruction"]
        print("Coded File:", coded_file_dict)

        # Check and create folder structure for the file and write the file based on file["file_path_as_array"], example: ["app", "src", "app.py"]
        initial_path = os.path.join(os.getcwd(), project_name)
        new_path_array = [initial_path] + file["file_path_as_array"]
        file_name = file["file_name"]
        file_path = os.path.join(*new_path_array)
        ensure_directory_exists(file_path)
        file_path_with_file_name = os.path.join(file_path, file_name)
        code_str = file["code"]
        write_or_update_file(file_path_with_file_name, code_str)
        # Save file as json
        file_path = file_path.replace(".", "_")
        file_path = file_path + ".json"
        with open(file_path, 'w') as file_to_save:
            json.dump(file, file_to_save)
        print("File created at:", file_path)

        codebase.append(coded_file)
  

    memory_manager.save_to_file("memory.json")


if __name__ == "__main__":
    main()

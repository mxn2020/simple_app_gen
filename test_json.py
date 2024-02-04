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

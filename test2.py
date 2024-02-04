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

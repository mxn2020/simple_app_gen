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
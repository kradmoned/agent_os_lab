import os
import pymupdf
from config import MAX_CHARS
from google.genai import types
import re
def get_pdf_content(working_directory, file_path):
    # get the absolute path of working directory
    abs_working_directory  = os.path.abspath(working_directory)
    # Get the absolute path of file
    abs_file_path = os.path.normcase(os.path.abspath(os.path.join(abs_working_directory,file_path)))
    # Check if file is actually inside the directory
    if os.path.commonpath([abs_file_path,abs_working_directory]) != abs_working_directory:
        return f'Error: Cannot read "{file_path}" as it is outside the permitted working directory'
    if not os.path.isfile(abs_file_path):
        return f'Error: File not found or is not a regular file: "{file_path}"'
    if not abs_file_path.endswith(".pdf"):
        return f'Error: "{file_path}" is not a pdf file'
    content = ""
    try:
        with pymupdf.open(abs_file_path) as doc:
            for page in doc:
                page_text = page.get_text("text")
                if len(content) + len(page_text) > MAX_CHARS:
                    content += page_text[:MAX_CHARS-len(content)] 
                    content += f'[...PDF "{file_path}" truncated at {MAX_CHARS} characters]'
                    break
                else:
                    content += page_text
    except Exception as e:
        return f'Error: {e} occured'
    task_pattern = r"(Task\s+\d+.*?)(?=Task\s+\d+|Example\s+\d+|Section\s+\d+|$)"
    example_pattern = r"(Example Task\s+\d+.*?|Example Problem.*?|Problem.*?)(?=Task\s+\d+|Example\s+\d+|Section\s+\d+|Explanation|Problem|$)"
    example = re.findall(example_pattern,content,flags=re.IGNORECASE | re.DOTALL)
    task = re.findall(task_pattern, content, flags=re.IGNORECASE | re.DOTALL)
    total_exercise = example + task
    return "\n".join(total_exercise)

    

    


    # try: 
    #     with open(abs_file_path, "r") as f:
    #         file_content_string = f.read(MAX_CHARS)
    #     # IF f.read(1) return any non empty string then there is additional things located in file    
    #         if f.read(1):
    #             file_content_string += f'[...File "{file_path}" truncated at {MAX_CHARS} characters]'
    # except Exception as e:
    #     return f"Error: {e} occured"
    # return file_content_string


schema_get_pdf_content = types.FunctionDeclaration(
    name= "get_pdf_content",
    description= "Read pdf in a specified directory relative to the working directory, providing what is written in file in a string",
    parameters= types.Schema(
        type= types.Type.OBJECT,
        properties= {
            "file_path" : types.Schema(
                type= types.Type.STRING,
                description= "Directory path to read file content from, relative to the working directory"
            )
        },
        required=["file_path"]
    )
)
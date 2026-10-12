import subprocess
from dotenv import load_dotenv
import os
from groq import Groq

load_dotenv()

groq_api_key = os.getenv("GROQ_API_KEY")
groq_model = os.getenv("GROQ_MODEL")

client = Groq(api_key=groq_api_key)

def write_file(filename, content):
    with open(filename, "w") as file:
        file.write(content)


def read_file(filename):
    with open(filename, "r") as file:
        return file.read()
        # contents = file.read()
        # return contents

# read = read_file("sample.py")
# print(read)


def run_file(filename):
    result = subprocess.run(
        ["python", filename], 
        capture_output=True,
        text=True)
    return result

# write_file(
#     "sample.py",
#     'print("Hello Agent. This is the beginning of building my own coding agent.")'
# )
#
# print(read_file("sample.py"))
MAX_RETRIES = 3
previous_error = None
task = input("Enter the task you want to accomplish: ")
for attempt in range(MAX_RETRIES):
    result = run_file()    #original attempt
    if result.returncode == 0:
        print("Task completed successfully")
        print("OUTPUT:")
        print(result.stdout)
        break

    print(f"Attempt {attempt + 1} failed.")

    broken_code = read_file("sample.py")
    error_message = result.stderr
    if previous_error is not None and previous_error == error_message:
        print("The same error occurred again. Stopping further attempts.")
        break
    previous_error = error_message

    prompt = f"""
            You are a coding agent.

            USER TASK:
            {task}

            Your job is to create the Python program required to accomplish the user's task.

            Rules:
            1. Understand the user's task before generating code.
            2. If the user specifies a filename, use that filename.
            3. If the user does not specify a filename, choose a suitable Python filename based on the task.
            4. Generate the complete Python code required for the task.
            5. Do not assume that a file already exists.
            6. Response should be in the format of {{
            "filename": "filename.py",
             "code": "..."
            }}.
            7. Do not include explanations or markdown.    
                        """

    response = client.chat.completions.create(
            model=groq_model,
            messages=[{"role": "user", "content": prompt}]
        )
        # print(response.choices[0].message.content)
    corrected_code = response.choices[0].message.content

    print("CORRECTED CODE:")
    print(corrected_code)
    write_file("sample.py", corrected_code)



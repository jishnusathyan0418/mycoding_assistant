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
result = run_file("sample.py")    #original attempt

if result.returncode == 0:
    print("Task completed successfully")
else:
    print("Task failed")
    broken_code = read_file("sample.py")
    error_message = result.stderr

    prompt = f"""
        Fix the broken python code
        BROKEN CODE:
        {broken_code}
        ERROR:
        {error_message}
        Return only the corrected code without any explanation or additional text. Do not provide explanations. Do not use markdown formatting. Do not include any text outside of the corrected code.    
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
    retry_result = run_file("sample.py")   #attempt after the LLM fix

    print("Second attempt to run the code after LLM fix:")
    if retry_result.returncode == 0:
        print("Task completed successfully after LLM fix")
        print("OUTPUT:")
        print(retry_result.stdout)
    else:
        print("Task failed even after LLM fix")
        print("NEW ERROR:")
        print(retry_result.stderr)



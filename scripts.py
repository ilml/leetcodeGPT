"""
Input: LC questions number
Process:
Use leetcode cli to get the question description
Find the class definition in the local file system
Form a prompt and send to openai service
Receive the response and parse it
Send the response to leetcode cli to submit the answer
Return: LC OJ response

@tom 2023-08-19

"""
import os
import sys
import subprocess
from config import *
from utils import *


def generate_lc_question(question):
    cmd = ["leetcode", "p" ,  question]
    process = subprocess.Popen(cmd, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    stdout, stderr = process.communicate()
    # rm the cache file first
    cmd = f"rm /root/.leetcode/code/{question}.*"
    try:
        process = subprocess.Popen(cmd, shell=True, stdout=subprocess.PIPE)
        _, _ = process.communicate()
    except FileNotFoundError:
        pass  # Do nothing, suppress the error
    cmd = ["leetcode", "e" ,  question]
    process = subprocess.Popen(cmd, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    _, _ = process.communicate()
    description = stdout.decode().replace('is on the run...\n\n', '')
    return description

def find_file_by_number(directory, number):
    files = os.listdir(directory)
    matching_files = [f for f in files if f.startswith(number+'.')]
    return os.path.abspath(os.path.join(directory, matching_files[0])) if matching_files else None

def generate_prompt(description, class_def):
    return PREFIX + description + PROMPT +  class_def + RESPONSE 
    
def send_to_openai(prompt):
    response = openai.Completion.create(
      model= MODEL,
      prompt= prompt,
      temperature=1,
      max_tokens=MAX_TOKENS,
      top_p=1,
      frequency_penalty=0,
      presence_penalty=0
    )
    return response 

def parse_response_gpt3_5(response):
    code_content = response["choices"][0]["message"]["content"]
    # Splitting the content to extract the code section
    code_start = code_content.index("```") + 10 
    code_end = code_content.rindex("```")
    code = code_content[code_start:code_end].strip()
    return code

def parse_response_davinci(response):
    code_content = response["choices"][0]["text"]
    if code_content.startswith("\""):
        code_content = code_content[2:]
    code_content.strip()
    # Splitting the content to extract the code section
    return code_content

def submit_to_lc(question):
    cmd = ["leetcode", "x" ,  question]
    process = subprocess.Popen(cmd, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    stdout, stderr = process.communicate()
    stdout = stdout.decode().replace("Stdout:", '').strip()
    return stdout 

def generate_debug_prompt(solution, oj_response):
    return f"\n This is your previous solution: {solution} \n This solution is not correct, here is the debug information:\n{oj_response}\n  please debug your code and retun a correct answer."

def generate_solve_prompt(description, class_def):
    return description + PROMPT +  class_def

def generate_executable(code, unit_test):
    return code + "\n" + unit_test

if __name__ == "__main__":
    start = int(sys.argv[1])
    end = int(sys.argv[2])
    shot = int(sys.argv[3])
    for question in range(start, end):
        question = str(question)
        print("Processing question: " + question)
        description = generate_lc_question(question)
        write_file(LC_PATH + question + ".txt", description)
        question_file =  find_file_by_number(QUESTION_PATH, question)
        class_def = read_file(question_file)
        prompt = generate_prompt(description, class_def).__repr__()
        write_file(PROMPT_PATH + question + ".prompt", prompt)
        response = send_to_openai(prompt)
        write_json(GPT_PATH + question + ".json", response)
        code = parse_response_davinci(response.to_dict())
        write_file(question_file, code)
        oj_response = submit_to_lc(question)
        print(oj_response)
        write_file(OJ_PATH + question + ".txt", oj_response)

    
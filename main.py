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
import openai
import json


PREFIX = "### Instruction: You are a helpful AI Assistant. Please provide python code based on the user's instructions, please only return python code and the code ### Input: "
PROMPT = "Return the solution using the following class definition:\n"
openai.api_key = "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"
MODEL = "text-davinci-003"
QUESTION_PATH = "/root/.leetcode/code/"
LC_PATH = "./data/lc/"
GPT_PATH = "./data/gpt/"
PROMPT_PATH = "./data/prompt/"
OJ_PATH = "./data/oj/"
MAX_TOKENS = 2000

def read_file(file_name):
    with open(file_name, 'r') as file:
        content = file.read()
    return content

def write_file(file_name, content):
    with open(file_name, 'w') as file:
        file.write(content)

def write_json(file_name, data):
    with open(file_name, "w") as outfile:
        json.dump(data, outfile)

def generate_lc_question(question):
    cmd = ["leetcode", "p" ,  question]
    process = subprocess.Popen(cmd, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    stdout, stderr = process.communicate()
    cmd = ["leetcode", "e" ,  question]
    process = subprocess.Popen(cmd, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    _ , _ = process.communicate()
    return stdout.decode() 

def find_file_by_number(directory, number):
    files = os.listdir(directory)
    matching_files = [f for f in files if f.startswith(number+'.')]
    return os.path.abspath(os.path.join(directory, matching_files[0])) if matching_files else None

def generate_prompt(description, class_def):
    description = description[5:]
    description = description.replace('is on the run...\n\n', '')
    return PREFIX + description + PROMPT +  class_def + "### Response:"
    
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
    return stdout.decode() 

if __name__ == "__main__":
    start = int(sys.argv[1])
    end = int(sys.argv[2])
    for question in range(start, end):
        question = str(question)
        print("Processing question: " + question)
        description = generate_lc_question(question)
        write_file(LC_PATH + question + ".txt", description)
        question_file =  find_file_by_number(QUESTION_PATH, question)
        class_def = read_file(question_file)
        prompt = generate_prompt(description, class_def).__repr__()
        # prompt = "1+1="
        # print(prompt)
        write_file(PROMPT_PATH + question + ".prompt", prompt)
        response = send_to_openai(prompt)
        write_json(GPT_PATH + question + ".json", response)
        code = parse_response_davinci(response.to_dict())
        write_file(question_file, code)
        oj_response = submit_to_lc(question)
        print(oj_response)
        write_file(OJ_PATH + question + ".txt", oj_response)

    
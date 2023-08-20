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



PROMPT = "Return the solution using the following class definition:\n"
openai.api_key = "add your key here"
MODEL = "gpt-3.5-turbo"
QUESTION_PATH = "/root/.leetcode/code/"
LC_PATH = "./data/lc/"
GPT_PATH = "./data/gpt/"
PROMPT_PATH = "./data/prompt/"
OJ_PATH = "./data/oj/"

PROMPT_test = 'Two Sum \nGiven an array of integers nums\xa0and an integer target, return indices of the two numbers such that they add up to target.\n\nYou may assume that each input would have exactly one solution, and you may not use the same element twice.\n\nYou can return the answer in any order.\n\n\xa0\nExample 1:\n\nInput: nums = [2,7,11,15], target = 9\nOutput: [0,1]\nExplanation: Because nums[0] + nums[1] == 9, we return [0, 1].\n\n\nExample 2:\n\nInput: nums = [3,2,4], target = 6\nOutput: [1,2]\n\n\nExample 3:\n\nInput: nums = [3,3], target = 6\nOutput: [0,1]\n\n\n\xa0\nConstraints:\n\n\n\t2 <= nums.length <= 10⁴\n\t-10⁹ <= nums[i] <= 10⁹\n\t-10⁹ <= target <= 10⁹\n\tOnly one valid answer exists.\n\n\n\xa0\nFollow-up:\xa0Can you come up with an algorithm that is less than O(n²)\xa0time complexity?\nReturn the solution using the following class definition:\nclass Solution:\n    def twoSum(self, nums: List[int], target: int) -> List[int]:\n        \n'
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
    return description + PROMPT +  class_def
    
def send_to_openai(prompt):
    response = openai.ChatCompletion.create(
      model= MODEL,
      messages=[
        {
          "role": "user",
          "content": prompt,
        }
      ],
      temperature=1,
      max_tokens=1000,
      top_p=1,
      frequency_penalty=0,
      presence_penalty=0
    )
    return response 

def parse_response(response):
    code_content = response["choices"][0]["message"]["content"]
    # Splitting the content to extract the code section
    code_start = code_content.index("```") + 10 
    code_end = code_content.rindex("```")
    code = code_content[code_start:code_end].strip()
    return code

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
        write_file(PROMPT_PATH + question + ".prompt", prompt)
        response = send_to_openai(prompt)
        write_json(GPT_PATH + question + ".json", response)
        code = parse_response(response.to_dict())
        write_file(question_file, code)
        oj_response = submit_to_lc(question)
        write_file(OJ_PATH + question + ".txt", oj_response)

    
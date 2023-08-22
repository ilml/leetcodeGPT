"""
class for solve one leetcode question
Solve process:
generate promt -> model response -> parse code -> OJ -> debug info -> generate prompt ... until AC

Memory dict: 
step: (prompt, model_response, code, oj_response)

@tom 2023-08-21
"""

from scripts import *
from collections import deque

class leetcodeGPT:
    def __init__(self,
                 question, # question number in leetcode
                 n_debug = 0, # times of debug, default 0 means no debug, just sumbit for one time
                 n_history = 0, # lengths of history, default 0 means no history 
                 model="text-davinci-003" # model to use, default davinci-003
                ):
        self.question = question
        self.n_debug = n_debug
        self.n_history = n_history
        self.model = model
        self.step = 0
        self.memory = dict() # memory of everything
        self.description = generate_lc_question(question) # description of the question
        self.solution_file = find_file_by_number(QUESTION_PATH, question) # solution file
        self.class_def = read_file(self.solution_file)   # class definition of the question
    
    def _add_step(self):
        """ Must/Only call this function to modify step
        """
        self.step += 1
    

    def generate_prompt(self):
        """ Generate prompt for one round with historical debug information
        """
        if self.step == 0: # first round, we only need description and class definition
            prompt = PREFIX + self.description + PROMPT +  self.class_def + RESPONSE 
        else: # We form the prompt from historical prompts and current debug information
            for i in range(self.step - self.n_history, self.step):
                prompt += self.memory[i]["prompt"] + "\n" + self.memory[i]["model_response"] + "\n" + self.memory[i]["code"] + "\n" + self.memory[i]["oj_response"] + "\n"
        return prompt


    def submit(self, answer):
    
    def process_oj_response(self, oj_response):

    def solve(self, question):
        question = str(question)
        print("Solving question: " + question)
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

    
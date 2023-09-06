"""
class for solve one leetcode question
Solve process:
generate promt -> model response -> parse code -> OJ/local unit tests -> debug info -> generate prompt ... until AC

Memory dict: 
step: (prompt, debug_prompt, model_response, code, execute_result)

@tom 2023-08-21
"""

from scripts import *
from collections import defaultdict
from execute import check_correctness

MEMORY_SEGMENT = ["prompt", "debug_prompt", "model_response", "code", "execute_result"]

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
        self.memory = defaultdict(dict) # memory of everything
        self.description = generate_lc_question(question) # description of the question
        self.solution_file = find_file_by_number(QUESTION_PATH, question) # solution file
        self.class_def = read_file(self.solution_file)   # class definition of the question
        self.solve_prompt = generate_solve_prompt(self.description, self.class_def)
        self.unit_test = None
    
    def _add_step(self):
        """ Must/Only call this function to modify step
        """
        self.step += 1

    def _add_memory(self, mem_seg, mem_value):
        """ Must/Only call this function to modify memory
        """
        assert mem_seg in MEMORY_SEGMENT
        self.memory[self.step][mem_seg] = mem_value

    def generate_prompt(self):
        """ Generate prompt for one round with historical debug information
        """
        if self.step == 0: # first round, we only need description and class definition
            prompt = PREFIX + self.solve_prompt + RESPONSE 
        else: # We form the prompt from historical prompts and current debug information
            debug_prompt = ""
            for i in range(self.step - self.n_history, self.step):
                debug_prompt += self.memory[i]["debug_prompt"]
            prompt = PREFIX + self.solve_prompt + debug_prompt + RESPONSE 
        return prompt
        
        
    def solve(self, use_unit_test = True):
        """ Solve the question 
        """
        for _ in range(self.n_debug + 1):
            print("Solving question: " + self.question + " at step " + str(self.step))
            prompt = self.generate_prompt()
            self._add_memory("prompt", prompt)
            response = send_to_openai(prompt)
            self._add_memory("model_response", response)
            code = parse_response_davinci(response.to_dict())
            self._add_memory("code", code)
            write_file(self.solution_file, code)
            if use_unit_test:
                executable = generate_executable(code, self.unit_test)
                execute_result = check_correctness(executable) 
            else:
                execute_result = submit_to_lc(self.question)
            self._add_memory("execute_result", execute_result)
            if "Success" in execute_result: 
                write_json(MEM_PATH + self.question + ".json", self.memory)
                print("question " + self.question + " solved at step " + str(self.step))
                return
            else:
                debug_prompt = generate_debug_prompt(code, execute_result)
                self._add_memory("debug_prompt", debug_prompt)
            self._add_step()
        write_json(MEM_PATH + self.question + ".json", self.memory)
        print("question " + self.question + " can't be solved within " + str(self.n_debug+1) + " steps")

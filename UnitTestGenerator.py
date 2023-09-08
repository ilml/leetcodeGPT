"""
generate unit test for a question

@tom 2021-09-06
"""
from scripts import *

class UnitTestGenerator:
    def __init__(self, 
                 question, 
                 model="text-davinci-003"):
        self.question = question
        self.model = model
        self.step = 0
        self.description = generate_lc_question(question) # description of the question
        self.solution_file = find_file_by_number(QUESTION_PATH, question) # solution file
        self.class_def = read_file(self.solution_file)   # class definition of the question
        self.prompt = generate_unit_test_prompt(self.description, self.class_def)
    
    def generate_unit_test(self):
        response = send_to_openai(self.prompt, self.model)
        code = parse_response_davinci(response.to_dict())
        write_json(UNIT_TEST_PATH + self.question + ".json", code)

    def save_prompt(self):
        write_file(UT_PROMPT_PATH + self.question + ".prompt", self.prompt)


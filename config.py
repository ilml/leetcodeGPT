import openai
openai.api_key = 
MODEL = "text-davinci-003"
MAX_TOKENS = 2000

QUESTION_PATH = "/root/.leetcode/code/"
LC_PATH = "./data/lc/"
GPT_PATH = "./data/gpt/"
PROMPT_PATH = "./data/prompt/"
OJ_PATH = "./data/oj/"
MEM_PATH = "./data/mem/"

PREFIX = "### Instruction: You are a helpful AI Assistant. Please provide python solution based on the user's instructions, please only return python code. ### Input: "
PROMPT = "Return the solution using the following class definition:\n"
RESPONSE = "### Response:"
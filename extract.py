import json
import sys

def extract_code_from_json(filename):
    with open(filename, 'r') as file:
        data = json.load(file)

    code_content = data["choices"][0]["message"]["content"]

    # Splitting the content to extract the code section
    code_start = code_content.index("```") + 10 
    code_end = code_content.rindex("```")
    code = code_content[code_start:code_end].strip()

    return code


if __name__ == "__main__":
    
    filename = sys.argv[1]
    # print(extract_code_from_json(filename))
    with open(sys.argv[2], 'w') as file:
        file.write(extract_code_from_json(filename))
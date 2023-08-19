import json
import sys

def extract_code_from_json(filename):
    with open(filename, 'r') as file:
        data = json.load(file)

    code_content = data["choices"][0]["message"]["content"]

    # Splitting the content to extract the code section
    code_start = code_content.index("```") + 3
    code_end = code_content.rindex("```")
    code = code_content[code_start:code_end].strip()

    return code


if __name__ == "__main__":
    if len(sys.argv) != 2:
        print("Usage: python extract_code.py <path_to_json_file>")
        sys.exit(1)
    
    filename = sys.argv[1]
    print(extract_code_from_json(filename))

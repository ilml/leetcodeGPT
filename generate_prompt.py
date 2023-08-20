import sys

PROMPT = "Return the solution using the following class definition:\n"

filename = sys.argv[1]

with open(filename, 'r') as file:
    content = file.read()
content = content[5:]
content = content.replace('is on the run...\n\n', '')
print(content)

with open(sys.argv[2], 'r') as file:
    class_def = file.read()

content = content + PROMPT +  class_def
#print(content)
#print(repr(content))
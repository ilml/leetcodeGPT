import subprocess
import sys

filename = sys.argv[1]
cmd = ["leetcode", "p" ,  filename]

process = subprocess.Popen(cmd, stdout=subprocess.PIPE, stderr=subprocess.PIPE)

stdout, stderr = process.communicate()
with open("./data/lc/" + filename + ".txt", 'a') as file:
    file.write(stdout.decode())

cmd = ["leetcode", "e" ,  filename]
process = subprocess.Popen(cmd, stdout=subprocess.PIPE, stderr=subprocess.PIPE)


# print(stdout.decode())



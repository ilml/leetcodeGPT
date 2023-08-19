import subprocess
import sys

filename = sys.argv[1]
cmd = ["leetcode", "p" ,  filename]

process = subprocess.Popen(cmd, stdout=subprocess.PIPE, stderr=subprocess.PIPE)

stdout, stderr = process.communicate()

print(stdout.decode())



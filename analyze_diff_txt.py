import re
import sys

diff_path = "diff/diff.txt"
if(len(sys.argv) > 1):
    diff_path = str(sys.argv[1])
start = 4
end = 8
if(len(sys.argv) > 3):
    start = int(sys.argv[2])
    end = int(sys.argv[3])

diff_file = open(diff_path, "r")
dict = {}
for line in diff_file:
    array = re.split('/',line)
    key = '/'.join(array[start:end]).rstrip("\n\r")
    if key in dict:
        value = dict.get(key) + 1
        dict[key] = value
    else:
        dict[key] = 1

for key in dict:
    print("{} {}".format(key, dict[key]))

diff_file.close()
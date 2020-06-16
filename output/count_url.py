'''
file = open("words.txt", "r")
count = 0
output = open("unique_url.txt", "a")
line = file.readline()
while line != "":
    if "==================" in line:
        line = file.readline()
        output.write(line)
        count += 1
    line = file.readline()
print(count)
file.close()
output.close()
'''

output = open("unique_url.txt")
output_2 = open("real_unique_url.txt", "w")
all_url = []
line = output.readline().rstrip("\n")
while line != "":
    line = line.replace("https", "http")
    combo = line.split(" ")
    all_url.append(combo[0])
    line = output.readline().rstrip("\n")
print("Before set:", len(all_url))
all_url = list(set(all_url))
print("After set:", len(all_url))
for i in all_url:
    print(i)
    output_2.write(str(i) + "\n")
output.close()
output_2.close()

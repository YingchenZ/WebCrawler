all_url_list = []
file = open("output3.txt", "r")
line = file.readline()
while line != "":
    all_url_list.append(line)
    line = file.readline()
file.close()
print("All urls:", len(all_url_list))
all_url_list = list(set(all_url_list))
print("All non repeat urls:", len(all_url_list))
file2 = open("output_nonrepeat_3.txt", "w")
for url in all_url_list:
    file2.write(str(url))
file2.close()

f = open("data.txt", "r", encoding='utf-8')
k = f.readlines()[0].split("。")
f.close()
f = open("handle.txt", "w+", encoding='utf-8')
for item in k:
    LIST = item.split(" ")
    if len(LIST)>2:
        f.write(LIST[2].split("：")[1][:-1]+"\n")
f.close()

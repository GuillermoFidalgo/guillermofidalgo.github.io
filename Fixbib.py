def fixbib(data):
    for id, line in enumerate(data):
        if "$" in line:
            line = line.replace("$", "$$").replace(r"\_", "_")
            print(f'Fixed line {id} with "{line}" ')
            data[id] = line
        if "{{s}_" in line:
            line = line.replace("{{s}_", "{s_")
            print(f'Fixed line {id} with "{line}" ')
            data[id] = line
        # if "" in line:
        #     line = line.replace("</span>","")
        #     print(f'Fixed line {id} with "{line}" ')
        #     data[id] = line


with open("_includes/allPubs.md") as f:
    data = f.readlines()

fixbib(data)
with open("_includes/allPubs.md", "w") as f:
    f.writelines(data)

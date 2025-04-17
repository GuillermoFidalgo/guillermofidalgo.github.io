with open("_includes/allPubs.md") as f:
    data = f.readlines()


def fixbib(data):
    for id, line in enumerate(data):
        if "$" in line:
            line = line.replace("$", "$$").replace(r"\_", "_")
            print(line)
            data[id] = line


fixbib(data)
with open("_includes/allPubs.md", "w") as f:
    f.writelines(data)

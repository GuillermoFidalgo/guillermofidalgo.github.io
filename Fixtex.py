text = r"""
\author{Guillermo Fidalgo}
\date{\today}
\title{Publication List}
\begin{document}
\maketitle
"""

characters = {
    "ψ": r"\psi",
    "ν": r"\nu",
    "γ": r"\gamma",
    "τ": r"\tau",
    "μ": r"\mu",
}
# nitems = len(characters)


def fixbib(data):
    for id, line in enumerate(data):
        # if "ν" in line :
        #     line = line.replace("ν",r"\nu")
        #     print(f'Fixed line {id} with "{line}" ')
        #     data[id] = line

        if r"\author{}" in line:
            data[id : id + 5] = text
            print("added author, title, date and maketitle in lines", id, id + 5)

        for k, v in characters.items():
            if k in line:
                line1 = line.replace(k, v)
                print(f'Fixed line {id} from \n"{line:^30}"\n to \n"{line1:^30}" ')
                data[id] = line1
                line = line1


with open("latex_files/texfile.tex") as f:
    data = f.readlines()

fixbib(data)
with open("latex_files/texfile.tex", "w") as f:
    f.writelines(data)

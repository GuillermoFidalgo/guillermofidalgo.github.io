
text = r'''
\author{Guillermo Fidalgo}
\date{\today}
\title{Publication List}
\begin{document} 
\maketitle
'''

def fixbib(data):
    for id,line in enumerate(data):
        if "ν" in line : 
            line = line.replace("ν",r"\nu")
            print(f'Fixed line {id} with "{line}" ')
            data[id] = line

        # if r"\author" in line:
        #     line = line.replace(r'\author{}',r'\author{Guillermo Fidalgo}')
        #     print(f'Fixed line {id} with "{line}" ')
        #     data[id] = line

        # if r"\date" in line:
        #     line = line.replace(r"\date{}",r"\date{\today}")
        #     print(f'Fixed line {id} with "{line}" ')
        #     data[id] = line


        # if r'\begin{document}' in line:
        #     line = line.replace(r"\begin{document}",r"\begin{document} \maketitle")
        #     print(f'Fixed line {id} with "{line}" ')
        #     data[id] = line            
        if r"\author{}" in line:
            data[id:id+5] = text
            print("added author, title, date and maketitle in lines",id,id+5)

with open("latex_files/texfile.tex") as f:
    data = f.readlines()

fixbib(data)
with open("latex_files/texfile.tex","w") as f:
    f.writelines(data)

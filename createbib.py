import requests, time
pages = [1,2,3]
all_bibtex = ""

for page in pages:
    url = f"https://inspirehep.net/api/literature?sort=mostrecent&size=50&page={page}&q=a Guillermo.Fidalgo.1&format=bibtex"
    # print(url)
    print(f"Getting {page = } ")
    inspire = requests.get(url,).text
    time.sleep(1)
    # print(inspire)
    all_bibtex += inspire + "\n"

zenodo = r"""
@misc{alexander_moreno_briceno_2022_7115834,
  author       = {Alexander Moreno Briceño and Aman Goel and Guillermo Antonio Fidalgo Rodriguez},
  title        = {Teaching Python the Sustainable Way: Lessons Learned at HSF Training},
  month        = sep,
  year         = 2022,
  publisher    = {Zenodo},
  doi          = {10.5281/zenodo.7115834},
  url          = {https://doi.org/10.5281/zenodo.7115834}
}
"""

# Write everything out to a .bib file
if all_bibtex:
    with open("latex_files/bibfile.bib","w",encoding="utf-8") as f:
        f.write(all_bibtex)
        f.write(zenodo)
    print("\n Success! 'latex_files/bibfile.bib' has been created.")
else:
    print("\n No BibTeX entries were successfully retrieved.")



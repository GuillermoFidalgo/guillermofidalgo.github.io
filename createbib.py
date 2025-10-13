import requests

url = "https://inspirehep.net/api/literature?sort=mostrecent&size=250&page=1&q=a Guillermo.Fidalgo.1&format=bibtex"
inspire = requests.get(url).text

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
with open("latex_files/bibfile.bib","w") as f:
    f.write(inspire)
    f.write(zenodo)

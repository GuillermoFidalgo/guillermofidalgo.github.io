import re
import requests, time

GREEK_MACROS = (
    "alpha|beta|gamma|delta|epsilon|eta|theta|lambda|mu|nu|pi|rho|sigma|tau|"
    "phi|chi|psi|omega|Gamma|Delta|Theta|Lambda|Pi|Sigma|Upsilon|Phi|Psi|Omega"
)


def sanitize_bibtex(bib: str) -> str:
    """Fix INSPIRE records whose math is not in math mode, before pandoc runs."""
    # {\Upsilon}(1S) -> {$\Upsilon$}(1S)
    # The lookbehind skips braces that are a macro argument, e.g. \ensuremath{\Upsilon}
    bib = re.sub(rf"(?<![A-Za-z])\{{\\({GREEK_MACROS})\}}", r"{$\\\1$}", bib)
    # INSPIRE sometimes drops the sqrt: "at s=13{\,}{\,}TeV" -> "at $\sqrt{s}=13$ TeV"
    bib = re.sub(
        r"(?<![\w$\\{])s=(\d+(?:\.\d+)?)(?:\{\\,\})*\s*TeV",
        r"$\\sqrt{s}=\1$ TeV",
        bib,
    )
    return bib


pages = [1, 2, 3]
all_bibtex = ""

for page in pages:
    url = f"https://inspirehep.net/api/literature?sort=mostrecent&size=50&page={page}&q=a Guillermo.Fidalgo.1&format=bibtex"
    # print(url)
    print(f"Getting {page = } ")
    inspire = requests.get(
        url,
    ).text
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
    all_bibtex = sanitize_bibtex(all_bibtex)
    with open("latex_files/bibfile.bib", "w", encoding="utf-8") as f:
        f.write(all_bibtex)
        f.write(zenodo)
    print("\n Success! 'latex_files/bibfile.bib' has been created.")
else:
    print("\n No BibTeX entries were successfully retrieved.")

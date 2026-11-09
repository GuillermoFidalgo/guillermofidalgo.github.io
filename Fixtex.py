"""Post-process the pandoc-generated texfile.tex so it compiles with pdflatex.

Title/author/date and extra preamble lines are now handled by pandoc itself
(see latex_files/pandoc-defaults.yaml), so this script only replaces Unicode
characters that pdflatex cannot typeset.
"""

import logging
import re
import sys

TEXFILE = "latex_files/texfile.tex"

# \ensuremath works both inside and outside math mode, and the braces keep a
# following letter from being glued onto the macro name (e.g. "γZ" -> "\gammaZ").
GREEK = {
    "α": "alpha",
    "β": "beta",
    "γ": "gamma",
    "δ": "delta",
    "ε": "epsilon",
    "η": "eta",
    "θ": "theta",
    "λ": "lambda",
    "μ": "mu",
    "ν": "nu",
    "π": "pi",
    "ρ": "rho",
    "σ": "sigma",
    "τ": "tau",
    "φ": "phi",
    "χ": "chi",
    "ψ": "psi",
    "ω": "omega",
    "Γ": "Gamma",
    "Δ": "Delta",
    "Λ": "Lambda",
    "Σ": "Sigma",
    "Υ": "Upsilon",
    "Φ": "Phi",
    "Ψ": "Psi",
    "Ω": "Omega",
}

characters = {k: rf"\ensuremath{{\{v}}}" for k, v in GREEK.items()}
characters[" "] = r" ~ "  # six-per-em space

log = logging.getLogger("Fixtex")


def fixtex(text: str) -> str:
    for k, v in characters.items():
        n = text.count(k)
        if n:
            text = text.replace(k, v)
            log.info("Replaced %d x %r with %s", n, k, v)
    return text


def report_non_ascii(text: str) -> None:
    """Warn about leftover characters pdflatex probably can't typeset, so new
    INSPIRE oddities are obvious here instead of a cryptic TeX error later.
    Accented Latin letters (up to U+017F, e.g. ñ, é) are fine with utf8 inputenc."""
    for lineno, line in enumerate(text.splitlines(), start=1):
        leftover = set(re.findall(r"[^\x00-ſ]", line))
        if leftover:
            log.warning(
                "line %d still has non-ASCII %s: %s",
                lineno,
                sorted(leftover),
                line.strip(),
            )


def main() -> int:
    logging.basicConfig(level=logging.INFO, format="%(levelname)s: %(message)s")
    with open(TEXFILE, encoding="utf-8") as f:
        text = f.read()

    text = fixtex(text)
    report_non_ascii(text)

    with open(TEXFILE, "w", encoding="utf-8", newline="\n") as f:
        f.write(text)
    return 0


if __name__ == "__main__":
    sys.exit(main())

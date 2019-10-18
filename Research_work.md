---
title: My Research
layout: page
---

# Machine Learning for HCAL DQM [report](/assets/Biblatex_version_main.pdf)

# Presentation links
{% assign links=site.data.presentations | sort: 'date' | reverse %}
{%for link in links%}
 1. {{link.date | date_to_long_string }}-*[{{link.link}}]({{link.link}})*
{% endfor %}

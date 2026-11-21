---
title : CV
layout: default
permalink: /cv/
---
{%- comment -%}
  Renders the CV generated from _data/cv.yml by `python cv/build_cv.py`.
  Edit _data/cv.yml, not this file or cv/CV.md.
{%- endcomment -%}
{% include_relative cv/CV.md %}

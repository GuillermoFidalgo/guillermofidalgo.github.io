---
layout: page
title: Outreach and Education
permalink: /outreach/
---

{%- comment -%}
  Everything listed here comes from _data/cv.yml:
  `teaching`, `mentoring`, `outreach` and `service`.
{%- endcomment -%}

Beyond research, I spend a good part of my time teaching, mentoring and serving the science community, with a particular focus on students and teachers in Puerto Rico and on training the next generation of HEP researchers.

## Software Training Workshops

Workshops I have taught or mentored on the software tools used in high-energy physics analysis (e.g. Python, Git, machine learning and the HEP software ecosystem), aimed at audiences ranging from students to new postdocs.

{% assign items = site.data.cv.teaching | sort: "date" | reverse %}
{% for e in items %}
1. {% if e.url %}[*__{{ e.title }}__*]({{ e.url | relative_url }}){% else %}*__{{ e.title }}__*{% endif %}{% if e.role %} ({{ e.role }}){% endif %} - {{ e.location }}{% capture when %}{% include cv_date.html date=e.date end=e.end period=e.period %}{% endcapture %}{% if when != "" %} - {{ when }}{% endif %}
{% endfor %}

## Student Mentoring

{% assign items = site.data.cv.mentoring | sort: "date" | reverse %}
{% for e in items %}
1. {% if e.url %}[**{{ e.title }}**]({{ e.url | relative_url }}){% else %}**{{ e.title }}**{% endif %} - {{ e.location }}{% capture when %}{% include cv_date.html date=e.date end=e.end period=e.period %}{% endcapture %}{% if when != "" %} - {{ when }}{% endif %}{% if e.description %}. {{ e.description }}{% endif %}
{% endfor %}

## Education and Outreach Activities Organized

I have developed, organized and mentored the following education and outreach activities with high school teachers and students in Puerto Rico.

{% assign items = site.data.cv.outreach | sort: "date" | reverse %}
{% for e in items %}
1. {% if e.url %}[**"{{ e.title }}"**]({{ e.url | relative_url }}){% else %}**"{{ e.title }}"**{% endif %} ({{ e.location }}){% capture when %}{% include cv_date.html date=e.date end=e.end period=e.period %}{% endcapture %}{% if when != "" %} - {{ when }}{% endif %}{% if e.description %} - {{ e.description }}{% endif %}
{% endfor %}

## Judging and Service

Service to the science education community in Puerto Rico.

{% assign items = site.data.cv.service | sort: "date" | reverse %}
{% for e in items %}
1. **{{ e.role }}**, {% if e.url %}[{{ e.organization }}]({{ e.url | relative_url }}){% else %}{{ e.organization }}{% endif %} ({{ e.location }}){% capture when %}{% include cv_date.html date=e.date end=e.end period=e.period %}{% endcapture %}{% if when != "" %} - {{ when }}{% endif %}{% if e.description %}. {{ e.description }}{% endif %}
{% endfor %}

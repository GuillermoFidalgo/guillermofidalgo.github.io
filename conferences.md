---
title: Talks at International/National conferences
permalink: /conf_talks/
---

{%- comment -%} Edit talks in _data/cv.yml (the `talks:` list). {%- endcomment -%}
{% assign talks = site.data.cv.talks | sort: "date" | reverse %}

{% for talk in talks %}
1. {% if talk.url %}[*__{{ talk.title }}__*]({{ talk.url | relative_url }}){% else %}*__{{ talk.title }}__*{% endif %}{% if talk.type == "poster" %} (poster){% endif %} at {{ talk.event }} ({{ talk.location }}){% assign when = "" %}{% capture when %}{% include cv_date.html date=talk.date end=talk.end period=talk.period %}{% endcapture %}{% if when != "" %} - {{ when }}{% endif %}
{% endfor %}

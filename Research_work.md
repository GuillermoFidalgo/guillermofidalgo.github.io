---
title: Weekly TKDQM meetings
layout: page
---
# Main link
[https://indico.cern.ch/category/10166/](https://indico.cern.ch/category/10166/) (CMS Only)


# Presentation links


{% assign presents_ByYear =
    site.data.presentations | sort: 'date' | reverse | group_by_exp:"post", "post.date | date: '%Y'"  %}

{% for year in presents_ByYear %}
<h1>{{ year.name }}</h1>

{% assign postsByMonth = year.items | group_by_exp:"post", "post.date | date: '%B'" %}

{% for month in postsByMonth %}
## {{month.name}}
{% for link in month.items %}
  1. {{link.date | date_to_long_string }}-*[{{link.link}}]({{link.link}})*
{% endfor %}
{% endfor %}
{% endfor %}

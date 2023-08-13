--- 
title: Talks at International/National conferences
permalink: /conf_talks/
---

{% assign confs = site.data.sorted_confs | sort: "date"  | reverse %}

{% for talk in confs %}
{% assign date_ord = talk.date | date_to_string: "ordinal", "US"  %}

{% if talk.title != "" %}
1. [*__{{talk.title}}__*]({{talk.url|relative_url}}) at {{talk.location}} - {{date_ord}} 
{% endif %}

{% endfor %}
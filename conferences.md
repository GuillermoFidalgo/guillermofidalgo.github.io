--- 
title: Conference Talks
permalink: /conf_talks/
---



{% for talk in site.data.Conference %}
{% if talk.title != "" %}
1. [*__{{talk.title}}__*]({{talk.url|relative_url}}) at {{talk.location}} - {{talk.date}} 
{% endif %}
{% endfor %}
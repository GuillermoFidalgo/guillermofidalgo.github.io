--- 
title: Conference Talks
permalink: /conf_talks/
---



{% for talk in site.data.Conference %}
{% if talk.title != "" %}
1. [*__{{talk.title}}__*]({{talk.url}}) at {{talk.location}} - {{talk.date}} 
{% endif %}
{% endfor %}
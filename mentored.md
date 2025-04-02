---
title: Software Training Workshops Mentored
permalink: /mentored/
---


{% for talk in site.data.sorted_mentored %}
{% assign date_ord = talk.date | date_to_string: "ordinal", "US" %}
{% if talk.title != "" %}
1. [*__{{talk.title}}__*]({{talk.url}}) - ({{talk.location}}) - {{date_ord}}
{% endif %}
{% endfor %}


## Education and Outreach activities organized

I have developed, organized and mentored the following education and outreach activities with high school teachers and students Puerto Rico.

1. [**"Machine Learning Basics"**](https://indico.cern.ch/event/1353933/) (CROEM, Mayagüez, Puerto Rico) - Nov 28, 2023
1. [**"Python Programming Series: Machine Learning"**](https://indico.cern.ch/event/1353942/) (UPRM, Puerto Rico) -  Nov 17, 2023
2. [**"Python Programming Series: Pandas"**](https://indico.cern.ch/event/1353941/) (UPRM, Puerto Rico) - Nov 10, 2023
3. [**"Python Programming Series: Matplotlib"**](https://indico.cern.ch/event/1353937/) (UPRM, Puerto Rico) - Oct 6, 2023
4. [**"Machine Learning Training for Physics Undergrads"**](https://indico.cern.ch/event/1327230/) (UPRM, Puerto Rico) - Sep 16 - Sep 17, 2023
5. [**"Python Programming Series: Basics"**](https://indico.cern.ch/event/1353934/) (UPRM, Puerto Rico) - Sept 15, 2023
6. [**"Coding Camp"**](https://indico.cern.ch/event/1305236/) (Virtual) - July 10 - July 12, 2023
7. [**"Python 101 for STEM Teacher"**](https://indico.cern.ch/event/1180502/) (UPRM, Puerto Rico) - August 20, 2022
8. [**"Python 101 for STEM Teachers @CROEM"**](https://indico.cern.ch/event/1188757/) (CROEM, Mayagüez, Puerto Rico) - August 17, 2022
9. **"Astronomy Course for CROEM high school students"** (Virtual) - Jan - May 2021 - Complemented the programming side of an introductory course of Physics and Astronomy with Python programming and exercises for local high school students.
10. [**"2020 STEM Teachers Workshop"**](https://indico.cern.ch/event/860466/) (Virtual) - 15-16 July, 2021 - Workshop dedicated to enabling K-12 teachers with python coding language.
11. [**"Machine Learning Basics for STEM Teachers"**](https://indico.cern.ch/event/998732/) (Virtual) - February 13-14, 2021
12. [**"Data Analysis for STEM Teachers"**](https://indico.cern.ch/event/927162/) (Virtual) - July 15-16, 2020
13. [**"Introduction to python programming for Undergrads"**](https://indico.cern.ch/event/891702/timetable/?view=standard) (UPRM, Puerto Rico) - 22 February, 2020 - Workshop intended to teach local Physics students with python coding language with HEP applications.
14. [**"STEM Teachers Workshop"**](https://indico.cern.ch/event/817539/) (UPRM, Puerto Rico) - 3-4 June, 2019
    Workshop dedicated to enabling high school STEM teachers with coding.

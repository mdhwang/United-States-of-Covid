# UNITED STATES OF COVID

## Dashboard tracking COVID-19 spread across the USA

On Dec 31, 2019, the World Health Organization (WHO) was informed an outbreak of “pneumonia of unknown cause” detected in Wuhan, Hubei Province, China. The virus that caused the outbreak of COVID-19 was lately known as severe acute respiratory syndrome coronavirus 2 (SARS-CoV-2). The WHO declared the outbreak to be a Public Health Emergency of International Concern on Jan 30, 2020 and recognized it as a pandemic on Mar 11, 2020.

Since then, we've been in an endless 24/7 permanent press spin cycle of COVID news.

To help visualize it I created a website that serves as an interactive dashboard that automatically tracks daily cases as published by the New York Times.

Go check it out at [https://united-states-of-covid.herokuapp.com/](https://united-states-of-covid.herokuapp.com/)
<br>
(Note: Might take a little to load since it's on the free tier of Heroku 😬)

![Website_Overview](/images/Website_Overview.png)

Included is a map of the United States down to the county level that uses the current Covid case count with 2019 US Census population data to calculate the percentage of population that has been confirmed as infected.

![Population_Infected_Gif](/images/Percentage_Population_Infected_County_Level.gif)

There are also two charts that track the timeline of case and death count since the first occurance in the United States.  One follows the cumulative count and the other tracks the daily increase numbers.

![Cumulative_Tracker](/images/Case_Timeline.png)

![Daily_Tracker](/images/Daily_Increase_Timeline.png)

Next is a overall case map and table with all the data that was collected so far.

![Cumulative_Case_Map](/images/Case_Table.png)

Finally, a table consisting of each of the individual state's case loads over time is displayed.  Further, they are color coded based on rate changes of the previous three days.  Ranging from deep red for three consecutive days of case increases to deep green for three consecutive days of case decreases.

![color](/images/colortable.png)

![state](/images/statecases.png)


Go check it out at [https://united-states-of-covid.herokuapp.com/](https://united-states-of-covid.herokuapp.com/)

Stay safe out in them streets. Keep your distance and most importantly:
### Wash 👏 Your 👏 Hands 👏
<br>
[www.THWDesigns.com](https://www.thwdesigns.com)
<br>

<br>

___
Shout out to the below GitHub repos for inspiration.

[Perishleaf Project](https://github.com/Perishleaf/data-visualisation-scripts/tree/master/dash-2019-coronavirus)

<br>

[New York Times Github](https://github.com/nytimes/covid-19-data)
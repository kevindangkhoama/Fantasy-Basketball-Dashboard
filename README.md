# Fantasy-Basketball-Dashboard
Kevin Ma DS4003 \
[Render Link](https://fantasy-basketball-dashboard.onrender.com)

## About Fantasy Basketball Dashboard:
The fantasy basketball dashboard offers a powerful tool for basketball enthusiasts to analyze their player performance in their specific league on a week-by-week basis through various barplots, polar charts, and tables. It caters to fantasy basketball managers seeking insights into player trends, specific player's fantasy point compositions (what stats contribute the most or least to their fantasy points), and strategic decision-making when setting lineups.

## Graphs
### Bar Chart Racer
This is the first of the two bar charts on the bar chart page. By default, you can press pause and play to run the animation to see the accumulation of fantasy points of the players you have had in your weekly lineups. Additionally, you can utilize the dropdown to see this animation work for other stats, such as points, rebounds, and assists.
### Grouped Bar Chart
This is the second of the two bar charts on the bar chart page. By default, the slider displays the 5 latest weeks, and fantasy points are displayed. All players are selected by default to ensure that you will be able to view them when viewing specific weeks, but players can be deselected.
### Polar Chart
The polar chart displays the fantasy point breakdown for each player. In fantasy basketball leagues, certain stats contribute differently to the calculations of the fantasy points. The stat percentages are relative to how much of the player's fantasy points come from said stat. The player chosen by default when the page is loaded is Kawhi Leonard, and the first five weeks are displayed. Selecting multiple weeks calculates the average % of each stat, and as you select more weeks, you get a more holistic visual of what stats are contributing the most to their fantasy points. There are also buttons to select and deselect all weeks.

## Dashboard Building Process:
1. **Data Collection**: Gathered player statistics from specific ESPN fantasy league from [ESPN-API](https://github.com/cwendt94/espn-api).
2. **Data Cleaning and Transformation**: Processed raw data to be in suitable format for various types of graphs and ensured data consistency.
3. **Data Visualization**: Leveraged Plotly and [raceplotly](https://github.com/lucharo/raceplotly) to create visualizations such as barcharts for player stats, race bar charts for seeing player stat accumulation over time, and polar charts for fantasy point breakdowns
4. **Dashboard Implementation**: Utilized Dash framework and hosted on Render to design an interactive dashboard interface, enabling users to explore data and insights seamlessly.

## Strengths and Learning Experiences:
1. **API Integration**: Demonstrated proficiency in collecting data from APIs, ensuring access to up-to-date player for specific fantasy leagues.
2. **Data Preprocessing**: Applied various techniques for data cleaning and transformation, ensuring data quality and integrity for accurate analysis.
3. **Data Visualization**: Developed skills in creating visually appealing and informative charts and graphs to convey insights effectively.
4. **Dashboard Development**: Acquired experience in designing and implementing interactive dashboards, enhancing user experience and engagement.
5. **Domain Knowledge**: Gained familiarity with basketball analytics and fantasy sports, applying statistical concepts to analyze player and team performance.
6. **Problem-Solving Skills**: Overcame challenges in data manipulation and visualization, showcasing adaptability and resilience in building the dashboard solution.

Future employers can benefit from my demonstrated ability to leverage data science techniques and tools to deliver practical solutions, as evidenced by the creation of the fantasy basketball dashboard.

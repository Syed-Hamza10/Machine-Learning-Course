import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

# Load data
def load_data():
    World_cup = pd.read_csv("World_cup_2023.csv")
    results = pd.read_csv("results.csv")
    return World_cup, results

World_cup, results = load_data()

# Title
st.title('World Cup 2023 Data Analysis')

# Display data
if st.checkbox('Show World Cup data'):
    st.subheader('World Cup 2023 Data')
    st.write(World_cup)

if st.checkbox('Show Results data'):
    st.subheader('Results Data')
    st.write(results)

# Plotting function
def plot_bar(data, x, y, title):
    sns.set(rc={'figure.figsize':(20, 5)})
    plt.figure(figsize=(20, 5))
    sns.barplot(x=x, y=y, data=data)
    plt.title(title)
    st.pyplot(plt)

# Visualize team titles
if st.checkbox('Show Team Titles'):
    plot_bar(World_cup, 'Team_name', 'Titles', 'Team Titles')

# Visualize Win Percentage
if st.checkbox('Show Win Percentage ODI'):
    plot_bar(World_cup, 'Team_name', 'Win_percentage_ODI', 'Win Percentage ODI')

# Visualize WC Match Won
if st.checkbox('Show WC Matches Won'):
    plot_bar(World_cup, 'Team_name', 'WC_match_won', 'World Cup Matches Won')

# Visualize Ratings
if st.checkbox('Show Ratings'):
    plot_bar(World_cup, 'Team_name', 'Rating', 'Team Ratings')

# Drop 'Match abandoned' and 'No result' from results
results.drop(results[(results['Winner'] == 'Match abandoned') | (results['Winner'] == 'No result')].index, inplace=True)

# Filtering functions
def filter_team(results, team_name):
    return results[(results['Team_1'] == team_name) | (results['Team_2'] == team_name)]

# Display team-specific analysis
team = st.selectbox('Select a team for analysis', ['India', 'Australia', 'Pakistan', 'New Zealand', 'England'])

if team:
    team_df = filter_team(results, team)
    st.subheader(f'{team} Match Results')
    st.write(team_df)
    
    # Filter wins
    team_wins = team_df[team_df['Winner'] == team]
    
    # Exclude the team name
    exclude = team
    
    # Opponents faced
    opponents_team1 = team_wins[team_wins['Team_2'] != exclude]['Team_2'].value_counts()
    opponents_team2 = team_wins[team_wins['Team_1'] != exclude]['Team_1'].value_counts()
    
    # Combine both
    opponents = opponents_team1.add(opponents_team2, fill_value=0).sort_values(ascending=False)
    
    st.subheader(f'Top 5 Opponents faced by {team}')
    st.bar_chart(opponents.head(5))
    
    # Win percentages against each team
    team_win_counts = {
        'India': 54, 'New Zealand': 58, 'South Africa': 37, 'Pakistan': 55, 'Sri Lanka': 93,
        'Bangladesh': 30, 'England': 57, 'Netherlands': 2, 'Afghanistan': 3
    }
    
    total_matches = sum(team_win_counts.values())
    win_percentages = {team: (wins / total_matches) * 100 for team, wins in team_win_counts.items()}
    
    st.subheader(f'Win Percentage of {team} Against Each Team')
    fig, ax = plt.subplots()
    ax.pie(win_percentages.values(), labels=win_percentages.keys(), autopct='%1.1f%%', startangle=140)
    ax.axis('equal')
    st.pyplot(fig)

# Run the Streamlit app
# if __name__ == '__main__':
#     st.run()

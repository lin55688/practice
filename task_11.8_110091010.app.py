from dash import Dash, html, dcc 
from dash.dependencies import Input, Output
import plotly.express as px
import pandas as pd


df = pd.read_csv('gym_members_exercise_tracking.csv')


colors = ['#7FFFD4', '#FFE5B4', '#708090', '#008080']

avg_calories_by_workout = df.groupby('Workout_Type')['Calories_Burned'].mean().reset_index()
avg_duration_by_workout_gender = df.groupby(['Workout_Type', 'Gender'])['Session_Duration (hours)'].mean().reset_index()

# Initialize the app
app = Dash(__name__)
server = app.server
# App layout
app.layout = html.Div([
    html.H1(children='Gym Members Exercise Analysis', style={'textAlign': 'center'}),
    html.Hr(),
    dcc.RadioItems(
        options=[
            {'label': 'Average calories by workout', 'value': 'calories'},
            {'label': 'Average Hours of Session by workout', 'value': 'hours'}
        ],
        value='calories',  # 設定預設值
        id='controls-and-radio-item'
    ),
    dcc.Graph(id='controls-and-graph')
])

# Callback to update graph
@app.callback(
    Output(component_id='controls-and-graph', component_property='figure'),
    Input(component_id='controls-and-radio-item', component_property='value')
)
def update_graph(selected_value):
    if selected_value == 'calories':
        fig = px.bar(avg_calories_by_workout, 
                    x='Workout_Type', 
                    y='Calories_Burned',
                    color='Workout_Type',
                    color_discrete_sequence=colors,
                    title='Average Calories Burned by Workout Type')

        fig.update_layout(
            xaxis_title='Workout Type',
            yaxis_title='Average Calories Burned',
            bargap=0.2
        )
    else:
        fig = px.bar(avg_duration_by_workout_gender, 
                    x='Workout_Type',
                    y='Session_Duration (hours)',
                    color='Gender',
                    color_discrete_sequence=['#FFB3E6','#2A52BE'],
                    barmode='group',
                    title='Average Session Duration by Workout Type and Gender')

        fig.update_layout(
            xaxis_title='Workout Type',
            yaxis_title='Average Session Duration (hours)',
            bargap=0.2,
            legend_title='Gender'
        )
    
    return fig

# Run the app
if __name__ == '__main__':
    app.run(debug=True)
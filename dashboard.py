import pandas as pd
import seaborn as sns
import dash
from dash import dcc, html, Input, Output, State
import plotly.graph_objs as go

# Load the tips dataset into a Pandas DataFrame
df = sns.load_dataset("tips")

# Cleaning the data
# Drop any rows with missing values
df.dropna(inplace=True)

# Convert the 'total_bill' column to numeric
df['total_bill'] = pd.to_numeric(df['total_bill'], errors='coerce')

# Convert the 'tip' column to numeric
df['tip'] = pd.to_numeric(df['tip'], errors='coerce')

# Convert the 'size' column to integer
df['size'] = df['size'].astype(int)

# Create the Dash app
app = dash.Dash(__name__)

# Define the layout of the dashboard
app.layout = html.Div(
    children=[
        html.H1("Tips Dataset Dashboard"),
        html.Div(
            children=[
                dcc.Markdown("#### Select Days:"),
                dcc.Checklist(
                    id="day-filter",
                    options=[
                        {'label': 'Thur', 'value': 'Thur'},
                        {'label': 'Fri', 'value': 'Fri'},
                        {'label': 'Sat', 'value': 'Sat'},
                        {'label': 'Sun', 'value': 'Sun'}
                    ],
                    value=['Thur', 'Fri', 'Sat', 'Sun']
                ),
                dcc.Graph(id="scatter-plot"),
            ],
            style={"width": "100%", "display": "inline-block", "margin-bottom": "20px"},
        ),
        html.Div(
            children=[
                dcc.Markdown("#### Select Time:"),
                dcc.Checklist(
                    id="time-filter",
                    options=[
                        {'label': 'Lunch', 'value': 'Lunch'},
                        {'label': 'Dinner', 'value': 'Dinner'}
                    ],
                    value=['Lunch', 'Dinner']
                ),
                dcc.Graph(id="pie-chart"),
            ],
            style={"width": "100%", "display": "inline-block", "margin-bottom": "20px"},
        ),
        html.Div(
            children=[
                dcc.RadioItems(
                    id="sex-filter",
                    options=[
                        {'label': 'Male', 'value': 'Male'},
                        {'label': 'Female', 'value': 'Female'}
                    ],
                    value='Female',
                    labelStyle={'display': 'inline-block'}
                ),
                dcc.Graph(id="size-tip-comparison"),
            ],
            style={"width": "100%", "display": "inline-block", "margin-bottom": "20px"},
        ),
        html.Div(
            children=[
                dcc.RangeSlider(
                    id="total-bill-filter",
                    min=df['total_bill'].min(),
                    max=df['total_bill'].max(),
                    step=1,
                    marks={i: str(i) for i in range(int(df['total_bill'].min()), int(df['total_bill'].max()) + 1)},
                    value=[df['total_bill'].min(), df['total_bill'].max()]
                ),
                dcc.Checklist(
                    id="time-filter-2",
                    options=[
                        {'label': 'Lunch', 'value': 'Lunch'},
                        {'label': 'Dinner', 'value': 'Dinner'}
                    ],
                    value=['Lunch', 'Dinner']
                ),
                dcc.Graph(id="filtered-scatter-plot"),
            ],
            style={"width": "100%", "display": "inline-block", "margin-bottom": "20px"},
        ),
    ]
)


@app.callback(
    Output("scatter-plot", "figure"),
    Input("day-filter", "value")
)
def update_scatter_plot(selected_days):
    filtered_df = df[df['day'].isin(selected_days)]
    scatter_plot_figure = go.Figure(
        data=[
            go.Scatter(
                x=filtered_df["total_bill"],
                y=filtered_df["tip"],
                mode="markers",
                marker=dict(size=8),
            )
        ],
        layout=go.Layout(
            title="Total Bill vs Tip Amount",
            xaxis=dict(title="Total Bill"),
            yaxis=dict(title="Tip Amount"),
            hovermode="closest",
        ),
    )
    return scatter_plot_figure


@app.callback(
    Output("pie-chart", "figure"),
    [Input("time-filter", "value")]
)
def update_pie_chart(selected_time):
    filtered_df = df[df['time'].isin(selected_time)]
    pie_chart_figure = go.Figure(
        data=[
            go.Pie(
                labels=["Smokers", "Non-smokers"],
                values=[filtered_df['smoker'].value_counts()[1], filtered_df['smoker'].value_counts()[0]],
                hole=0.5,
                marker=dict(colors=['#FFA07A', '#A0CED9']),
            )
        ],
        layout=go.Layout(
            title="Smokers vs Non-smokers",
        )
    )
    return pie_chart_figure


@app.callback(
    Output("size-tip-comparison", "figure"),
    [Input("sex-filter", "value")]
)
def update_size_tip_comparison(selected_sex):
    filtered_df = df[df['sex'] == selected_sex]
    size_tip_figure = go.Figure(
        data=[
            go.Bar(x=filtered_df['size'], y=filtered_df['tip'], name='Tip Amount'),
        ],
        layout=go.Layout(
            title="Size vs Tip Amount",
            xaxis=dict(title="Size"),
            yaxis=dict(title="Tip Amount"),
        )
    )
    return size_tip_figure


@app.callback(
    Output("filtered-scatter-plot", "figure"),
    [Input("total-bill-filter", "value"),
     Input("time-filter-2", "value")]
)
def update_filtered_scatter_plot(total_bill_range, selected_time):
    filtered_df = df[(df["total_bill"].between(total_bill_range[0], total_bill_range[1])) & (df["time"].isin(selected_time))]
    filtered_scatter_plot_figure = go.Figure(
        data=[
            go.Scatter(
                x=filtered_df["total_bill"],
                y=filtered_df["tip"],
                mode="markers",
                marker=dict(size=8),
            )
        ],
        layout=go.Layout(
            title="Filtered Scatter Plot",
            xaxis=dict(title="Total Bill"),
            yaxis=dict(title="Tip Amount"),
            hovermode="closest",
        ),
    )
    return filtered_scatter_plot_figure


# Run the app
if __name__ == "__main__":
    app.run_server(port=8051)


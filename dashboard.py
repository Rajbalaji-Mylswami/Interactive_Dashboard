import pandas as pd
import seaborn as sns
import streamlit as st
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

# Define a function for the scatter plot
def plot_scatter(selected_days):
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
    st.plotly_chart(scatter_plot_figure)

# Define a function for the pie chart
def plot_pie(selected_time):
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
    st.plotly_chart(pie_chart_figure)

# Define a function for the bar chart
def plot_bar(selected_sex):
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
    st.plotly_chart(size_tip_figure)

# Define a function for the filtered scatter plot
def plot_filtered_scatter(total_bill_range, selected_time):
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
    st.plotly_chart(filtered_scatter_plot_figure)

# Create the Streamlit app
def main():
    st.title("Tips Dataset Dashboard")
    
    selected_days = st.multiselect("Select Days:", df['day'].unique().tolist(), default=df['day'].unique().tolist(), key="days_multiselect")
    plot_scatter(selected_days)
    
    selected_time = st.multiselect("Select Time:", df['time'].unique().tolist(), default=df['time'].unique().tolist(), key="time_multiselect")
    plot_pie(selected_time)
    
    selected_sex = st.radio("Select Sex:", df['sex'].unique().tolist(), key="sex_radio")
    plot_bar(selected_sex)
    
    total_bill_range = st.slider("Select Total Bill Range:", float(df['total_bill'].min()), float(df['total_bill'].max()), 
                                 (float(df['total_bill'].min()), float(df['total_bill'].max())), key="total_bill_range_slider")
    selected_time_2 = st.multiselect("Select Time:", df['time'].unique().tolist(), default=df['time'].unique().tolist(), key="time_multiselect_2")
    plot_filtered_scatter(total_bill_range, selected_time_2)

if __name__ == "__main__":
    main()

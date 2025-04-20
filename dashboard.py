import streamlit as st
import pandas as pd
import plotly.express as px
import random
from datetime import datetime, timedelta

st.set_page_config(page_title="IT Ticket Dashboard", layout="wide")

# ------------------------ Dummy Data Generator ------------------------
def generate_dummy_data(num_records=100):
    issues = ['Blue Screen', 'Slow System', 'App Crash', 'Network Issue', 'Printer Problem']
    resolved_by = ['Bot', 'Engineer']
    teams = ['IT', 'Networking', 'Hardware']

    data = []
    for _ in range(num_records):
        issue = random.choice(issues)
        # Make bots solve fewer tickets than engineers (around 20% bots, 80% engineers)
        resolved = random.choices(resolved_by, weights=[1, 4], k=1)[0]
        assigned = random.choice(['Yes', 'No'])
        closed = random.choice(['Yes', 'No'])
        date = datetime.now() - timedelta(days=random.randint(0, 6))
        team = random.choice(teams)
        data.append([issue, resolved, assigned, closed, date.date(), team])

    return pd.DataFrame(data, columns=[
        'issue', 'resolved_by', 'assigned', 'closed', 'date', 'team'
    ])

df = generate_dummy_data()

# ------------------------ Title and Date Filter ------------------------
st.markdown("# 🎯 IT Weekly Ticket Analytics Dashboard")

min_date = df['date'].min()
max_date = df['date'].max()
selected_date = st.slider("Select Date", min_value=min_date, max_value=max_date, value=max_date)
df = df[df['date'] == selected_date]

# ------------------------ Chart 1: Tickets Resolved by Bot vs Engineer ------------------------
def chart_resolved_by(df):
    resolved_counts = df['resolved_by'].value_counts().reset_index()
    resolved_counts.columns = ['resolved_by', 'count']
    fig = px.bar(
        resolved_counts,
        x='resolved_by',
        y='count',
        text='count',
        title="Tickets Resolved by Bot vs Engineer",
        color='resolved_by',
        color_discrete_map={
            'Bot': '#9b59b6',         # Light Purple
            'Engineer': '#6c3483'     # Dark Purple
        }
    )
    fig.update_layout(transition_duration=500)
    return fig

# ------------------------ Chart 2: Most Common Issues ------------------------
def chart_common_issues(df):
    issue_counts = df['issue'].value_counts().head(5).reset_index()
    issue_counts.columns = ['issue', 'count']
    fig = px.bar(
        issue_counts,
        x='issue',
        y='count',
        text='count',
        title="Top 5 Common IT Issues",
        color='issue',
        color_discrete_sequence=px.colors.sequential.Purples[::-1]
    )
    fig.update_layout(transition_duration=500)
    return fig

# ------------------------ Chart 3: Assigned vs Unassigned Tickets ------------------------
def chart_assignment_status(df):
    assignment_counts = df['assigned'].value_counts().reset_index()
    assignment_counts.columns = ['assigned', 'count']
    fig = px.pie(
        assignment_counts,
        names='assigned',
        values='count',
        title="Assigned vs Unassigned Tickets",
        color='assigned',
        color_discrete_map={
            'Yes': '#7bc96f',  # Green for Assigned
            'No': '#c49dd9'    # Lavender for Unassigned
        },
        hole=0.4
    )
    fig.update_traces(textinfo='label+value')
    return fig

# ------------------------ Streamlit Dashboard Layout ------------------------
col1, col2 = st.columns(2)

with col1:
    st.plotly_chart(chart_resolved_by(df), use_container_width=True)

with col2:
    st.plotly_chart(chart_common_issues(df), use_container_width=True)

st.plotly_chart(chart_assignment_status(df), use_container_width=True)

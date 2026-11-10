
import streamlit as st
import pandas as pd
import plotly.express as px
from pathlib import Path

st.set_page_config(
    page_title="Employee Engagement Analytics",
    page_icon="📊",
    layout="wide"
)

st.title("📊 Employee Engagement Analytics Dashboard")
st.subheader("Impact of Hybrid and Remote Work on Organisational Structure and Employee Engagement")
st.write("**Researcher:** Kaviyasree K | **Sample size:** 140")

DATA_PATH = Path(__file__).parent / "data" / "response_counts.csv"

@st.cache_data
def load_data():
    return pd.read_csv(DATA_PATH)

df = load_data()

st.info(
    "This dashboard uses aggregate frequency counts from the original UG project. "
    "It does not contain individual respondent records. Percentages are calculated "
    "from the counts, while statistical test results are reproduced from the report."
)

LIKERT_ORDER = [
    "Strongly Disagree",
    "Disagree",
    "Neutral",
    "Agree",
    "Strongly Agree"
]

def get_question_data(question):
    data = df[df["question"] == question].copy()
    total = data["respondents"].sum()
    data["percentage"] = (data["respondents"] / total * 100).round(1)
    return data, total

def positive_percentage(data):
    positive = data[
        data["category"].isin(["Agree", "Strongly Agree"])
    ]["respondents"].sum()
    total = data["respondents"].sum()
    return positive / total * 100 if total else 0

# Key performance indicators
engagement, _ = get_question_data("I am actively engaged")
motivation, _ = get_question_data("I feel motivated to perform my job")
productivity, _ = get_question_data("My productivity has increased")

col1, col2, col3 = st.columns(3)
col1.metric("Total Respondents", "140")
col2.metric("Positive Engagement", f"{positive_percentage(engagement):.1f}%")
col3.metric("Positive Motivation", f"{positive_percentage(motivation):.1f}%")

tab1, tab2, tab3, tab4 = st.tabs([
    "Overview",
    "Demographics",
    "Survey Analysis",
    "Statistical Results"
])

with tab1:
    st.header("Project Overview")
    st.write(
        "This study analyses how hybrid and remote working arrangements "
        "relate to organisational structure, employee engagement, productivity, "
        "work-life balance and job satisfaction."
    )

    work_data, _ = get_question_data("Current work mode")

    fig = px.pie(
        work_data,
        names="category",
        values="respondents",
        title="Respondents by Work Mode",
        hole=0.4
    )
    st.plotly_chart(fig, use_container_width=True)

    st.subheader("Key Research Areas")
    st.write("""
    - Organisational structure and reporting relationships
    - Employee motivation and engagement
    - Communication and team coordination
    - Work-life balance and productivity
    - Technical and managerial support
    - Employee satisfaction with hybrid and remote work
    """)

with tab2:
    st.header("Demographic Analysis")

    demographic_questions = df[
        df["group"] == "Demographics"
    ]["question"].unique().tolist()

    selected_demo = st.selectbox(
        "Choose a demographic category",
        demographic_questions
    )

    data, total = get_question_data(selected_demo)

    fig = px.bar(
        data,
        x="category",
        y="respondents",
        text="respondents",
        title=selected_demo,
        labels={
            "category": "Category",
            "respondents": "Number of Respondents"
        }
    )
    st.plotly_chart(fig, use_container_width=True)

    st.dataframe(data, use_container_width=True)
    st.write("Total responses:", total)

with tab3:
    st.header("Questionnaire Analysis")

    questions = df[
        df["group"] == "Survey statements"
    ]["question"].unique().tolist()

    selected_question = st.selectbox(
        "Select a survey statement",
        questions
    )

    data, total = get_question_data(selected_question)

    fig = px.bar(
        data,
        x="category",
        y="respondents",
        text="respondents",
        category_orders={"category": LIKERT_ORDER},
        title=selected_question,
        labels={
            "category": "Response",
            "respondents": "Number of Respondents"
        }
    )
    st.plotly_chart(fig, use_container_width=True)

    st.dataframe(data, use_container_width=True)

    st.metric(
        "Positive Responses (Agree + Strongly Agree)",
        f"{positive_percentage(data):.1f}%"
    )

with tab4:
    st.header("Statistical Results from the UG Report")

    results = pd.DataFrame([
        ["Chi-square", "Work mode vs Employee engagement", "0.852", "Not significant"],
        ["Chi-square", "Work experience vs Productivity", "0.060", "Not significant"],
        ["Chi-square", "Gender vs Work-life balance", "0.095", "Not significant"],
        ["Pearson correlation", "Engagement vs Productivity", "r = 0.315; p < 0.001", "Positive; significant"],
        ["Pearson correlation", "Work-life balance vs Job satisfaction", "r = 0.222; p = 0.008", "Positive; significant"],
        ["Pearson correlation", "Technical support vs Motivation", "r = -0.036; p = 0.673", "Not significant"]
    ], columns=[
        "Test",
        "Variables",
        "Reported Result",
        "Interpretation"
    ])

    st.dataframe(results, use_container_width=True)

    st.caption(
        "These statistical results are transcribed from the original project report. "
        "They have not been recalculated from the aggregate frequency tables."
    )

    st.warning(
        "Some percentages in the original report do not match the reported counts. "
        "This dashboard calculates percentages from the counts in the CSV file. "
        "Individual respondent data would be needed to independently recalculate "
        "the statistical tests."
    )

st.divider()
st.caption("Developed using Python, Pandas, Plotly and Streamlit | Academic Portfolio Project")

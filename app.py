import numpy as np
import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt

st.set_page_config(page_title="Multi-Subject Student Analyzer", layout="centered")

st.title("🎓 Multi-Subject Student Analyzer")

# -------------------------------
# Generate Students
# -------------------------------
st.header("🎲 Generate Student Data")

n = st.number_input("Number of Students", min_value=1, value=10)

if st.button("Generate Students"):
    names = np.array([f"Student {i+1}" for i in range(int(n))])
    scores = np.random.randint(0, 101, size=(int(n), 3))

    df = pd.DataFrame(scores, columns=["Math", "Science", "English"])
    df.insert(0, "Student", names)

    st.session_state["data"] = df

# Display Data
if "data" in st.session_state:
    st.subheader("📋 Student Scores")
    st.dataframe(st.session_state["data"], use_container_width=True)


# -------------------------------
# Student Summary
# -------------------------------
st.header("📊 Student Totals & Averages")

if st.button("Compute Student Summary"):
    if "data" not in st.session_state:
        st.error("Generate data first!")
    else:
        df = st.session_state["data"]

        df["Total"] = df[["Math", "Science", "English"]].sum(axis=1)
        df["Average"] = df[["Math", "Science", "English"]].mean(axis=1)

        st.dataframe(df[["Student", "Total", "Average"]])

        # 📊 Bar Chart - Total Scores
        st.subheader("📊 Total Scores per Student")
        plt.figure()
        plt.bar(df["Student"], df["Total"])
        plt.xticks(rotation=45)
        st.pyplot(plt)


# -------------------------------
# Subject Averages
# -------------------------------
st.header("📈 Subject Averages")

if st.button("Compute Subject Averages"):
    if "data" not in st.session_state:
        st.error("Generate data first!")
    else:
        df = st.session_state["data"]

        averages = df[["Math", "Science", "English"]].mean()

        st.write(averages)

        # 📊 Bar Chart - Subject Averages
        st.subheader("📊 Average Score per Subject")
        plt.figure()
        plt.bar(averages.index, averages.values)
        st.pyplot(plt)


# -------------------------------
# Rankings
# -------------------------------
st.header("🏆 Rankings")

if st.button("Rank Students"):
    if "data" not in st.session_state:
        st.error("Generate data first!")
    else:
        df = st.session_state["data"].copy()

        df["Total"] = df[["Math", "Science", "English"]].sum(axis=1)
        df = df.sort_values(by="Total", ascending=False)
        df["Rank"] = np.arange(1, len(df) + 1)

        st.dataframe(df[["Rank", "Student", "Total"]])

        # 📊 Top Students Chart
        st.subheader("🏆 Top Performers")
        plt.figure()
        plt.bar(df["Student"], df["Total"])
        plt.xticks(rotation=45)
        st.pyplot(plt)


# -------------------------------
# Filter Above Average
# -------------------------------
st.header("🔍 Filter by Average")

threshold = st.number_input("Average Threshold", value=70)

if st.button("Filter Students"):
    if "data" not in st.session_state:
        st.error("Generate data first!")
    else:
        df = st.session_state["data"]

        df["Average"] = df[["Math", "Science", "English"]].mean(axis=1)
        filtered = df[df["Average"] > threshold]

        st.dataframe(filtered[["Student", "Average"]])

        if not filtered.empty:
            st.subheader("📊 Filtered Students Chart")
            plt.figure()
            plt.bar(filtered["Student"], filtered["Average"])
            plt.xticks(rotation=45)
            st.pyplot(plt)

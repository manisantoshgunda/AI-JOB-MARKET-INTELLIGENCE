import streamlit as st

from app.dashboard import Dashboard
from app.resume_analyzer import ResumeAnalyzer
from app.resume_ui import ResumeUI
from app.ui import DashboardUI
from app.career_advisor import CareerAdvisor

# ---------------------------------------------------
# PAGE CONFIG
# ---------------------------------------------------

st.set_page_config(
    page_title="AI Job Market Intelligence",
    page_icon="🤖",
    layout="wide",
)
st.markdown("""
<style>

.main > div {
    padding-top: 1rem;
}

.block-container {
    padding-top: 1rem;
    padding-bottom: 2rem;
}

hr {
    margin-top: 25px;
    margin-bottom: 25px;
}

</style>
""", unsafe_allow_html=True)

st.markdown("""
# 🤖 AI-Powered Job Market Intelligence Platform

### Discover Market Trends • Analyze Your Resume • Get AI-Powered Career Recommendations

---
""")

# ---------------------------------------------------
# LOAD DATA
# ---------------------------------------------------

try:

    dashboard = Dashboard("data/jobs.csv")
    dashboard.initialize()

    df = dashboard.df

except Exception as e:

    st.error(e)
    st.stop()

# ---------------------------------------------------
# SIDEBAR
# ---------------------------------------------------
st.sidebar.markdown("# 🤖 AI Career Hub")
st.sidebar.caption("Career Intelligence Platform")
st.sidebar.divider()

st.sidebar.header("🎯 Recommendation Filters")

skills_input = st.sidebar.text_input(
    "Skills",
    value="Python, SQL",
)

location = st.sidebar.selectbox(
    "Preferred Location",
    ["Any"] + sorted(df["location"].dropna().unique()),
)

experience = st.sidebar.selectbox(
    "Experience",
    ["Any"] + sorted(df["experience"].dropna().unique()),
)

minimum_salary = st.sidebar.number_input(
    "Minimum Salary",
    min_value=0,
    value=0,
    step=50000,
)

st.sidebar.divider()

st.sidebar.header("📄 Resume Analyzer")

resume_file = st.sidebar.file_uploader(
    "Upload Resume (PDF)",
    type=["pdf"],
)

resume_skills = sorted(
    {
        skill.strip()
        for skills in df["skills"].dropna()
        for skill in skills.split(",")
    }
)

if resume_file:

    analyzer = ResumeAnalyzer(resume_skills)

    resume_text = analyzer.extract_text_from_pdf(
        resume_file
    )

    result = analyzer.analyze(resume_text)

    ResumeUI.show_resume_analysis(result)

    advisor = CareerAdvisor.generate(result)

    st.sidebar.divider()

    st.sidebar.subheader("🤖 AI Career Advisor")

    st.sidebar.write(
        f"📈 Current ATS Score: {advisor['current_score']}%"
    )

    st.sidebar.write(
        f"🎯 Estimated ATS Score: {advisor['estimated_score']}%"
    )

    st.sidebar.markdown("### 🗺️ Personalized Roadmap")

    for item in advisor["roadmap"]:

        with st.sidebar.expander(
            f"Week {item['week']} - {item['skill']}"
        ):

            st.write(f"**Priority:** {item['priority']}")
            st.write(f"**Estimated Time:** {item['estimated_time']}")

    if not skills_input.strip():

        skills_input = ", ".join(
            result["matched_skills"]
        )
# ---------------------------------------------------
# DASHBOARD
# ---------------------------------------------------

tab1, tab2, tab3, tab4 = st.tabs([
    "📊 Dashboard",
    "📈 Market Analytics",
    "📋 Job Dataset",
    "ℹ️ About Project",
])

with tab1:

    DashboardUI.show_metrics(df)

with tab2:

    DashboardUI.show_charts(df)

with tab3:

    DashboardUI.show_dataset(df)
with tab4:

    st.subheader("🤖 AI-Powered Job Market Intelligence Platform")

    st.write("""
This platform helps users analyze current job market trends and receive
AI-powered recommendations based on their skills, experience, preferred
location, and uploaded resume.

### 🚀 Features

- 📊 Interactive Dashboard
- 📈 Market Analytics
- 🤖 AI Job Recommendation Engine
- 📄 Resume ATS Analyzer
- 🎯 Skill Gap Analysis
- 🤖 AI Career Advisor
- 📄 Resume Analysis PDF Report
- 📥 CSV Export

### 🛠️ Technology Stack

- Python
- Streamlit
- Pandas
- NumPy
- Plotly
- Scikit-learn
- Git & GitHub

### 🎯 Objective

To help students and job seekers understand market trends,
improve their resumes, identify missing skills, and discover
relevant career opportunities using AI.
""")
# ---------------------------------------------------
# AI JOB RECOMMENDATIONS
# ---------------------------------------------------


st.divider()
st.header("🤖 AI Job Recommendations")

if st.button("Generate Recommendations", use_container_width=True):

    if skills_input.strip():

        recommendations = dashboard.recommend_jobs(
            skills=skills_input,
            location=location if location != "Any" else None,
            experience=experience if experience != "Any" else None,
            min_salary=minimum_salary,
        )

        if recommendations.empty:

            st.warning("No matching jobs found.")

        else:

            st.success(
                f"Found {len(recommendations)} matching jobs."
            )

            st.dataframe(
                recommendations,
                use_container_width=True,
            )

            csv = recommendations.to_csv(index=False)

            st.download_button(
                "⬇ Download Recommendations",
                csv,
                file_name="recommended_jobs.csv",
                mime="text/csv",
                use_container_width=True,
            )

    else:

        st.warning(
            "Please enter at least one skill or upload a resume."
        )

st.divider()

st.markdown("""
<div style='text-align:center; color:gray; padding:20px;'>

### 🤖 AI-Powered Job Market Intelligence Platform

Developed using ❤️ with Python, Streamlit, Machine Learning and AI

© 2026 All Rights Reserved

</div>
""", unsafe_allow_html=True)
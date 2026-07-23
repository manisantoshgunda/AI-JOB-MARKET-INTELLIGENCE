import streamlit as st

from app.charts import DashboardCharts


class DashboardUI:

    @staticmethod
    def show_metrics(df):

        c1, c2, c3, c4 = st.columns(4)

        c1.metric("Jobs", len(df))
        c2.metric("Companies", df["company"].nunique())
        c3.metric("Locations", df["location"].nunique())
        c4.metric(
            "Average Salary",
            f"₹{int(df['salary'].mean()):,}"
        )

    @staticmethod
    def show_charts(df):

        left, right = st.columns(2)

        with left:
            st.plotly_chart(
                DashboardCharts.company_chart(df),
                use_container_width=True
            )

        with right:
            st.plotly_chart(
                DashboardCharts.location_chart(df),
                use_container_width=True
            )

        left, right = st.columns(2)

        with left:
            st.plotly_chart(
                DashboardCharts.salary_chart(df),
                use_container_width=True
            )

        with right:
            st.plotly_chart(
                DashboardCharts.skills_chart(df),
                use_container_width=True
            )

    @staticmethod
    def show_dataset(df):

        st.subheader("📋 Dataset Preview")

        st.dataframe(
            df,
            use_container_width=True,
            height=300,
        )
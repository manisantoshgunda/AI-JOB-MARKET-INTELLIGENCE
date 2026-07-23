import plotly.express as px


class DashboardCharts:

    @staticmethod
    def company_chart(df):

        company_df = (
            df["company"]
            .value_counts()
            .head(10)
            .reset_index()
        )

        company_df.columns = ["Company", "Jobs"]

        return px.bar(
            company_df,
            x="Company",
            y="Jobs",
            title="🏢 Top Hiring Companies"
        )

    @staticmethod
    def location_chart(df):

        location_df = (
            df["location"]
            .value_counts()
            .reset_index()
        )

        location_df.columns = ["Location", "Jobs"]

        return px.pie(
            location_df,
            names="Location",
            values="Jobs",
            title="📍 Jobs by Location"
        )

    @staticmethod
    def salary_chart(df):

        return px.histogram(
            df,
            x="salary",
            nbins=20,
            title="💰 Salary Distribution"
        )

    @staticmethod
    def skills_chart(df):

        skills = (
            df["skills"]
            .str.split(",")
            .explode()
            .str.strip()
        )

        skill_df = (
            skills.value_counts()
            .head(15)
            .reset_index()
        )

        skill_df.columns = ["Skill", "Count"]

        return px.bar(
            skill_df,
            x="Skill",
            y="Count",
            color="Count",
            title="🔥 Top Skills in Market"
        )
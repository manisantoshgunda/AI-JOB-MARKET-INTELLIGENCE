from app.pdf_report import PDFReport
import streamlit as st
import plotly.graph_objects as go


class ResumeUI:

    @staticmethod
    def show_resume_analysis(result):

        st.sidebar.subheader("📊 ATS Resume Score")

        fig = go.Figure(
            go.Indicator(
                mode="gauge+number",
                value=result["resume_score"],
                title={"text": "ATS Score"},
                gauge={
                    "axis": {"range": [0, 100]},
                    "bar": {"thickness": 0.3},
                    "steps": [
                        {"range": [0, 50], "color": "#ff4d4d"},
                        {"range": [50, 75], "color": "#ffd24d"},
                        {"range": [75, 100], "color": "#4CAF50"},
                    ],
                },
            )
        )

        fig.update_layout(
            height=250,
            margin=dict(l=20, r=20, t=40, b=20),
        )

        st.sidebar.plotly_chart(
            fig,
            use_container_width=True,
        )

        st.sidebar.success(
            f"⭐ Rating: {result['rating']}"
        )

        with st.sidebar.expander("✅ Matched Skills"):

            if result["matched_skills"]:
                st.write(", ".join(result["matched_skills"]))
            else:
                st.write("No matched skills found.")

        with st.sidebar.expander("❌ Missing Skills"):

            if result["missing_skills"]:
                st.write(", ".join(result["missing_skills"]))
            else:
                st.write("No missing skills.")

        with st.sidebar.expander("💡 Suggestions"):

            if result["suggestions"]:

                for suggestion in result["suggestions"]:
                    st.write("•", suggestion)

            else:

                st.success("Excellent resume!")

        st.sidebar.subheader("📈 Skill Gap Analysis")

        total = (
            len(result["matched_skills"])
            + len(result["missing_skills"])
        )

        if total > 0:

            progress = len(result["matched_skills"]) / total

            st.sidebar.progress(progress)

            st.sidebar.write(
                f"Current Skills: {len(result['matched_skills'])}/{total}"
            )

        if result["missing_skills"]:

            st.sidebar.markdown(
                "### 🎯 Learning Priority"
            )

            for skill in result["missing_skills"][:5]:
                st.sidebar.write(f"🔹 {skill}")

        st.sidebar.divider()

        st.sidebar.subheader("📄 Resume Report")

        pdf_file = PDFReport.generate(result)

        with open(pdf_file, "rb") as file:

            st.sidebar.download_button(
                label="⬇ Download Resume Analysis",
                data=file,
                file_name="resume_analysis.pdf",
                mime="application/pdf",
                use_container_width=True,
            )
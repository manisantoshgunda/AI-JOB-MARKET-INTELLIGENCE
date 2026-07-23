class CareerAdvisor:

    @staticmethod
    def generate(result):

        roadmap = []

        missing = result.get("missing_skills", [])

        priority_skills = missing[:5]

        week = 1

        for skill in priority_skills:

            roadmap.append({
                "week": week,
                "skill": skill,
                "priority": "High",
                "estimated_time": "5-7 days"
            })

            week += 1

        current_score = result["resume_score"]

        estimated_score = min(
            current_score + len(priority_skills) * 4,
            100
        )

        return {
            "current_score": current_score,
            "estimated_score": estimated_score,
            "roadmap": roadmap
        }
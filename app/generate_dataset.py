import random
from pathlib import Path

import pandas as pd

random.seed(42)

companies = [
    "Google", "Microsoft", "Amazon", "Apple", "Meta",
    "Netflix", "Adobe", "Oracle", "IBM", "Intel",
    "TCS", "Infosys", "Wipro", "Accenture", "Capgemini",
    "Cognizant", "HCLTech", "Tech Mahindra", "Deloitte", "EY"
]

job_titles = [
    "Software Engineer",
    "Python Developer",
    "Java Developer",
    "Full Stack Developer",
    "Frontend Developer",
    "Backend Developer",
    "Data Analyst",
    "Data Scientist",
    "Machine Learning Engineer",
    "AI Engineer",
    "Cloud Engineer",
    "DevOps Engineer",
    "Cyber Security Analyst",
    "Business Analyst",
    "QA Engineer"
]

locations = [
    "Bengaluru",
    "Hyderabad",
    "Chennai",
    "Pune",
    "Mumbai",
    "Delhi",
    "Noida",
    "Gurugram",
    "Kolkata",
    "Ahmedabad"
]

experience_levels = [
    "Fresher",
    "0-2 Years",
    "2-4 Years",
    "4-6 Years",
    "6+ Years"
]

skills_pool = [
    "Python",
    "Java",
    "C++",
    "SQL",
    "JavaScript",
    "React",
    "Node.js",
    "HTML",
    "CSS",
    "Git",
    "Docker",
    "Kubernetes",
    "AWS",
    "Azure",
    "GCP",
    "TensorFlow",
    "PyTorch",
    "Machine Learning",
    "Deep Learning",
    "Pandas",
    "NumPy",
    "Scikit-learn",
    "Power BI",
    "Tableau",
    "Excel",
    "Linux",
    "MongoDB",
    "PostgreSQL",
    "REST API",
    "FastAPI"
]

records = []

for _ in range(500):
    salary = random.randint(300000, 3500000)

    record = {
        "job_title": random.choice(job_titles),
        "company": random.choice(companies),
        "location": random.choice(locations),
        "salary": salary,
        "experience": random.choice(experience_levels),
        "skills": ", ".join(random.sample(skills_pool, random.randint(4, 8)))
    }

    records.append(record)

df = pd.DataFrame(records)

output_dir = Path("data")
output_dir.mkdir(exist_ok=True)

output_file = output_dir / "jobs.csv"

df.to_csv(output_file, index=False)

print("=" * 50)
print("Dataset Generated Successfully!")
print(f"Rows    : {len(df)}")
print(f"Columns : {len(df.columns)}")
print(f"Saved to: {output_file}")
print("=" * 50)
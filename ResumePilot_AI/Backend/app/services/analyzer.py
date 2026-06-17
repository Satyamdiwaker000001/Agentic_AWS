import random

def analyze_resume(file_path: str, job_title: str, job_description: str):
    """
    Mock AI analysis service.
    In a real scenario, this would extract text from the PDF using PyPDF2 or pdfplumber,
    and send it to an LLM (OpenAI, Claude, AWS Bedrock) along with the JD to get a structured response.
    """
    
    # Generate mock scores based on simple length checks or random for demo purposes
    base_score = random.randint(75, 95)
    
    return {
        "score": base_score,
        "findings": {
            "aligned": "React, JavaScript, Component Architecture",
            "missing": "GraphQL, AWS Deployment, CI/CD"
        },
        "suggestions": [
            "Add quantifiable metrics to your recent 'Frontend Engineer' role (e.g., 'Improved load time by X%').",
            "Include keywords like 'GraphQL' and 'AWS' in a dedicated Skills section to pass ATS.",
            "Condense older non-technical experience to make room for an impactful Projects section.",
            "Use strong action verbs like 'Architected' and 'Spearheaded' instead of 'Worked on'."
        ],
        "radarData": [
            { "subject": 'Skills Match', "A": random.randint(70, 100), "fullMark": 100 },
            { "subject": 'Experience', "A": random.randint(70, 100), "fullMark": 100 },
            { "subject": 'Keywords', "A": random.randint(60, 95), "fullMark": 100 },
            { "subject": 'Formatting', "A": random.randint(80, 100), "fullMark": 100 },
            { "subject": 'Impact', "A": random.randint(65, 95), "fullMark": 100 },
        ],
        "scoreBreakdown": [
            { "name": 'Technical Skills', "value": random.randint(70, 95) },
            { "name": 'Soft Skills', "value": random.randint(70, 95) },
            { "name": 'Experience', "value": random.randint(70, 95) },
            { "name": 'Education', "value": random.randint(80, 100) },
        ],
        "roleMatch": {
            "title": job_title,
            "matchPercentage": base_score,
            "level": "Senior" if "Senior" in job_title else "Mid-Level"
        }
    }

from flask import Flask, render_template, request, make_response, session
from reportlab.lib.styles import getSampleStyleSheet
from reportlab.platypus import SimpleDocTemplate, Paragraph
from io import BytesIO

app = Flask(__name__)
app.secret_key = "skillbridge-secret-key"

@app.route('/')
def home():
    return render_template('index.html')

@app.route('/analyze', methods=['POST'])
def analyze():
    name = request.form['name']
    degree = request.form['degree']
    semester = request.form['semester']
    skills = request.form['skills'].lower()
    goal = request.form['goal'].lower()

    # Internship Readiness Score
    score = 40

    if 'python' in skills:
        score += 15
    if 'html' in skills:
        score += 10
    if 'css' in skills:
        score += 5
    if 'javascript' in skills:
        score += 10
    if 'react' in skills:
        score += 10
    if 'flask' in skills:
        score += 10
    if 'github' in skills:
        score += 10
    if 'sql' in skills:
        score += 10
    if 'excel' in skills:
        score += 5

    score = min(score, 95)

    # Strengths
    strengths = []

    if 'python' in skills:
        strengths.append('Python Programming')
    if 'html' in skills or 'css' in skills:
        strengths.append('Web Development Fundamentals')
    if 'javascript' in skills:
        strengths.append('Frontend Development')
    if 'react' in skills:
        strengths.append('Modern Web Frameworks')
    if 'flask' in skills:
        strengths.append('Backend Development with Flask')
    if 'github' in skills:
        strengths.append('Version Control & Collaboration')
    if 'sql' in skills:
        strengths.append('Database Fundamentals')
    if 'excel' in skills:
        strengths.append('Data Organization & Analysis')

    if not strengths:
        strengths.append('Strong learning potential and beginner-friendly growth path')

    degree_lower = degree.lower()

    if 'bca' in degree_lower:

        next_skills = [
            'Python',
            'Flask',
            'REST APIs',
            'Git & GitHub',
            'Database Management'
        ]

        projects = [
            'AI Resume Analyzer',
            'Student Career Dashboard',
            'Internship Tracker'
        ]

        internships = [
            'Python Developer Intern',
            'Web Developer Intern',
            'Software Development Intern'
        ]

    elif 'btech' in degree_lower or 'engineering' in degree_lower:

        next_skills = [
            'Data Structures & Algorithms',
            'System Design',
            'React.js',
            'Node.js',
            'Cloud Basics'
        ]

        projects = [
            'Smart Campus System',
            'IoT Monitoring Dashboard',
            'Full Stack Web Application'
        ]

        internships = [
            'Software Engineer Intern',
            'Full Stack Intern',
            'Cloud Intern'
        ]

    elif 'bcom' in degree_lower:

        next_skills = [
            'Excel',
            'Power BI',
            'SQL',
            'Financial Analysis',
            'Business Communication'
        ]

        projects = [
            'Expense Tracker',
            'Sales Dashboard',
            'Financial Report Generator'
        ]

        internships = [
            'Data Analyst Intern',
            'Finance Intern',
            'Business Operations Intern'
        ]

    elif 'mba' in degree_lower:

        next_skills = [
            'Market Research',
            'Power BI',
            'Product Management',
            'Leadership',
            'Digital Marketing'
        ]

        projects = [
            'Market Analysis Dashboard',
            'Startup Evaluation Tool',
            'Business KPI Tracker'
        ]

        internships = [
            'Product Intern',
            'Business Analyst Intern',
            'Marketing Intern'
        ]

    elif 'nursing' in degree_lower or 'bsc nursing' in degree_lower:

        next_skills = [
            'Patient Care Documentation',
            'Healthcare Software',
            'Medical Communication',
            'Healthcare Analytics',
            'Emergency Response'
        ]

        projects = [
            'Patient Record Manager',
            'Hospital Appointment System',
            'Medicine Reminder App'
        ]

        internships = [
            'Clinical Intern',
            'Hospital Management Intern',
            'Healthcare Assistant Intern'
        ]

    else:

        next_skills = [
            'Communication Skills',
            'Digital Literacy',
            'Basic Programming',
            'Excel',
            'Career Planning'
        ]

        projects = [
            'Portfolio Website',
            'Task Manager',
            'Career Planner'
        ]

        internships = [
            'Administrative Intern',
            'Operations Intern',
            'Support Executive Intern'
        ]

    goal_display = goal.title()

    if 'genai' in goal or 'ai' in goal:

        next_skills.extend([
            'Prompt Engineering',
            'Machine Learning Basics',
            'LLM Applications'
        ])

        projects.append('AI Chatbot for Students')

        internships.append('AI/ML Intern')

    elif 'full stack' in goal or 'web' in goal:

        next_skills.extend([
            'Authentication',
            'Deployment',
            'MongoDB'
        ])

        projects.append('E-commerce Website')

        internships.append('Full Stack Developer Intern')

    next_skills = list(dict.fromkeys(next_skills))
    projects = list(dict.fromkeys(projects))
    internships = list(dict.fromkeys(internships))

    learning_plan = [
        'Week 1: Strengthen your core programming and Git skills',
        'Week 2: Build a web application using Flask',
        'Week 3: Create one portfolio project related to your career goal',
        'Week 4: Improve your resume and apply to at least 20 internships'
    ]

    summary = f'''
    Based on your {degree} profile and current skills ({skills}),
    SkillBridge AI believes that you have strong potential to become a {goal_display}.
    Your internship readiness score is {score}%, which means you are on the right
    track but should focus on strengthening practical projects, APIs, and portfolio
    development. Completing the recommended projects and following the 30-day
    learning plan can significantly improve your chances of securing internships
    and entry-level opportunities.
    '''
    session['report'] = {
        'name': name,
        'degree': degree,
        'semester': semester,
        'goal': goal_display,
        'score': score,
        'strengths': strengths,
        'next_skills': next_skills,
        'projects': projects,
        'internships': internships,
        'learning_plan': learning_plan,
        'summary': summary
    }
    return render_template(
        'result.html',
        name=name,
        degree=degree,
        semester=semester,
        goal=goal_display,
        score=score,
        strengths=strengths,
        next_skills=next_skills,
        projects=projects,
        internships=internships,
        learning_plan=learning_plan,
        summary=summary
    )

@app.route('/download-report')
def download_report():
    data = session.get('report')

    if not data:
        return "No report available. Please analyze your career profile first."

    buffer = BytesIO()
    doc = SimpleDocTemplate(buffer)
    styles = getSampleStyleSheet()
    story = []

    story.append(Paragraph("SkillBridge AI - Personalized Career Roadmap Report", styles['Title']))
    story.append(Paragraph("A personalized employability and career guidance report generated by SkillBridge AI.", styles['Normal']))
    story.append(Paragraph("<br/>", styles['Normal']))

    # Student Profile
    story.append(Paragraph("<b>Student Profile</b>", styles['Heading2']))
    story.append(Paragraph(f"Name: {data['name']}", styles['Normal']))
    story.append(Paragraph(f"Degree: {data['degree']}", styles['Normal']))
    story.append(Paragraph(f"Semester: {data['semester']}", styles['Normal']))
    story.append(Paragraph(f"Career Goal: {data['goal']}", styles['Normal']))
    story.append(Paragraph("<br/>", styles['Normal']))

    # AI Insight
    story.append(Paragraph("<b>AI Career Insight</b>", styles['Heading2']))
    story.append(Paragraph(data['summary'], styles['Normal']))
    story.append(Paragraph("<br/>", styles['Normal']))

    # Score
    story.append(Paragraph("<b>Internship Readiness Score</b>", styles['Heading2']))
    story.append(Paragraph(f"Current Score: {data['score']}%", styles['Normal']))
    story.append(Paragraph("A higher score indicates stronger internship readiness based on current skills and career alignment.", styles['Normal']))
    story.append(Paragraph("<br/>", styles['Normal']))

    # Strengths
    story.append(Paragraph("<b>Current Strengths</b>", styles['Heading2']))
    for item in data['strengths']:
        story.append(Paragraph(f"- {item}", styles['Normal']))
    story.append(Paragraph("<br/>", styles['Normal']))

    # Skills
    story.append(Paragraph("<b>Recommended Skills to Learn Next</b>", styles['Heading2']))
    for item in data['next_skills']:
        story.append(Paragraph(f"- {item}", styles['Normal']))
    story.append(Paragraph("<br/>", styles['Normal']))

    # Projects
    story.append(Paragraph("<b>Suggested Portfolio Projects</b>", styles['Heading2']))
    for item in data['projects']:
        story.append(Paragraph(f"- {item}", styles['Normal']))
    story.append(Paragraph("<br/>", styles['Normal']))

    # Internships
    story.append(Paragraph("<b>Recommended Internship Roles</b>", styles['Heading2']))
    for item in data['internships']:
        story.append(Paragraph(f"- {item}", styles['Normal']))
    story.append(Paragraph("<br/>", styles['Normal']))

    # Learning Plan
    story.append(Paragraph("<b>30-Day Career Action Plan</b>", styles['Heading2']))
    for item in data['learning_plan']:
        story.append(Paragraph(f"- {item}", styles['Normal']))
    story.append(Paragraph("<br/>", styles['Normal']))

    # Resume Tips
    story.append(Paragraph("<b>Resume Improvement Tips</b>", styles['Heading2']))
    story.append(Paragraph("- Add measurable achievements.", styles['Normal']))
    story.append(Paragraph("- Include GitHub repository links.", styles['Normal']))
    story.append(Paragraph("- Mention technologies used in each project.", styles['Normal']))
    story.append(Paragraph("- Add project screenshots and deployment links where possible.", styles['Normal']))
    story.append(Paragraph("<br/>", styles['Normal']))

    # Future Enhancements
    story.append(Paragraph("<b>Future Enhancements</b>", styles['Heading2']))
    story.append(Paragraph("- Real AI integration using Gemini/OpenAI APIs", styles['Normal']))
    story.append(Paragraph("- Resume upload and AI-based scoring", styles['Normal']))
    story.append(Paragraph("- Live internship listings from companies", styles['Normal']))
    story.append(Paragraph("- Progress tracking dashboard", styles['Normal']))
    story.append(Paragraph("- Support for all academic courses and career paths", styles['Normal']))
    story.append(Paragraph("<br/>", styles['Normal']))

    story.append(Paragraph("This report was generated by SkillBridge AI for educational and career planning purposes.", styles['Italic']))

    doc.build(story)
    pdf = buffer.getvalue()
    buffer.close()

    response = make_response(pdf)
    response.headers['Content-Type'] = 'application/pdf'
    response.headers['Content-Disposition'] = 'attachment; filename=SkillBridge_Career_Report.pdf'

    return response
if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
# JD-Buster
Transform lengthy job descriptions into actionable skill checklists using AI &amp; NLP
JD Buster: The Job Description Skill Buster
Live Demo: Check out the https://jd-buster-mhbou2ggsptav6nd4aivex.streamlit.app/ here!

🚀 Why I Built This
Job seekers often spend hours manually scanning long, jargon-heavy job descriptions to find the actual requirements. I built this tool to provide "X-Ray Vision" into job ads, using Natural Language Processing (NLP) to strip away the "fluff" and highlight what actually matters.

✨ Key Features
Must-Have Extraction: Automatically identifies non-negotiable requirements like degrees and years of experience.

Nice-to-Have Identification: Finds "bonus" skills and exposure-based requirements.

Automated Tech-Stack Mapping: Uses Named Entity Recognition (NER) to identify tools, platforms, and programming languages.

Jargon Buster Sidebar: Provides plain-English explanations for common corporate buzzwords.

Clean UI: A responsive dashboard built for a seamless user experience.

🛠️ Technical Stack
Language: Python

NLP Engine: SpaCy (en_core_web_sm model)

Web Framework: Streamlit

Data Handling: Pandas

Deployment: Streamlit Community Cloud

🧠 How it Works
The application follows a four-step pipeline:

Text Input: User pastes a raw job description into the web interface.

Processing: SpaCy's NLP model tokenizes the text and analyzes sentence structure.

Classification: A custom logic engine scans for "trigger keywords" (e.g., proficiency, must, plus, exposure) to categorize sentences.

Entity Extraction: The model identifies Proper Nouns (PROPN) and Organizations (ORG) to list the technical stack.

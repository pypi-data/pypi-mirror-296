
class Resume:
    def __init__(self):
        self.name = "Akanksha Raj"
        self.email = "akanksha1601raj@gmail.com"
        self.github = "https://github.com/its-akanksha"
        self.linkedin = "https://linkedin.com/in/akanksha-raj-202404209/"
        self.technical_skills = [
            "Python - Machine Learning, Data Science",
            "C++", "SQL", "Tableau", "R Programming", "Angular", "HTML", "CSS", "Javascript"
        ]
        self.education = {
            "M.Tech (CSE - AI and ML)": "VIT Bhopal University, 8.5/10 (Sep 2020 - Ongoing)",
            "Class XII": "DAV Public School, 87% (May 2019)",
            "Class X": "Krishna Sudarshan Central School, 10/10 (May 2017)"
        }
        self.projects = [
            {
                "title": "HandSyncTube (Feb 2024 – April 2024)",
                "description": "Developed and trained a machine learning model utilizing hand gestures to enhance user interaction with YouTube videos.",
                "technologies": ["MediaPipe", "Python", "Pyautogui"],
                "role": "Led ML model training and seamless integration with YouTube"
            },
            {
                "title": "Amazon Reviews Sentiment Analysis (Jan 2023-Feb 2023)",
                "description": "Engineered an NLP model for sentiment analysis of Amazon Reviews using XGB classifier.",
                "technologies": ["Scikit-learn", "Pandas", "Matplotlib", "BeautifulSoup"],
                "role": "Achieved 93% accuracy and 89% precision"
            },
            {
                "title": "Movie Recommender (May 2023)",
                "description": "Created a content-based recommender system for movie suggestions.",
                "technologies": ["Natural Language Processing", "NLTK", "Scikit-learn"],
                "role": "Efficiently trained and implemented a recommendation system"
            }
        ]

    def display(self):
        print(f"Name: {self.name}")
        print(f"Email: {self.email}")
        print(f"GitHub: {self.github}")
        print(f"LinkedIn: {self.linkedin}\n")
        
        print("Technical Skills:")
        for skill in self.technical_skills:
            print(f" - {skill}")
        
        print("\nEducation:")
        for degree, details in self.education.items():
            print(f" - {degree}: {details}")
        
        print("\nProjects:")
        for project in self.projects:
            print(f" - {project['title']}: {project['description']}")
            print(f"   Technologies: {', '.join(project['technologies'])}")
            print(f"   Role: {project['role']}")
            print()

def show_resume():
    resume = Resume()
    resume.display()

if __name__ == "__main__":
    show_resume()

from setuptools import setup, find_packages

setup(
    name="akanksha",
    version="0.0.2",
    description="A deep dive into Resume of Akanksha Raj",
    author="Akanksha Raj",
    author_email="akanksha1601raj@gmail.com",
    packages=find_packages(),
    entry_points={
        'console_scripts': [
            'akanksha=resume.display_resume:show_resume', 
        ],
    },
    classifiers=[
        'Programming Language :: Python :: 3',
        'License :: OSI Approved :: MIT License',
        'Operating System :: OS Independent',
    ],
    python_requires='>=3.6',
)

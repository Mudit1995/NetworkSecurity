

from setuptools import find_packages, setup
from typing import List

def get_requirements() -> List[str]:
    """
    This function reads the requirements.txt file and returns a list of dependencies.
    """
    requirements = []
    try:
        with open("requirments.txt", "r") as f:
            for line in f:
                # Strip newline and skip '-e .' 
                line = line.strip()
                if line and line != "-e .":
                    requirements.append(line)
    except FileNotFoundError:
        print("requirements.txt not found")
    return requirements

setup(
    name="NetworkSecurity",  # Fixed case
    version="0.0.1",  # Fixed typo
    author="Mudit Mohan Aggarwal",
    author_email="mudit.m.aggarwal@gmail.com",
    packages=find_packages(),  # Fixed key
    install_requires=get_requirements(),  # Reads from requirements.txt
)


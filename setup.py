

from setuptools import find_packages,setup
from typing import List


def get_requirements()->List[str]:
    """
     this function will return the list of requirment s
    """


    requirement_list:list[str]=[]
    try :
        with open("requirments.txt",'r') as f:
            # read line bu libne 
            lines = f.readlines()

            # Process in each line 
            for line in lines :
                # requirement = [req.replace("\n","") for req in line]
                # or we can strip it 
                # we are stripingh it because we will for sure get the libe ahead so to go the next libne we need to remove it 
                requirement = line.strip()
                if requirement and requirement != '-e .':
                    requirement_list.append(requirement)

    except FileNotFoundError:
        print("File not foiund")

    return requirement_list

setup(

    Name = "Network Security",
    versin ="0.0.1",
    author="Mudit",
    author_email="mudit.m.aggarwal@gnail.com",
    package=find_packages(),
    install_requires=get_requirements()

)

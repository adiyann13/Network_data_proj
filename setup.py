from setuptools import find_packages,setup
from typing import List

def get_requirements()->List[str]:
    requirement_lst: List[str]=[]
    try:
        with open('requirements.txt','r') as f:
            lines = f.readlines()
            for l in lines:
                requirement = l.strip()
                if requirement and requirement!='-e .':
                    requirement_lst.append(requirement)
    except FileNotFoundError:
        print("file not found !!")
    
    return requirement_lst

print(get_requirements())

setup(
    name = 'network_security',
    version= '0.0.1',
    author='adiyan',
    author_email='adiyannmd@gmail.com',
    packages=find_packages(),
    install_requires= get_requirements()
    
)
            

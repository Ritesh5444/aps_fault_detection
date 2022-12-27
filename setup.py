from setuptools import find_packages, setup

from typing import List

REQUIREMENT_FILE_NAME = "requirements.txt"
HYPHEN_E_DOT = "-e ."

def get_requirements() ->List[str]:
    with open(REQUIREMENT_FILE_NAME) as requirement_file:
        #This will read the text file line by line and return list 
        requirement_list = requirement_file.readlines() 
        #In the returned list we will  have \n values which have been used in text file to display
        #packages in different lines, we will replace them
        requirement_list = [requirement_name.replace("\n","") for requirement_name in requirement_list]

    if HYPHEN_E_DOT in requirement_list:
        requirement_list.remove(HYPHEN_E_DOT)
    return requirement_list

    if HYPHEN_E_DOT in requirement_list:
        requirement_list.remove(HYPHEN_E_DOT)
    return requirement_list


setup(
    name = "sensor",
    version = "0.0.1",
    author = "ineueon",
    author_email = "avnish@ineuron.ai",
    packages = find_packages(),
    install_requires = get_requirements(),
)
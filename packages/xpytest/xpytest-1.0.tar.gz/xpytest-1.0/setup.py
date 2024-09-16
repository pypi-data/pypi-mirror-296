# Auteur : Esteban COLLARD, Nordine EL AMMARI
# Modifications : Reda ID TALEB & Manal LAGHMICH

from setuptools import find_packages, setup
import os.path

# Le chemin vers le programme qui lance le l1test en mode CLI
L1TEST_CLI_MAIN = "thonnycontrib.frontend.cli.l1test_cli:main"
# Le nom de la commande à exécuter dans le terminal
L1TEST_CLI_COMMAND = "xpytest"

def recursive_files(directory):
    paths = []
    for (path, _, filenames) in os.walk(directory):
        for filename in filenames:
            if not filename.endswith(".pyc"):
                paths.append(os.path.join('..', path, filename))
    return paths

packages = find_packages()

def get_packages_data(packages: list[str]=packages) -> dict[str, list[str]]:
    """
    Récupère les fichiers de chaque package python et les autres dossiers.
    Inclut les fichiers qui ne sont pas des .py comme les images, les traductions etc.
    
    Note: Les fichiers .pyc sont exclus.
    """
    py_packs = {p: ["*.py"] for p in packages}
    
    # Les autres dossiers qui ne sont pas des packages python
    list_of_dirs = ["thonnycontrib/i18n/locale", 
                    "thonnycontrib/img", 
                    "thonnycontrib/l1test_config"] 
    explored_dirs = []
    for p in list_of_dirs:
        explored_dirs += recursive_files(p)
    return {**py_packs, **{"": explored_dirs}} 

setupdir = os.path.dirname(__file__)


requirements = []
for line in open(os.path.join(setupdir, "requirements.txt"), encoding="ASCII"):
    if line.strip() and not line.startswith("#"):
        requirements.append(line)
        
setup(
    name=L1TEST_CLI_COMMAND,
    version="1.0",
    author="Reda ID-TALEB",
    description="Xpytest is a tool to test your python code",
    long_description="Xpytest is a tool to test your python code",
    classifiers=[
        "Topic :: Education :: Testing",
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
        "Development Status :: 3 - Alpha",
        "Intended Audience :: Education"
        ],
    platforms=["Windows", "macOS", "Linux"],
    python_requires=">=3.9",
    package_data=get_packages_data(),
    install_requires=requirements,
    packages=packages,
    entry_points={
        'console_scripts': [
            '%s=%s' % (L1TEST_CLI_COMMAND,L1TEST_CLI_MAIN),
        ],
    }
)

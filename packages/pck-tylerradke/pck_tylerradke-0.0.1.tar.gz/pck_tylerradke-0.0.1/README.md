# Overview

The goal of this activity is to introduce you to python's packaging system called **PyPi** (Python Package Index).  **PyPi** maintains a directory service for contributed packages that is accessible by **pip** whenever the tool is used to install a new package. 

# Part 1

Begin by creating a folder for your package under **src**. Because the name of your package has to be unique, name it as "<your_name>lib", replacing <your_name> accordingly (don't use spaces). 

```
src/<your_name>lib
```

Next, create the following file structure for your package. 

```
src
|__pck_<your_name>
   |__ __init__.py
   |__ mod.py
|__test.py
|__README.md
|__pyproject.toml
```

Leave **__init__.py** blank. **__init__.py** is required to import the directory as a package, and can be left empty. Next, add the following code in **mod.py**, which will be the single module in your package. 

```
def add_one(number):
    return number + 1
```

Add the following code in **test.py**. It will not be a proper test, just a validation that the package can be properly imported and used. 

```
from <your_name>lib import mod

print(mod.add_one(5))
```

Make sure you are able to run **test.py** from **src**. 

After the validation, add the following in **pyproject.toml**, making sure to update <your_name>. TOML stands for Tom's Obvious Minimal Language and it is a configuration format. 

```
[build-system]
requires = ["hatchling"]
build-backend = "hatchling.build"

[project]
name = "<your_name>lib"
version = "0.0.1"
authors = [
  { name="Example Author", email="author@example.com" },
]
description = "A small example package"
readme = "README.md"
requires-python = ">=3.7"
classifiers = [
    "Programming Language :: Python :: 3",
    "License :: OSI Approved :: MIT License",
    "Operating System :: OS Independent",
]

[project.urls]
"Homepage" = "https://github.com/pypa/sampleproject"
"Bug Tracker" = "https://github.com/pypa/sampleproject/issues"
```

Write something about your project in **README.md** (it cannot be left blank). 

Next, try to build your project using: 

```
python3 -m build src
```

If you get an error saying "No module named build" it means that you need to install build using pip3. After a successful build, a **dist** folder will be created (under src).

# Part 2

Next, it is time to publish your package so others can use. You need an account in [https://pypi.org/](https://pypi.org/). Then, go to [https://pypi.org/manage/account/](https://pypi.org/manage/account/) and scroll down so you can click on the "Add API token" button. Give your token a name and select "Entire account (all projects)" as the scope. Copy the token and use it to run the following: 

```
python3 -m twine upload -u __token__ -p <replace with your token> src/dist/*
```

You can repeat this process multiple times if needed. For example, you may want to update your package. To do that, update the version of your package in **pyproject.toml**. Next, remove the **dist** folder and rebuild. Finally, upload the new version. 

To test the installation and use of your package from PyPi, create a virtual environment and run **test.py**. 

# More Information

**PyPi** user guide is available [here](https://packaging.python.org/en/latest/tutorials/packaging-projects/).  
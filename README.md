# KBase - Tech Challenge

## Table of contents
* [General info](#general-info)
* [Technologies](#technologies)
* [Task 1 Usage](#task-1-usage)
* [Task 2 Usage](#task-2-usage)

## General info
The 2 tasks below allow me to demonstrate my programming skills for review by the KBase interview panel.

* Task 1: reassemble a text file that has been fragmented, for more details see [Task 1 Usage](#task-1-usage)

* Task 2: create a simple web service that uses the program from task 1, for more details see [Task 2 Usage](#task-2-usage)

## Technologies
Project is created with:
* Python version: 3.7.3
* Flask 1.1.2
* numpy 1.19.0
* pipenv 2018.11.26

## Installation
Open Terminal. <br />
Change the current working directory to the location where you want the cloned repository. <br />
clone the repository with git:
```bash
$ git clone https://gitlab.com/JTap159/kbase-challange.git
```

cd to the project ../kbase-challenge directory and create the virtual environment with pipenv. <br />
If pipenv is not installed use:

 ```bash
 pip install pipenv
 ```
Then, create the virtual environment with:
```bash
pipenv install --ignore-pipfile
```

## Task 1 Usage

cd to the project directory in the terminal

```bash
python assemble_fragments.py <file>
```

## Task 2 Usage

cd to the project directory in the terminal

```bash
flask run
```

Use Postman https://www.postman.com/ to send a post request of the fragments as a single input parameter
The single input parameters for each file to be reassembled can be found in

```bash
 kbase-challange/delim_files/
 ```
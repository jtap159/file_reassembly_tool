# KBase - Tech Challenge

## Table of contents
* [General info](#general-info)
* [Technologies](#technologies)
* [Installation and Setup](#installation-and-setup)
* [Task 1 Usage](#task-1-usage)
* [Task 2 Usage](#task-2-usage)
* [Lessons Learned](#lessons-learned)

## General info
The 2 tasks below allow me to demonstrate my programming skills for review by the KBase interview panel.

* Task 1: reassemble a text file that has been fragmented, for more details see [Task 1 Usage](#task-1-usage)

* Task 2: create a simple web service that uses the program from task 1, for more details see [Task 2 Usage](#task-2-usage)

## Technologies
Project is created with:
* Operating System: Linux, Ubuntu 18.04.3 LTS
* Python version: 3.7.3
* Flask 1.1.2
* numpy 1.19.0
* Pipenv 2018.11.26

## Installation and Setup
Open Terminal. <br />
Change the current working directory to the location where you want the cloned repository. <br />
Clone the repository with git:

```bash
$ git clone https://gitlab.com/JTap159/kbase-challange.git
```

cd to the project directory.

```bash
$ cd kbase-challange/
```

If Pipenv is not installed use:

 ```bash
$ pip install pipenv
 ```
Then, create the virtual environment with:

```bash
$ pipenv install --ignore-pipfile
```

Lastly, activate the Pipenv shell:
```bash
$ pipenv shell
```
for basic usage of Pipenv (specifying version of python) please see:

* [Pipenv Basic Usages](https://pipenv-fork.readthedocs.io/en/latest/basics.html)

for all other information on Pipenv please see:

* [Pipenv Documentation](https://pipenv.pypa.io/en/latest/)

## Task 1 Usage
**Description**: <br />
A text file has been fragmented into a series of fixed length substrings which are guaranteed to overlap by at 
least 3 characters and they are guaranteed not to be identical. The input file is a series of lines, each containing 
one of the fixed length substrings. Read this input file and then output the re-assembled source text. <br />

cd to the project directory in the terminal (terminal should look like this).

```bash
(kbase-challange) (base) jeremy@jeremy-Ubuntu:~/Desktop/kbase-challange$
```

All of the fragmented text files are in the frag_files folder:

```
kbase-challange/frag_files/
```

To reassemble a fragmented text file use below code passing in one argument <text-file-location>

```bash
$ python assemble_fragments.py <text-file-location>
```

**Example:** <br />
result will be printed to the terminal window:
```bash
(kbase-challange) (base) jeremy@jeremy-Ubuntu:~/Desktop/kbase-challange$ python assemble_fragments.py frag_files/hello-ordered-frags.txt 
// Sample program
public class HelloWorld {
    public static void main(String[] args) {
        // Prints "Hello, World" to the terminal window.
        System.out.println("Hello, World");
    }
}

```

**Note:** the fragmented text files can be anywhere on the computer, only the proper <text-file-location> needs to be used
## Task 2 Usage
Description: <br />
Take the program you have from task 1, and turn it into a very simple web service that accepts a POST method 
that includes all the fragments as a single input parameter, and then returns re-assembled source text 
as the response body. Your web service should be able to be started from the command line.

cd to the project directory in the terminal (terminal should look like this).

```bash
(kbase-challange) (base) jeremy@jeremy-Ubuntu:~/Desktop/kbase-challange$
```

To start the web service locally:

```bash
$ flask run
```

The terminal window should display the below information:

```bash
(kbase-challange) (base) jeremy@jeremy-Ubuntu:~/Desktop/kbase-challange$ flask run
 * Environment: production
   WARNING: This is a development server. Do not use it in a production deployment.
   Use a production WSGI server instead.
 * Debug mode: off
 * Running on http://127.0.0.1:5000/ (Press CTRL+C to quit)
```

**Note:** The fragmented files from task 1 had to be transformed adding a ",,, " delimiter 
between each fragment so that the fragments can be passed to the web service as a single input parameter.
The transformed files are located:

```
kbase-challange/delim_files/
```

Use [Postman](https://www.postman.com/) to send a post request of the fragments as a single input parameter.
the web service route to send the post request is (using fragments as a key):

```
http://127.0.0.1:5000/reassemble_frags?fragments=...
```

**Example:**<br />
Using the hello-ordered-frags_delim.txt file copy and paste the line in the file into 
the post request parameter value related to the "fragment" key. 
The URL should look like this:

```
http://127.0.0.1:5000/reassemble_frags?fragments=%2F%2F+Sample+progr,,, program%0Apublic+,,, ublic+class+Hel,,, lass+HelloWorld,,, elloWorld+%7B%0A+++,,, d+%7B%0A++++public+,,, public+static+v,,, c+static+void+m,,, id+main%28String%5B,,, %28String%5B%5D+args%29,,, args%29+%7B%0A+++++++,,, ++++++%2F%2F+Prints,,, %2F%2F+Prints+%22Hell,,, ts+%22Hello%2C+Worl,,, %2C+World%22+to+the,,, %22+to+the+termin,,, rminal+window.%0A,,, ow.%0A++++++++Sys,,, +++++++System.o,,, stem.out.printl,,, intln%28%22Hello%2C+W,,, o%2C+World%22%29%3B%0A+++,,, rld%22%29%3B%0A++++%7D%0A%7D%0A,,, %3B%0A++++%7D%0A%7D%0A
```

Output (reassembled source text as response body):

```
// Sample program
public class HelloWorld {
    public static void main(String[] args) {
        // Prints "Hello, World" to the terminal window.
        System.out.println("Hello, World");
    }
}

```
**Note:** if reassembling the file is not possible then all of the best possible reassembles will be returned

## Lessons Learned
* Firstly, thank you for your time to review my application
* This was a great challenge for me to be able to use many of the problem solving skills i have gained in the past few
years and work on areas i have neglected as well.
* Using the debugger in pycharm was crucial for the completion of this project, for example: debugging through 
multiple scopes and looping iterations
* I have never used gitlab before but it was easy to learn and gave me exposure to a different remote repository
solution other than github.
* Overall i had fun solving this problem and look forward to solving many other problems like this in the future.

Cheers! <br />
-Jeremy Tapia
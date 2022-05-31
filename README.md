Argument Mining with Tone Analysis 6.0 

- This is currently still in BETA mode. We need to fine-tune and tweek the seed files (argument files) to better 
extract arguments
- Similar to LDA analysis, it's straightforward just to run 'report_output.py'
- Understanding validity of each review. And no, it's not to catch if the review is really valid,
but it's to better understand if the review can be valid or not. 

### Learn and Purpose:
- Main purpose of running this program is to extract arguments, labels for each argument,
and which sentences that contain the arguments. Therefore, we have a better understanding
of each review's intentions, goals, purpose, reasons, etc.; to see if the stated attributes are even true or false, 
to better category if the reviews are valid or nonsense. 

- Through process of finding certain rhetorical phrases and keywords, we can extract if they contain 
a valid or false argument in the review. Argument mining is a way to check the validity of the review,
if the author is making any contradictions, if the author is having any strong or weak emotions in their arguments, 
or if the author is making any sense. This can lead to some bias, but in a certain way, we want to check if their is a 
contradiction between their own emotion (through Tone Analysis) and their argument - to ensure we don't just rely
 on analyzing their arguments. 
 
- Rhetorical mining is still underway ... 

#### Installing Requirements:
Add configurations from 'requirements.txt'. If you're using an IDE, it will prompt you
to install the packages. Otherwise, simply run:
- _pip install <package_names>_

#### Expected prerequisites:
You should know how to run Apache Spark on Python IDE. Make sure Apache Spark
and Pypsark package (Python) is running properly before executing the program 

#### Prerequistes

#### Before execution:
Make sure the following are existed in the program:
* 'author_info' folder (for outputs)
* 'data' folder (for the original raw data of reviews)

Then, run:
- _python report_output.py_

#### Warnings:
You may see few WARNINGS if not none of them. You can simply ignore them.

#### Resources:
- https://pypi.org/project/spacy-arguing-lexicon/

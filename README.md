# Health-ID
![HealthIDlogo](https://user-images.githubusercontent.com/103985810/216312683-4221cd84-d7bf-4a2c-8d13-aa42f630d147.png)

This project aims to create a blockchain based database system for the peoples associated with the healthcare system. The most important objective was to keep the data of the patients secure, maintaining their privacy as the prime focus.

## Table of Contents

## Introduction
### About Health-ID
We have used the blockchain technology which we have implemented through Flask-Python on the server side. It also uses the MySQL database for storing the user, appointment, prescription details and theses uploaded from the research institutes. This website can be used by the Patients, Doctors, Researchers and Organizations such as the hospitals and research institutes. The blockchain service has been displayed on the website using HTML/CSS and Javascript. We have obtained a plethora of knowledge about Blockchain, MySQL and in general, database management systems.

### Tech-Stack
Frontend
1. HTML/CSS
2. Javascript

Backend
1. Python
2. APIs-Flask, Filestack
3. MySQL 
4. JSON

Code Editor
Visual Studio Code

###File Structure

## Getting Started
###Pre-Requisites
* You must have the latest version of ![Python3](https://www.python.org/downloads/).
* Since the website uses ![Flask](https://pypi.org/project/Flask/), this framework should be present.
* You also have to install some modules such as passlib.hash, hashlib, wtforms, functool and sys if they are not already present in your system.
* To connect your flask with your MySQL database, you require the flask_mysqldb module.

###Installations
* Install Flask
`pip install flask`
`pip install flask-mysqldb`
`pip install passlib`

* Install wtforms
`pip install wtforms`

* Install ![MySQL](https://www.mysql.com/downloads/)

* Install ![Filestack]

### Operating MYSQL tables
Open your MYSQL Command Line Client or enter the following command in your command prompt
`mysql -u root -p`
On doing this, it would ask you for your password.

`CREATE DATABASE healthid;`
`USE healthid`
You would recieve the message that the database has been changed.

### Usage
We hope that you already have git installed in your system.

1. Clone our Git repository
`git clone https://github.com/KedarDhamankar/Health-ID.git`

2. Move into the directory
`cd .../Health-ID`

3. Run the app.py python file
`python app.py`

## What we learned from this project

## Future Scope
* Catalouging previous health records of the patient.
* More functionality for the Doctor user.
* Search Engine function for theses and research papers.
* Maintaining digital records of the Organisation user.
* Increasing security.
* GPU support for data mining.

## Contributors
* [Rucha Patil](https://github.com/Ruchapatil03)
* [Kedar Dhamankar](https://github.com/KedarDhamankar)
* [Yash Singavi](https://github.com/YashSingavi)
* [Komal Sambhus](https://github.com/Komal0103)

## Mentors
We are extremely grateful to our mentors for encouraging and guiding us throughout this project
* [Arnav Zutshi](https://github.com/AsRaNi1)
* [Abhishek Gupta]()

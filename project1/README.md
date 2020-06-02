# cs50
Harvard course on web programming with Python/JS

# Project 1
In Project 1 the book review website was created.
And below is the short description of project files (what files are included and what project requirements are met)

# .gitignore
Contains records for exclusion two folders from commitment to github. These two folders __pycache__ and flask_session contain temporary files

# application.py
Main file with all website logic written

# books.csv
Dataset of books provided and to be uploaded to the PostgreSQL database

# check_goodreads.py
Python script for checking if Goodreads api key received after registration on the website is valid and can be used in the Project 1

# import.py
Python script developed separately as per task requirements. It inserts data from books.csv file into books table of out database

# README.md
short writeup describing my project and the short description of each file

# requirements.txt
List of Python libraries to be install for correct application work

# scripts/scripts.sql
Contains raw scripts for initial tables creation in PostgreSQL database.
Shows fields names chosen and type of each fields

# static/styles.css
Styles file for the project

# templates/book.html
Contains all needed information about selected book. It has a block with the detailed info for the book (ISBH code, title, author, year of publishing).
Another block shows the list of all reviews posted on our web site with information on user who posted the review and book rank by his opinion (number from 1 to 5).
A separate block proposes the form for submission of your own rank/comment. Please be noted that for every user it is allowed to post one comment to one book only.
Also there is a section with addition information received from Goodreads website through official api (number of reviews and average score).

# templates/books.html
Shows search results for requests input on the main (search) page.
Every found result contains hyperlink to the page with detailed information on the selected book.

# templates/errors.html
This page is presented when user request contains some kind of error. For the instance it can be wrong user name or password during authorization or the attempt to post the second review for the one book from the same user.

# templates/index.html
Starting page of our website. Shows search input field. Search can be done by ISBH code, book title of author name. Search by part of the string is enabled as per project requirements.

# templates/layout.html
layout template. Also contains information about authorized user and link allowing user to log off from the system.

# templates/login.html
This is the form where user can log in into the system by entering his/her user name and password. Password is hidden and not shown on the screen.
If user enters incorrect login name or password, system does not allow him to be authorized.

# templates/register.html
This is the form where user can register in the system. Password is hidden by dots. If new user enters existing user name, he/she will receive a notification.

# templates/success_add_review.html
Page with notification about successful comment posting.

# templates/success_login.html
Page with notification about successful login.

# templates/success_register.html
Page with notification about successful registration in the system.

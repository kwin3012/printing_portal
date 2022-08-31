# Printing-portal
It is a web developed using Django Framework, where user can upload his/her document to be printed and can pay respective amount using integrated epayment gateway.
The website includes seperate login system for general users and shopkeepers. Visit the website at [Printing Portal](https://printingportal.pythonanywhere.com/).

## Installation
Python and Django need to be installed

```bash
pip install django
```
## Usage

Go to the printing-portal folder and run 

```bash
python manage.py runserver
```

Then go to the browser and enter the url **http://localhost:8000/**

## Login

The login page is common for customer and shopkeeper.

You can access the django admin page at **http://localhost:8000/admin**, after creating new admin user by following command

```bash
python manage.py createsuperuser
```
## User
There is no need to create any user from admin page.
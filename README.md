# Planner 🕒
A reminder management web application built with Django.

Planner allows users to create, manage, and organize their personal reminders. Each user has their own reminders, including title, description, date, time, and color information.

This project was developed to learn and practice Django fundamentals, including models, ORM, authentication, templates, static files, and database management.

## Features
- User authentication
- Login/logout
- User-specific data access
- Create, read, update, and delete reminders
- Each user can manage their own reminders
- Reminder attributes:
 - Title
 - Description
 - Date
 - Time
 - Color
- Admin dashboard for managing application data
- PostgreSQL database integration
- Responsive template structure using Django templates
## Technology Stack
Backend
- Python 3.13
- Django
- Django ORM
- Django Authentication System
Database
- PostgreSQL 15
Frontend
- Django Templates
- HTML
- CSS
## Development Tools
- Git
- Virtual Environment
- Environment variables (.env)
## Project Architecture

The project follows Django's MVT (Model-View-Template) architecture:

Browser
   |
   ↓
URL Dispatcher
   |
   ↓
View
   |
   ↓
Model / ORM
   |
   ↓
PostgreSQL Database

View
   |
   ↓
Template
   |
   ↓
HTML Response

## Data Model
- User

Django's built-in authentication user model is used.

User
----
id
username
password
email
Reminder

Each user has many reminders:

Reminder
---------
id
user_id (Foreign Key)
title
description
date
time
color

## Authentication
Planner uses Django's built-in authentication system.
Protected views ensure users can only access their own data.


## Admin Panel
Django Admin is configured to manage reminders.
Features:
- List display customization
- Filtering
- Searching
- Ordering

## Running Locally
- Clone the repository:
```shell
git clone https://github.com/farkhondehsharifi/Django_planner.git
```
- Create virtual environment:
```shell
python3 -m venv venv
```
- Activate:

 - macOS/Linux:
```shell
source venv/bin/activate
```
- Install dependencies:
```shell
pip install -r requirements.txt
```
- Create database migrations:
```shell
python manage.py migrate
```
- Create admin user:
```shell
python manage.py createsuperuser
```
- Run server:
```shell
python manage.py runserver
```
- Open:

[Planner](http://127.0.0.1:8000/)



## Learning Goals

This project helped me practice:

- Django project/app structure
- Model design
- Database relationships
- PostgreSQL integration
- Django ORM queries
- Authentication and authorization
- Template inheritance
- Static file management
- Git workflow
- Reminder notifications
- Email reminders
- Calendar view
- Recurring reminders
- REST API using Django REST Framework
- Mobile application client
- Docker deployment

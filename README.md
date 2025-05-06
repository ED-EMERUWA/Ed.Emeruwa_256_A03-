# EventFlow 
A Django Web Application for Event Registration

## Overview

**EventFlow** is a web-based event registration system developed for ITAS256 assignment 3. It supports two types of users: **Administrators** and **Registrants**.

- **Administrators** can manage events and generate system reports.
- **Registrants** can create accounts and register/unregister for events.

This application is built using the Django framework with templates, forms, and built-in authentication.

## Features

### Accounts
- **Registrant Sign Up** with:
  - Email validation
  - Secure password rules
- **Login & Logout** for both Admins and Registrants
- Role-based access control

### Events
- **Create / Update / Delete** events (Admin only)
- **Register / Unregister** for events (Registrant only)
- **View upcoming and past events**


## Tech Stack

- **Framework**: Django
- **Frontend**: Django Templates + Tailwind
- **Database**: SQLite (dev) / MySQL (prod-ready)
- **Auth**: Django's built-in authentication system
- **Deployment Ready**: DigitalOcean + MySQL

## Getting Started

### 1. Clone the repo.
### 2. In you terminal run `python manage.py createsuperuser` to cretw supe user.
### 3. Add created super user to adminstrators group.
### 4. Run `python manage.py runserver` to run app.
### 5. Login to application.
### 6. Have fun.

```bash
git clone https://github.com/<your-username>/Ed.Emeruwa_256_A03-.git
cd Ed.Emeruwa_256_A03-

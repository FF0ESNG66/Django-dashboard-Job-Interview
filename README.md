# Improving a Login System

## Overview

In this project I received a template of a webpage and I had to add a new feature/page that I imagine could be used for the company.
Looking through the webpage the first thing that I noticed was that the login system was poorly developed.

The previous login system consisted in that a client/user can create an account and then log in. 
This system has many issues just like:

- No email confirmation at the moment of an account creation
- No password recovery system implemented
- An user can create multiple accounts with the same email address


## Key Features - Backend

1. **Email confirmation system**
   - I developed a simple email confirmation system using a token generator (`tokens.py`) and adding a few function-based views.
   - I do also modified the originals `login_view` and `register_user` view in order to have more flexibility at the momment of doing some verifications, validations and doing some querys to the
     database, however, I tried to maintain the essence of the original views as much as possible (such as leave them as s function-based views and not class-based views)
   - Now an email address must be unique through users
   - If a user creates a new account and for some reason they delete the verification email, they can receive another one just by trying to log in with that inactive account

2. **Password Recovery System**
   - I made a password recovery system using the Django's built-in auth views.
   - Now that users can't create multiple accounts using the same email, I'm available to implement a recovery system by going to the Log In page, then Password Recovery page and input the corresponding
     email associated with that account. If an account exists with that email then a password reset email will be send, otherwise the page will be rendered either way but nothing will be sended


## Key Features - Frontend

Multiple HTML templates were added in order to show the new pages created, these templates are:

- `inactive_user.html`
- `template_activate_account.html`
- `password_recovery.html`
- `password_reset_complete.html`
- `password_reset_confirm.html`
- `password_reset_done.html`
- `password_reset_email.html`

The last six templated related to password recovery system were added to a subdirectory named `password_folder` inside of `accounts` directory in order to maintain an order.
All these files follow the same design line of the entire webpage to no make a disruptive user experience

# Simple-Django-Authentication
A simple django website for logging in, out and resetting user passwords.
The site does not focus much on the frontend but the backend functionality using python django.
The core element of the site is the `accounts/views.py` which contains all the Function-Based Views (FBVs) and Class-Based Views (CBV) for user authentication.
Some of the views include: logout FBV, RegisterUser CBV and PasswordResetRequest CBV. 
Upon clicking the `forgot password`, a user fills a form with their registered address to request a generated token sent via email.
The token is used to redirect and reset the users password.

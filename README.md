# Quick Aid Backend
This is the backend for the Quick Aid app, built using Django. The backend handles user authentication, service requests, notifications, and manages communication between the app and emergency service providers.

# Features
* **User Authentication:** Registration, login, and OTP verification for users.
* **Service Requests:** Processes user requests for emergency services like ambulances or police.
* **Notifications:** Sends notifications to nearby service providers when a request is made.
* **Data Encryption:** Securely stores and encrypts sensitive data.
* **Offline Support:** Provides fallback options to ensure users can dial emergency numbers without an internet connection.
## Tech Stack
* **Framework:** Django (Python)
* **Database:** SqLite
* **Authentication:** Django REST Framework (DRF)
* **Notifications:** Integration with Firebase Cloud messaging (FCM) for push notifications
* **Security:** SHA-256 password encryption, OTP-based verification
## Setup and Installation
**Prerequisites**
* Python 12 or above
* Django 5 or above
* Virtualenv (optional but recommended)

# Installation Steps
**1. Clone the repository:**

```
git clone https://github.com/Innovate-X-team/quick-aid-backend.git
cd quick-aid-backend
```
**2. Create a virtual environment:**

```
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
```
**3. Install dependencies:**

```
pip install -r requirements.txt
```
**4. Configure environment variables:** Create a .env file in the project root with the following:

```
SECRET_KEY=your-secret-key
EMAIL_PASSWORD=your-email's-app-password
```

**5. Add service account key:**
Add service account key to connect firebase.

1. Go to firebase and create a new project.
2. Go to project's settings page
3. Go to service account tab
4. Now click on Generate new private key to download `serviceAccountKey.json` file
5. Put the json file on the root directory of your project.

**6. Set up the database:**
```
python manage.py migrate
```
**7. Create a superuser:** To access the Django admin panel, create a superuser:

```
python manage.py createsuperuser
```
**8. Run the development server:**
```
python manage.py runserver
```

## Running the App
See Quick Aid's user app repository for seting up the mobile application. https://github.com/Innovate-X-team/quick-aid-user-app.git

## API Endpoints
The backend exposes a set of REST APIs for the Quick Aid app:

**Authentication:**

* POST /api/login/: User login
* POST /api/create_user/: User registration
* POST /api/send_email_otp/: Send OTP to email
* POST /api/verify_email/: OTP verification
* POST /api/change_password/: CChange password
* POST /api/check_username/: Check username availability

**Service Requests:**
* POST /api/call_service/: Create a new emergency service request

**Service Provider:**

* POST /api/onduty_toggle/: Change the providers availablity status
* POST /api/is_onduty/: Check the providers availablity status
* POST /api/update_location/: Update provider's current location
* POST /api/get_assigned_task/: Get current assigned task
* POST /api/accept_task/: Accept current assigned task
* POST /api/complete_task/: Complete task

## Running Tests
To run unit tests for the backend:

```
python manage.py test
```

## Deployment

* Set DEBUG=False
* Add your domain to ALLOWED_HOSTS

* WSGI/ASGI: Use a WSGI/ASGI server like Gunicorn or Daphne for production:

```
pip install gunicorn
gunicorn quick_aid.wsgi:application
```

# Contributing
* Fork the repository
* Create a new branch (`git checkout -b feature/your-feature`)
* Commit your changes (`git commit -m 'Add some feature'`)
* Push to the branch (`git push origin feature/your-feature`)
* Create a pull request
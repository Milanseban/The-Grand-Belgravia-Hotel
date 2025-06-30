# The Grand Belgravia - Luxury Hotel Booking Web Application

<div align="center">
  <img src="https://img.shields.io/badge/Python-3776AB?style=for-the-badge&logo=python&logoColor=white" alt="Python Badge"/>
  <img src="https://img.shields.io/badge/Django-092E20?style=for-the-badge&logo=django&logoColor=white" alt="Django Badge"/>
  <img src="https://img.shields.io/badge/JavaScript-F7DF1E?style=for-the-badge&logo=javascript&logoColor=black" alt="JavaScript Badge"/>
</div>

---

This project is a full-stack web application for a luxury mock hotel, "The Grand Belgravia." It features a complete user journey, from Browse the hotel's amenities to creating user accounts and making real, persistent bookings in a database.

##  Project Overview

The application provides a seamless and elegant user experience, allowing guests to explore rooms, dining, and spa services. The core functionality includes a secure user authentication system (Signup/Login), a complete booking engine that handles real-time room availability, and a personalized user dashboard for managing reservations. The application is built with a robust Django backend serving a dynamic HTML, CSS, and JavaScript frontend.

---

##  Screenshots



**Homepage:**


<img width="950" alt="s1" src="https://github.com/user-attachments/assets/caafa1f9-1f61-4575-b1cd-23d9a6872673" />




**Account Dashboard:**


<img width="946" alt="s2" src="https://github.com/user-attachments/assets/b67aff57-9823-4b8a-bf57-734ed1e91821" />




---

##  Key Features

- **Full End-to-End Booking Flow:** A multi-step process for users to check room availability and make reservations that are saved permanently.
- **Real-time Availability Check:** The booking form connects to a backend API that checks the database for conflicting bookings before allowing a reservation.
- **Secure User Authentication:** A complete Signup & Login system built with Django's native user model and Django REST Framework's Token Authentication.
  - Secure password hashing for all user accounts.
  - Token-based authentication for all protected API requests.
- **Personalized Account Management Dashboard:** A dedicated `/account/` page for logged-in users to:
  - View their real **Upcoming and Past** booking history, fetched live from the backend.
  - **Cancel** upcoming bookings, subject to a 5-day notice period enforced by the backend.
  - **Modify** booking details.
  - **Update** their profile information (username and email).
- **Dynamic Frontend:** A fully interactive user interface built with modern HTML5, CSS3, and vanilla JavaScript, featuring on-scroll animations and DOM manipulation.
- **RESTful API Backend:** A robust API built with Django and Django REST Framework handles all data operations for users, rooms, and bookings.

---

##  Project Structure

```
The-Grand-Belgravia/
│
├── hotel_backend/        # Main Django project configuration
│   ├── settings.py
│   └── urls.py
│
├── reservations/         # Django app for all hotel logic
│   ├── models.py         # Database models (Room, Booking)
│   ├── serializers.py    # API data translators
│   ├── views.py          # Backend logic for pages and API endpoints
│   ├── urls.py           # App-specific URL routing
│   └── admin.py
│
├── assets/               # Static files (images, videos)
│
├── templates/            # All HTML files
│
├── .gitignore            # Specifies files for Git to ignore
├── manage.py             # Django's command-line utility
└── requirements.txt      # Python package dependencies
```

---

##  How to Run

1.  **Clone the repository:**
    ```bash
    git clone [https://github.com/Milanseban/The-Grand-Belgravia-Hotel.git](https://github.com/Milanseban/The-Grand-Belgravia-Hotel.git)
    cd The-Grand-Belgravia-Hotel
    ```

2.  **Set up the environment:**
    - Create and activate a Python virtual environment:
        ```bash
        python -m venv venv
        source venv/bin/activate  # On Windows: venv\Scripts\activate
        ```
    - Install dependencies from the `requirements.txt` file:
        ```bash
        pip install -r requirements.txt
        ```

3.  **Initialize the database:**
    ```bash
    python manage.py migrate
    ```

4.  **Create an administrator account** (to log into the admin panel at `/admin/` and add room data):
    ```bash
    python manage.py createsuperuser
    ```

5.  **Run the Django development server:**
    ```bash
    python manage.py runserver
    ```

The application will be live at `http://127.0.0.1:8000/`.

---

## 🛠️ Technologies Used

- **Backend:**
  - Python
  - Django & Django REST Framework
  - SQLite3
- **Frontend:**
  - HTML5
  - CSS3
  - Vanilla JavaScript (for DOM manipulation and API calls)
- **Deployment & Version Control:**
  - Git & GitHub

---

## ✍️ Author

**Milan Sebastian**
www.linkedin.com/in/milan-sebastian-a76236251
```


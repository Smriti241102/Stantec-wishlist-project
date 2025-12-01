#  Stantec Wishlist Project

## Wishlist App

A **Django-based** web application that allows users to create and manage **wishlists**, add items, share their wishlists with others, and mark items as purchased.

---

## ✨ Features

* **User Authentication**: Secure signup, login, and logout functionality.
* **Personal Wishlists**: Dedicated wishlists for each registered user.
* **Item Management**: Add items with detailed fields:
    * **Name**
    * **Description**
    * **Multiple Links**
    * **Priority Levels** (e.g., High, Medium, Low)
    * **Image Upload**
* **Sharing**: View other users’ wishlists.
* **Purchasing**: Mark items as **purchased** to prevent duplicate gift buying.
* **Filtering**: Filter purchased items on your own wishlist for better organization.
* **Responsive Design**: Modern and responsive user interface using **Bootstrap**.

---

## 🛠️ Tech Stack

* **Python** 3.12+
* **Django** 5
* **Database**: SQLite (default)
* **Frontend Framework**: Bootstrap 5
* **Web Technologies**: HTML + JavaScript

---

## Setup Instructions

Follow these steps to run the project locally.

### 1. Clone the repository

```bash
git clone [https://github.com/](https://github.com/)<your-repo>/wishlist-app.git
cd wishlist-app
```

### 2. Create virtual environment
```bash
python3 -m venv venv
source venv/bin/activate
# For Windows: venv\Scripts\activate
```
### 3. Install all the requirements
```bash
pip install -r requirements.txt
```

### 4. Create a .env file in the project root
```bash
DEBUG=True
ALLOWED_HOSTS=localhost,127.0.0.1
# Also replace email credentials in settings.py using your own to send emails
```
### 5. Run migrations
```bash
python manage.py migrate
```
### 6. Create superuser
```bash
python manage.py createsuperuser
```
### 7. Start the server
```bash
python manage.py runserver
```

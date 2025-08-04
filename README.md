# FileStorageApp

This is an app that will allow users to login, upload, and view specific files.

## Frontend Components

-   Register Page ✅
-   Login Page ✅
-   Upload Page ✅
-   View Page ✅
-   Manage Users Page ✅

## Backend Components

-   Users (Login / Register) ✅
-   Upload (Save to "Files" Directory) ✅
-   Files ✅
-   Database (Create, Insert, Get, Delete) ✅

## Running the Backend

1. Navigate to the backend directory:
    ```
    cd FileStorageApp/Backend
    ```
2. (Optional) Create and activate a virtual environment:
    ```
    python3 -m venv venv
    source venv/bin/activate
    ```
3. Install dependencies:
    ```
    pip install Flask Flask-Cors gunicorn
    ```
4. Run the backend server:
    ```
    ./app.py
    ```

## Running the Frontend

Open the desired HTML file in your browser from the `Frontend` directory, for example:

-   `index.html`
-   `login/login.html`
-   `register/register.html`
-   `home/home.html`
-   `files/files.html`
-   `manage-users/manage-users.html`

## Notes

-   Backend runs on port 3000 by default.
-   Static files are served from the `static/` directory.
-   Authentication is basic and not suitable for production use.
-   Make sure the backend is running before using the frontend.

DISCLAIMER : This code is generated with AI use with caution
# Post Office Receipt Generator (Web Version)

A web-based application for generating Pakistan Post Office receipt images.

## Overview

This project is a web application that automates the process of creating receipt images for Pakistan Post Office transactions. It's designed to simplify record-keeping and provide a user-friendly interface for generating professional-looking receipts. This project was created in 2025 by Danyal Khan.

## Features

*   **User-Friendly Web Interface:** Easily input receipt details through a web browser.
*   **Receipt Generation:** Dynamically generate receipt images based on user input.
*   **Customizable:** Allows for some level of customization of receipt content.
*   **Database Integration:** Uses a SQLite database (`customer_data.db`) to store customer data.
*   **Logo Included:** Includes the Pakistan Post logo (`pakistan_post_logo.png`) for authentic receipt appearance.
*   **Templates:** Uses the templates directory to provide a template of the UI
*   **CSV Import/Export:** Import data from CSV files or export existing data to CSV.
*   **PDF Generation:** Download receipt information as PDF files (all data or for the current day).

## Technologies Used

*   **Python:** The primary programming language.
*   **Flask:** A Python web framework used to build the application's web interface and handle requests.
*   **SQLite:** A lightweight database used to store data.
*   **ReportLab:** A Python library for generating PDF files.
*   **HTML/CSS/JavaScript:** Used for the frontend (user interface).
*   **chardet**: For automatic character encoding detection of the CSV import file.

## Python Libraries Used

*   **flask:** For creating the web application.
*   **sqlite3:** For interacting with the SQLite database.
*   **datetime:** For handling date and time information (e.g., timestamps).
*   **reportlab:** For generating PDF files.
*   **io:** For working with in-memory streams (e.g., creating a buffer for the PDF).
*   **os:** For interacting with the operating system (e.g., checking file existence).
*   **csv:** For reading and writing CSV files.
*   **chardet:** For character encoding detection of the CSV import file.

## Requirements

The application has been tested with:

*   Python 3.7+
*   Flask
*   SQLite
*   ReportLab

## Setup and Installation

1.  **Clone the repository:**

    ```bash
    git clone https://github.com/danyalkahn/post_office_receipt_generator_web_version.git
    cd post_office_receipt_generator_web_version
    ```

2.  **Create a virtual environment (recommended):**

    ```bash
    python3 -m venv venv
    source venv/bin/activate  # On Linux/macOS
    # venv\Scripts\activate  # On Windows
    ```

3.  **Install dependencies:**

    ```bash
    pip install -r requirements.txt
    ```

    **Example `requirements.txt` content (create it using `pip freeze > requirements.txt` after installing the packages):**

    ```
    Flask==2.3.3
    reportlab==4.0.3
    chardet==5.2.0
    ```

4.  **Set Environment Variables:**

      * The receipt logo location **PAKISTAN_POST_LOGO**
      * The text image used location **TEXT_IMAGE**
      * You can set these in your `.env` file if needed
        ```
        export PAKISTAN_POST_LOGO=./location/pakistan_post_logo.png
        export TEXT_IMAGE=./location/text.jpg
        ```

5.  **Run the application:**

    ```bash
    python code.py
    ```

6.  **Access the application:** Open a web browser and go to `http://localhost:5000` (or the address/port specified by Flask).

## File Structure
post_office_receipt_generator_web_version/
├── code.py # Main Flask application file
├── customer_data.db # SQLite database
├── pakistan_post_logo.png # Pakistan Post logo image
├── text.jpg # Text image for the receipt
├── templates/ # HTML templates
│ └── index.html # Main HTML template for the receipt generation form
├── requirements.txt # List of Python dependencies
└── README.md # This file



## Database

The application uses a SQLite database (`customer_data.db`). The database schema is as follows:

```sql
CREATE TABLE customer_data (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    name TEXT,
    address TEXT,
    city TEXT,
    phone TEXT,
    price TEXT,
    timestamp TEXT
);
```


**Key Improvements:**

*   **Complete `README.md` content:** Includes all previously discussed sections.
*   **Example `requirements.txt`:** Provides a concrete example, making setup easier.
*   **File Structure:** Added a file structure section, helps users understand the organization of the project.
*   **Database Schema:** Added a schema for the database.
*   **Clearer Language:** Improved phrasing and grammar throughout the document.
*   **Set Environment Variables:** Added section to set environment variables.
*   **Set Set environment variable to your logo and text location so the app can get their values from environment variables.**
*   **Added Disclaimer:** Added a disclaimer, which is extremely important

This revised version should be a good starting point for your repository's `README.md` file. Customize the bracketed placeholders and adapt the content to accurately reflect your project's details and features. Remember to create a `LICENSE` file as well.


How to Create and Use requirements.txt:

Ensure you're in your virtual environment: Activate your virtual environment before installing or freezing dependencies.

```source venv/bin/activate   # Linux/macOS
venv\Scripts\activate  # Windows
```
Install the packages (if you haven't already): If you don't have those libraries already:
```pip install Flask reportlab chardet gunicorn
```
Generate the requirements.txt file: This is the best way to ensure you capture all the dependencies (including transitive ones).
```pip freeze > requirements.txt
```
This command creates a file named requirements.txt in your current directory, listing all the packages and their versions that are installed in your virtual environment.

Using the requirements.txt file to install dependencies: If someone wants to install all the dependencies listed in your requirements.txt file, they can run:

```
pip install -r requirements.txt
```

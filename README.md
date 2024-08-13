# expenomy

Expenomy is an expense tracker web application built with React, Flask and SQLite. It is designed for easy use to help manage efficient expense tracking. 

## Diagrams

<img src="./docs/assets/Frame 64UML_diagram.png" style="width:300px">


# Expenomy Backend

[![License](https://img.shields.io/badge/license-MIT-blue.svg)](LICENSE)

The Expenomy backend is the core API and database management system for the Expenomy application, a tool designed for managing and tracking personal expenses. This backend is built using Python with Flask, and it handles the main operations such as user authentication, expense tracking, and data management. 

## Table of Contents

- [Features](#features)
- [Project Structure](#project-structure)
- [Installation](#installation)
- [Configuration](#configuration)
- [Usage](#usage)
- [API Endpoints](#api-endpoints)
- [Models](#models)
- [Contributing](#contributing)
- [License](#license)
- [Contact](#contact)

## Features

- **User Authentication**: Secure login and registration using JWT.
- **Expense Tracking**: CRUD operations for managing expenses.
- **Database Management**: SQLAlchemy models for efficient data handling.
- **Configuration Management**: Centralized configuration using a Python-based configuration file.

## Project Structure

```
backend/
│
├── app.py         # Main application file, entry point for the Flask app
├── config.py      # Configuration file for managing environment settings
├── models.py      # SQLAlchemy models for the application’s database schema

```

### `app.py`

The `app.py` file is the entry point for the Expenomy backend. It sets up the Flask application, initializes the database, and defines the main routes and endpoints.

- **Flask Application**: The core of the application is defined here, with all routes and middleware configurations.
- **Database Initialization**: The SQLAlchemy database is initialized and configured in this file.

### `config.py`

The `config.py` file centralizes all configuration settings for the application. This includes database connection strings, secret keys for JWT, and other environment-specific variables.

- **Environment-Based Configurations**: The application can be configured for different environments (development, testing, production) through this file.
- **Security Settings**: Configuration for secure handling of sensitive information like secret keys.

### `models.py`

The `models.py` file defines the database schema using SQLAlchemy models. It includes the structure for users, expenses, and any other entities required by the application.

- **User Model**: Defines the structure for user data, including authentication details.
- **Expense Model**: Manages expense records, including categories, amounts, and timestamps.

## Installation

### Prerequisites

- [Python 3.8+](https://www.python.org/downloads/)
- [pip](https://pip.pypa.io/en/stable/)

### Clone the Repository

```bash
git clone https://github.com/adnantabda/expenomy.git
cd expenomy/backend
```


## Configuration

Before running the application, make sure to configure the environment settings in `config.py`. Adjust the settings according to your environment (development, testing, production).

### Example Configuration

```python
class Config:
    SECRET_KEY = 'your_secret_key'
    SQLALCHEMY_DATABASE_URI = 'sqlite:///ExpenseTrackerDB.db'
    SQLALCHEMY_TRACK_MODIFICATIONS = False
```

## Usage

### Running the Application

To start the Flask development server:

```bash
flask run
```

### Expense Management

- **GET /expenses**: Retrieve a list of all expenses for the authenticated user.
- **POST /expenses**: Create a new expense record.
- **PUT /expenses/<id>**: Update an existing expense record.
- **DELETE /expenses/<id>**: Delete an expense record.

## Models

### User Model

The `User` model defines the following fields:

- **id**: Integer, primary key.
- **username**: String, unique, required.
- **expenses**: Relationship with the `Expense` model.

### Expense Model

The `Expense` model includes:

- **id**: Integer, primary key.
- **amount**: Float, required.
- **category**: String, category of the expense.
- **user_id**: Foreign key linking to the `User` model.

## Contributing

Contributions to Expenomy are welcome! Please follow these steps:

1. Fork the repository.
2. Create a new branch (`git checkout -b feature-branch`).
3. Commit your changes (`git commit -m 'Add some feature'`).
4. Push to the branch (`git push origin feature-branch`).
5. Open a pull request.

## License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

For any questions or feedback, feel free to reach out
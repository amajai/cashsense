# CASHSENSE
## Your Ultimate Expense Tracking Companion

Cashsense is a full-fledged web application built to help users manage their spending by tracking budgets and expenses. Users can create an account, set budgets, and add expenses to gain insights into their financial activities over a specific duration.

## Features

- **User Authentication:** Secure user registration, login, and logout functionalities.
- **Budget Management:** Create, edit, and delete budgets to plan and organize spending.
- **Expense Tracking:** Add, edit, and delete expenses associated with specific budgets.
- **Dashboard:** Visualize and analyze budget-related data on the user dashboard.

## Technologies Used

- **Backend:**
  - Flask: A lightweight web application framework in Python.
  - Flask-RESTful: Extension for building REST APIs with Flask.

- **Frontend:**
  - HTML, CSS, JavaScript: Building the user interface.
  - Flask for routing on the frontend.

## Getting Started

To run the application locally, follow these steps:

```bash
# Clone the repository
git clone https://github.com/zibxto/cashsense.git
cd cashsense

# Install dependencies
pip install -r requirements.txt

# Set up environment variables
# Create a .env file and configure the necessary variables (e.g., BACKEND_URL, SECRET_KEY and SQLALCHEMY_DATABASE_URI)

# Run frontend application
flask run -p 5000 -h localhost -e development -a frontend.run

# Run backend application
flask run -p 5000 -h localhost -e development -a backend.app
```

## Contributors

Special thanks to the contributors who have helped make this project better!

- **[Christian Aziba](mailto:christianaziba@gmail.com)**
  - Email: christianaziba@gmail.com.com
  - [LinkedIn](https://www.linkedin.com/in/christianaziba)

- **[Abdulmajeed Isa](mailto:abdulmajeed.isa@gmail.com)**
  - Email: another.email@example.com
  - [LinkedIn](https://www.linkedin.com/in/abdulmajeedai)


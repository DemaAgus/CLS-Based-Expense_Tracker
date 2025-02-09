# CLS Based Expense Tracker

An application to track your expenses and income using the CLS approach, helping you manage your personal finances in a simple and organized way.

## Table of Contents

- [Description](#description)
- [Features](#features)
- [Technologies Used](#technologies-used)
- [Installation](#installation)
- [Usage](#usage)
- [Contributing](#contributing)
- [Contact](#contact)

## Description

The **CLS Based Expense Tracker** is a tool designed to help you monitor and organize your finances. With this application, you can record both expenses and income, categorize your transactions, and view statistics that provide insights into your spending habits.

> **Note:** The acronym "CLS" is used to reflect the approach adopted in organizing and presenting the data. If "CLS" has a specific meaning in your implementation, please include a brief explanation here.

## Features

- **Transaction Recording:** Quickly add and manage expenses and income.
- **Category Classification:** Organize transactions into categories for easier analysis.
- **Interactive Dashboard:** Visualize charts and statistics of your financial activities.
- **Budget Configuration:** Set limits for various categories and receive alerts when nearing those limits.
- **Data Export:** Export your data in formats like CSV for further analysis.

## Technologies Used

- **Language:** Python
- **Database:** SQLite3
- **Libraries:**
  - **Pandas:** For data manipulation and analysis.
  - **NumPy:** For numerical computations.
  - **datetime:** For handling date and time operations.

> If you use other tools or dependencies (like testing tools, CSS preprocessors, etc.), list them in this section.

## Installation

Follow these steps to install and run the project locally:

1. **Clone the repository:**
   ```bash
   git clone https://github.com/DemaAgus/CLS-Based-Expense_Tracker.git
   cd CLS-Based-Expense_Tracker
   ```
   
2. *Create a virtual environment (optional but recommended):*
   ```bash
   python -m venv env
   source env/bin/activate  # On Windows use: env\Scripts\activate
   ```
   
3. *Install dependencies:*
   ```bash
   pip install -r requirements.txt
   ```
   If a *requirements.txt* file is not provided, you can manually install the required libraries:
   ```bash
   pip install pandas numpy
   ```
   
5. *Set up the SQLite3 database:*
   The project uses SQLite3 to store transaction data. No additional configuration is required; the application will create the database file if it does not already exist.
   
6. *Run the application:*
   ```bash
   python main.py
   ```
## Usage
Once the project is running, you can:
- *Add New Transactions:* Input expenses or income through the command-line interface or GUI (if available).
- *View Transactions:* Retrieve and display your recorded transactions.
- *Generate Reports:* Use built-in reporting features to analyze your spending and income trends over time.

## Contributing
Contributions are welcome! To contribute, please follow these steps:
1. Fork the repository.
2. Create a new branch for your feature or bug fix:
```bash
git checkout -b feature/your-feature-name
```
3. Make your changes and commit them:
 ```bash
git commit -m "Add: brief description of your changes"
```
4. Push your changes to your branch:
```bash
git push origin feature/your-feature-name
```
5. Open a Pull Request for your changes to be reviewed.

## Contact
For questions, suggestions, or to report issues, please contact agusdemarchi03@gmail.com or open an issue in this repository.

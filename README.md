# Py Expense Tracker 
Welcome to PyExpenseTracker, an application created with Python and Flet to manage your personal finances in a simple and effective way. With this app, you can record your income and expenses, create customized accounts, and view informative charts on the trend of your finances over time.

## Key Features
1. **Add Expenses and Incomes**: Easily record your financial transactions, specifying the amount, date, and a brief description.


2. **Account Management**: Create, modify, and delete customized accounts to organize your finances according to your needs.


3. **Informative Charts**: View clear and intuitive charts on the trend of your finances. The charts include:
  - Expenses in the selected period
  - Asset trend over time
  - Difference between income and expenses throughout the year  
  
   
4. **Integration with Matplotlib and Pandas**: Use powerful Python libraries, Matplotlib for chart creation, and Pandas for handling data in .csv format.

## Prerequisites
- Python 3.x installed on your system.
- Install the necessary dependencies by running the command:
  ```bash
   pip install -r requirements.txt 

## Getting Started
1. Clone the repository on your system.
   ```
   git clone https://github.com/Alegau03/PyExpenseTracker.git
2. Navigate to the application directory.
   ```
   cd pyexpensetracker
3. Start the Flet application
   ```
   flet app.py
## Project Structure
- app.py: The main file containing the Flask application startup code.
- /images/: Folder in which the charts are contained
- /assets/: Folder in which are .csv files of expenses, income, accounts, and asset performance

## Testing on Android
To test the app on android since it is still in beta follow these steps:
1. Install Flet app to your Android device. You will be using this app to see how your Flet project is working on Android device.
2. It's recommended to start with the creation of a new virtual environment:
     ```
   python.exe -m venv
   .venv  venv\Scripts\activate.bat```
3. Next, install the latest flet package
    ```
    pip install flet --upgrade
4. Create a new Flet project:
   ```
      flet create my-app
      cd my-app
5. Run the following command to start Flet development server with your app:
   ```
   flet run --android
A QR code with encoded project URL will be displayed in the terminal.  
Open Camera app on your Android device, point to a QR code and click URL to open it in Flet app.    

 
## Contributions
We are open to contributions and improvements. If you wish to contribute to FinanzApp, fork the repository, make your changes, and submit a pull request.

### Thank you for choosing PyExpenseTracker to manage your personal finances!

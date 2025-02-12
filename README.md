# Expense Tracker GUI

This Python project has a user interface and helps you log and visualize your expenses efficiently! Not every banking app has a tool to let you analyze your spending, so hopefully this tool can make it quicker and easier for you to keep track of your spending. 


### Features
1. You can input amount (automatically converted to currency format), category, description, and date (using a calendar picker! and today's date is automatically shown)
2. View Expense History: Displays expenses in a table format  
3. Edit & Delete Expenses: Modify or remove past entries in case you make a mistake
4. Filter Expenses: Sort expenses by category or date range
5. Data Visualization: Generates a pie chart showing expenses by category  
6. Persistent Data Storage: Uses SQLite database to store expenses

## Screenshots
<img width="700" alt="Screen Shot 2025-02-12 at 3 11 53 PM" src="https://github.com/user-attachments/assets/b73f8d6e-65f4-467e-817d-b56293e39bc6" />

GUI and list of example expenses

--

<img width="320" alt="Screen Shot 2025-02-12 at 3 12 09 PM" src="https://github.com/user-attachments/assets/45d71ae2-1c31-4be5-a645-b884fe205151" />

Calendar picker, with today's date automatically displayed

--

<img width="290" alt="Screen Shot 2025-02-12 at 3 12 17 PM" src="https://github.com/user-attachments/assets/ffbea984-8478-4c11-811d-f73d3b16683f" />

Drop-down for different spending categories

--

<img width="602" alt="Screen Shot 2025-02-12 at 3 12 42 PM" src="https://github.com/user-attachments/assets/56847350-c60e-4e91-a734-e72af754a26e" />

Pie chart generated using Matplotlib

--

### How It Was Made
This project was built using:
- **Tkinter**: For the graphical user interface  
- **SQLite3**: For storing expense records  
- **Matplotlib**: For generating expense distribution pie charts  
- **Tkcalendar**: For selecting dates easily  

---

### Future Ideas
1. Import or export tables for example a screenshot of a bank account's recent transactions
2. Trend graphs rather than just pie charts
3. Creating a mobile app or website 

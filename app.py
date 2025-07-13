import sys, csv, datetime
from pathlib import Path
import qtawesome as qta
from PyQt5.QtWidgets import *
from PyQt5.QtCore import QDate

data_path = Path("data")/"expense.csv"
income_path = Path("data") / "income.txt"

#creating csv file and file directory for saving the data
def expense(row):
    data_path.parent.mkdir(parents=True, exist_ok=True)
    file_exists = data_path.exists()
    with data_path.open("a", newline='') as f:
        writer = csv.writer(f)
        if not file_exists:
            writer.writerow(["Date", "Amount","Category", "Description"])
        writer.writerow(row)

def loading_csv_table(table, path):
    if not Path(data_path).exists():
        return
    with open(path, newline='') as f:
        reader = csv.reader(f)
        data = list(reader)
    if data:
        headers = data[0]
        table.setColumnCount(len(headers))
        table.setHorizontalHeaderLabels(headers)
        table.setRowCount(len(data) - 1)

        for row_index, row_data in enumerate(reversed(data[1:])):
            for col_index, cell in enumerate(row_data):
                table.setItem(row_index, col_index, QTableWidgetItem(cell))

class ExpenseTracker(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Expense Tracker")
        self.setMinimumSize(700,500)
        self.layout = QVBoxLayout()
        icon = qta.icon('fa5s.smile', color='orange')
        
        self.head = QLabel("Expense Tracker")
        self.head.setObjectName("Heading")
        self.submit_btn = QPushButton(icon, 'Submit')

        self.income_input = QLineEdit()
        self.income_input.setPlaceholderText("Enter monthly income (GHS)")
        self.income_input.setObjectName("IncomeInput")
        self.income_input.editingFinished.connect(self.save_income)

        self.summary_bar = QLabel()
        self.summary_bar.setObjectName("SummaryBar")

        #data_layout
        data_layout = QFormLayout()
        self.amount_input = QLineEdit()
        self.category = QComboBox()
        self.category.addItems([
            "Food", "Transport","Utilities",
            "Entertainment", "Health", "Other" 
        ])
        self.description = QLineEdit()
        self.date =QDateEdit()
        self.date.setDate(QDate.currentDate())

        self.submit_btn.clicked.connect(self.handle_submit)


        data_widget = QWidget()
        data_widget.setObjectName("data")
        data_widget.setLayout(data_layout)

        #Adding rows
        data_layout.addRow("Amount:",self.amount_input)
        data_layout.addRow("Category:",self.category)
        data_layout.addRow("Description", self.description)
        data_layout.addRow("Date", self.date)

        #Expense table
        self.table = QTableWidget()
        loading_csv_table(self.table, data_path)
        
        #Adding layout
        self.layout.addWidget(self.head)
        self.layout.addWidget(self.income_input)
        self.layout.addWidget(self.summary_bar)
        self.layout.addWidget(data_widget) 
        self.layout.addWidget(self.submit_btn)
        self.layout.addWidget(self.table)

        widget = QWidget()
        widget.setLayout(self.layout)
        self.setCentralWidget(widget)

        self.load_income()
        

    def handle_submit(self):
        amount = self.amount_input.text()
        category = self.category.currentText()
        description = self.description.text()
        date = self.date.date().toString("yyyy-MM-dd")

        if amount and category and description:
            expense([date, amount, category, description])
            loading_csv_table(self.table, data_path)  # refresh table
            self.amount_input.clear()
            #self.category.setCurrentIndex(0)
            self.description.clear()
            self.update_summary_bar()
        else:
            QMessageBox.warning(self, "Missing Info", "Please fill in all fields.")

    def load_income(self):
        try:
            with income_path.open("r") as f:
                self.income_input.setText(f.read())
        except FileNotFoundError:
            self.income_input.setText("")

    def save_income(self):
        income_path.parent.mkdir(parents=True, exist_ok=True)
        with income_path.open("w") as f:
            f.write(self.income_input.text())
        self.update_summary_bar()


    def update_summary_bar(self):
        income = self.get_monthly_income()
        expenses = 0.0
        current_month = QDate.currentDate().toString("yyyy-MM")

        if data_path.exists():
            with data_path.open(newline='') as f:
                reader = csv.reader(f)
                next(reader)
                for row in reader:
                    try:
                        date_str, amount, _, _ = row
                        date = datetime.datetime.strptime(date_str, "%Y-%m-%d")
                        if date.strftime("%Y-%m") == current_month:
                            expenses += float(amount)
                    except:
                        continue

        balance = income - expenses
        self.summary_bar.setText(f"💰 Income: GHS {income:.2f}💸 Expenses: GHS {expenses:.2f} 🧮 Balance: GHS {balance:.2f}")
    
    def get_monthly_income(self):
        try:
            return float(self.income_input.text())
        except ValueError:
            return 0.0


app = QApplication(sys.argv)

#Loading style sheet
with open("style.qss", "r") as f:
    style = f.read()
    app.setStyleSheet(style)

window = ExpenseTracker()
window.show()
app.exec()
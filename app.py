import sys, csv, datetime
from pathlib import Path
import qtawesome as qta
from PyQt5.QtWidgets import *
from PyQt5.QtCore import QDate

data_path = Path("data")/"expense.csv"
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

        for row_index, row_data in enumerate(data[1:]):
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

        #data_layout
        data_layout = QFormLayout()
        self.amount_input = QLineEdit()
        self.category = QComboBox()
        self.category.addItems([
            "Food",
            "Transport",
            "Utilities",
            "Entertainment",
            "Health",
            "Other" 
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
        self.layout.addWidget(data_widget) 
        self.layout.addWidget(self.submit_btn)
        self.layout.addWidget(self.table)

        widget = QWidget()
        widget.setLayout(self.layout)
        self.setCentralWidget(widget)

    def handle_submit(self):
        amount = self.amount_input.text()
        category = self.category.currentText()
        description = self.description.text()
        date = self.date.date().toString("yyyy-MM-dd")

        if amount and category and description:
            expense([date, amount, category, description])
            loading_csv_table(self.table, data_path)  # refresh table
            self.amount_input.clear()
            self.category.clear()
            self.description.clear()
        else:
            QMessageBox.warning(self, "Missing Info", "Please fill in all fields.")


app = QApplication(sys.argv)
#Loading style sheet
with open("style.qss", "r") as f:
    style = f.read()
    app.setStyleSheet(style)

window = ExpenseTracker()
window.show()
app.exec()
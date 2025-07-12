import sys, csv, datetime, os
import qtawesome as qta
from PyQt5.QtWidgets import *
from PyQt5.QtCore import QDate

data_path = "data/expenses.csv"
#creating csv file and file directory for saving the data

class ExpenseTracker(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Expense Tracker")
        self.layout = QVBoxLayout()
        icon = qta.icon('fa5s.smile', color='orange')
        
        self.head = QLabel("Expense Tracker")
        self.head.setObjectName("Heading")
        self.text_input = QTextEdit()
        self.submit_btn = QPushButton(icon, 'Submit')

        #data_layout
        data_layout = QFormLayout()
        self.amount_input = QLineEdit()
        self.category = QLineEdit()
        self.date =QDateEdit()
        self.date.setDate(QDate.currentDate())

        data_widget = QWidget()
        data_widget.setObjectName("data")
        data_widget.setLayout(data_layout)

        #Adding rows
        data_layout.addRow("Amount:",self.amount_input)
        data_layout.addRow("Category:",self.category)
        data_layout.addRow("Date", self.date)

        #Adding layout
        self.layout.addWidget(self.head)
        self.layout.addWidget(self.text_input)
        self.layout.addWidget(data_widget) 
        self.layout.addWidget(self.submit_btn)
        
        widget = QWidget()
        widget.setLayout(self.layout)
        self.setCentralWidget(widget)


app = QApplication(sys.argv)
#Loading style sheet
with open("style.qss", "r") as f:
    style = f.read()
    app.setStyleSheet(style)

window = ExpenseTracker()
window.show()
app.exec()
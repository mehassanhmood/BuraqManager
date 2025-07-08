import sys
from PyQt6.QtWidgets import QApplication, QMainWindow, QPushButton, QVBoxLayout, QLabel, QWidget, QLineEdit, QTableWidget, QTableWidgetItem, QComboBox, QHBoxLayout, QListWidget, QSplitter, QInputDialog
from PyQt6.QtCore import Qt
from backend import Priority, get_tasks, create_task, get_task, update_task, delete_task, create_subtask, update_subtask, delete_subtask, get_db, Task, Subtask

class BuraqManagerWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("BuraqManager")
        self.setGeometry(100, 100, 1000, 600)  # Increased width for sidebar

        # Central widget with splitter for sidebar and main content
        central_widget = QWidget()
        self.setCentralWidget(central_widget)
        main_layout = QHBoxLayout(central_widget)

        # Sidebar
        self.sidebar = QListWidget()
        self.sidebar.addItem("All")  # Default option to show all tasks
        self.sidebar.currentItemChanged.connect(self.filter_tasks)
        self.sidebar.setMaximumWidth(200)

        # Main content area
        self.main_widget = QWidget()
        self.main_layout = QVBoxLayout(self.main_widget)

        # Splitter to separate sidebar and main content
        splitter = QSplitter(Qt.Orientation.Horizontal)
        splitter.addWidget(self.sidebar)
        splitter.addWidget(self.main_widget)
        splitter.setStretchFactor(1, 1)  # Main content takes more space
        main_layout.addWidget(splitter)

        # Task Input Section
        input_layout = QHBoxLayout()
        self.category_input = QLineEdit(self)
        self.category_input.setPlaceholderText("Category")
        input_layout.addWidget(self.category_input)

        self.task_name_input = QLineEdit(self)
        self.task_name_input.setPlaceholderText("Task Name")
        input_layout.addWidget(self.task_name_input)

        self.task_detail_input = QLineEdit(self)
        self.task_detail_input.setPlaceholderText("Task Detail (optional)")
        input_layout.addWidget(self.task_detail_input)

        self.priority_combo = QComboBox(self)
        self.priority_combo.addItems([p.value for p in Priority])
        self.priority_combo.setCurrentIndex(-1)
        input_layout.addWidget(self.priority_combo)

        self.assignee_input = QLineEdit(self)
        self.assignee_input.setPlaceholderText("Assignee (optional)")
        input_layout.addWidget(self.assignee_input)

        add_task_button = QPushButton("Add Task")
        add_task_button.clicked.connect(self.add_task)
        input_layout.addWidget(add_task_button)
        self.main_layout.addLayout(input_layout)

        # Subtask Input Section
        subtask_layout = QHBoxLayout()
        self.subtask_name_input = QLineEdit(self)
        self.subtask_name_input.setPlaceholderText("Subtask Name")
        subtask_layout.addWidget(self.subtask_name_input)

        self.subtask_detail_input = QLineEdit(self)
        self.subtask_detail_input.setPlaceholderText("Subtask Detail (optional)")
        subtask_layout.addWidget(self.subtask_detail_input)

        self.task_id_input = QLineEdit(self)
        self.task_id_input.setPlaceholderText("Task ID")
        subtask_layout.addWidget(self.task_id_input)

        add_subtask_button = QPushButton("Add Subtask")
        add_subtask_button.clicked.connect(self.add_subtask)
        subtask_layout.addWidget(add_subtask_button)
        self.main_layout.addLayout(subtask_layout)

        # Task Table
        self.task_table = QTableWidget()
        self.task_table.setColumnCount(7)
        self.task_table.setHorizontalHeaderLabels(["ID", "Category", "Name", "Detail", "Priority", "Assignee", "Actions"])
        self.task_table.horizontalHeader().setStretchLastSection(True)
        self.main_layout.addWidget(self.task_table)

        # Subtask Table
        self.subtask_table = QTableWidget()
        self.subtask_table.setColumnCount(6)
        self.subtask_table.setHorizontalHeaderLabels(["ID", "Task ID", "Name", "Detail", "Completed", "Actions"])
        self.subtask_table.horizontalHeader().setStretchLastSection(True)
        self.main_layout.addWidget(self.subtask_table)

        # Load initial data and populate sidebar
        self.load_categories()
        self.load_data()

    def load_categories(self):
        with next(get_db()) as db:
            categories = db.query(Task.category).distinct().all()
            current_items = [self.sidebar.item(i).text() for i in range(self.sidebar.count())]
            for category, in categories:  # Unpack tuple
                if category and category not in current_items:
                    self.sidebar.addItem(category)

    def filter_tasks(self, current, previous):
        self.load_data(current.text() if current else "All")

    def load_data(self, category_filter="All"):
        with next(get_db()) as db:
            # Load tasks based on category filter
            if category_filter == "All":
                tasks = get_tasks(db)
            else:
                tasks = db.query(Task).filter(Task.category == category_filter).all()
            self.task_table.setRowCount(len(tasks))
            for row, task in enumerate(tasks):
                self.task_table.setItem(row, 0, QTableWidgetItem(str(task.id)))
                self.task_table.setItem(row, 1, QTableWidgetItem(task.category))
                self.task_table.setItem(row, 2, QTableWidgetItem(task.taskName))
                self.task_table.setItem(row, 3, QTableWidgetItem(task.taskDetail or ""))
                self.task_table.setItem(row, 4, QTableWidgetItem(task.priority or ""))
                self.task_table.setItem(row, 5, QTableWidgetItem(task.assignee or ""))

                edit_button = QPushButton("Edit")
                edit_button.clicked.connect(lambda checked, tid=task.id: self.edit_task(tid))
                self.task_table.setCellWidget(row, 6, edit_button)

                delete_button = QPushButton("Delete")
                delete_button.clicked.connect(lambda checked, tid=task.id: self.delete_task(tid))
                self.task_table.setCellWidget(row, 7, delete_button)

            # Load all subtasks (filtered by task ID implicitly)
            subtasks = db.query(Subtask).all()
            self.subtask_table.setRowCount(len(subtasks))
            for row, subtask in enumerate(subtasks):
                self.subtask_table.setItem(row, 0, QTableWidgetItem(str(subtask.id)))
                self.subtask_table.setItem(row, 1, QTableWidgetItem(str(subtask.taskId)))
                self.subtask_table.setItem(row, 2, QTableWidgetItem(subtask.name))
                self.subtask_table.setItem(row, 3, QTableWidgetItem(subtask.detail or ""))
                self.subtask_table.setItem(row, 4, QTableWidgetItem(str(subtask.completed)))

                edit_button = QPushButton("Edit")
                edit_button.clicked.connect(lambda checked, sid=subtask.id: self.edit_subtask(sid))
                self.subtask_table.setCellWidget(row, 5, edit_button)

                delete_button = QPushButton("Delete")
                delete_button.clicked.connect(lambda checked, sid=subtask.id: self.delete_subtask(sid))
                self.subtask_table.setCellWidget(row, 6, delete_button)

    def add_task(self):
        with next(get_db()) as db:
            category = self.category_input.text()
            priority = Priority(self.priority_combo.currentText()) if self.priority_combo.currentText() else None
            task = create_task(db, category, self.task_name_input.text(),
                             self.task_detail_input.text(), priority, self.assignee_input.text())
            if task:
                self.load_categories()  # Update sidebar with new category
                self.load_data(category)  # Load tasks for the new category
                self.clear_inputs()

    def edit_task(self, task_id):
        with next(get_db()) as db:
            task = get_task(db, task_id)
            if task:
                text, ok = QInputDialog.getText(self, "Edit Task", "Enter new task name:", QLineEdit.EchoMode.Normal, task.taskName)
                if ok and text:
                    update_task(db, task_id, task_name=text)
                    self.load_data(self.sidebar.currentItem().text() if self.sidebar.currentItem() else "All")

    def delete_task(self, task_id):
        with next(get_db()) as db:
            if delete_task(db, task_id):
                self.load_data(self.sidebar.currentItem().text() if self.sidebar.currentItem() else "All")

    def add_subtask(self):
        with next(get_db()) as db:
            task_id = int(self.task_id_input.text()) if self.task_id_input.text().isdigit() else None
            if task_id:
                subtask = create_subtask(db, task_id, self.subtask_name_input.text(), self.subtask_detail_input.text())
                if subtask:
                    self.load_data(self.sidebar.currentItem().text() if self.sidebar.currentItem() else "All")
                    self.clear_inputs()

    def edit_subtask(self, subtask_id):
        with next(get_db()) as db:
            subtask = db.query(Subtask).filter(Subtask.id == subtask_id).first()
            if subtask:
                text, ok = QInputDialog.getText(self, "Edit Subtask", "Enter new subtask name:", QLineEdit.EchoMode.Normal, subtask.name)
                if ok and text:
                    update_subtask(db, subtask_id, name=text)
                    self.load_data(self.sidebar.currentItem().text() if self.sidebar.currentItem() else "All")

    def delete_subtask(self, subtask_id):
        with next(get_db()) as db:
            if delete_subtask(db, subtask_id):
                self.load_data(self.sidebar.currentItem().text() if self.sidebar.currentItem() else "All")

    def clear_inputs(self):
        self.category_input.clear()
        self.task_name_input.clear()
        self.task_detail_input.clear()
        self.priority_combo.setCurrentIndex(-1)
        self.assignee_input.clear()
        self.subtask_name_input.clear()
        self.subtask_detail_input.clear()
        self.task_id_input.clear()

if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = BuraqManagerWindow()
    window.show()
    sys.exit(app.exec())
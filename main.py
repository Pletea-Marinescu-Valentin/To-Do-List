import sys
from pathlib import Path

from PySide6.QtGui import QGuiApplication
from PySide6.QtQml import QQmlApplicationEngine
from PySide6.QtCore import QObject, Qt, QAbstractListModel, QModelIndex, Slot, Property, Signal
from PySide6.QtWidgets import QMessageBox, QLineEdit, QInputDialog

class TodoListModel(QAbstractListModel):
    def __init__(self, parent=None):
        super().__init__(parent)
        self._tasks = []
        self.loadData()

    def rowCount(self, parent=QModelIndex()):
        return len(self._tasks)

    def data(self, index, role=Qt.DisplayRole):
        if role == Qt.DisplayRole:
            return self._tasks[index.row()]

    @Slot(str)
    def addTask(self, task):
        self.beginInsertRows(QModelIndex(), self.rowCount(), self.rowCount())
        self._tasks.append(task)
        self.endInsertRows()

    @Slot(int, str)
    def editTask(self, index, task_text):
        self._tasks[index] = task_text
        self.dataChanged.emit(self.index(index), self.index(index))

    @Slot(int)
    def removeTask(self, index):
        # Remove the task at the specified index
        self.beginRemoveRows(QModelIndex(), index, index)
        del self._tasks[index]
        self.endRemoveRows()

    @Slot(int, str)
    def applyTaskModification(self, index, new_task_text):
        self._tasks[index] = new_task_text
        self.dataChanged.emit(self.index(index), self.index(index))

    def loadData(self):
        self._tasks.clear()
        try:
            with open("data.txt", "r") as file:
                for line in file:
                    task = line.strip()
                    if task:
                        self._tasks.append(task)
        except FileNotFoundError:
            pass


    def saveData(self):
        with open("data.txt", "w") as file:
            for task in self._tasks:
                file.write(task + "\n")



class EditDialogHandler(QObject):
    def __init__(self, todoListModel):
        super().__init__()
        self.todoListModel = todoListModel

    @Slot(str)
    def handleTaskEdited(self, newTaskText):
        # Get the index of the task being edited
        index = self.todoListModel.rowCount() - 1
        # Edit the task
        self.todoListModel.editTask(index, newTaskText)

if __name__ == "__main__":
    app = QGuiApplication(sys.argv)
    engine = QQmlApplicationEngine()

    todoListModel = TodoListModel()
    todoListModel.loadData()
    engine.rootContext().setContextProperty("todoListModel", todoListModel)

    editDialogHandler = EditDialogHandler(todoListModel)
    engine.rootContext().setContextProperty("editDialogHandler", editDialogHandler)

    app.aboutToQuit.connect(todoListModel.saveData)

    qml_file = Path(__file__).resolve().parent / "main.qml"
    engine.load(qml_file)

    if not engine.rootObjects():
        sys.exit(-1)

    sys.exit(app.exec())

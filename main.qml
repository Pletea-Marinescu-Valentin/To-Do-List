import QtQuick
import QtQuick.Controls
import QtQuick.Dialogs

ApplicationWindow {
    visible: true
    width: 640
    height: 480
    title: qsTr("To Do List")

    property int taskIndex: -1;

    Column {
        id: mainColumn
        anchors.centerIn: parent
        spacing: 10

        TextField {
            id: taskInput
            placeholderText: "Enter a task"
            width: 200
            height: 30
            font.pixelSize: 16
            background: Rectangle {
                color: "#f0f0f0"
                radius: 5
            }
        }

        Button {
            text: "Add"
            width: 80
            height: 30
            font.pixelSize: 16
            onClicked: {
                if (taskInput.text !== "") {
                    todoListModel.addTask(taskInput.text)
                    taskInput.text = ""
                }
            }
            background: Rectangle {
                color: "#4CAF50"
                radius: 5
            }
            contentItem: Text {
                text: parent.text
                font.pixelSize: 16
                color: "white"
                verticalAlignment: Text.AlignVCenter
                horizontalAlignment: Text.AlignHCenter
                anchors.centerIn: parent
            }
        }

        ListView {
            id: taskListView
            width: 300
            height: 300
            clip: true
            model: todoListModel

            delegate: Row {
                spacing: 5
                Text {
                    id: taskText
                    text: model.display
                    color: "black"
                    font.pixelSize: 16
                    padding: 5
                    wrapMode: Text.WordWrap
                }
                CheckBox {
                    checked: model.checked
                    onClicked: {
                        todoListModel.toggleTaskStatus(index)
                    }
                }
                Button {
                    text: "Edit"
                    onClicked: {
                        todoListModel.editTask(index, model.display);
                        taskIndex = index;
                        editDialog.open();
                    }
                }
                Button {
                    text: "Delete"
                    onClicked: {
                        todoListModel.removeTask(index)
                    }
                }
            }
        }
    }

    // Define the dialog for editing tasks
    Dialog {
        id: editDialog
        width: 300
        height: 200
        title: "Edit Task"
        TextField {
            id: editTaskTextField
            anchors.centerIn: parent
        }
        Row {
            anchors {
                horizontalCenter: parent.horizontalCenter
                bottom: parent.bottom
            }
            spacing: 10
            Button {
                text: "Apply"
                onClicked: {
                    if (editTaskTextField.text.trim() !== "") {
                        todoListModel.applyTaskModification(taskIndex, editTaskTextField.text.trim())
                        editDialog.close()
                    }
                }
            }
            Button {
                text: "Cancel"
                onClicked: {
                    editDialog.close()
                }
            }
        }
    }

}

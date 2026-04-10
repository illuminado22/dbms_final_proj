from PyQt6.QtWidgets import (QWidget, QHBoxLayout, QPushButton, QTableWidget,
                             QTableWidgetItem, QHeaderView, QMessageBox)

def make_table(headers, stretch_cols=None):
    t = QTableWidget()
    t.setColumnCount(len(headers))
    t.setHorizontalHeaderLabels(headers)
    t.setEditTriggers(QTableWidget.EditTrigger.NoEditTriggers)
    t.verticalHeader().setVisible(False)
    if stretch_cols:
        for c in stretch_cols:
            t.horizontalHeader().setSectionResizeMode(c, QHeaderView.ResizeMode.Stretch)
    return t

def fill_table(table, rows, action_col, on_edit, on_del):
    table.setRowCount(len(rows))
    for i, row in enumerate(rows):
        for j, v in enumerate(row):
            table.setItem(i, j, QTableWidgetItem(str(v) if v else ""))
        fw = QWidget(); fh = QHBoxLayout(fw); fh.setContentsMargins(4,2,4,2)
        eb = QPushButton("Edit"); eb.setObjectName("secondary"); eb.setFixedWidth(50)
        db = QPushButton("Del");  db.setObjectName("danger");    db.setFixedWidth(50)
        rid = row[0]
        eb.clicked.connect(lambda _, id=rid: on_edit(id))
        db.clicked.connect(lambda _, id=rid: on_del(id))
        fh.addWidget(eb); fh.addWidget(db)
        table.setCellWidget(i, action_col, fw)
    table.resizeRowsToContents()

def confirm_delete(parent, msg="Delete this record?"):
    return QMessageBox.question(parent, "Confirm Delete", msg,
        QMessageBox.StandardButton.Yes | QMessageBox.StandardButton.No) == QMessageBox.StandardButton.Yes

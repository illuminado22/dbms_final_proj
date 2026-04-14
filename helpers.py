from PyQt6.QtWidgets import (QWidget, QHBoxLayout, QPushButton, QTableWidget,
                             QTableWidgetItem, QHeaderView, QMessageBox)
from PyQt6.QtCore import Qt

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
        fw = QWidget(); fh = QHBoxLayout(fw)
        fh.setContentsMargins(0, 0, 0, 0)
        fh.setSpacing(6)
        fh.setAlignment(Qt.AlignmentFlag.AlignLeft)
        eb = QPushButton("Edit"); eb.setObjectName("secondary"); eb.setFixedWidth(80)
        db = QPushButton("Delete");  db.setObjectName("danger");    db.setFixedWidth(80)
        rid = row[0]
        eb.clicked.connect(lambda _, id=rid: on_edit(id))
        db.clicked.connect(lambda _, id=rid: on_del(id))
        fh.addWidget(eb); fh.addWidget(db)
        table.setCellWidget(i, action_col, fw)
    table.resizeRowsToContents()
    table.horizontalHeader().setSectionResizeMode(action_col, QHeaderView.ResizeMode.ResizeToContents)

def reset_auto_increment(table, pk_column, get_conn):
    try:
        conn = get_conn(); cur = conn.cursor()
        cur.execute(f"SELECT COALESCE(MAX({pk_column}), 0) + 1 FROM {table}")
        next_id = cur.fetchone()[0]
        cur.execute(f"ALTER TABLE {table} AUTO_INCREMENT = %s", (next_id,))
        conn.commit(); conn.close()
    except Exception:
        try:
            conn.close()
        except Exception:
            pass


def confirm_delete(parent, msg="Delete this record?"):
    return QMessageBox.question(parent, "Confirm Delete", msg,
        QMessageBox.StandardButton.Yes | QMessageBox.StandardButton.No) == QMessageBox.StandardButton.Yes

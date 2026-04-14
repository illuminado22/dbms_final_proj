from PyQt6.QtWidgets import (QWidget, QVBoxLayout, QHBoxLayout, QLabel, QPushButton,
                             QDialog, QFormLayout, QLineEdit, QDialogButtonBox, QMessageBox, QListWidget, QListWidgetItem)
from PyQt6.QtCore import Qt
from config import get_conn
from helpers import make_table, fill_table, confirm_delete, reset_auto_increment

class TeamsPage(QWidget):
    def __init__(self):
        super().__init__()
        layout = QVBoxLayout(self); layout.setContentsMargins(24,24,24,24)
        h = QHBoxLayout()
        t = QLabel("Teams"); t.setObjectName("title")
        h.addWidget(t); h.addStretch()
        btn = QPushButton("+ Add Team"); btn.clicked.connect(lambda: self._open(None))
        h.addWidget(btn); layout.addLayout(h); layout.addSpacing(10)
        self.table = make_table(["ID","Team Name","Members","Actions"], stretch_cols=[1,2])
        layout.addWidget(self.table)

    def _load(self):
        try:
            conn = get_conn(); cur = conn.cursor()
            cur.execute("""
                SELECT t.team_id, t.team_name,
                    IFNULL(GROUP_CONCAT(s.student_name ORDER BY s.student_name SEPARATOR ', '), '') AS members
                FROM team t
                LEFT JOIN team_member tm ON t.team_id = tm.team_id
                LEFT JOIN students s ON tm.student_id = s.student_id
                GROUP BY t.team_id, t.team_name
                ORDER BY t.team_id DESC
            """)
            rows = cur.fetchall(); conn.close()
            fill_table(self.table, rows, 3, self._open, self._delete)
        except Exception as e: QMessageBox.critical(self,"DB Error",str(e))

    def _open(self, tid):
        if TeamDialog(self, tid).exec(): self._load()

    def _delete(self, tid):
        if confirm_delete(self, "Delete this team?"):
            try:
                conn = get_conn(); cur = conn.cursor()
                cur.execute("DELETE FROM team_member WHERE team_id=%s",(tid,))
                cur.execute("DELETE FROM team WHERE team_id=%s",(tid,))
                conn.commit(); conn.close()
                reset_auto_increment('team', 'team_id', get_conn)
                self._load()
            except Exception as e: QMessageBox.critical(self,"Error",str(e))

class TeamDialog(QDialog):
    def __init__(self, parent, tid=None):
        super().__init__(parent); self.tid = tid
        self.setWindowTitle("Edit Team" if tid else "Add Team"); self.setMinimumWidth(400)
        f = QFormLayout(self); f.setSpacing(12)
        self.name = QLineEdit()
        f.addRow("Team Name *", self.name)
        self.students_list = QListWidget()
        self.students_list.setMaximumHeight(220)
        self.students_list.setSelectionMode(QListWidget.SelectionMode.SingleSelection)
        f.addRow("Members", self.students_list)
        btns = QDialogButtonBox(QDialogButtonBox.StandardButton.Ok | QDialogButtonBox.StandardButton.Cancel)
        btns.accepted.connect(self._save); btns.rejected.connect(self.reject); f.addRow(btns)
        self._load_students()
        if tid: self._load()

    def _load_students(self):
        try:
            conn = get_conn(); cur = conn.cursor()
            if self.tid:
                cur.execute(
                    """
                    SELECT s.student_id, s.student_name
                    FROM students s
                    LEFT JOIN team_member tm ON s.student_id = tm.student_id
                    WHERE tm.team_id IS NULL OR tm.team_id = %s
                    ORDER BY s.student_name
                    """,
                    (self.tid,)
                )
            else:
                cur.execute(
                    "SELECT s.student_id, s.student_name FROM students s"
                    " LEFT JOIN team_member tm ON s.student_id = tm.student_id"
                    " WHERE tm.team_id IS NULL"
                    " ORDER BY s.student_name"
                )
            students = cur.fetchall(); conn.close()
            self.students_list.clear()
            if not students:
                placeholder = QListWidgetItem("No available students")
                placeholder.setFlags(Qt.ItemFlag.NoItemFlags)
                placeholder.setForeground(Qt.GlobalColor.darkGray)
                self.students_list.addItem(placeholder)
                return
            for sid, name in students:
                item = QListWidgetItem(name)
                item.setData(Qt.ItemDataRole.UserRole, sid)
                item.setFlags(
                    item.flags()
                    | Qt.ItemFlag.ItemIsUserCheckable
                    | Qt.ItemFlag.ItemIsEnabled
                    | Qt.ItemFlag.ItemIsSelectable
                )
                item.setCheckState(Qt.CheckState.Unchecked)
                self.students_list.addItem(item)
        except Exception as e: QMessageBox.critical(self,"Error",str(e))

    def _load(self):
        try:
            conn = get_conn(); cur = conn.cursor()
            cur.execute("SELECT team_name FROM team WHERE team_id=%s",(self.tid,))
            r = cur.fetchone()
            if r: self.name.setText(r[0])
            # Load current members
            cur.execute("SELECT student_id FROM team_member WHERE team_id=%s",(self.tid,))
            members = {row[0] for row in cur.fetchall()}; conn.close()
            for i in range(self.students_list.count()):
                item = self.students_list.item(i)
                sid = item.data(Qt.ItemDataRole.UserRole)
                if sid in members:
                    item.setCheckState(Qt.CheckState.Checked)
        except Exception as e: QMessageBox.critical(self,"Error",str(e))

    def _save(self):
        n = self.name.text().strip()
        if not n: QMessageBox.warning(self,"Required","Team name required."); return
        try:
            conn = get_conn(); cur = conn.cursor()
            if self.tid:
                cur.execute("UPDATE team SET team_name=%s WHERE team_id=%s",(n,self.tid))
                tid = self.tid
            else:
                cur.execute("INSERT INTO team (team_name) VALUES (%s)",(n,))
                tid = cur.lastrowid
            # Now, update members
            cur.execute("DELETE FROM team_member WHERE team_id=%s",(tid,))
            selected_students = []
            for i in range(self.students_list.count()):
                item = self.students_list.item(i)
                if item.checkState() == Qt.CheckState.Checked:
                    sid = item.data(Qt.ItemDataRole.UserRole)
                    selected_students.append((tid, sid))
            if selected_students:
                cur.executemany("INSERT INTO team_member (team_id, student_id) VALUES (%s, %s)", selected_students)
            conn.commit(); conn.close(); self.accept()
        except Exception as e: QMessageBox.critical(self,"Error",str(e))

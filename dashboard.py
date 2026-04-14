from PyQt6.QtWidgets import QWidget, QVBoxLayout, QHBoxLayout, QLabel, QFrame, QTableWidget, QTableWidgetItem, QHeaderView
from PyQt6.QtCore import Qt
from config import get_conn

class DashboardPage(QWidget):
    def __init__(self):
        super().__init__()
        layout = QVBoxLayout(self); layout.setContentsMargins(24, 24, 24, 24)

        title = QLabel("Dashboard"); title.setObjectName("title")
        layout.addWidget(title); layout.addSpacing(16)

        # Stat cards
        row = QHBoxLayout()
        self.stats = {}
        for key, label in [("projects","Projects"),("students","Students"),("advisers","Advisers"),("teams","Teams")]:
            card = QFrame(); card.setObjectName("card")
            cv = QVBoxLayout(card); cv.setContentsMargins(20,14,20,14)
            num = QLabel("–"); num.setStyleSheet("font-size:30px; font-weight:bold; color:#1a3c5e;")
            lbl = QLabel(label); lbl.setStyleSheet("color:#888;")
            cv.addWidget(num); cv.addWidget(lbl)
            self.stats[key] = num; row.addWidget(card)
        layout.addLayout(row); layout.addSpacing(20)

        layout.addWidget(QLabel("Recent Projects") )
        self.table = QTableWidget(); self.table.setColumnCount(4)
        self.table.setHorizontalHeaderLabels(["ID","Title","Year","Team"])
        self.table.horizontalHeader().setSectionResizeMode(1, QHeaderView.ResizeMode.Stretch)
        self.table.setEditTriggers(QTableWidget.EditTrigger.NoEditTriggers)
        self.table.verticalHeader().setVisible(False)
        self.table.setMaximumHeight(200)
        layout.addWidget(self.table); layout.addStretch()

    def _load(self):
        try:
            conn = get_conn(); cur = conn.cursor()
            for key, tbl in [("projects","projects"),("students","students"),("advisers","advisers"),("teams","team")]:
                cur.execute(f"SELECT COUNT(*) FROM {tbl}")
                self.stats[key].setText(str(cur.fetchone()[0]))
            cur.execute("""SELECT p.project_id, p.title, p.year_completed, t.team_name
                           FROM projects p LEFT JOIN team t ON p.team_id=t.team_id
                           ORDER BY p.project_id DESC LIMIT 5""")
            rows = cur.fetchall(); conn.close()
            self.table.setRowCount(len(rows))
            for i, row in enumerate(rows):
                for j, v in enumerate(row):
                    self.table.setItem(i, j, QTableWidgetItem(str(v) if v else ""))
        except: pass

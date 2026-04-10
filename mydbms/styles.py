COLORS = {
    "bg_1": "#f5f7ef",
    "bg_2": "#e5ebdb",
    "ink_900": "#1f2b2a",
    "ink_700": "#334445",
    "ink_500": "#5a6a69",
    "paper": "#fcfcf8",
    "border": "#cfd7ca",
    "accent": "#0f5d53",
    "accent_strong": "#084840",
    "warn": "#8c2f2f",
    "focus": "#edb458",
}


MAIN_STYLESHEET = f"""
QMainWindow {{
    background-color: {COLORS['bg_1']};
}}

QWidget#mainContainer {{
    background: qlineargradient(
        x1:0, y1:0, x2:1, y2:1,
        stop:0 {COLORS['bg_1']},
        stop:1 {COLORS['bg_2']}
    );
}}

QWidget#introPanel {{
    background: transparent;
    color: {COLORS['ink_900']};
}}

QLabel#titleLabel {{
    font-family: 'Source Serif 4', Georgia, serif;
    font-size: 32px;
    font-weight: bold;
    color: {COLORS['ink_900']};
    margin: 0px;
    padding: 0px;
}}

QLabel#pointsLabel {{
    color: {COLORS['ink_700']};
    font-size: 13px;
    line-height: 1.85;
}}

QWidget#authCard {{
    background-color: {COLORS['paper']};
    border: 1px solid {COLORS['border']};
    border-radius: 18px;
}}

QLabel#authTitle {{
    font-family: 'Source Serif 4', Georgia, serif;
    font-size: 24px;
    font-weight: bold;
    color: {COLORS['ink_900']};
}}

QLabel#authSubtitle {{
    color: {COLORS['ink_500']};
    font-size: 12px;
}}

QLabel#fieldLabel {{
    font-size: 12px;
    font-weight: 600;
    color: {COLORS['ink_900']};
}}

QLineEdit {{
    border: 1px solid {COLORS['border']};
    border-radius: 10px;
    padding: 8px;
    background-color: white;
    color: {COLORS['ink_900']};
    font-size: 13px;
}}

QLineEdit:focus {{
    border: 2px solid {COLORS['focus']};
    outline: 3px solid rgba(237, 180, 88, 0.28);
}}

QComboBox {{
    border: 1px solid {COLORS['border']};
    border-radius: 10px;
    padding: 8px;
    background-color: white;
    color: {COLORS['ink_900']};
    font-size: 13px;
}}

QComboBox:focus {{
    border: 2px solid {COLORS['focus']};
}}

QComboBox::drop-down {{
    border: none;
    width: 20px;
}}

QComboBox::down-arrow {{
    image: url(none);
}}

QPushButton#primaryButton {{
    background: qlineargradient(
        x1:0, y1:0, x2:1, y2:1,
        stop:0 {COLORS['accent']},
        stop:1 {COLORS['accent_strong']}
    );
    color: white;
    border: none;
    border-radius: 10px;
    padding: 10px;
    font-weight: 700;
    font-size: 13px;
}}

QPushButton#primaryButton:hover {{
    background: qlineargradient(
        x1:0, y1:0, x2:1, y2:1,
        stop:0 {COLORS['accent']},
        stop:1 {COLORS['accent_strong']}
    );
    filter: brightness(1.03);
}}

QPushButton#primaryButton:pressed {{
    background: {COLORS['accent_strong']};
}}

QPushButton#primaryButton:disabled {{
    opacity: 0.7;
}}

QPushButton#toggleButton {{
    border: 1px solid {COLORS['border']};
    background-color: #f2f5ec;
    color: {COLORS['ink_700']};
    border-radius: 10px;
    padding: 8px 12px;
    font-weight: 600;
    font-size: 12px;
}}

QPushButton#toggleButton:hover {{
    background-color: #eaf0e3;
}}

QPushButton#linkButton {{
    border: none;
    background-color: transparent;
    color: {COLORS['accent']};
    font-weight: 700;
    text-decoration: underline;
}}

QPushButton#linkButton:hover {{
    color: {COLORS['accent_strong']};
}}

QLabel#errorLabel {{
    color: {COLORS['warn']};
    font-size: 11px;
    min-height: 15px;
}}

QLabel#switchLabel {{
    color: {COLORS['ink_700']};
    font-size: 12px;
}}
"""

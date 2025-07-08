import sys
from PyQt6.QtWidgets import *
from PyQt6.QtCore import *
from PyQt6.QtGui import *

class ModernButton(QPushButton):
    def __init__(self, text, parent=None):
        super().__init__(text, parent)
        self.setStyleSheet("""
            QPushButton {
                background: qlineargradient(x1:0, y1:0, x2:0, y2:1,
                    stop:0 #4a90e2, stop:1 #357abd);
                border: none;
                border-radius: 8px;
                color: white;
                font-weight: bold;
                font-size: 14px;
                padding: 12px 24px;
                min-width: 120px;
            }
            QPushButton:hover {
                background: qlineargradient(x1:0, y1:0, x2:0, y2:1,
                    stop:0 #5ba0f2, stop:1 #4080cd);
                transform: translateY(-2px);
            }
            QPushButton:pressed {
                background: qlineargradient(x1:0, y1:0, x2:0, y2:1,
                    stop:0 #3a80d2, stop:1 #2570ad);
            }
        """)

class StatsCard(QFrame):
    def __init__(self, title, value, icon, color, parent=None):
        super().__init__(parent)
        self.setFixedSize(200, 120)
        self.setStyleSheet(f"""
            QFrame {{
                background: qlineargradient(x1:0, y1:0, x2:1, y2:1,
                    stop:0 {color}, stop:1 {self.darken_color(color)});
                border-radius: 12px;
                border: 1px solid rgba(255, 255, 255, 0.1);
            }}
        """)
        
        layout = QVBoxLayout(self)
        layout.setSpacing(5)
        
        # Icon and title row
        top_layout = QHBoxLayout()
        icon_label = QLabel(icon)
        icon_label.setStyleSheet("font-size: 24px; color: white;")
        title_label = QLabel(title)
        title_label.setStyleSheet("color: rgba(255, 255, 255, 0.9); font-size: 12px; font-weight: bold;")
        
        top_layout.addWidget(icon_label)
        top_layout.addStretch()
        top_layout.addWidget(title_label)
        
        # Value
        value_label = QLabel(value)
        value_label.setStyleSheet("color: white; font-size: 28px; font-weight: bold;")
        value_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        
        layout.addLayout(top_layout)
        layout.addWidget(value_label)
        layout.addStretch()
    
    def darken_color(self, color):
        # Simple color darkening
        return color.replace('#', '#').replace('4a90e2', '357abd').replace('e74c3c', 'c0392b').replace('2ecc71', '27ae60').replace('f39c12', 'e67e22')

class ModernDashboard(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Modern Dashboard")
        self.setGeometry(100, 100, 1200, 800)
        
        # Set dark theme
        self.setStyleSheet("""
            QMainWindow {
                background: qlineargradient(x1:0, y1:0, x2:1, y2:1,
                    stop:0 #1a1a2e, stop:1 #16213e);
            }
            QLabel {
                color: white;
            }
            QFrame {
                color: white;
            }
        """)
        
        self.setup_ui()
    
    def setup_ui(self):
        central_widget = QWidget()
        self.setCentralWidget(central_widget)
        
        main_layout = QVBoxLayout(central_widget)
        main_layout.setSpacing(30)
        main_layout.setContentsMargins(40, 40, 40, 40)
        
        # Header
        header_layout = QHBoxLayout()
        
        title = QLabel("Dashboard")
        title.setStyleSheet("""
            font-size: 32px;
            font-weight: bold;
            color: white;
            margin-bottom: 10px;
        """)
        
        subtitle = QLabel("Welcome to your modern control center")
        subtitle.setStyleSheet("""
            font-size: 16px;
            color: rgba(255, 255, 255, 0.7);
            margin-bottom: 20px;
        """)
        
        header_text = QVBoxLayout()
        header_text.addWidget(title)
        header_text.addWidget(subtitle)
        
        header_layout.addLayout(header_text)
        header_layout.addStretch()
        
        # Add a profile section
        profile_btn = ModernButton("Profile")
        settings_btn = ModernButton("Settings")
        
        header_layout.addWidget(profile_btn)
        header_layout.addWidget(settings_btn)
        
        main_layout.addLayout(header_layout)
        
        # Stats cards
        stats_layout = QHBoxLayout()
        stats_layout.setSpacing(20)
        
        cards = [
            ("Users", "2,847", "👥", "#4a90e2"),
            ("Revenue", "$45.2K", "💰", "#2ecc71"),
            ("Orders", "1,234", "📦", "#e74c3c"),
            ("Growth", "+12.5%", "📈", "#f39c12")
        ]
        
        for title, value, icon, color in cards:
            card = StatsCard(title, value, icon, color)
            stats_layout.addWidget(card)
        
        stats_layout.addStretch()
        main_layout.addLayout(stats_layout)
        
        # Content area
        content_layout = QHBoxLayout()
        content_layout.setSpacing(30)
        
        # Left panel - Chart area
        left_panel = QFrame()
        left_panel.setStyleSheet("""
            QFrame {
                background: rgba(255, 255, 255, 0.05);
                border-radius: 16px;
                border: 1px solid rgba(255, 255, 255, 0.1);
            }
        """)
        left_panel.setMinimumSize(600, 300)
        
        left_layout = QVBoxLayout(left_panel)
        left_layout.setContentsMargins(30, 30, 30, 30)
        
        chart_title = QLabel("Analytics Overview")
        chart_title.setStyleSheet("font-size: 20px; font-weight: bold; color: white; margin-bottom: 20px;")
        left_layout.addWidget(chart_title)
        
        # Simulate chart with colored bars
        chart_area = QFrame()
        chart_area.setStyleSheet("""
            QFrame {
                background: qlineargradient(x1:0, y1:0, x2:1, y2:1,
                    stop:0 rgba(74, 144, 226, 0.3), stop:1 rgba(46, 204, 113, 0.3));
                border-radius: 8px;
                border: 1px solid rgba(255, 255, 255, 0.1);
            }
        """)
        chart_area.setMinimumHeight(200)
        
        chart_layout = QVBoxLayout(chart_area)
        chart_info = QLabel("📊 Interactive chart would go here")
        chart_info.setAlignment(Qt.AlignmentFlag.AlignCenter)
        chart_info.setStyleSheet("color: rgba(255, 255, 255, 0.8); font-size: 16px;")
        chart_layout.addWidget(chart_info)
        
        left_layout.addWidget(chart_area)
        
        # Right panel - Activity feed
        right_panel = QFrame()
        right_panel.setStyleSheet("""
            QFrame {
                background: rgba(255, 255, 255, 0.05);
                border-radius: 16px;
                border: 1px solid rgba(255, 255, 255, 0.1);
            }
        """)
        right_panel.setFixedWidth(350)
        
        right_layout = QVBoxLayout(right_panel)
        right_layout.setContentsMargins(30, 30, 30, 30)
        
        activity_title = QLabel("Recent Activity")
        activity_title.setStyleSheet("font-size: 20px; font-weight: bold; color: white; margin-bottom: 20px;")
        right_layout.addWidget(activity_title)
        
        # Activity items
        activities = [
            ("New user registered", "2 min ago", "🟢"),
            ("Payment processed", "5 min ago", "💳"),
            ("Order shipped", "15 min ago", "📦"),
            ("System backup completed", "1 hour ago", "✅"),
            ("New message received", "2 hours ago", "💬")
        ]
        
        for activity, time, icon in activities:
            activity_item = QFrame()
            activity_item.setStyleSheet("""
                QFrame {
                    background: rgba(255, 255, 255, 0.05);
                    border-radius: 8px;
                    border: 1px solid rgba(255, 255, 255, 0.05);
                    padding: 10px;
                    margin: 5px 0;
                }
            """)
            activity_item.setFixedHeight(60)
            
            item_layout = QHBoxLayout(activity_item)
            
            icon_label = QLabel(icon)
            icon_label.setStyleSheet("font-size: 18px;")
            
            text_layout = QVBoxLayout()
            activity_label = QLabel(activity)
            activity_label.setStyleSheet("color: white; font-weight: bold; font-size: 14px;")
            time_label = QLabel(time)
            time_label.setStyleSheet("color: rgba(255, 255, 255, 0.6); font-size: 12px;")
            
            text_layout.addWidget(activity_label)
            text_layout.addWidget(time_label)
            
            item_layout.addWidget(icon_label)
            item_layout.addLayout(text_layout)
            item_layout.addStretch()
            
            right_layout.addWidget(activity_item)
        
        right_layout.addStretch()
        
        content_layout.addWidget(left_panel)
        content_layout.addWidget(right_panel)
        
        main_layout.addLayout(content_layout)
        
        # Bottom action buttons
        bottom_layout = QHBoxLayout()
        bottom_layout.setSpacing(20)
        
        action_buttons = ["Export Data", "Generate Report", "Send Notification", "View Details"]
        
        for btn_text in action_buttons:
            btn = ModernButton(btn_text)
            btn.clicked.connect(lambda checked, text=btn_text: self.show_message(f"{text} clicked!"))
            bottom_layout.addWidget(btn)
        
        bottom_layout.addStretch()
        main_layout.addLayout(bottom_layout)
    
    def show_message(self, message):
        msg_box = QMessageBox()
        msg_box.setWindowTitle("Action")
        msg_box.setText(message)
        msg_box.setStyleSheet("""
            QMessageBox {
                background: #2c3e50;
                color: white;
            }
            QMessageBox QPushButton {
                background: #3498db;
                color: white;
                border: none;
                padding: 8px 16px;
                border-radius: 4px;
            }
            QMessageBox QPushButton:hover {
                background: #2980b9;
            }
        """)
        msg_box.exec()

if __name__ == "__main__":
    app = QApplication(sys.argv)
    
    # Set application style
    app.setStyle('Fusion')
    
    window = ModernDashboard()
    window.show()
    
    sys.exit(app.exec())
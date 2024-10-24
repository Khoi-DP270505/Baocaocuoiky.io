from PyQt5.QtWidgets import QWidget, QLabel, QLineEdit, QPushButton, QVBoxLayout, QMessageBox
from csv_backend import NetCafeSystem

class RegisterWindow(QWidget):
    def __init__(self):
        super().__init__()
        self.cafe = NetCafeSystem()  # Hệ thống quản lý dữ liệu
        self.init_ui()

    def init_ui(self):
        self.setWindowTitle("Đăng ký")
        self.setGeometry(100, 100, 300, 300)

        layout = QVBoxLayout()

        # Nhãn và ô nhập tên đăng nhập
        self.label_username = QLabel("Tên đăng nhập:")
        self.entry_username = QLineEdit()
        layout.addWidget(self.label_username)
        layout.addWidget(self.entry_username)

        # Nhãn và ô nhập mật khẩu
        self.label_password = QLabel("Mật khẩu:")
        self.entry_password = QLineEdit()
        self.entry_password.setEchoMode(QLineEdit.Password)
        layout.addWidget(self.label_password)
        layout.addWidget(self.entry_password)

        # Nhãn và ô nhập xác nhận mật khẩu
        self.label_confirm_password = QLabel("Xác nhận mật khẩu:")
        self.entry_confirm_password = QLineEdit()
        self.entry_confirm_password.setEchoMode(QLineEdit.Password)
        layout.addWidget(self.label_confirm_password)
        layout.addWidget(self.entry_confirm_password)

        # Nút đăng ký
        button_register = QPushButton("Xác nhận đăng ký")
        button_register.clicked.connect(self.register_user)
        layout.addWidget(button_register)

        self.setLayout(layout)

    def register_user(self):
        username = self.entry_username.text()
        password = self.entry_password.text()
        confirm_password = self.entry_confirm_password.text()

        if password != confirm_password:
            QMessageBox.warning(self, 'Lỗi', 'Mật khẩu không khớp!')
            return

        if self.cafe.username_exists(username):
            QMessageBox.warning(self, 'Lỗi', 'Tên đăng nhập đã tồn tại!')
        else:
            self.cafe.register_user(username, password)
            QMessageBox.information(self, 'Thành công', 'Đăng ký thành công!')
            self.close()

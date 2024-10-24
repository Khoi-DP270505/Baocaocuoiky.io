from PyQt5.QtWidgets import QWidget, QLabel, QLineEdit, QPushButton, QVBoxLayout, QMessageBox
from ui.main_screen import MainScreen
from ui.admin_screen import AdminScreen  # Import giao diện Admin
from ui.register import RegisterWindow  # Import giao diện Đăng ký
from csv_backend import NetCafeSystem

class LoginWindow(QWidget):
    def __init__(self):
        super().__init__()
        self.cafe = NetCafeSystem()  # Hệ thống quản lý quán net
        self.init_ui()

    def init_ui(self):
        self.setWindowTitle("Đăng nhập")
        self.setGeometry(100, 100, 300, 250)

        layout = QVBoxLayout()

        # Nhãn và ô nhập cho tên đăng nhập
        self.label_username = QLabel("Tên đăng nhập:")
        self.entry_username = QLineEdit()
        layout.addWidget(self.label_username)
        layout.addWidget(self.entry_username)

        # Nhãn và ô nhập cho mật khẩu
        self.label_password = QLabel("Mật khẩu:")
        self.entry_password = QLineEdit()
        self.entry_password.setEchoMode(QLineEdit.Password)
        layout.addWidget(self.label_password)
        layout.addWidget(self.entry_password)

        # Nút đăng nhập
        button_login = QPushButton("Đăng nhập")
        button_login.clicked.connect(self.login)
        layout.addWidget(button_login)

        # Nút đăng ký
        button_register = QPushButton("Đăng ký")
        button_register.clicked.connect(self.open_register_window)
        layout.addWidget(button_register)

        self.setLayout(layout)

    # Hàm xử lý đăng nhập
    def login(self):
        username = self.entry_username.text()  # Lấy tên đăng nhập từ ô nhập
        password = self.entry_password.text()  # Lấy mật khẩu từ ô nhập

        user = self.cafe.authenticate(username, password)  # Xác thực người dùng
        if user:
            QMessageBox.information(self, 'Thành công', 'Đăng nhập thành công!')

            if user["is_admin"] == "True":  # Nếu người dùng là admin
                # Mở giao diện AdminScreen
                self.admin_screen = AdminScreen()
                self.admin_screen.show()
            else:
                # Mở giao diện MainScreen cho người dùng thường
                pc_id = self.cafe.get_user_pc(username)["pc_id"] if self.cafe.get_user_pc(username) else 1
                self.main_screen = MainScreen(username, pc_id)
                self.main_screen.show()

            self.close()  # Đóng cửa sổ đăng nhập sau khi thành công
        else:
            # Thông báo lỗi nếu tên đăng nhập hoặc mật khẩu không đúng
            QMessageBox.warning(self, 'Lỗi', 'Tên đăng nhập hoặc mật khẩu không đúng!')

    # Mở cửa sổ đăng ký người dùng mới
    def open_register_window(self):
        self.register_window = RegisterWindow()
        self.register_window.show()


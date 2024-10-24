from PyQt5.QtWidgets import QApplication
from ui.login import LoginWindow
import sys

if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = LoginWindow()  # Tạo cửa sổ đăng nhập
    window.show()  # Hiển thị cửa sổ đăng nhập
    sys.exit(app.exec_())  # Giữ ứng dụng chạy sau khi hiển thị cửa sổ

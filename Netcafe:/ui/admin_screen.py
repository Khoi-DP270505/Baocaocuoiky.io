from PyQt5.QtWidgets import QWidget, QLabel, QPushButton, QVBoxLayout, QHBoxLayout, QMessageBox, QTableWidget, QTableWidgetItem, QLineEdit
from csv_backend import NetCafeSystem

class AdminScreen(QWidget):
    def __init__(self):
        super().__init__()
        self.cafe = NetCafeSystem()
        self.init_ui()

    def init_ui(self):
        self.setWindowTitle("Giao diện Quản trị viên")
        self.setGeometry(100, 100, 800, 600)

        layout = QVBoxLayout()

        # Tiêu đề
        self.label_title = QLabel("Quản lý hệ thống quán net")
        layout.addWidget(self.label_title)

        # Nút hiển thị danh sách người dùng
        button_view_users = QPushButton('Xem danh sách người dùng', self)
        button_view_users.clicked.connect(self.view_users)
        layout.addWidget(button_view_users)

        # Nút quản lý người dùng (Thêm, Xóa)
        button_manage_users = QPushButton('Quản lý người dùng', self)
        button_manage_users.clicked.connect(self.manage_users)
        layout.addWidget(button_manage_users)

        # Nút quản lý máy trạm (Thêm, Xóa)
        button_manage_pcs = QPushButton('Quản lý máy trạm', self)
        button_manage_pcs.clicked.connect(self.manage_pcs)
        layout.addWidget(button_manage_pcs)

        # Nút quản lý dịch vụ (Thêm, Xóa, Cập nhật)
        button_manage_services = QPushButton('Quản lý dịch vụ', self)
        button_manage_services.clicked.connect(self.manage_services)
        layout.addWidget(button_manage_services)

        # Nút báo cáo doanh thu
        button_view_reports = QPushButton('Xem báo cáo doanh thu', self)
        button_view_reports.clicked.connect(self.view_reports)
        layout.addWidget(button_view_reports)

        # Nút thoát
        button_logout = QPushButton('Đăng xuất', self)
        button_logout.clicked.connect(self.logout)
        layout.addWidget(button_logout)

        self.setLayout(layout)

    # Hiển thị danh sách người dùng
    def view_users(self):
        user_list_window = QWidget()
        user_list_window.setWindowTitle("Danh sách người dùng")
        user_list_window.setGeometry(100, 100, 600, 400)

        layout = QVBoxLayout()

        table_users = QTableWidget()
        table_users.setColumnCount(4)
        table_users.setHorizontalHeaderLabels(["Tên đăng nhập", "Mật khẩu", "Số dư", "Quyền admin"])
        table_users.setRowCount(len(self.cafe.users))

        for row, user in enumerate(self.cafe.users):
            table_users.setItem(row, 0, QTableWidgetItem(user["username"]))
            table_users.setItem(row, 1, QTableWidgetItem(user["password"]))
            table_users.setItem(row, 2, QTableWidgetItem(user["balance"]))
            table_users.setItem(row, 3, QTableWidgetItem("Có" if user["is_admin"] == "True" else "Không"))

        layout.addWidget(table_users)
        user_list_window.setLayout(layout)
        user_list_window.show()

    # Quản lý người dùng: thêm, xóa người dùng
    def manage_users(self):
        manage_users_window = QWidget()
        manage_users_window.setWindowTitle("Quản lý người dùng")
        manage_users_window.setGeometry(100, 100, 400, 300)

        layout = QVBoxLayout()

        # Thêm người dùng
        self.add_username = QLineEdit()
        self.add_username.setPlaceholderText("Tên đăng nhập mới")
        layout.addWidget(self.add_username)

        self.add_password = QLineEdit()
        self.add_password.setEchoMode(QLineEdit.Password)
        self.add_password.setPlaceholderText("Mật khẩu mới")
        layout.addWidget(self.add_password)

        button_add_user = QPushButton('Thêm người dùng', self)
        button_add_user.clicked.connect(self.add_user)
        layout.addWidget(button_add_user)

        # Xóa người dùng
        self.remove_username = QLineEdit()
        self.remove_username.setPlaceholderText("Tên đăng nhập cần xóa")
        layout.addWidget(self.remove_username)

        button_remove_user = QPushButton('Xóa người dùng', self)
        button_remove_user.clicked.connect(self.remove_user)
        layout.addWidget(button_remove_user)

        manage_users_window.setLayout(layout)
        manage_users_window.show()

    # Thêm người dùng
    def add_user(self):
        username = self.add_username.text()
        password = self.add_password.text()

        if self.cafe.username_exists(username):
            QMessageBox.warning(self, 'Lỗi', 'Tên đăng nhập đã tồn tại!')
        else:
            self.cafe.register_user(username, password)
            QMessageBox.information(self, 'Thành công', 'Người dùng đã được thêm thành công!')

    # Xóa người dùng
    def remove_user(self):
        username = self.remove_username.text()

        if not self.cafe.username_exists(username):
            QMessageBox.warning(self, 'Lỗi', 'Tên đăng nhập không tồn tại!')
        else:
            self.cafe.remove_user(username)
            QMessageBox.information(self, 'Thành công', 'Người dùng đã được xóa thành công!')

    # Quản lý máy trạm: thêm, xóa máy trạm
    def manage_pcs(self):
        manage_pcs_window = QWidget()
        manage_pcs_window.setWindowTitle("Quản lý máy trạm")
        manage_pcs_window.setGeometry(100, 100, 400, 300)

        layout = QVBoxLayout()

        # Thêm máy trạm
        self.add_pc_id = QLineEdit()
        self.add_pc_id.setPlaceholderText("ID Máy mới")
        layout.addWidget(self.add_pc_id)

        self.add_pc_type = QLineEdit()
        self.add_pc_type.setPlaceholderText("Loại Máy (thường/vip)")
        layout.addWidget(self.add_pc_type)

        button_add_pc = QPushButton('Thêm máy trạm', self)
        button_add_pc.clicked.connect(self.add_pc)
        layout.addWidget(button_add_pc)

        # Xóa máy trạm
        self.remove_pc_id = QLineEdit()
        self.remove_pc_id.setPlaceholderText("ID Máy cần xóa")
        layout.addWidget(self.remove_pc_id)

        button_remove_pc = QPushButton('Xóa máy trạm', self)
        button_remove_pc.clicked.connect(self.remove_pc)
        layout.addWidget(button_remove_pc)

        manage_pcs_window.setLayout(layout)
        manage_pcs_window.show()

    # Thêm máy trạm
    def add_pc(self):
        pc_id = self.add_pc_id.text()
        pc_type = self.add_pc_type.text()

        if pc_id and pc_type:
            self.cafe.add_pc(pc_id, pc_type)
            QMessageBox.information(self, 'Thành công', 'Máy trạm đã được thêm thành công!')
        else:
            QMessageBox.warning(self, 'Lỗi', 'ID Máy và Loại Máy không được để trống!')

    # Xóa máy trạm
    def remove_pc(self):
        pc_id = self.remove_pc_id.text()

        if pc_id:
            self.cafe.remove_pc(pc_id)
            QMessageBox.information(self, 'Thành công', 'Máy trạm đã được xóa thành công!')
        else:
            QMessageBox.warning(self, 'Lỗi', 'ID Máy không được để trống!')

    # Quản lý dịch vụ: thêm, xóa, cập nhật dịch vụ
    def manage_services(self):
        manage_services_window = QWidget()
        manage_services_window.setWindowTitle("Quản lý dịch vụ")
        manage_services_window.setGeometry(100, 100, 400, 300)

        layout = QVBoxLayout()

        # Thêm dịch vụ
        self.add_service_name = QLineEdit()
        self.add_service_name.setPlaceholderText("Tên dịch vụ mới")
        layout.addWidget(self.add_service_name)

        self.add_service_price = QLineEdit()
        self.add_service_price.setPlaceholderText("Giá dịch vụ mới")
        layout.addWidget(self.add_service_price)

        button_add_service = QPushButton('Thêm dịch vụ', self)
        button_add_service.clicked.connect(self.add_service)
        layout.addWidget(button_add_service)

        manage_services_window.setLayout(layout)
        manage_services_window.show()

    # Thêm dịch vụ
    def add_service(self):
        service_name = self.add_service_name.text()
        service_price = self.add_service_price.text()

        if service_name and service_price:
            try:
                service_price = float(service_price)
                self.cafe.add_service(service_name, service_price)
                QMessageBox.information(self, 'Thành công', 'Dịch vụ đã được thêm thành công!')
            except ValueError:
                QMessageBox.warning(self, 'Lỗi', 'Giá dịch vụ phải là một số!')
        else:
            QMessageBox.warning(self, 'Lỗi', 'Tên dịch vụ và Giá dịch vụ không được để trống!')

    # Xem báo cáo doanh thu
    def view_reports(self):
        report_window = QWidget()
        report_window.setWindowTitle("Báo cáo doanh thu")
        report_window.setGeometry(100, 100, 600, 400)

        layout = QVBoxLayout()

        report_table = QTableWidget()
        transactions = self.cafe.get_all_transactions()
        report_table.setRowCount(len(transactions))
        report_table.setColumnCount(5)
        report_table.setHorizontalHeaderLabels(["ID Giao dịch", "Tên người dùng", "Loại giao dịch", "Số tiền", "Thời gian"])

        for row, transaction in enumerate(transactions):
            report_table.setItem(row, 0, QTableWidgetItem(transaction["transaction_id"]))
            report_table.setItem(row, 1, QTableWidgetItem(transaction["username"]))
            report_table.setItem(row, 2, QTableWidgetItem(transaction["transaction_type"]))
            report_table.setItem(row, 3, QTableWidgetItem(transaction["amount"]))
            report_table.setItem(row, 4, QTableWidgetItem(transaction["timestamp"]))

        layout.addWidget(report_table)
        report_window.setLayout(layout)
        report_window.show()

    # Đăng xuất
    def logout(self):
        QMessageBox.information(self, 'Đăng xuất', 'Bạn đã đăng xuất khỏi hệ thống quản trị.')
        self.close()

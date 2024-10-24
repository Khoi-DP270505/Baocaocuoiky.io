from PyQt5.QtWidgets import QWidget, QLabel, QPushButton, QVBoxLayout, QComboBox, QMessageBox
from csv_backend import NetCafeSystem

class MainScreen(QWidget):
    def __init__(self, username, pc_id):
        super().__init__()
        self.username = username
        self.pc_id = pc_id
        self.cafe = NetCafeSystem()
        self.init_ui()

    def init_ui(self):
        self.setWindowTitle(f"Chào mừng {self.username}")
        self.setGeometry(100, 100, 400, 400)

        layout = QVBoxLayout()

        # Lời chào
        self.label_welcome = QLabel(f"Chào mừng {self.username}!")
        layout.addWidget(self.label_welcome)

        # Hiển thị số dư tài khoản
        self.label_balance = QLabel(f"Số dư tài khoản: {self.get_user_balance()} VNĐ")
        layout.addWidget(self.label_balance)

        # Hiển thị máy và thời gian sử dụng
        self.label_pc = QLabel(f"Bạn đang sử dụng máy: {self.get_user_pc()}")
        layout.addWidget(self.label_pc)

        # Dịch vụ
        self.label_service = QLabel("Chọn dịch vụ:")
        layout.addWidget(self.label_service)

        self.combo_services = QComboBox(self)
        self.load_services()
        layout.addWidget(self.combo_services)

        # Nút sử dụng dịch vụ
        button_use_service = QPushButton('Sử dụng dịch vụ', self)
        button_use_service.clicked.connect(self.use_service)
        layout.addWidget(button_use_service)

        # Nút kết thúc phiên
        button_logout = QPushButton('Kết thúc phiên', self)
        button_logout.clicked.connect(self.end_session)
        layout.addWidget(button_logout)

        self.setLayout(layout)

    # Hàm lấy số dư người dùng
    def get_user_balance(self):
        for user in self.cafe.users:
            if user["username"] == self.username:
                return user["balance"]
        return 0

    # Hàm lấy máy của người dùng
    def get_user_pc(self):
        pc = self.cafe.get_user_pc(self.username)
        if pc:
            return f"Mã máy: {pc['pc_id']}, Loại máy: {pc['pc_type']}"
        return "Bạn chưa ngồi máy nào"

    # Tải dịch vụ
    def load_services(self):
        for service in self.cafe.services:
            service_name = f"{service['service_name']} - {service['service_price']} VNĐ"
            self.combo_services.addItem(service_name, service['service_name'])

    # Sử dụng dịch vụ
    def use_service(self):
        service_name = self.combo_services.currentText().split(" - ")[0]
        selected_service = next((service for service in self.cafe.services if service['service_name'] == service_name), None)

        if not selected_service:
            QMessageBox.warning(self, 'Lỗi', 'Dịch vụ không tồn tại!')
            return

        service_price = float(selected_service['service_price'])
        current_balance = float(self.get_user_balance())

        if current_balance >= service_price:
            # Trừ số dư và ghi nhận giao dịch
            self.cafe.update_user_balance(self.username, -service_price, "mua_dich_vu", f"Mua {service_name}")
            self.label_balance.setText(f"Số dư tài khoản: {self.get_user_balance()} VNĐ")
            QMessageBox.information(self, 'Thành công', f"Bạn đã sử dụng {service_name} với giá {service_price} VNĐ")
        else:
            QMessageBox.warning(self, 'Lỗi', 'Số dư không đủ để sử dụng dịch vụ này!')

    # Kết thúc phiên và tính toán chi phí
    def end_session(self):
        pc = self.cafe.get_user_pc(self.username)
        if pc:
            # Cập nhật trạng thái PC và tính tiền
            self.cafe.update_pc_status(pc["pc_id"], "available", self.username)
            QMessageBox.information(self, 'Thành công', 'Bạn đã kết thúc phiên làm việc. Tiền đã được trừ vào tài khoản.')
        else:
            QMessageBox.warning(self, 'Lỗi', 'Không tìm thấy thông tin máy bạn đang sử dụng!')
        
        self.close()

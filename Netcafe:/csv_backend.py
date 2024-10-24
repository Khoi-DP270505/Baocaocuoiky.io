import csv
from datetime import datetime

class NetCafeSystem:
    def __init__(self):
        self.users = []
        self.pcs = []
        self.services = []
        self.transactions = []
        self.load_users()
        self.load_pcs()
        self.load_services()
        self.load_transactions()
        self.ensure_minimum_users()

    # Load người dùng từ CSV
    def load_users(self):
        try:
            with open('data/users.csv', mode='r') as file:
                reader = csv.DictReader(file)
                self.users = list(reader)
        except FileNotFoundError:
            self.users = []

    # Load PC từ CSV
    def load_pcs(self):
        try:
            with open('data/pcs.csv', mode='r') as file:
                reader = csv.DictReader(file)
                self.pcs = list(reader)
        except FileNotFoundError:
            self.pcs = []

    # Load dịch vụ từ CSV
    def load_services(self):
        try:
            with open('data/services.csv', mode='r') as file:
                reader = csv.DictReader(file)
                self.services = list(reader)
        except FileNotFoundError:
            self.services = []

    # Load giao dịch từ CSV
    def load_transactions(self):
        try:
            with open('data/transactions.csv', mode='r') as file:
                reader = csv.DictReader(file)
                self.transactions = list(reader)
        except FileNotFoundError:
            self.transactions = []

    # Hàm thêm giao dịch mới vào file transactions.csv
    def add_transaction(self, username, transaction_type, amount, details):
        transaction_id = len(self.get_all_transactions()) + 1
        timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        transaction = {
            "transaction_id": transaction_id,
            "username": username,
            "transaction_type": transaction_type,
            "amount": amount,
            "timestamp": timestamp,
            "details": details
        }

        # Ghi giao dịch vào file CSV
        with open('data/transactions.csv', mode='a', newline='') as file:
            writer = csv.DictWriter(file, fieldnames=["transaction_id", "username", "transaction_type", "amount", "timestamp", "details"])
            writer.writerow(transaction)

    # Hàm lấy tất cả các giao dịch
    def get_all_transactions(self):
        try:
            with open('data/transactions.csv', mode='r') as file:
                reader = csv.DictReader(file)
                return list(reader)
        except FileNotFoundError:
            return []

    # Hàm xác thực người dùng khi đăng nhập
    def authenticate(self, username, password):
        for user in self.users:
            if user["username"] == username and user["password"] == password:
                return user  # Trả về thông tin người dùng
        return None

    # Hàm kiểm tra tên người dùng có tồn tại không
    def username_exists(self, username):
        for user in self.users:
            if user["username"] == username:
                return True
        return False

    # Hàm đăng ký người dùng mới
    def register_user(self, username, password):
        user = {"username": username, "password": password, "balance": "0", "is_admin": "False"}
        self.users.append(user)
        self.save_user(user)

    # Hàm lưu người dùng mới vào file CSV
    def save_user(self, user):
        with open('data/users.csv', mode='a', newline='') as file:
            writer = csv.DictWriter(file, fieldnames=["username", "password", "balance", "is_admin"])
            writer.writerow(user)

    # Hàm lưu toàn bộ người dùng vào CSV
    def save_all_users(self):
        with open('data/users.csv', mode='w', newline='') as file:
            writer = csv.DictWriter(file, fieldnames=["username", "password", "balance", "is_admin"])
            writer.writeheader()
            writer.writerows(self.users)

    # Xóa người dùng
    def remove_user(self, username):
        self.users = [user for user in self.users if user["username"] != username]
        self.save_all_users()

    # Thêm máy trạm
    def add_pc(self, pc_id, pc_type):
        pc = {"pc_id": pc_id, "pc_type": pc_type, "status": "available", "username": "", "start_time": ""}
        self.pcs.append(pc)
        self.save_all_pcs()

    # Xóa máy trạm
    def remove_pc(self, pc_id):
        self.pcs = [pc for pc in self.pcs if pc["pc_id"] != pc_id]
        self.save_all_pcs()

    # Hàm lưu lại toàn bộ thông tin PC
    def save_all_pcs(self):
        with open('data/pcs.csv', mode='w', newline='') as file:
            writer = csv.DictWriter(file, fieldnames=["pc_id", "pc_type", "status", "username", "start_time"])
            writer.writeheader()
            writer.writerows(self.pcs)

    # Thêm dịch vụ
    def add_service(self, service_name, service_price):
        service = {"service_name": service_name, "service_price": service_price}
        self.services.append(service)
        self.save_all_services()

    # Lưu toàn bộ thông tin dịch vụ vào CSV
    def save_all_services(self):
        with open('data/services.csv', mode='w', newline='') as file:
            writer = csv.DictWriter(file, fieldnames=["service_name", "service_price"])
            writer.writeheader()
            writer.writerows(self.services)

    # Cập nhật số dư người dùng và ghi nhận giao dịch
    def update_user_balance(self, username, amount, transaction_type, details):
        for user in self.users:
            if user["username"] == username:
                current_balance = float(user["balance"])
                user["balance"] = str(current_balance + amount)
                break
        self.save_all_users()
        # Ghi nhận giao dịch
        self.add_transaction(username, transaction_type, amount, details)

    # Cập nhật trạng thái của PC và lưu thời gian bắt đầu
    def update_pc_status(self, pc_id, new_status, username=""):
        for pc in self.pcs:
            if pc["pc_id"] == pc_id:
                pc["status"] = new_status
                pc["username"] = username
                if new_status == "in-use":
                    # Lưu thời gian bắt đầu sử dụng máy
                    pc["start_time"] = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
                elif new_status == "available":
                    # Tính tiền và trừ vào tài khoản người dùng
                    session_duration, cost = self.calculate_cost(pc)
                    self.update_user_balance(username, -cost, "thanh_toan_pc", f"Thanh toán cho sử dụng máy PC số {pc_id}")
                    pc["start_time"] = ""  # Xóa thời gian khi kết thúc
                    pc["username"] = ""  # Giải phóng máy
                break
        self.save_all_pcs()

    # Tính toán thời gian sử dụng và chi phí dựa trên loại máy
    def calculate_cost(self, pc):
        if pc["start_time"]:
            start_time = datetime.strptime(pc["start_time"], "%Y-%m-%d %H:%M:%S")
            end_time = datetime.now()
            session_duration = (end_time - start_time).total_seconds() / 3600  # Tính giờ
            cost_per_hour = 10000 if pc["pc_type"] == "thường" else 20000
            total_cost = session_duration * cost_per_hour
            return session_duration, round(total_cost)
        return 0, 0

    # Thêm dịch vụ cho người dùng và ghi nhận giao dịch
    def use_service(self, username, service_name):
        for service in self.services:
            if service["service_name"] == service_name:
                price = float(service["service_price"])
                self.update_user_balance(username, -price, "mua_dich_vu", f"Mua {service_name}")
                break

    # Đảm bảo luôn có ít nhất 5 người dùng trong danh sách
    def ensure_minimum_users(self):
        while len(self.users) < 5:
            username = f"user{len(self.users) + 1}"
            password = "password"
            user = {"username": username, "password": password, "balance": "0", "is_admin": "False"}
            self.users.append(user)
        self.save_all_users()

    # Lấy thông tin máy trạm mà người dùng đang sử dụng
    def get_user_pc(self, username):
        for pc in self.pcs:
            if pc["username"] == username:
                return pc  # Trả về thông tin máy mà người dùng đang sử dụng
        return None  # Nếu không có máy nào đang được sử dụng

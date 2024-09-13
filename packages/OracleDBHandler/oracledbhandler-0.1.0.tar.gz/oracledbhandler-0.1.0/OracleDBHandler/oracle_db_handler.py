import oracledb
import pandas as pd

class OracleDBHandler:
    def __init__(self, user, password, host, port, serviceName):
        self.user = user
        self.password = password
        self.host = host
        self.port = port
        self.serviceName = serviceName
        self.conn = None
        self.cursor = None

    def connect(self):
        """Kết nối tới cơ sở dữ liệu Oracle."""
        try:
            oracledb.init_oracle_client()
            self.conn = oracledb.connect(user=self.user, password=self.password, host=self.host, port=self.port, service_name=self.serviceName)
            self.cursor = self.conn.cursor()
            print("Kết nối thành công tới Oracle Database")
        except oracledb.DatabaseError as e:
            print(f"Lỗi kết nối: {e}")
            raise

    def insert_data(self, df, table_name):
        """Chèn dữ liệu từ DataFrame vào bảng."""
        if self.conn is None or self.cursor is None:
            raise ConnectionError("Chưa kết nối tới cơ sở dữ liệu. Gọi hàm connect() trước.")

        # Tạo câu lệnh INSERT dựa trên số lượng cột của DataFrame
        columns = ", ".join(df.columns)
        placeholders = ", ".join([f":{i+1}" for i in range(len(df.columns))])
        insert_query = f"INSERT INTO {table_name} ({columns}) VALUES ({placeholders})"

        try:
            self.cursor.executemany(insert_query, df.values.tolist())
            self.conn.commit()
            print(f"Chèn thành công {len(df)} hàng vào bảng {table_name}.")
        except oracledb.DatabaseError as e:
            print(f"Lỗi khi chèn dữ liệu: {e}")
            self.conn.rollback()
            raise

    def update_data(self, df, table_name, id_column, update_columns=None):
        """Cập nhật dữ liệu trong bảng từ DataFrame."""
        if self.conn is None or self.cursor is None:
            raise ConnectionError("Chưa kết nối tới cơ sở dữ liệu. Gọi hàm connect() trước.")

        if update_columns is None:
            update_columns = [col for col in df.columns if col != id_column]

        # Tạo câu lệnh UPDATE với thứ tự biến tham chiếu theo thứ tự tăng dần
        set_clause = ", ".join([f"{col} = :{i+1}" for i, col in enumerate(update_columns)])
        where_clause = f"{id_column} = :{len(update_columns) + 1}"
        update_query = f"UPDATE {table_name} SET {set_clause} WHERE {where_clause}"

        # print("SET clause:", set_clause)
        # print("UPDATE query:", update_query)

        # Chuẩn bị dữ liệu để cập nhật
        data_to_update = [
            tuple([row[col] for col in update_columns] + [row[id_column]])
            for _, row in df.iterrows()
        ]

        # print("Data to update:", data_to_update)

        try:
            self.cursor.executemany(update_query, data_to_update)
            self.conn.commit()
            print(f"Cập nhật thành công {len(df)} hàng trong bảng {table_name}.")
        except oracledb.DatabaseError as e:
            print(f"Lỗi khi cập nhật dữ liệu: {e}")
            self.conn.rollback()
            raise

    def execute_query(self, query, params=None):
        """Thực thi một truy vấn bất kỳ và trả về kết quả (nếu có)."""
        if self.conn is None or self.cursor is None:
            raise ConnectionError("Chưa kết nối tới cơ sở dữ liệu. Gọi hàm connect() trước.")
        
        try:
            self.cursor.execute(query, params or {})
            if self.cursor.description:  # Nếu có dữ liệu trả về
                columns = [col[0] for col in self.cursor.description]
                result = pd.DataFrame(self.cursor.fetchall(), columns=columns)
                return result
            else:
                self.conn.commit()  # Nếu không có dữ liệu trả về (ví dụ: câu lệnh DML)
                print(f"Thực hiện truy vấn thành công.")
        except oracledb.DatabaseError as e:
            print(f"Lỗi khi thực thi truy vấn: {e}")
            self.conn.rollback()
            raise

    def delete_data(self, table_name, condition=None):
        """Xóa dữ liệu từ bảng với điều kiện (nếu được cung cấp)."""
        if self.conn is None or self.cursor is None:
            raise ConnectionError("Chưa kết nối tới cơ sở dữ liệu. Gọi hàm connect() trước.")
        
        # Nếu không có điều kiện, xóa toàn bộ dữ liệu trong bảng
        if condition:
            delete_query = f"DELETE FROM {table_name} WHERE {condition}"
        else:
            delete_query = f"DELETE FROM {table_name}"

        try:
            self.cursor.execute(delete_query)
            self.conn.commit()
            if condition:
                print(f"Đã xóa dữ liệu từ bảng {table_name} với điều kiện: {condition}")
            else:
                print(f"Đã xóa tất cả dữ liệu từ bảng {table_name}.")
        except oracledb.DatabaseError as e:
            print(f"Lỗi khi xóa dữ liệu: {e}")
            self.conn.rollback()
            raise
        
    def check_duplicates(self, table_name, columns=None):
        """
        Kiểm tra các bản ghi trùng lặp trong bảng dựa trên danh sách các cột được chỉ định.
        Nếu không chỉ định cột, kiểm tra trên tất cả các cột.
        
        Args:
        - table_name (str): Tên bảng cần kiểm tra.
        - columns (list): Danh sách tên cột cần kiểm tra trùng lặp. Nếu để trống, kiểm tra tất cả các cột.
        
        Returns:
        - DataFrame chứa các bản ghi trùng lặp (nếu có).
        """
        if self.conn is None or self.cursor is None:
            raise ConnectionError("Chưa kết nối tới cơ sở dữ liệu. Gọi hàm connect() trước.")
        
        try:
            # Lấy tất cả các cột nếu không có danh sách cột được chỉ định
            if not columns:
                query = f"SELECT column_name FROM all_tab_columns WHERE table_name = UPPER('{table_name}')"
                self.cursor.execute(query)
                columns = [row[0] for row in self.cursor.fetchall()]
                print(f"Kiểm tra trùng lặp trên tất cả các cột: {columns}")
            
            # Tạo truy vấn để kiểm tra trùng lặp
            columns_str = ", ".join(columns)
            query = f"""
                SELECT {columns_str}, COUNT(*) as count
                FROM {table_name}
                GROUP BY {columns_str}
                HAVING COUNT(*) > 1
            """
            self.cursor.execute(query)
            
            # Lấy kết quả và chuyển thành DataFrame
            result = pd.DataFrame(self.cursor.fetchall(), columns=columns + ['count'])
            
            if result.empty:
                print("Không có bản ghi trùng lặp.")
            else:
                print(f"Đã tìm thấy {len(result)} bản ghi trùng lặp.")
            
            return result
        
        except oracledb.DatabaseError as e:
            print(f"Lỗi khi kiểm tra trùng lặp: {e}")
            raise

    def close(self):
        """Đóng kết nối tới cơ sở dữ liệu Oracle."""
        if self.cursor:
            self.cursor.close()
        if self.conn:
            self.conn.close()
        print("Đã đóng kết nối tới Oracle Database.")

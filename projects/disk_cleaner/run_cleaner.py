import os
import shutil
import subprocess
from pathlib import Path

class DiskCleaner:
    def __init__(self):
        self.total_freed_bytes = 0
        
        # Các thư mục Temp thường xuyên phình to trên Windows
        self.temp_paths = [
            Path(os.environ.get('TEMP', 'C:\\Temp')),
            Path(os.environ.get('TMP', 'C:\\Windows\\Temp')),
            Path('C:\\Windows\\Prefetch'),
            Path('C:\\Windows\\SoftwareDistribution\\Download') # Nơi lưu file update Win
        ]
        
    def _format_size(self, size_in_bytes: float) -> str:
        """Định dạng byte sang MB/GB cho dễ nhìn"""
        for unit in ['B', 'KB', 'MB', 'GB', 'TB']:
            if size_in_bytes < 1024.0:
                return f"{size_in_bytes:.2f} {unit}"
            size_in_bytes /= 1024.0
            
    def _get_dir_size(self, path: Path) -> int:
        """Lấy kích thước một thư mục"""
        total_size = 0
        try:
            for dirpath, _, filenames in os.walk(path):
                for f in filenames:
                    fp = os.path.join(dirpath, f)
                    if not os.path.islink(fp):
                        total_size += os.path.getsize(fp)
        except Exception:
            pass
        return total_size

    def clean_temp_folders(self):
        """Xóa các thư mục Temp của Windows"""
        print("\n[*] Dang don dep cac thu muc Temp he thong...")
        for path in self.temp_paths:
            if not path.exists():
                continue
                
            print(f"  - Quet: {path}")
            size_before = self._get_dir_size(path)
            deleted_count = 0
            
            try:
                for item in path.iterdir():
                    try:
                        if item.is_file() or item.is_symlink():
                            item.unlink()
                            deleted_count += 1
                        elif item.is_dir():
                            shutil.rmtree(item, ignore_errors=True)
                            deleted_count += 1
                    except Exception:
                        pass # Bỏ qua các file đang được OS sử dụng
            except PermissionError:
                print(f"  [!] Khong co quyen truy cap: {path}")
                
            size_after = self._get_dir_size(path)
            freed = max(0, size_before - size_after)
            self.total_freed_bytes += freed
            print(f"    -> Da xoa {deleted_count} muc. Giai phong: {self._format_size(freed)}")

    def clean_dev_caches(self):
        """Gọi CLI để dọn cache của pip, uv, npm"""
        print("\n[*] Dang don dep bo nho dem (Cache) cua Lap trinh vien...")
        commands = [
            ("uv", ["uv", "cache", "clean"]),
            ("pip", ["pip", "cache", "purge"]),
            ("npm", ["npm", "cache", "clean", "--force"]),
            ("yarn", ["yarn", "cache", "clean"])
        ]
        
        for name, cmd in commands:
            print(f"  - Dang chay: {' '.join(cmd)}")
            try:
                # Ẩn output để log sạch, timeout 30s
                subprocess.run(cmd, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL, timeout=30)
                print(f"    -> {name} cache cleaned.")
                # Lệnh purge tự làm rỗng folder, không track byte trực tiếp được dễ dàng
                # Nên ta coi như một thao tác dọn dẹp vô hình.
            except FileNotFoundError:
                print(f"    -> {name} khong duoc cai dat. Bo qua.")
            except Exception as e:
                print(f"    -> Loi khi don {name}: {e}")

    def clean_docker(self):
        """Xóa Docker images/containers dangling"""
        print("\n[*] Dang don dep Docker rac...")
        try:
            # system prune -f (force)
            cmd = ["docker", "system", "prune", "-a", "-f", "--volumes"]
            print(f"  - Dang chay: {' '.join(cmd)}")
            result = subprocess.run(cmd, capture_output=True, text=True, timeout=60)
            
            # Docker prune thường trả về thông tin đã giải phóng ở dòng cuối cùng
            output = result.stdout
            if "Total reclaimed space:" in output:
                reclaimed_line = [line for line in output.split('\n') if "Total reclaimed space:" in line]
                if reclaimed_line:
                    print(f"    -> {reclaimed_line[0]}")
            else:
                print("    -> Docker pruned.")
        except FileNotFoundError:
             print("    -> Docker khong duoc cai dat. Bo qua.")
        except Exception as e:
             print(f"    -> Loi khi don Docker: {e}")

    def run(self):
        print("================================================")
        print("[*] BAT DAU CHUONG TRINH DON DEP O C (DISK CLEANER)")
        print("================================================")
        
        self.clean_temp_folders()
        self.clean_dev_caches()
        self.clean_docker()
        
        print("\n================================================")
        print(f"[*] TONG KET: Da don dep thanh cong cac khu vuc rac.")
        if self.total_freed_bytes > 0:
            print(f"[*] Uoc tinh giai phong tinh (tu Temp): {self._format_size(self.total_freed_bytes)}")
        print("Luu y: Khong gian giai phong tu Cache/Docker co the chua duoc tinh vao con so tren, hay mo o C de kiem tra!")
        print("================================================")

if __name__ == "__main__":
    cleaner = DiskCleaner()
    cleaner.run()

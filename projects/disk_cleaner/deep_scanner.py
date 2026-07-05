import os
import argparse
from pathlib import Path
from typing import List, Tuple

def format_size(size_in_bytes: float) -> str:
    """Format bytes to human readable format"""
    for unit in ['B', 'KB', 'MB', 'GB', 'TB']:
        if size_in_bytes < 1024.0:
            return f"{size_in_bytes:.2f} {unit}"
        size_in_bytes /= 1024.0
    return f"{size_in_bytes:.2f} PB"

class DeepScanner:
    def __init__(self, root_dir: str):
        self.root_dir = Path(root_dir).resolve()
        self.large_files: List[Tuple[Path, int]] = []
        self.dir_sizes: dict = {}
        
    def scan(self, limit_mb: int = 100):
        print(f"[*] Dang quet thu muc: {self.root_dir} (Co the mat vai phut...)")
        
        limit_bytes = limit_mb * 1024 * 1024
        
        # Bỏ qua các thư mục hệ thống để tránh lỗi và quét nhanh hơn
        skip_dirs = {'Windows', 'Program Files', 'Program Files (x86)', '$Recycle.Bin', 'System Volume Information'}
        
        for dirpath, dirnames, filenames in os.walk(self.root_dir):
            # Cắt bớt thư mục bị bỏ qua
            dirnames[:] = [d for d in dirnames if d not in skip_dirs and not d.startswith('.')]
            
            current_dir_size = 0
            
            for f in filenames:
                try:
                    fp = Path(dirpath) / f
                    if not fp.is_symlink():
                        size = fp.stat().st_size
                        current_dir_size += size
                        
                        if size > limit_bytes:
                            self.large_files.append((fp, size))
                except Exception:
                    pass # Bo qua file khong co quyen hoac bi xoa
            
            self.dir_sizes[dirpath] = current_dir_size
            
    def report_top_files(self, top_n: int = 20):
        print(f"\n{'='*60}")
        print(f"[*] TOP {top_n} FILE NANG NHAT ( > 100MB )")
        print(f"{'='*60}")
        
        # Sort by size descending
        self.large_files.sort(key=lambda x: x[1], reverse=True)
        
        if not self.large_files:
            print("Khong tim thay file nao qua lon.")
            return
            
        for i, (path, size) in enumerate(self.large_files[:top_n], 1):
            print(f"{i:02d}. {format_size(size):>10} | {path}")
            
    def report_top_dirs(self, top_n: int = 15):
        print(f"\n{'='*60}")
        print(f"[*] TOP {top_n} THU MUC NANG NHAT")
        print(f"{'='*60}")
        
        # Sort by size descending
        sorted_dirs = sorted(self.dir_sizes.items(), key=lambda x: x[1], reverse=True)
        
        for i, (path, size) in enumerate(sorted_dirs[:top_n], 1):
            if size > 50 * 1024 * 1024: # Chi hien thi thu muc > 50MB
                print(f"{i:02d}. {format_size(size):>10} | {path}")

def clean_project_archives():
    """Don dep cac file zip rac trong thu muc archives cua project"""
    print(f"\n{'='*60}")
    print("[*] DON DEP FILE ZIP RAC TRONG WORKSPACE")
    print(f"{'='*60}")
    
    current_workspace = Path(__file__).resolve().parent.parent.parent
    archive_dir = current_workspace / "archives"
    
    deleted_size = 0
    deleted_count = 0
    
    # 1. Xoa trong thu muc archives
    if archive_dir.exists():
        for zip_file in archive_dir.glob("*.zip"):
            try:
                size = zip_file.stat().st_size
                zip_file.unlink()
                deleted_size += size
                deleted_count += 1
                print(f"  - Da xoa: {zip_file.name} ({format_size(size)})")
            except Exception as e:
                print(f"  [!] Loi khi xoa {zip_file.name}: {e}")
                
    # 2. Xoa cac file zip ngoai root do AI tu tao lan truoc
    for root_zip in current_workspace.glob("*.zip"):
         try:
             size = root_zip.stat().st_size
             root_zip.unlink()
             deleted_size += size
             deleted_count += 1
             print(f"  - Da xoa (Root): {root_zip.name} ({format_size(size)})")
         except Exception as e:
             pass
             
    print(f"\n[*] Tong cong da xoa {deleted_count} file zip rac. Giai phong: {format_size(deleted_size)}")


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Deep Scanner - Tim va don rac o đia")
    parser.add_argument("--scan", type=str, help="Duong dan thu muc de quet (VD: C:\\Users\\Admin)", default="")
    parser.add_argument("--clean-archives", action="store_true", help="Don dep cac file zip rac trong workspace")
    args = parser.parse_args()
    
    if args.clean_archives:
        clean_project_archives()
        
    if args.scan:
        scanner = DeepScanner(args.scan)
        scanner.scan()
        scanner.report_top_files()
        scanner.report_top_dirs()
    elif not args.clean_archives:
        print("Vui long cung cap lenh. VD: python deep_scanner.py --scan C:\\Users\\Admin")
        print("Hoac: python deep_scanner.py --clean-archives")

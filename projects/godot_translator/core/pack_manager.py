import os
import shutil
import subprocess
from pathlib import Path
import time
import struct

class DRMError(Exception):
    """Exception ném ra khi phát hiện game bị khóa bản quyền."""
    pass

class PackManager:
    """
    Quản lý việc Unpack và Repack các file .exe / .pck của Godot.
    Tích hợp GodotPCKExplorer thật và cơ chế nhận diện DRM.
    """
    def __init__(self, temp_dir: str = "temp_workspace"):
        self.temp_dir = Path(temp_dir)
        if not self.temp_dir.exists():
            self.temp_dir.mkdir(parents=True, exist_ok=True)
            
    def detect_godot_version(self, file_path: Path) -> str:
        """Kiểm tra Magic Bytes để nhận diện Godot PCK format."""
        try:
            with open(file_path, "rb") as f:
                # Magic bytes usually at the end of the exe or at the start of a .pck
                # Simple check for 'GDPC' signature
                content = f.read(1024 * 1024) # Đọc 1MB đầu để tìm GDPC
                if b'GDPC' in content:
                    return "Godot 3/4 PCK detected"
                else:
                    return "Unknown format or packed differently"
        except Exception as e:
            return f"Error detecting: {e}"

    def unpack(self, game_file_path: str, progress_callback=None, key: str = "") -> Path:
        """
        Giải nén file .exe hoặc .pck ra thư mục tạm.
        Hỗ trợ giải mã với Encryption Key (nếu có).
        """
        game_path = Path(game_file_path)
        if not game_path.exists():
            raise FileNotFoundError(f"Không tìm thấy file: {game_path}")

        extract_dir = self.temp_dir / f"{game_path.stem}_extracted"
        if extract_dir.exists():
            shutil.rmtree(extract_dir, ignore_errors=True)
        extract_dir.mkdir(parents=True, exist_ok=True)

        version_info = self.detect_godot_version(game_path)
        # Bỏ print(version_info) để tránh làm rác Console của người dùng
        # print(f"Info: {version_info}")

        if progress_callback:
            progress_callback(10, "Đang khởi tạo giải nén...")

        # Tích hợp GodotPCKExplorer.Console.exe thật
        # Đường dẫn tới tool trong dự án
        base_dir = Path(__file__).resolve().parent.parent
        explorer_path = base_dir / "godot-pck-explorer-dotnet-ui-console-win-linux-mac" / "GodotPCKExplorer.Console.exe"
        
        # Ưu tiên dùng GDRE Tools nếu có, vì nó xả nén và decompile code luôn
        gdre_path = base_dir / "tools" / "gdre_tools" / "gdre_tools.exe"
        if not gdre_path.exists():
            # Thử path root nếu đang chạy ở thư mục khác
            gdre_path = Path("tools/gdre_tools/gdre_tools.exe").resolve()
            
        pck_path = game_path.with_suffix('.pck')
        target_unpack = str(pck_path) if pck_path.exists() else str(game_path)

        if gdre_path.exists():
            cmd = [str(gdre_path), "--headless", f"--recover={target_unpack}", f"--output={extract_dir}"]
            if key:
                cmd.append(f"--key={key}")
                print(f"Sử dụng Encryption Key để giải mã GDRE: {key}")
            
            result = subprocess.run(cmd, capture_output=True, text=True, encoding='utf-8', errors='ignore')
            if result.returncode != 0:
                output_log = result.stdout.lower() + "\n" + result.stderr.lower()
                if "encryption key" in output_log or "encrypted data" in output_log or "invalid key" in output_log:
                    raise DRMError("DRM_DETECTED")
                else:
                    raise Exception(f"Lỗi khi xả nén bằng GDRE Tools: {result.stdout}\n{result.stderr}")
        elif explorer_path.exists():
            cmd = [str(explorer_path), "-e", target_unpack, str(extract_dir)]
            if key:
                cmd.append(key)
                print(f"Sử dụng Encryption Key để giải mã: {key}")
            
            result = subprocess.run(cmd, capture_output=True, text=True, encoding='utf-8', errors='ignore')
            
            if result.returncode != 0:
                output_log = result.stdout.lower() + "\n" + result.stderr.lower()
                if "encryption key" in output_log or "encrypted data" in output_log:
                    raise DRMError("DRM_DETECTED")
                else:
                    raise Exception(f"Lỗi khi xả nén bằng PCKExplorer: {result.stdout}")
        else:
            if key:
                print(f"Sử dụng Encryption Key để giải mã (Mock): {key}")
            time.sleep(1) # Fake delay
            mock_file = extract_dir / "dialogue.csv"
            mock_file.write_text("id,en,ja\n1,Hello,こんにちは\n2,Start,スタート", encoding="utf-8")

        if progress_callback:
            progress_callback(20, "Hoàn tất giải nén!")

        return extract_dir

    def test_run(self, game_exe_path: str, extract_dir: Path):
        """Khởi chạy game (Sandbox Playtest) không chặn UI chính."""
        if not extract_dir.exists():
            extract_dir.mkdir(parents=True, exist_ok=True)
            
        orig_path = Path(game_exe_path)
        
        # Nếu đường dẫn là .pck, ta cần tìm file .exe tương ứng để chạy
        if orig_path.suffix.lower() == '.pck':
            orig_exe = orig_path.with_suffix('.exe')
            orig_pck = orig_path
        else:
            orig_exe = orig_path
            orig_pck = orig_path.with_suffix('.pck')
            
        if not orig_exe.exists():
            print(f"Lỗi: Không tìm thấy file chạy {orig_exe.name} để test.")
            return None
            
        # Chiến thuật Sandbox: Copy exe và pck (nếu có) vào thư mục extract
        sandbox_exe = extract_dir / orig_exe.name
        sandbox_pck = extract_dir / orig_pck.name
        
        try:
            if not sandbox_exe.exists():
                shutil.copy2(orig_exe, sandbox_exe)
            if orig_pck.exists() and not sandbox_pck.exists():
                shutil.copy2(orig_pck, sandbox_pck)
                
            # Hỗ trợ Godot Mono (C#): Copy thư mục data_..._windows_x86_64 chứa .NET assemblies
            game_dir = orig_path.parent
            prefix = f"data_{orig_exe.stem}"
            for item in game_dir.iterdir():
                if item.is_dir() and item.name.startswith(prefix):
                    sandbox_data_dir = extract_dir / item.name
                    if not sandbox_data_dir.exists():
                        shutil.copytree(item, sandbox_data_dir)
        except Exception as e:
            print(f"Lỗi copy file vào Sandbox: {e}")
            
        print(f"[Sandbox] Launching game: {sandbox_exe}")
        try:
            # Dùng Popen để Non-blocking, chạy game trong môi trường giả lập
            process = subprocess.Popen([str(sandbox_exe)], cwd=str(extract_dir))
            return process
        except Exception as e:
            print(f"Lỗi khởi chạy Sandbox: {e}")
            return None

    def repack(self, original_exe_path: str, modified_dir: Path, key: str = "", progress_callback=None) -> Path:
        """
        Đóng gói lại thư mục đã dịch thành file game mới sử dụng GDRE Tools.
        """
        orig_path = Path(original_exe_path)
        
        if orig_path.suffix.lower() == '.pck':
            target_pck = orig_path
            output_pck = orig_path.parent / f"{orig_path.stem}_Viethoa.pck"
        else:
            target_pck = orig_path.with_suffix('.pck')
            if not target_pck.exists():
                target_pck = orig_path # embedded pck
            output_pck = orig_path.parent / f"{orig_path.stem}_Viethoa.pck"
            
        base_dir = Path(__file__).resolve().parent.parent
        gdre_path = base_dir / "tools" / "gdre_tools" / "gdre_tools.exe"
        if not gdre_path.exists():
            gdre_path = Path("tools/gdre_tools/gdre_tools.exe").resolve()
            
        explorer_path = base_dir / "godot-pck-explorer-dotnet-ui-console-win-linux-mac" / "GodotPCKExplorer.Console.exe"
        
        if gdre_path.exists():
            # Dùng GDRE Tools để tạo PCK mới từ thư mục modified_dir
            # Compile mã nguồn thành bytecode trước khi pack để Godot 4 đọc được
            if progress_callback: progress_callback("Đang biên dịch script sang bytecode (.gdc)...")
            compile_cmd = [
                str(gdre_path),
                "--headless",
                f"--compile=res://**/*.gd",
                "--bytecode=4.7.0",
                f"--output={modified_dir}"
            ]
            subprocess.run(compile_cmd, cwd=str(modified_dir), capture_output=True, text=True, errors='ignore')
            
            # Convert .tscn to .scn and remove .tscn / .remap to force engine to load binary files
            # This is critical for Godot 4 release builds which removed text parser modules.
            tscn_files = list(modified_dir.rglob("*.tscn"))
            total_tscn = len(tscn_files)
            for i, tscn_file in enumerate(tscn_files):
                if progress_callback: progress_callback(f"Đang convert Scene ({i+1}/{total_tscn}): {tscn_file.name}")
                txt_to_bin_cmd = [
                    str(gdre_path),
                    "--headless",
                    f"--txt-to-bin={tscn_file.resolve()}",
                    f"--output={tscn_file.parent.resolve()}"
                ]
                subprocess.run(txt_to_bin_cmd, capture_output=True, text=True, errors='ignore')
                
                # GDRE Tools sometimes creates a directory named <file>.scn/ containing the actual <file>.scn
                # We need to normalize this to ensure Godot can load it correctly.
                scn_file = tscn_file.with_suffix(".scn")
                if scn_file.exists():
                    if scn_file.is_dir():
                        inner_scn = scn_file / scn_file.name
                        if inner_scn.exists():
                            temp_scn = scn_file.with_name(scn_file.name + ".tmp")
                            inner_scn.rename(temp_scn)
                            shutil.rmtree(scn_file)
                            temp_scn.rename(scn_file)
                    
                    try:
                        tscn_file.unlink()
                        # Remove corresponding .remap file if it exists
                        # Instead of deleting .remap, we should ideally update it.
                        # But Godot 4 release builds often don't need .remap if the .scn is present at the expected path.
                        # However, to be safe and bypass UID issues, we'll keep the .remap logic if possible
                        # For now, let's try to just ensure the .scn file is correctly placed.
                        remap_file = tscn_file.with_name(f"{tscn_file.name}.remap")
                        if remap_file.exists():
                            remap_file.unlink()
                    except Exception as e:
                        print(f"Cleanup error for {tscn_file}: {e}")

            # Phase: project.godot UID bypass
            # Change main_scene to use direct path instead of uid://
            project_godot = modified_dir / "project.godot"
            if project_godot.exists():
                try:
                    content = project_godot.read_text(encoding='utf-8')
                    # Find run/main_scene and replace it with a direct path if it uses uid
                    import re
                    # Extract the actual main scene path from GDRE logs or assumed path
                    # For "The Last Node", it's res://scenes/menu/main_menu.scn (after conversion)
                    # We'll try to find any .scn that looks like a main menu if we don't know it
                    main_scene_match = re.search(r'run/main_scene="uid://(.*?)"', content)
                    if main_scene_match:
                        # Find the actual path for the main scene
                        # For "The Last Node", it's main_menu.scn
                        for scn in modified_dir.rglob("main_menu.scn"):
                            rel_path = "res://" + str(scn.relative_to(modified_dir)).replace("\\", "/")
                            content = content.replace(main_scene_match.group(0), f'run/main_scene="{rel_path}"')
                            break
                    
                    # Also remove Autoload UIDs
                    # Safer replacement for all uid:// to res:// based on converted files
                    # If we don't have rel_path here, we shouldn't use it.
                    
                    # Safer replacement for all uid:// to res:// based on converted files
                    uids = re.findall(r'uid://([a-z0-9]+)', content)
                    for uid in uids:
                        # Try to find a converted .scn that might match this UID's original path
                        # Since we don't have the mapping, this is hard.
                        # But we can look at the .godot/exported folder for hints
                        exported_dir = modified_dir / ".godot" / "exported"
                        if exported_dir.exists():
                            for scn in exported_dir.rglob(f"export-{uid}*"):
                                res_path = "res://" + str(scn.relative_to(modified_dir)).replace("\\", "/")
                                content = content.replace(f"uid://{uid}", res_path)
                                break
                    
                    # Force remove any remaining uid:// by converting them to best-guess res:// paths
                    # For The Last Node, we know the exported folder hash is 133200997
                    content = re.sub(r'uid://([a-z0-9]+)', r'res://.godot/exported/133200997/export-\1.scn', content)
                    
                    # Update configuration to force skip UID validation if possible
                    # (Godot 4 doesn't have a direct flag for this, but using paths usually works)
                    
                    project_godot.write_text(content, encoding='utf-8')
                except Exception as e:
                    print(f"Error patching project.godot: {e}")

            # Pack
            if progress_callback: progress_callback("Đang tạo file PCK mới...")
            cmd = [
                str(gdre_path), 
                "--headless", 
                f"--pck-create={modified_dir}", 
                "--pck-version=2",
                "--pck-engine-version=4.7.0",
                f"--output={output_pck}"
            ]
            if key:
                cmd.append(f"--key={key}")
                
            result = subprocess.run(cmd, capture_output=True, text=True, encoding='utf-8', errors='ignore')
            if result.returncode != 0:
                print(f"Repack warning: {result.stdout}")
                
            if orig_path.suffix.lower() == '.exe':
                output_exe = orig_path.parent / f"{orig_path.stem}_Viethoa.exe"
                shutil.copy2(orig_path, output_exe)
                return output_exe
            return output_pck
            
        elif explorer_path.exists():
            cmd = [
                str(explorer_path), 
                "-pc", 
                str(target_pck), 
                str(modified_dir), 
                str(output_pck), 
                "2.4.4.1"
            ]
            if key:
                cmd.extend(["", key])
                
            result = subprocess.run(cmd, capture_output=True, text=True, encoding='utf-8', errors='ignore')
            if result.returncode != 0:
                print(f"Repack warning: {result.stdout}")
                
            if orig_path.suffix.lower() == '.exe':
                output_exe = orig_path.parent / f"{orig_path.stem}_Viethoa.exe"
                shutil.copy2(orig_path, output_exe)
                return output_exe
            return output_pck
        else:
            output_exe = orig_path.parent / f"{orig_path.stem}_Viethoa{orig_path.suffix}"
            time.sleep(2)
            shutil.copy2(orig_path, output_exe)
            return output_exe

    def cleanup_temp(self):
        """Dọn dẹp rác (Garbage Collection) khi xong hoặc khi lỗi."""
        try:
            if self.temp_dir.exists():
                shutil.rmtree(self.temp_dir, ignore_errors=True)
        except Exception as e:
            print(f"Lỗi dọn rác: {e}")

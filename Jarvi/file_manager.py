import os
import sys

class FileManager:
    def __init__(self, start_dir=None):
        if start_dir is None:
            # Default to the workspace root directory
            self.current_dir = os.path.abspath(os.path.dirname(os.path.dirname(__file__)))
        else:
            self.current_dir = os.path.abspath(start_dir)

    def get_current_directory(self) -> str:
        return self.current_dir

    def list_contents(self):
        """
        Lists files and folders in the current directory.
        Returns a list of dicts: [{'name': ..., 'is_dir': True/False, 'path': ...}]
        """
        items = []
        try:
            for item in os.listdir(self.current_dir):
                full_path = os.path.join(self.current_dir, item)
                is_directory = os.path.isdir(full_path)
                items.append({
                    "name": item,
                    "is_dir": is_directory,
                    "path": full_path
                })
            
            # Sort: directories first, then files, both alphabetically
            items.sort(key=lambda x: (not x["is_dir"], x["name"].lower()))
        except PermissionError:
            items.append({
                "name": "[Permission Denied]",
                "is_dir": False,
                "path": ""
            })
        except Exception as e:
            items.append({
                "name": f"[Error: {str(e)}]",
                "is_dir": False,
                "path": ""
            })
        return items

    def navigate_to(self, folder_name) -> bool:
        """
        Enters a subdirectory. Returns True on success.
        """
        target = os.path.join(self.current_dir, folder_name)
        if os.path.isdir(target):
            self.current_dir = os.path.abspath(target)
            return True
        return False

    def navigate_up(self) -> bool:
        """
        Moves to the parent directory. Returns True if navigated up, False if already at root.
        """
        parent = os.path.dirname(self.current_dir)
        # Check if we are already at root (e.g. A:\ on Windows or / on Unix)
        if parent == self.current_dir:
            return False
        self.current_dir = parent
        return True

    def open_file(self, file_path) -> bool:
        """
        Launches the file natively in the OS.
        """
        try:
            if os.path.exists(file_path) and os.path.isfile(file_path):
                if sys.platform == "win32":
                    os.startfile(file_path)
                elif sys.platform == "darwin":
                    import subprocess
                    subprocess.call(["open", file_path])
                else:
                    import subprocess
                    subprocess.call(["xdg-open", file_path])
                return True
        except Exception:
            pass
        return False

    def search_and_execute_file(self, query) -> tuple[bool, str]:
        """
        Recursively searches A: drive for a file matching the query.
        If found, launches it natively and returns (True, absolute_path).
        """
        search_root = "A:\\"
        if not os.path.exists(search_root):
            search_root = self.current_dir  # Fallback to current directory (workspace)

        query = query.lower().strip()
        matches = []
        
        try:
            for root, dirs, files in os.walk(search_root):
                # Optimize walk: exclude hidden directories, caches, virtualenvs, etc.
                dirs[:] = [d for d in dirs if not d.startswith('.') and d not in (
                    '__pycache__', 'venv', 'env', 'node_modules', 'dist', 'build', '.git', '.gemini'
                )]
                
                for file in files:
                    # Match name case-insensitively (e.g. query "calculator" matches "Calculator.exe")
                    if query in file.lower():
                        full_path = os.path.join(root, file)
                        matches.append(full_path)
                        
                        # Direct exact match (without extension) takes precedence
                        base_name, _ = os.path.splitext(file.lower())
                        if base_name == query:
                            matches = [full_path]
                            break
                
                # Stop walking if exact match found
                if len(matches) == 1 and os.path.splitext(os.path.basename(matches[0]))[0].lower() == query:
                    break
        except Exception as e:
            return False, f"Search scan failed: {str(e)}"
            
        if not matches:
            return False, "File not found."
            
        target_path = matches[0]
        if self.open_file(target_path):
            return True, target_path
        return False, f"Found match: {target_path}, but could not launch it."


import os
import pwd
import grp
import stat
import time

def list_files(directory="."):
    """Lists files and directories with detailed metadata (ls -la style)."""
    try:
        items = []
        # Use scandir for better performance and easier type checking
        with os.scandir(directory) as it:
            for entry in it:
                try:
                    s = entry.stat()
                    
                    # Get Owner and Group names
                    try:
                        uid = s.st_uid
                        gid = s.st_gid
                        owner = pwd.getpwuid(uid).pw_name
                        group = grp.getgrgid(gid).gr_name
                    except KeyError:
                        owner = str(uid)
                        group = str(gid)
                    
                    # File Type
                    if entry.is_dir():
                        ftype = "directory"
                    elif entry.is_file():
                        ftype = "file"
                    elif entry.is_symlink():
                        ftype = "symlink"
                    else:
                        ftype = "other"
                        
                    items.append({
                        "name": entry.name,
                        "type": ftype,
                        "owner": owner,
                        "permissions": stat.filemode(s.st_mode),
                        "group": group,
                        "size": s.st_size,
                        "modified": time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(s.st_mtime))
                    })
                except OSError:
                    # Skip files we can't access
                    continue
                    
        return {"files": items}
    except Exception as e:
        return {"error": str(e)}

def read_file_content(path):
    """Reads content of a file."""
    try:
        if not os.path.exists(path):
            return {"error": "File not found"}
        with open(path, 'r') as f:
            content = f.read()
        return {"content": content}
    except Exception as e:
        return {"error": str(e)}

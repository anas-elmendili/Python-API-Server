import os
import shutil

def delete_item(path, recursive=False):
    """Deletes a file or directory."""
    try:
        if not os.path.exists(path):
            return {"error": "Path not found"}
            
        if os.path.isdir(path):
            if recursive:
                shutil.rmtree(path)
                return {"message": "Directory deleted recursively"}
            else:
                try:
                    os.rmdir(path)
                    return {"message": "Directory deleted"}
                except OSError:
                    return {"error": "Directory not empty. Use recursive=true"}
        else:
            os.remove(path)
            return {"message": "File deleted successfully"}
    except Exception as e:
        return {"error": str(e)}
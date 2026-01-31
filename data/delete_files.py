import os

def delete_file_data(path):
    """Deletes a file."""
    try:
        if not os.path.exists(path):
            return {"error": "File not found"}
        os.remove(path)
        return {"message": "File deleted successfully"}
    except Exception as e:
        return {"error": str(e)}

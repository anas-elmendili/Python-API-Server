import os

def update_file(path, content):
    """Updates an existing file."""
    try:
        if not os.path.exists(path):
            return {"error": "File not found"}
        with open(path, 'w') as f:
            f.write(content)
        return {"message": "File updated successfully"}
    except Exception as e:
        return {"error": str(e)}

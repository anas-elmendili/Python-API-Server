import os

def create_file(path, content=""):
    """Creates a new file with content."""
    try:
        if os.path.exists(path):
            return {"error": "File already exists"}
        with open(path, 'w') as f:
            f.write(content)
        return {"message": "File created successfully"}
    except Exception as e:
        return {"error": str(e)}

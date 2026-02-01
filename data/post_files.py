import os

def create_item(path, is_dir=False, content=""):
    """Creates a new file or directory."""
    try:
        if os.path.exists(path):
            return {"error": "Path already exists"}
        
        if is_dir:
            os.makedirs(path)
            return {"message": "Directory created successfully"}
        else:
            with open(path, 'w') as f:
                f.write(content)
            return {"message": "File created successfully"}
    except Exception as e:
        return {"error": str(e)}
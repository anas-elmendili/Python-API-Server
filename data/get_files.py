import os

def list_files(directory="."):
    """Lists files in a directory."""
    try:
        files = []
        for f in os.listdir(directory):
            if os.path.isfile(os.path.join(directory, f)):
                files.append(f)
        return {"files": files}
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

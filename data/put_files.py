import os
import shutil
from utils.command_runner import run_system_command

def update_item(path, content=None, permissions=None, owner=None):
    """Updates a file/directory content, permissions, or owner."""
    if not os.path.exists(path):
        return {"error": "Path not found"}

    try:
        # Update Content (Files only)
        if content is not None:
            if os.path.isdir(path):
                return {"error": "Cannot write content to a directory"}
            with open(path, 'w') as f:
                f.write(content)

        # Update Permissions (chmod) - expects octal string e.g. "755"
        if permissions:
            try:
                mode = int(permissions, 8)
                os.chmod(path, mode)
            except ValueError:
                return {"error": "Invalid permissions format"}

        # Update Owner (chown) - expects "user:group"
        if owner:
            # simple validation
            res = run_system_command(["chown", owner, path])
            if not res['success']:
                return {"error": f"Failed to change owner: {res['error']}"}

        return {"message": "Update successful"}
    except Exception as e:
        return {"error": str(e)}
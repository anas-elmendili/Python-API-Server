import subprocess

def run_system_command(command, input_text=None):
    """
    Executes a system command securely.
    
    Args:
        command (list): The command and arguments as a list.
        input_text (str): Optional input text to pipe to the command.
        
    Returns:
        dict: A dictionary containing 'success' (bool), 'stdout' (str), 'error' (str).
    """
    try:
        result = subprocess.run(
            command,
            input=input_text,
            capture_output=True,
            text=True,
            check=True
        )
        return {"success": True, "stdout": result.stdout.strip(), "error": None}
    except subprocess.CalledProcessError as e:
        return {"success": False, "stdout": e.stdout.strip(), "error": e.stderr.strip()}
    except Exception as e:
        return {"success": False, "stdout": None, "error": str(e)}

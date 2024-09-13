import subprocess
import os
import pkg_resources

def download(filename, root):
    """
    Download a file using the Go-based CLI.

    Args:
    filename (str): The name of the file to download.
    root (str): The root hash for the download.

    Returns:
    tuple: A tuple containing (filename, status_message).
           If successful, status_message is "Success".
           If failed, status_message contains error details.
    """
    try:
        cli_path = pkg_resources.resource_filename('zerog_python_api', 'cli_tool')
        if not os.access(cli_path, os.X_OK):
            raise PermissionError(f"CLI tool at {cli_path} is not executable")
        if not os.path.exists(cli_path):
            raise FileNotFoundError(f"CLI tool not found at {cli_path}")


        # Call the Go binary
        result = subprocess.run([cli_path, "download", filename, root],
                                capture_output=True, text=True, check=True)
        
        if "Download successful" in result.stdout:
            return filename, "Success"
        else:
            return filename, f"Unexpected output: {result.stdout}"

    except subprocess.CalledProcessError as e:
        return filename, f"Error (exit code {e.returncode}):\nstdout: {e.stdout}\nstderr: {e.stderr}"
    except Exception as e:
        return filename, f"Unexpected error: {str(e)}"
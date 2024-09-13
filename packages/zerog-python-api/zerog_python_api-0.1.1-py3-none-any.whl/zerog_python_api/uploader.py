import subprocess
import json
import pkg_resources
import os

def upload(file_path, indexer, private_key, url="", contract="0xbD2C3F0E65eDF5582141C35969d66e34629cC768", tags="0x", expected_replica=1,
           finality_required=True, skip_tx=False, task_size=10, fee=0):
    """
    Upload a file using the Go-based CLI and return the Merkle root hash.
    Args:
        (same as before)
    Returns:
        tuple: A tuple containing (status_message, merkle_root).
        If successful, status_message is "Success" and merkle_root contains the Merkle hash.
        If failed, status_message contains error details and merkle_root is None.
    """
    try:
        # Prepare the arguments
        args = {
            "file": file_path,
            "tags": tags,
            "url": url,
            "indexer": indexer,
            "contract": contract,
            "key": private_key,
            "expectedReplica": expected_replica,
            "finalityRequired": finality_required,
            "skipTx": skip_tx,
            "taskSize": task_size,
            "fee": fee
        }
        # Convert arguments to JSON string
        args_json = json.dumps(args)

        # Locate the CLI tool
        cli_path = pkg_resources.resource_filename('zerog_python_api', 'cli_tool')
        if not os.access(cli_path, os.X_OK):
            raise PermissionError(f"CLI tool at {cli_path} is not executable")

        if not os.path.exists(cli_path):
            raise FileNotFoundError(f"CLI tool not found at {cli_path}")

        # Call the Go binary and capture the output
        result = subprocess.run([cli_path, "upload", args_json],
                                capture_output=True, text=True, check=True)
        
        stdout = result.stdout
        if result.returncode == 0:
            # The output should now include the Merkle root on success
            merkle_root_line = stdout.strip()
            return merkle_root_line, "Success" 
        else:
            return f"Unexpected output: {stdout}", None
    except subprocess.CalledProcessError as e:
        return f"Error (exit code {e.returncode}):\nstdout: {e.stdout}\nstderr: {e.stderr}", None
    except FileNotFoundError as e:
        return f"CLI tool not found: {str(e)}", None
    except Exception as e:
        return f"Unexpected error: {str(e)}", None

# # Example usage
# status_message, merkle_root = upload("path/to/file", "tags", "url", "indexer", "contract", "private_key")
# if status_message == "Success":
#     print(f"Upload successful. Merkle root: {merkle_root}")
# else:
#     print(f"Upload failed: {status_message}")
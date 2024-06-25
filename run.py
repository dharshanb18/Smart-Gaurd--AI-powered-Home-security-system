import subprocess

def execute_script(script_path, project_path):
    try:
        # Construct the command to change directory, set execution policy, activate virtual environment, and run script
        command = f'cmd /c cd /D "{project_path}" && ' \
                  f'powershell Set-ExecutionPolicy -Scope CurrentUser -ExecutionPolicy Unrestricted && ' \
                  f'call myenv\\Scripts\\activate.bat && ' \
                  f'python -u "{script_path}"'

        # Run the command in the terminal
        subprocess.run(command, check=True, shell=True)
    except subprocess.CalledProcessError as e:
        print(f"Error: {e}")
    except FileNotFoundError:
        print("Error: Command not found or path incorrect.")

# Example usage:
if __name__ == "__main__":
    script_path = "D:/RAO/IoT/IOT project/main.py"
    project_path = "D:/RAO/IoT/IOT project"
    execute_script(script_path, project_path)

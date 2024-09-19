import subprocess

class ShellAgent:
    def execute_command(self, command):
        """
        Executes a shell command and returns the output.
        """
        try:
            output = subprocess.check_output(command, shell=True, stderr=subprocess.STDOUT)
            return output.decode().strip()
        except subprocess.CalledProcessError as e:
            return f"Error executing command: {e.output.decode().strip()}"

    def execute_action(self, action):
        """
        Executes a useful action in the current system.
        """
        # Implement your action logic here
        pass
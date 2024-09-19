import unittest
from src.agents.shell_agent import ShellAgent

class TestShellAgent(unittest.TestCase):
    def test_execute_command(self):
        # Test the execute_command method of ShellAgent
        agent = ShellAgent()
        result = agent.execute_command("ls")
        self.assertIsNotNone(result)
        # Add more test cases here

if __name__ == "__main__":
    unittest.main()
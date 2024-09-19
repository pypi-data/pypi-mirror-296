import unittest
from unittest.mock import patch
from cli_jgmarxiv import ask_agent, serialize_response_to_json, serialize_response_to_markdown

class TestCliJgmarxiv(unittest.TestCase):
    @patch('cli_jgmarxiv._create_agent_tools')
    def test_ask_agent(self, mock_create_agent_tools):
        # Mock agent_executor and response
        agent_executor = mock_create_agent_tools.return_value[1]
        response = {
            "output": "Sample output",
            # Add other response fields as needed
        }
        agent_executor.invoke.return_value = response

        # Call ask_agent function
        input_request = "Sample input"
        resp = ask_agent(input_request, agent_executor)

        # Assert the response
        self.assertEqual(resp, response)

    def test_serialize_response_to_json(self):
        # Create a sample response
        response = {
            "output": "Sample output",
            # Add other response fields as needed
        }

        # Call serialize_response_to_json function
        json_str = serialize_response_to_json(response)

        # Assert the serialized JSON string
        self.assertEqual(json_str, '{"output": "Sample output"}')

    def test_serialize_response_to_markdown(self):
        # Create a sample response
        response = {
            "output": "Sample output",
            # Add other response fields as needed
        }

        # Call serialize_response_to_markdown function
        markdown_str = serialize_response_to_markdown(response)

        # Assert the serialized Markdown string
        expected_str = "# Output\n\nSample output\n"
        self.assertEqual(markdown_str, expected_str)

if __name__ == "__main__":
    unittest.main()
import unittest
from client import ChatClient

class TestChatClient(unittest.TestCase):
    def test_chat_sequence(self):
        client = ChatClient()
        
        # Ask the LLM to answer "tell me a good joke for a 4-year-old"
        response_1 = client.generate("tell me a good joke for a 4-year-old")
        print(response_1)

        print("\n\n------------------\n\n")
        
        # Generate again while appending "ok, now add a duck to the joke"
        response_2 = client.generate("ok, now add a duck to the joke")
        print(response_2)

if __name__ == "__main__":
    unittest.main()

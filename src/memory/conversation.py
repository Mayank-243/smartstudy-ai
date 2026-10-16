# src/memory/conversation.py


class ConversationMemory:
    """Simple sliding-window memory for chat history."""
    
    def __init__(self, max_messages: int = 10):
        """
        max_messages: kitne messages yaad rakhne hain (default 10)
        """
        self.messages = []
        self.max_messages = max_messages
    
    def add_user_message(self, content: str):
        """User ka message add karo."""
        self.messages.append(("user", content))
        self._trim()
    
    def add_ai_message(self, content: str):
        """AI ka message add karo."""
        self.messages.append(("assistant", content))
        self._trim()
    
    def _trim(self):
        """Agar messages zyada ho gaye, toh purane hatao."""
        if len(self.messages) > self.max_messages:
            self.messages = self.messages[-self.max_messages:]
    
    def get_messages(self):
        """Current messages ki list return karo."""
        return self.messages.copy()
    
    def clear(self):
        """Poori history delete karo."""
        self.messages = []
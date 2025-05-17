class Messages:
    def __init__(self):
        self.messages = []

    def add_user_message(self, message: str) -> None:
        self.messages.append({"role": "user", "content": message})

    def add_assistant_message(self, message: str) -> None:
        self.messages.append({"role": "assistant", "content": message})

    def add_system_message(self, message: str) -> None:
        self.messages.append({"role": "system", "content": message})

    def remove_last_message(self) -> None:
        if len(self.messages) > 0:
            self.messages.pop()

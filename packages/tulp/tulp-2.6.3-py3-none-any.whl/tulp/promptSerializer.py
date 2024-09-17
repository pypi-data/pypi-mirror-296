import json

class RequestMessageSerializer:
    def __init__(self, filename):
        self.filename = filename

    def save(self, request_messages, response=None):
        if response:
            request_messages.append(response)
        
        with open(self.filename, 'w') as file:
            json.dump(request_messages, file, indent=2)
        
        if response:
            request_messages.pop()



    def load(self):
        with open(self.filename, 'r') as file:
            return json.load(file)

    def getMessage(self):
        messages = self.load()
        for message in messages:
            return message
        return None

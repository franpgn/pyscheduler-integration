import json
import os


class Mem:
    def __init__(self):
        current_dir = os.path.dirname(os.path.abspath(__file__))
        self.data = os.path.join(current_dir, 'DATA', 'mem.json')
        if os.path.exists(self.data):
            self.load_process_queue()
        else:
            self.process_queue = []

    def add_process(self, process_data):
        self.process_queue.append(process_data)
        self.write_process_queue()

    def write_process_queue(self):
        with open(self.data, 'w') as f:
            json.dump(self.process_queue, f, indent=4)

    def load_process_queue(self):
        with open(self.data, 'r') as f:
            self.process_queue = json.load(f)

    def get_last_id(self):
        if self.process_queue:
            return self.process_queue[-1]['id'] + 1
        else:
            return 1

    def get_process_queue(self):
        if self.process_queue is not None:
            return self.process_queue

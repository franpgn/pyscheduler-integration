import json
import os
import sys

script_dir = os.path.dirname(os.path.abspath(__file__))
project_root = os.path.abspath(os.path.join(script_dir, '..', '..'))
sys.path.append(project_root)

from pyscheduler.src.scheduler import Scheduler
from pyscheduler.src.process import Process


class Memory:
    __process_queue = []
    base_dir = os.path.dirname(os.path.abspath(__file__))
    data_dir = os.path.join(base_dir, '..', 'DATA')
    __data = os.path.join(data_dir, 'mem.json')

    @staticmethod
    def __init__():
        if not os.path.exists(Memory.data_dir):
            os.makedirs(Memory.data_dir)
        if os.path.exists(Memory.__data):
            print("Initializing memory...")
            Memory.__load_process_queue()

    @staticmethod
    def add_process(process_data):
        Memory.__process_queue.append(process_data)
        print(Memory.__process_queue[-1])
        Memory.__write_process_queue()

    @staticmethod
    def __write_process_queue():
        with open(Memory.__data, 'w') as f:
            json.dump(Memory.__process_queue, f, indent=4)

    @staticmethod
    def __load_process_queue():
        with open(Memory.__data, 'r') as f:
            Memory.__process_queue = json.load(f)

    @staticmethod
    def get_last_id():
        if Memory.__process_queue:
            return Memory.__process_queue[-1]['pid'] + 1
        else:
            return 1

    @staticmethod
    def get_process_queue():
        if Memory.__process_queue is not None:
            return Memory.__process_queue
        else:
            print('No processes on memory ')

    @staticmethod
    def send_process_queue():
        for process in Memory.__process_queue:
            Scheduler.set_process_queue(process)
        print('Memory process queue sent to Scheduler')

    @staticmethod
    def start_scheduler():
        Scheduler.add_processes()
        Scheduler.start_scheduling()
        print('Scheduler started')

    @staticmethod
    def clear_memory():
        Memory.__process_queue = []
        Memory.__write_process_queue()
        print('Memory cleared')

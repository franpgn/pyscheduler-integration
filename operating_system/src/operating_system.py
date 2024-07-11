import sys
import os
from apps.src.sobel_filter import to_byte_code as sobel_to_byte_code
from apps.src.mean_filter import to_byte_code as mean_to_byte_code
from simulator.src.memory import Memory

script_dir = os.path.dirname(os.path.abspath(__file__))
project_root = os.path.abspath(os.path.join(script_dir, '..', '..'))
sys.path.append(project_root)


if __name__ == "__main__":
    print("Operating System is running...")
    sobel_to_byte_code()
    mean_to_byte_code()
    Memory.__init__()
    Memory.start_scheduler()

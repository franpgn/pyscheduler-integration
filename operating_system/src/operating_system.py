import sys
import os
#from apps.src.sobel_filter import load_execution_log
from simulator.src.memory import Memory

script_dir = os.path.dirname(os.path.abspath(__file__))
project_root = os.path.abspath(os.path.join(script_dir, '..', '..'))
sys.path.append(project_root)


if __name__ == "__main__":
    print("Operating System is running...")
    #load_execution_log()
    Memory.__init__()
    Memory.start_scheduler()

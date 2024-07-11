

# PyScheduler Integration

## Overview

This project is separated into four packages:
1. **Applications Package**: Handles applications that are transformed into bytecodes.
2. **Processor Simulator Package**: Simulates a processor.
3. **Scheduler Package**: Implements a scheduler for the processor.
4. **Manager Package**: Utilizes all other packages to manage the entire process.

The main focus is to provide a streamlined process for executing scheduling tasks with advanced features and an easy-to-use interface.

## Features

- **🔄 Scheduling Integration**:
  - Integrates seamlessly with PyScheduler for advanced scheduling capabilities.
  - Supports multiple scheduling algorithms including Round Robin and First Come First Served (FCFS).

- **⚡ Dynamic Scheduling**:
  - Adjusts scheduling based on system performance and load.
  - Provides real-time feedback and adjustments to improve efficiency.

- **🔧 Extensible Framework**:
  - Easily add new scheduling algorithms and features.
  - Modular design to customize and extend functionality.

- **🖼️ Mean and Sobel Filter Execution**:
  - Supports the execution of mean_filter and sobel_filter functions.
  - Managed through the `operating_system.py` file.

## Project Structure

- **📂 operating_system.py**: Entry point for the scheduler. Defines processes, queues, and starts scheduling.
- **📄 process.py**: Contains the Process class, representing each process with its attributes.
- **📋 queue.py**: Defines the Queue class, which manages process queues.
- **🔄 round_robin.py**: Contains RoundRobin class for scheduling.
- **⏳ fcfs.py**: Contains FCFS class for scheduling.
- **⚙️ quantum.py**: Manages quantum values for different queues.
- **🗂️ scheduler.py**: Contains the scheduling process for the queues.
- **🧠 ai_quantum_scheduler.py**: AI class to optimize quantum values using reinforcement learning.
- **🌐 app.py**: Flask application to display execution graphs.
- **📊 execution_log.json**: Stores the execution log of processes for visualization.
- **🔍 disassemble.py**: Receives a function, transforms it into bytecode, and sends it to a JSON file.
- **💾 memoria.py**: Stores the processes and sends them to the ready queue.
- **🖥️ cpu.py**: Contains instructions and executes the processes received from the scheduler.
- **📦 stack.py**: Implements a stack to store values.
- **🔢 ula.py**: Performs binary operations.

## Getting Started

### Prerequisites

- 🐍 Python 3.12 or higher
- 🟦 PyScheduler
- 🌐 Flask
- 📊 Matplotlib
- 🔢 Numpy

### Installation

1. Clone the repository:
   ```
   git clone https://github.com/franpgn/pyscheduler-integration.git
   cd pyscheduler-integration
   ```

2. Initialize and update submodules:
   ```
   git submodule init
   git submodule update
   ```

3. Install the required packages:
   ```
   pip install -r requirements.txt
   ```

### Running the Integration

1. Run the integration:
   ```
   python operating_system.py
   ```

2. Run the Flask application for visualization (if applicable):
   ```
   python app.py
   ```

3. Open your browser and navigate to:
   ```
   http://127.0.0.1:5000/
   ```

## Contribution

Feel free to fork the repository and submit pull requests. For major changes, please open an issue first to discuss what you would like to change.

## License

This project is licensed under the MIT License.

<p align="center">
  <img alt="License" src="https://img.shields.io/static/v1?label=license&message=MIT&color=49AA26&labelColor=000000">
</p>

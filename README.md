# Project Setup Instructions

This document outlines the steps to set up and run the project from scratch, assuming no prior installations or configurations.

## Prerequisites

Before starting, ensure your system meets the following requirements:

1. **Operating System**: Linux (Ubuntu recommended).
2. **Internet Connection**: Required to download dependencies.

## Step-by-Step Setup Instructions

### 1. Update and Upgrade System Packages
Ensure your system is up to date:
```bash
sudo apt update && sudo apt upgrade -y
```

### 2. Install Python and Required Tools
Install Python 3.8 or higher along with pip and venv:
```bash
sudo apt install -y python3 python3-pip python3-venv
```

### 3. Install Git
Install Git to clone the repository:
```bash
sudo apt install -y git
```

Verify the installation of Git:
```bash
git --version
```

### 4. Install MPI (Message Passing Interface)
Install MPICH, a recommended MPI implementation:
```bash
sudo apt install -y mpich libmpich-dev
```

Verify the installation of MPI:
```bash
mpirun --version
```

### 5. Clone the Repository
Download the project repository from GitHub:
```bash
git clone https://github.com/iMaary/final_project_ipb.git
cd final_project_ipb
```

### 6. Create and Activate a Virtual Environment
Set up an isolated Python environment for the project:
```bash
python3 -m venv repast4py-env
source repast4py-env/bin/activate
```

### 7. Install Python Dependencies
Upgrade pip and install the required Python libraries:
```bash
pip install --upgrade pip
pip install numpy mpi4py repast4py
```

Verify that `repast4py` is installed:
```bash
pip show repast4py
```

### 8. Run the Project
Execute the main script with MPI:
```bash
mpirun -n <num_processes> python3 ./main.py ./conf.yaml
```
Replace `<num_processes>` with the desired number of processes (e.g., `2`).

Example:
```bash
mpirun -n 2 python3 ./main.py ./conf.yaml
```

## Troubleshooting Common Issues

### 1. "Cannot import name 'random' from 'repast4py'"
- Ensure `repast4py` is installed in the active Python environment.
- Activate the virtual environment before running:
  ```bash
  source repast4py-env/bin/activate
  ```

### 2. "mpi.h: No such file or directory"
- Ensure MPI development libraries are installed:
  ```bash
  sudo apt install -y mpich libmpich-dev
  ```

### 3. "File not found: ./main.py"
- Ensure you are in the correct directory containing `main.py`.
- Use the absolute path to the script if necessary.

### 4. "conf.yaml not found"
- Ensure the `conf.yaml` file exists in the project directory.
- Use the absolute path to the configuration file if needed.

## License

This project is licensed under the [MIT License](LICENSE).

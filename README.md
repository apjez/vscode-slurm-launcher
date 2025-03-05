# VS Code Slurm Launcher
This repository provides the user tools to launch Slurm jobs on remote clusters directly from their local machine. This assumes you have VS Code with the Remote SSH extension installed.

## Requirements
- [Remote SSH](https://code.visualstudio.com/docs/remote/ssh) extension for VS Code
- Python `curses` library (should be a standard library on Linux, MacOS - on Windows, install `windows-curses`)
- Login node with `vscode-job-launch.sh` installed with executable bit set and in a directory included in PATH (i.e. users should be able to run `vscode-job-modify.sh` without an absolute path)
  -  `SLURM_ROOT` should be updated to reflect the environment on the cluster  

## Usage
- Configure a cluster with `python3 configure.py -c CLUSTER_NAME -j`
  - The first time, you'll be prompted to enter the cluster login node (IP address or FQDN) and your username
  - This will add an SSH configuration at the default path called `cluster_name-job`
  - After the configuration is set up, you'll land in an interactive editor to set job submission options
- Update job submission options
  - Run `python3 configure.py -c CLUSTER_NAME -j` again to modify existing job submission options
    - You can pass a string to the `-j` option to non-interactively modify the job submission options
    - Alternatively, omit arguments for the `-j` option to enter the interactive editor
- Launch an interactive job via VS Code
  - In VS Code, connect session (either with "Connect to Host" or ssh from terminal) to `cluster_name-job`.
  
***TIP:** IT IS RECOMMENDED THAT YOU USE* `ssh-keygen` *AND* `ssh-copy-id` *TO USE SSH KEYS FOR AUTHENTICATION!*

***TIP:** YOU MAY NEED TO INCREASE YOUR VS CODE REMOTE SSH TIMEOUT SETTING TO ACCOUNT FOR JOB SCHEDULING TIME (F1 > Remote-SSH: Settings -> Connect Timeout: 60)*

## Demonstration

![example workflow](vsc-slurm-launcher.gif "Example Workflow")


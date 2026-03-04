# VS Code Slurm Launcher
This repository provides the user tools to launch Slurm jobs on remote clusters directly from their local machine. This assumes you have VS Code with the Remote SSH extension installed.

## Requirements
- [Remote SSH](https://code.visualstudio.com/docs/remote/ssh) extension for VS Code
- Python `curses` library (should be a standard library on Linux, MacOS - on Windows, install `windows-curses`)
- Login node with `vscode-job-launch.sh` installed with executable bit set and in a directory included in PATH (i.e. users should be able to run `vscode-job-modify.sh` without an absolute path)
  -  `SLURM_ROOT` should be updated to reflect the environment on the cluster  

## Usage
- Ensure that you have an SSH key pair to access the AI Makerspace
  - On your **local machine**, run `ssh-keygen -t rsa -b 4096` to create a new key pair. When prompted, press `Enter` to accept the default location and skip setting a passphrase.
    - Note the path of the newly created key, as it will be needed in the next step (by default, it will be `~/.ssh/id_rsa`)
  - Use `ssh-copy-id -i /path/to/id_rsa username@login-ice.pace.gatech.edu` (replace 'username' with your GT username) to copy the public key to the cluster. When prompted, enter your password and confirm the message indicates success.
  - Attempt to login without a password using `ssh username@login-ice.pace.gatech.edu` (replace 'username' with your GT username). If successful, proceed to the next step.
- Configure a cluster with `python3 configure.py -c aims -j='-c8 --mem=256gb -t0-8 -G1 -CHX00'`
  - The first time, you'll be prompted to enter the cluster login node (`login-ice.pace.gatech.edu`) and your username
  - This will add an SSH configuration at the default path called `aims-job`
  - This sets the default recommended configuration (8 CPUs, 256GB DRAM, 1 H100 or H200 GPU, 8 hours)
- Update job submission options
  - Run `python3 configure.py -c aims -j` again to modify existing job submission options
    - You can pass a string to the `-j` option to non-interactively modify the job submission options
    - Alternatively, omit arguments for the `-j` option to enter the interactive editor
- Launch an interactive job via VS Code
  - In VS Code, connect session (either with "Connect to Host" or ssh from terminal) to `aims-job`.

***TIP:** YOU MAY NEED TO INCREASE YOUR VS CODE REMOTE SSH TIMEOUT SETTING TO ACCOUNT FOR JOB SCHEDULING TIME (F1 > Remote-SSH: Settings -> Connect Timeout: 60)*

## Demonstration

![example workflow](vsc-slurm-launcher.gif "Example Workflow")


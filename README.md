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

## Skynet
On your **local machine**, if you haven't already, generate your public SSH key:

```bash
ssh-keygen -t rsa -b 4096 -C "your_email@example.com"
```

When prompted, press `Enter` to accept the default file location and skip setting a passphrase if you prefer passwordless access.

Next, display your public key:

```bash
cat ~/.ssh/id_rsa.pub
```

Copy the output of this command.

Then, on **Skynet**, log in to the `sky1` login node and open your `authorized_keys` file:

```bash
nano ~/.ssh/authorized_keys
```

Paste your public key at the end of the file (or on a new line if it’s the first key), then save and close (`Ctrl+O`, `Enter`, `Ctrl+X`).

After this, you should be able to SSH into `sky1` without a password. This setup enables seamless job launching via VS Code Remote SSH.

Now run the following command to configure the cluster:

```bash
python3 configure.py -c SKY -j
```

When prompted:
- For **"Cluster login node (IP or FQDN):"**, enter:
  ```
  sky1.cc.gatech.edu
  ```
- For **"Cluster username (Your login username):"**, enter your Georgia Tech username.

Now follow the demonstration workflow below to add the correct SLURM arguments.  
For example, to request a single GPU A40 node with 12 CPUs on the `hoffman-lab` account and partition, enter:

```
-G a40 -c 12 -A hoffman-lab -p hoffman-lab
```

Then press `Enter`. Your `~/.ssh/config` will be updated automatically.

If followed correctly, then relaunch VS Code and you should see a new host called:

```
sky-job
```
  
***TIP:** IT IS RECOMMENDED THAT YOU USE* `ssh-keygen` *AND* `ssh-copy-id` *TO USE SSH KEYS FOR AUTHENTICATION!*

***TIP:** YOU MAY NEED TO INCREASE YOUR VS CODE REMOTE SSH TIMEOUT SETTING TO ACCOUNT FOR JOB SCHEDULING TIME (F1 > Remote-SSH: Settings -> Connect Timeout: 60)*

## Demonstration

![example workflow](vsc-slurm-launcher.gif "Example Workflow")


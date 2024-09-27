# VS Code Slurm Launcher
This repository provides the user tools to launch Slurm jobs on remote clusters directly from their local machine. This assumes you have VS Code with the Remote SSH extension installed.

## Installation
A guided configuration takes as input:
- **SSH configuration path**: Path to SSH configuration on your local host. If left blank, defaults to standard path (e.g. `~/.ssh/config`).
- **Cluster name**: This name is defined by cluster admins and should be provided in documentation.
- **Cluster login node**: Provide either the fully qualified domain name (FQDN, or hostname + DNS domain name) or the IP address of the the login node.
- **Cluster username**: The username used to access the remote cluster.

### Linux / macOS
- Open a terminal in VS Code and run `curl -s https://raw.githubusercontent.com/apjez/vscode-slurm-launcher/refs/heads/main/configure.py -o configure.py && python3 configure.py`
- Follow the guided setup process. 
- Open `{cluster_name}-job-submit}` and modify the job submission requests as appropriate. Fields without a defined value and comments are ignored.
- Choose 'Connect to Host...' or 'Connect Current Window to Host...' and select or type `{cluster_name}-job`.
- Your terminal should update to reflect the allocated compute node.

*TIP: IT IS RECOMMENDED THAT YOU USE* `ssh-keygen` *and* `ssh-copy-id` *to use SSH keys for authentication!*

#!/usr/bin/env python

import urllib.request
import os

def update_ssh_config(ssh_config_path, cluster_name, cluster_jump, cluster_user, job_submit_config):
  print(f"\nUpdating SSH configuration at {ssh_config_path}:")
  with open(ssh_config_path, 'a+') as f:
    f.seek(0)
    if not f"Host {cluster_jump}" in f.read():
      print(f"  - Adding jump host {cluster_jump}\n")
      f.write(f"Host {cluster_jump}\n"
        f"    SendEnv {cluster_name}_VSC_LAUNCH\n"
        f"    User {cluster_user}\n"
        f"    ForwardX11Trusted yes\n"
        f"    ForwardAgent yes\n")
    else:
      print(f"  - Job submission host {cluster_jump}-job already in config")
    f.seek(0)
    if not f"Host {cluster_name.lower()}-job\n" in f.read():
      print(f"  - Adding job submission host {cluster_name.lower()}-job\n")
      f.write(f"Host {cluster_name.lower()}-job\n"
        f"    RequestTTY force\n"
        f"    User {cluster_user}\n"
        f"    UserKnownHostsFile=/dev/null\n"
        f"    ForwardAgent yes\n"
        f"    StrictHostKeyChecking no\n"
        f"    ProxyCommand ssh {cluster_jump} vscode-launch.sh\n")
    else:
      print(f"  - Job submission host {cluster_name.lower()}-job already in config")

def update_shell_env(cluster_name, job_submit_config):
  if 'bash' in os.environ['SHELL']:
    shell_config_path = os.environ['HOME'] + "/.bashrc"
  elif 'zsh' in os.environ['SHELL']:
     shell_config_path = os.environ['HOME'] + "/.zshenv"
  print(f"\nUpdating shell configuration at {shell_config_path}:")
  with open(shell_config_path, 'a+') as f:
    f.seek(0)
    if not f"export {cluster_name}_JOB_CONFIG=" in f.read():
      print(f"  - Appending {shell_config_path} with job submission configuration file path")
      f.write(f"export {cluster_name}_JOB_CONFIG={job_submit_config}\n")
    else:
      print(f"  - {shell_config_path} already contains job submission configuration file path")
    f.seek(0)
    if not f"export {cluster_name}_VSC_LAUNCH=" in f.read():
      print(f"  - Appending {shell_config_path} with job submission parser and environment setting")
      f.write(f"""export {cluster_name}_VSC_LAUNCH=$(awk -v ORS=" " '!/^#/ && /=[^\\S\\r\\n]+$/ {{print "--"$0}}' ~/.{cluster_name.lower()}-job-submit)\n""")
    else:
      print(f"  - {shell_config_path} already contains job submission parser and environment setting")

def install_job_submit_config(job_submit_config):
  print(f"\nInstalling job configuration file at {job_submit_config}:")
  if not os.path.isfile(job_submit_config):
    urllib.request.urlretrieve("https://raw.githubusercontent.com/apjez/vscode-slurm-launcher/refs/heads/main/job_submit_config.template", job_submit_config)
    print(f"  - Job configuration file installed at {job_submit_config}")
  else:
    print(f"  - {job_submit_config} already installed on local machine")

def read_user_input():
  ssh_config_path = input("Path to SSH config (default ${HOME}/.ssh/config): ").strip() or os.environ['HOME']+"/.ssh/config"
  cluster_name = input("Name of cluster (Refer to Cluster Documentation): ")
  cluster_jump = input("Cluster jump node (IP or FQDN): ")
  cluster_user = input("Cluster username (Your login username): ")
  job_submit_config = os.path.dirname(ssh_config_path) + f'.{cluster_name.lower()}-job-submit'
  return ssh_config_path, cluster_name, cluster_jump, cluster_user, job_submit_config

def configure_env(ssh_config_path, cluster_name, cluster_jump, cluster_user, job_submit_config):
  update_ssh_config(ssh_config_path, cluster_name, cluster_jump, cluster_user, job_submit_config)
  update_shell_env(cluster_name,job_submit_config)
  install_job_submit_config(job_submit_config)

def main():
  ssh_config_path, cluster_name, cluster_jump, cluster_user, job_submit_config = read_user_input()
  configure_env(ssh_config_path, cluster_name, cluster_jump, cluster_user, job_submit_config)

if __name__=="__main__":
  main()

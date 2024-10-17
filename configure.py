#!/usr/bin/env python

import os
import curses
import string
import json
import re
import argparse

def init_curses():
    stdscr = curses.initscr()
    curses.noecho()
    curses.cbreak()
    stdscr.keypad(True)
    return stdscr

def parse_args():
  parser = argparse.ArgumentParser(description="Create and update vscode-slurm-launcher configurations.")
  parser.add_argument("-c", "--cluster", type=str, default=None, required=True)
  parser.add_argument("-j", "--job-options", type=str, nargs="?", default=None, const="")
  parser.add_argument("-s", "--ssh-config", type=str, default=os.environ['HOME']+"/.ssh/config")
  return parser.parse_args()

def create_ssh_config(cluster_name, ssh_conf_path, job_submit_config):
  cluster_jump = input("Cluster login node (IP or FQDN): ")
  cluster_user = input("Cluster username (Your login username): ")
  job_submit_config = os.path.dirname(ssh_conf_path) + f'/.{cluster_name.lower()}-job-submit'
  print(f"\nUpdating SSH configuration at {ssh_conf_path}:")
  with open(ssh_conf_path, 'a+') as f:
    f.seek(0)
    if not f"Host {cluster_name.lower()}-job\n" in f.read():
      print(f"  - Adding job submission host {cluster_name.lower()}-job\n")
      f.write(f"Host {cluster_name.lower()}-job\n"
        f"\tUser {cluster_user}\n"
        f"\tUserKnownHostsFile=/dev/null\n"
        f"\tForwardAgent yes\n"
        f"\tStrictHostKeyChecking no\n"
        f"\tProxyCommand ssh %r@{cluster_jump} \"{cluster_name}_VSC_LAUNCH=\\\"$(cat {job_submit_config})\\\" vscode-launch.sh\"\n")
    else:
      print(f"  - Job submission host {cluster_name.lower()}-job already in config")
  if not os.path.isfile(job_submit_config):
    with open(job_submit_config, 'w') as f:
      f.write("--ntasks=1")
    print(f"  - Job configuration file installed at {job_submit_config}")
  else:
    print(f"  - {job_submit_config} already installed on local machine")

def get_arg_opt(job_options, y):
  matches = list(re.finditer(r'([^ ]+)', job_options))
  num_matches = len(matches)
  arg, opt, index_start, index_end = None, None, None, None
  for i in range(num_matches):
    if matches[i].start() <= y < matches[i].end():
      if m := re.match(r'(--[^=]+)=([^\s]+)',matches[i].group().strip()):
        arg = m.group(1)
        opt = m.group(2)
        index_start = matches[i].start()
        index_end = matches[i].end()
      elif m := re.match(r'(-[a-zA-Z])([^\s]+)',matches[i].group().strip()):
        arg = m.group(1)
        opt = m.group(2)
        index_start = matches[i].start()
        index_end = matches[i].end()
      elif re.match(r'^([^-][^\s]?)',matches[i].group().strip()) and i>0 and re.match(r'^-[a-zA-Z]$',matches[i-1].group().strip()):
        arg = matches[i-1].group()
        opt = matches[i].group()
        index_start = matches[i-1].start()
        index_end = matches[i].end()
      else:
        arg = matches[i].group()
        opt = None
        index_start = matches[i].start()
        index_end = matches[i].end()
    elif y<len(job_options) and job_options[y].isspace() and i<num_matches-1 and y<matches[i+1].start() and re.match(r'^-[a-zA-Z]$',matches[i].group().strip()):
      arg = matches[i].group()
      index_start = matches[i].start()
      try:
        opt = matches[i+1].group()
        index_end = matches[i+1].end()
      except IndexError:
        opt = None
        index_end = None
    if arg != None:
      break
  return arg, opt, index_start, index_end

def print_job_opts(win, rows, cols, y, job_options, job_options_dict):
  arg, opt, index_start, index_end = get_arg_opt(job_options, y)
  win.addstr(0,0,job_options)
  if arg != None:
    if arg in job_options_dict.keys():
      win.addstr(0,index_start,arg,curses.color_pair(1))
      if opt != None:
        win.addstr(0,index_end-len(opt),opt,curses.color_pair(2))
      win.addstr(3,0,"Option Description:",curses.A_UNDERLINE)
      win.addstr(4,0,job_options_dict[arg].split("\n",1)[0],curses.A_BOLD)
      try:
        win.addstr(5,0,job_options_dict[arg].split("\n",1)[1])
      except curses.error:
        pass
    else:
      arg = arg[:equal_pos] if (equal_pos := arg.find("=")) else arg
      win.addstr(0,index_start,arg,curses.color_pair(1))
      matches = list(filter(lambda x: arg in x, job_options_dict.keys()))
      if len(matches)>0:
        win.addstr(0,index_start,arg,curses.color_pair(1))
        win.addstr(3,0,"Possible Options:",curses.A_UNDERLINE)
        try:
          win.addstr(4,0,'\n'.join(matches))
        except curses.error:
          pass
      else:
        win.addstr(3,0,"No matching option found.",curses.A_BOLD)
  win.refresh()

def interactive_editor(stdscr,job_submit_config):
  with open('job_options.dict', 'r') as job_options_dict_file:
    job_options_dict = json.load(job_options_dict_file,strict=False)

  try:
    with open(job_submit_config, "r+") as job_submit_file:
      job_options = job_submit_file.read().rstrip('\n')
  except:
    job_options = ""

  curses.start_color()
  curses.use_default_colors()
  curses.init_pair(1, curses.COLOR_CYAN,-1)
  curses.init_pair(2,curses.COLOR_MAGENTA,-1)
  stdscr.clear()

  rows, cols = stdscr.getmaxyx()

  x, y, y_lookup = 0, 0, 0

  print_job_opts(stdscr, rows, cols, y, job_options, job_options_dict)
  stdscr.move(x, y)

  while True:
    key = stdscr.getkey()
    stdscr.clear()
    if key == "KEY_LEFT" and y>0:
      y -= 1
      y_lookup = y
    elif key == "KEY_RIGHT" and y<len(job_options):
      y += 1
      y_lookup = y
    elif key in string.printable.replace("\t\n\r\x0b\x0c",""):
      job_options = job_options[:y] + key + job_options[y:]
      y_lookup = y
      y += 1
    elif key in ["\b","\x7f","KEY_BACKSPACE"] and len(job_options)>0:
      y = y-1 if y>0 else 0
      y_lookup = y
      if y<len(job_options):
        job_options = job_options[:y] + job_options[y+1:]
    elif key == "KEY_DC":
      y_lookup = y
      job_options = job_options[:y] + job_options[y+1:]
    elif key == "KEY_RESIZE":
      rows, cols = stdscr.getmaxyx()
    elif key in ["\n","C-M","KEY_RETURN"]:
      with open(job_submit_config, "w+") as job_submit_file:
        job_submit_file.write(job_options)
        job_submit_file.truncate()
      stdscr.clear()
      stdscr.refresh()
      break
    print_job_opts(stdscr, rows, cols, y_lookup, job_options, job_options_dict)
    stdscr.move(x, y)

def main():
  args = parse_args()

  ssh_conf_path = args.ssh_config
  cluster_name = args.cluster
  job_submit_config = os.path.dirname(ssh_conf_path) + f'/.{cluster_name.lower()}-job-submit'  
  job_options = args.job_options

  with open(ssh_conf_path, 'r+') as f:
    if not os.path.isfile(job_submit_config) or not f"Host {cluster_name.lower()}-job\n" in f.read():
      create_ssh_config(cluster_name, ssh_conf_path, job_submit_config)
    
  if job_options is not None:
    if len(job_options) > 0:
      with open(job_submit_config, 'w') as job_submit_file:
        job_submit_file.write(job_options)
        job_submit_file.truncate()
    else:
      stdscr = init_curses()
      interactive_editor(stdscr,job_submit_config)
      

if __name__=="__main__":
  main()

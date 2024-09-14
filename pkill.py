import psutil
import logging
import sys
import subprocess
import os

# Configure logging
logging.basicConfig(filename='pkill.log', level=logging.INFO,
                    format='%(asctime)s - %(levelname)s - %(message)s')


def start_process(command_line:str):
    try:
        si = subprocess.STARTUPINFO()
        si.dwFlags |= subprocess.STARTF_USESHOWWINDOW 
        print(f"Starting {command_line}")
        po = subprocess.Popen([command_line], startupinfo=si, 
                         creationflags=subprocess.DETACHED_PROCESS | subprocess.CREATE_NEW_PROCESS_GROUP, 
                         close_fds=True)
        logging.info(f"Started, waiting for completion")
        po.wait()
        print(f"Done")
    except Exception as e:
        logging.error(f"Failed to start process: {e}")
        print(f"Failed to start process: {e}")

        

def kill_process_by_name(process_name:str)->str:
    # Iterate over all running processes
    command_line:str = ""
    for process in psutil.process_iter(['pid', 'name']):
        # If the process name matches the specified name, terminate it
        logging.info(f"Checking process: {process.info['name']} (PID: {process.info['pid']})")
        if process_name.lower() in process.info['name'].lower():
            try:
                command_line = process.cmdline()[0]
                process.terminate()  # Gracefully terminate the process
                logging.info(f"Terminated process: {process.info['name']} (PID: {process.info['pid']})")
                print(f"Terminated process: {process.info['name']} (PID: {process.info['pid']})")
            except psutil.NoSuchProcess:
                logging.info(f"Process {process_name} not found.")
                print(f"Process {process_name} not found.")
            except psutil.AccessDenied:
                logging.info(f"Access denied while trying to terminate {process_name}.")
                print(f"Access denied while trying to terminate {process_name}.")
            except Exception as e:
                logging.info(f"An error occurred: {e}")
                print(f"An error occurred: {e}")
    return command_line

if __name__ == "__main__":
    if len(sys.argv) < 2 or len(sys.argv) > 4:
        print("Usage: python pkill.py <process_name> [--restart cmdline]")
        sys.exit(1)

    process_name_to_kill = sys.argv[1]
    restart = len(sys.argv) == 4 and sys.argv[2] == '--restart'

    command_line: str = kill_process_by_name(process_name_to_kill)

    if restart:
        if command_line == "":
            command_line = sys.argv[3]
        start_process(command_line)
        print("Finished restarting process.")




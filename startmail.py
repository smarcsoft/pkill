from pkill import kill_process_by_name, start_process


if __name__ == "__main__":
    kill_process_by_name("outlook.exe")
    start_process("C:\\Program Files\\Microsoft Office\\root\\Office16\\OUTLOOK.EXE")
from domains import SystemManagementMark
from output import CLI

def main():
    system = SystemManagementMark()

    ok = system.load_from_dat("students.dat")
    if not ok:
        system.load_from_files()

    CLI(system).start()

if __name__ == "__main__":
    main()

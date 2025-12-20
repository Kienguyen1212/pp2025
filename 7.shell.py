import subprocess

def main():
    while True:
        try:
            command_line = input("myshell> ").strip()

            if not command_line: continue
            if command_line == "exit": break

            # Xử lý PIPE (|)
            if "|" in command_line:
                parts = command_line.split("|")
                cmd1 = parts[0].strip().split()
                cmd2 = parts[1].strip().split()

                # stdout=subprocess.PIPE: Đẩy output vào ống dẫn thay vì màn hình
                p1 = subprocess.Popen(cmd1, stdout=subprocess.PIPE)
                
                # stdin=p1.stdout: Lấy input từ đầu ra của lệnh trước
                p2 = subprocess.Popen(cmd2, stdin=p1.stdout)
                
                p1.stdout.close() # Đóng luồng ra để báo hiệu kết thúc dữ liệu (EOF) cho p2
                p2.communicate()  # Chờ p2 xử lý xong

            # Xử lý Output Redirection (>)
            elif ">" in command_line:
                parts = command_line.split(">")
                cmd = parts[0].strip().split()
                filename = parts[1].strip()

                with open(filename, "w") as f:
                    subprocess.run(cmd, stdout=f) # Chuyển hướng output vào file

            # Xử lý Input Redirection (<)
            elif "<" in command_line:
                parts = command_line.split("<")
                cmd = parts[0].strip().split()
                filename = parts[1].strip()

                with open(filename, "r") as f:
                    subprocess.run(cmd, stdin=f) # Lấy input từ file

            # Lệnh thường
            else:
                subprocess.run(command_line.split())

        except Exception as e:
            print(f"Error: {e}")

if __name__ == "__main__":
    main()
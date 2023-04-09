from tkinter import *
import paramiko

root=Tk()

root.title("L.Checker")
root.geometry("700x400+100+100")
root.resizable(True,True)
root.configure(bg='white')

frame_top = Frame(root)
frame_top.grid(row=0, padx=60, pady=10)

frame_left = Frame(root)
frame_left.grid(column=0, padx=100, pady=10)

frame_left = Frame(root)
frame_left.grid(column=7, padx=100, pady=10)

label_title = Label(root, text="L.Checker", bg='white')
label_title.grid(row=1, column=2, padx=10, pady=10)


#ip입력받기
label_1 = Label(root, text="IP : ", bg='white')
label_1.grid(row=2, column=1, padx=10, pady=10)

entry_ip = Entry(root, width=30)
entry_ip.grid(row=2, column=2)

#host입력받기
label_2 = Label(root, text="host : ", bg='white')
label_2.grid(row=3, column=1, padx=10, pady=10)

entry_host = Entry(root, width=30)
entry_host.grid(row=3, column=2)

#pw입력받기
label_3 = Label(root, text="passwd : ", bg='white')
label_3.grid(row=4, column=1, padx=10, pady=10)

entry_pw = Entry(root, width=30, show='*')
entry_pw.grid(row=4, column=2)


label_re = Label(root, bg='white', justify='left')
label_re.grid(row=6, column=2, padx=10, pady=10)


def result():

    ssh = paramiko.SSHClient()

    ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())

    ssh.connect(entry_ip.get(), port=22, username=entry_host.get(), password=entry_pw.get())

    stdin, stdout, stderr = ssh.exec_command('python3 test.py') # 리눅스 내에 있는 test.py 파일 실행 후 결과 출력
    #stdin, stdout, stderr = ssh.exec_command('ls')

    label_re.configure(text=(stdout.read().decode()))

    ssh.close()


button=Button(root, width=10, text="실행", bg='white', command=result)
button.grid(row=5, column=2, padx=10, pady=10)


root.mainloop()
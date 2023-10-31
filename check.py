from tkinter import *
from tkinter import Toplevel, Button
import re
from tkinter import Tk
import paramiko
import tkinter.font
import socket
import tkinter as tk
from tkinter import ttk

def make_parsed_data(security_data):
    parsed_data = []
    for security in security_data:
        if "취약" in security or "양호" in security:
            items = security.split('|')[1:-1]
            item = [items[0].strip(), items[1].strip(), items[2].strip()]
            parsed_data.append(item)
    return parsed_data

root=Tk()

root.title("L.Checker")
root.geometry("600x400+100+100")
root.resizable(False,False)
root.configure(bg='white')

root.grid_rowconfigure(0, weight=1)
root.grid_columnconfigure(0, weight=1)

font_title = tkinter.font.Font(family="Cambria", size=30, weight='bold')
font_main = tkinter.font.Font(family="Cambria", size=12)
font_text = tkinter.font.Font(family="Cambria")

#시작화면 프레임
frame_start = Frame(root, bg='white')
frame_start.grid(row=0, column=0, sticky="nsew")
frame_start.grid_rowconfigure(0, weight=1)
frame_start.grid_columnconfigure(0, weight=1)

#정보화면 프레임
frame_info = Frame(root, bg='white')
frame_info.grid(row=0, column=0, sticky="nsew")
frame_info.grid_rowconfigure(0, weight=1)
frame_info.grid_columnconfigure(0, weight=1)

btn_gostart0 = Button(frame_info, font=20, relief=FLAT, bg='white',text="←", command=lambda:[openFrame(frame_start)])
btn_gostart0.place(x=0, y=0)
btn_goexplain = Button(frame_info, width=10, text="다음", bg='white', command=lambda: [openFrame(frame_explain)])
btn_goexplain.place(x=483, y=335)

#설명화면 프레임
frame_explain = Frame(root, bg='white')
frame_explain.grid(row=0, column=0, sticky="nsew")
frame_explain.grid_rowconfigure(0, weight=1)
frame_explain.grid_columnconfigure(0, weight=1)

btn_gostart1 = Button(frame_explain, font=20, relief=FLAT, bg='white',text="←", command=lambda:[openFrame(frame_start)])
btn_gostart1.place(x=0, y=0)
btn_gomain = Button(frame_explain, width=10, text="시작", bg='white', command=lambda: [openFrame(frame_main)])
btn_gomain.place(x=506, y=360)

#설명화면 프레임
frame_explain = Frame(root, bg='white')
frame_explain.grid(row=0, column=0, sticky="nsew")
frame_explain.grid_rowconfigure(0, weight=1)
frame_explain.grid_columnconfigure(0, weight=1)

btn_gostart1 = Button(frame_explain, font=20, relief=FLAT, bg='white',text="←", command=lambda:[openFrame(frame_start)])
btn_gostart1.place(x=0, y=0)
btn_goexplain = Button(frame_explain, width=10, bg='white',text="뒤로가기", command=lambda:[openFrame(frame_info)])
btn_goexplain.place(x=395, y=335)
btn_gomain = Button(frame_explain, width=10, text="시작", bg='white', command=lambda: [openFrame(frame_main)])
btn_gomain.place(x=483, y=335)

#메인화면 프레임
frame_main = Frame(root, bg='white')
frame_main.grid(row=0, column=0, sticky="nsew")
frame_main.grid_rowconfigure(0, weight=1)
frame_main.grid_columnconfigure(0, weight=1)

btn_gostart2 = Button(frame_main, font=20, relief=FLAT, bg='white',text="←", command=lambda:[openFrame(frame_start)])
btn_gostart2.place(x=0, y=0)

font_title = tkinter.font.Font(size=30, weight='bold')
font_main = tkinter.font.Font(size=12)


def openFrame(frame):
    frame.tkraise()

#시작화면 타이틀
start_title = Label(frame_start, text="L.Checker", bg='white', font=font_title)
start_title.place(x=210, y=100)

#시작화면 설명
text_info = Text(frame_info, bg='white', height=20, width=75)
text_info.place(x=35, y=65)
text_info.insert(END,
                  "\n"
                  "< L.Checker >\n\n"
                  "KISA에서 배포한 <주요정보통신기반시설 기술적 취약점 분석 평가> 기반으로\n\n"
                  "Unix 분야 취약점 항목 계정관리, 파일 및 디렉터리 관리에서 중요도 \n\n"
                  "상, 중 20여개 항목을 선정하여 점검하는 프로그램\n\n"
                  "\n"
                 )

text_info.tag_config("bold", font=("Cambria", 12, "bold"))
text_info.tag_add("bold", "2.0", "2.30")
text_info.config(state=DISABLED)

#주의사항 설명
text_explain = Text(frame_explain, bg='white', height=20, width=75)
text_explain.place(x=35, y=65)
#text_info.grid(sticky="nsew", row=1, column=1, padx=10, pady=10)
text_explain.insert(END,
                  "\n"
                  "< L.Checker 사용 전 주의 사항 >\n\n"
                  "1. ssh server 설치 확인\n: sudo systemctl status openssh \n\n"
                  "2. 설치 되어 있지 않다면 설치\n: sudo apt-get update → sudo apt-get install openssh-server \n\n"
                  "3. 설치 완료시 상태 확인\n: sudo systemctl status openssh\n\n"
                  "4. 자신의 리눅스에 대한 정보 입력 (IP, ID, PASSWD)"
                  "\n"
                 )

text_explain.tag_config("bold", font=("Cambria", 12, "bold"))
text_explain.tag_add("bold", "2.0", "2.30")
text_explain.config(state=DISABLED)

#시작화면 버튼 - 메인버튼, 설명버튼
btn_gomain = Button(frame_start, width=10, text="시작", bg='white', command=lambda: [openFrame(frame_main)])
btn_gomain.place(x=320, y=250)
btn_goinfo = Button(frame_start, width=10, text="설명", bg='white', command=lambda: [openFrame(frame_info)])
btn_goinfo.place(x=200, y=250)

#메인화면 타이틀
main_title = Label(frame_main, text="L.Checker", bg='white', font=font_title)
main_title.place(x=210, y=30)

#ip입력받기
label_ip = Label(frame_main, text="IP : ", bg='white', font=font_main)
label_ip.place(x=110, y=130)

entry_ip = Entry(frame_main, width=35, font=font_main)
entry_ip.place(x=160, y=130)

#id입력받기
label_id = Label(frame_main, text="ID : ", bg='white', font=font_main)
label_id.place(x=110, y=190)

entry_id = Entry(frame_main, width=35, font=font_main)
entry_id.place(x=160, y=190)

#pw입력받기
label_pw = Label(frame_main, text="PW : ", bg='white', font=font_main)
label_pw.place(x=110, y=250)

entry_pw = Entry(frame_main, width=35, show='*', font=font_main)
entry_pw.place(x=160, y=250)

def show_error_message(msg):
    new = Toplevel(bg='white')
    new.title('Error')
    new.geometry('300x100+500+300')
    message = Label(new, text=msg, font=('Cambria', 12),bg='white')
    message.pack(pady=20)
    close_button = Button(new, width=10, text='닫기', bg='white', command=new.destroy)
    close_button.pack(pady=3)

def run_result_new():
    ssh, table_view = [], []
    data1, data2 = [], []
    try:
        # 사용명령어
        commands = [
            'wget https://github.com/pridejy/capstone/raw/main/test.py',
            'python3 test.py',
            # 'rm -rf test.py'
        ]
        # SSH 연결
        ssh = paramiko.SSHClient()
        ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
        ssh.connect(hostname=entry_ip.get(), port=22, username=entry_id.get(), password=entry_pw.get())

        for cmd in commands:
            stdin, stdout, stderr = ssh.exec_command(cmd)
            result_list = stdout.read().decode().split('\n')
            print(result_list)

            if cmd == 'python3 test.py':
                split_index = result_list.index("")

                account_security_raw = result_list[:split_index]
                file_security_raw = result_list[split_index + 1:]

                data1 = make_parsed_data(account_security_raw)
                data2 = make_parsed_data(file_security_raw)

        # tkinter 창 생성
        table_view = tk.Tk()
        table_view.title("L.Checker Result")
        table_view.geometry("700x700")
        # 제목 레이블 추가
        title_label = tk.Label(table_view, text="계정 보안 점검")
        title_label.pack()

        # 수직 분할 레이아웃을 위한 PanedWindow 생성
        paned = ttk.Panedwindow(table_view, orient=tk.VERTICAL)
        paned.pack(fill=tk.BOTH, expand=True)

        # 첫 번째 표 생성
        frame1 = ttk.Frame(paned)
        tree1 = ttk.Treeview(frame1, columns=("1", "2", "3"), show="headings")

        tree1.heading("1", text="항목")
        tree1.heading("2", text="설명")
        tree1.heading("3", text="상태")

        tree1.column("1", width=100)
        tree1.column("2", width=320)
        tree1.column("3", width=100)

        tree1.pack()

        # Treeview에 색상 설정
        tree1.tag_configure('green', background='green')
        tree1.tag_configure('red', background='red')

        # 데이터 추가
        for item in data1:
            if "양호" in item[2]:
                tree1.insert("", "end", values=item, tags=('green',))
            elif "취약" in item[2]:
                tree1.insert("", "end", values=item, tags=('red',))

        # 두 번째 표 생성
        frame2 = ttk.Frame(paned)
        title_label2 = tk.Label(frame2, text="파일 보안 점검")
        title_label2.pack()
        tree2 = ttk.Treeview(frame2, columns=("1", "2", "3"), show="headings")

        tree2.heading("1", text="항목")
        tree2.heading("2", text="설명")
        tree2.heading("3", text="상태")

        tree2.column("1", width=100)
        tree2.column("2", width=320)
        tree2.column("3", width=100)

        tree2.pack()

        tree1['height'] = len(data1)
        tree2['height'] = len(data2)

        tree2.tag_configure('green', background='green')
        tree2.tag_configure('red', background='red')

        # 데이터 추가
        for item in data2:
            if "양호" in item[2]:
                tree2.insert("", "end", values=item, tags=('green',))
            elif "취약" in item[2]:
                tree2.insert("", "end", values=item, tags=('red',))

        # PanedWindow에 프레임과 레이블 추가
        paned.add(frame1, weight=1)
        paned.add(frame2, weight=1)
        # 버튼 추가
        btn_view_contents = Button(table_view, text="점검 내용 보기", command=view_inspection_contents_new)
        btn_view_contents.pack(side=tk.RIGHT, padx=10, pady=10)  # 오른쪽 아래에 배치

        table_view.mainloop()
    except socket.error:
        show_error_message("IP주소가 틀렸습니다.")
    except paramiko.AuthenticationException:
        show_error_message("ID 혹은 PASSWD가 틀렸습니다.")
    except Exception as e:
        table_view.destroy()
        print(e)
    finally:
        ssh.close()
        table_view.deiconify() #결과 창 보이기

def view_inspection_contents_new():
    log_file_path = "~/checklinux/inspection_contents.log"
    table_data = []
    current_id = None
    current_condition = []
    current_description = []

    try:
        ssh = paramiko.SSHClient()
        ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
        ssh.connect(hostname=entry_ip.get(), port=22, username=entry_id.get(), password=entry_pw.get())

        stdin, stdout, stderr = ssh.exec_command(f"cat {log_file_path}")
        inspection_contents = stdout.read().decode('utf-8').split("\n")
        ssh.close()

        for i, line in enumerate(inspection_contents):
            line = line.strip()
            if line:
                if "조건" in line:
                    if current_id:
                        table_data.append([current_id, "\n".join(current_condition), "\n".join(current_description)])
                        current_condition, current_description = [], []
                    current_id = re.findall(r'U-\d{2}', line)
                elif "양호" in line or "취약" in line:
                    current_condition.append(line)
                elif line != '' and "======" not in line:
                    current_description.append(line)

        if current_id:
            table_data.append([current_id, "\n".join(current_condition), "\n".join(current_description)])

        # tkinter 윈도우 생성
        inspection_view = tk.Tk()
        inspection_view.title("점검 내용 표")
        inspection_view.geometry("1800x1000")
        style = ttk.Style(inspection_view)
        style.configure("mystyle.Treeview", rowheight=60)

        frame = Frame(inspection_view)
        frame.pack(fill='both', expand=True)


        # Treeview 표 생성
        tree3 = ttk.Treeview(frame, style='mystyle.Treeview', columns=("ID", "조건", "점검 내용"), show="headings")
        tree3.heading("ID", text="ID")
        tree3.heading("조건", text="조건")
        tree3.heading("점검 내용", text="점검 내용")

        tree3.column("ID", width=100)
        tree3.column("조건", width=900)
        tree3.column("점검 내용", width=600)

        tree3['height'] = 200

        # 데이터 추가
        for row in table_data:
            tree3.insert("", "end", values=row)

        tree3.pack()

        inspection_view.mainloop()
    except FileNotFoundError:
        print(f"로그 파일이 없습니다:{log_file_path}")

#점검 시작 버튼
button = Button(frame_main, width=10, text="실행", bg='white', command=lambda:run_result_new())
button.place(x=260, y=300)
#button.grid(row=4, column=2, padx=10, pady=10)

openFrame(frame_start)
root.mainloop()

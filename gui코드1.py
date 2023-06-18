from tkinter import *
from tkinter import Toplevel, Button
from tkinter import ttk
from threading import Thread
from tkinter.scrolledtext import ScrolledText

from tkinter import Tk, Canvas, PhotoImage

import paramiko
import tkinter.font
import socket
import threading
import time


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

def show_loading_bar(root):
    # 로딩바 생성
    progressbar = ttk.Progressbar(root, mode='determinate', maximum=100, length=300)
    progressbar.place(x=150, y=350)

    # 결과 윈도우 창
    new = Toplevel(bg='white')
    new.title('L.Checker Result')
    new.geometry('680x830+150+20')
    new.withdraw() # 결과 창 숨기기

    # 결과를 나타낼 text 위젯
    text_re = Text(new, bg='white', height=59, width=90)
    text_re.grid(row=6, column=2, padx=10, pady=10)

    # 결과 text 위젯 스크롤바
    scrollbar = Scrollbar(new)
    scrollbar.grid(row=6, column=3, sticky='NS', pady=10)
    text_re.config(yscrollcommand=scrollbar.set)
    scrollbar.config(command=text_re.yview)

    # 사용명령어
    commands = [
        # 'wget -P ~ https://raw.githubusercontent.com/pridejy/capstone/main/test.py',
        'python3 test2.py',
        # 'rm -rf test.py'
    ]

    def run_result():
        try:
            # SSH 연결
            ssh = paramiko.SSHClient()
            ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
            ssh.connect(hostname=entry_ip.get(), port=22, username=entry_id.get(), password=entry_pw.get())

            # 결과 text 위젯에 출력할 점검 내용별 글씨 색상
            for cmd in commands:
                stdin, stdout, stderr = ssh.exec_command(cmd)
                result_list = stdout.read().decode().split('\n')

                if cmd == 'python3 test2.py':
                    for result in result_list:
                        if "취약" in result:
                            index = result.find("|  취약  |")
                            text_re.insert(END, result[:index], 'black')
                            text_re.insert(END, result[index:] + '\n\n', 'red')
                        elif "양호" in result:
                            index = result.find("|  양호  |")
                            text_re.insert(END, result[:index], 'black')
                            text_re.insert(END, result[index:] + '\n\n', 'green')
                        else:
                            text_re.insert(END, result + '\n')



            btn_view_contents = Button(new, text="점검 내용 보기", command=view_inspection_contents)
            btn_view_contents.place(x=580, y=793)

            text_re.config(state=DISABLED)
            text_re.tag_configure('green', foreground='green')
            text_re.tag_configure('red', foreground='red')

        except socket.error:
            show_error_message("IP주소가 틀렸습니다.")
        except paramiko.AuthenticationException:
            show_error_message("ID 혹은 PASSWD가 틀렸습니다.")
        except Exception as e:
            new.destroy()
            print(e)
        finally:
            ssh.close()
            progressbar.place_forget()
            new.deiconify() #결과 창 보이기

    def update_loading_bar():
        progress = 0
        while progress < 100:
            progress += 1
            progressbar['value'] = progress
            progressbar.update()
            time.sleep(0.1)

        # 로딩 작업이 완료되면 결과 창 열기
        Thread(target=run_result).start()

    # 작업을 처리할 스레드 실행
    Thread(target=update_loading_bar).start()
def view_inspection_contents():
    log_file_path = "~/checklinux/inspection_contents.log"

    try:
        ssh = paramiko.SSHClient()
        ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
        ssh.connect(hostname=entry_ip.get(), port=22, username=entry_id.get(), password=entry_pw.get())

        stdin, stdout, stderr = ssh.exec_command(f"cat {log_file_path}")
        inspection_contents = stdout.read().decode('utf-8')

        ssh.close()

        new_window = Toplevel(bg='white')
        new_window.title("점검 내용 결과")
        new_window.geometry("700x830+700+20")

        text_widget = Text(new_window, bg='white', height=59, width=93)
        text_widget.insert(END, inspection_contents)
        text_widget.grid(row=6, column=2, padx=10, pady=10)

        scrollbar = Scrollbar(new_window)
        scrollbar.grid(row=6, column=3, sticky='NS', pady=10)
        text_widget.config(yscrollcommand=scrollbar.set)
        scrollbar.config(command=text_widget.yview)

        text_widget.config(state=DISABLED)

        btn_cls = Button(new_window, width=10, text='닫기', bg='white', command=new_window.destroy)
        btn_cls.place(x=610, y=793)
    except FileNotFoundError:
        print(f"로그 파일이 없습니다:{log_file_path}")


#점검 시작 버튼
button = Button(frame_main, width=10, text="실행", bg='white', command=lambda:show_loading_bar(root))
button.place(x=260, y=300)
#button.grid(row=4, column=2, padx=10, pady=10)

openFrame(frame_start)
root.mainloop()

import subprocess
from datetime import datetime

def NOTICE():
	print('[OK] : 양호')
	print('[WARN] : 취약')
	print('[INFO] : 정보')

def OK(msg):
	print(f'\033[32m[양호]:{msg} \033[0m')

def WARN(msg):
	print(f'\033[31m[취약]:{msg} \033[0m')

def INFO(msg):
	print(f'\033[35m[정보]:{msg} \033[0m')

def CODE(msg):
	print(f'\033[36m{msg} \33[0m')

def run_msg(msg):
	return subprocess.Popen(
		msg, stdout=subprocess.PIPE,stderr=subprocess.PIPE, shell=True).communicate()

##U-05
CODE('[U-05 root 홈, 패스 디렉터리 권한 및 패스 설정]')
OUTPUT,_ = run_msg('echo $PATH')
CHECK = any(x in OUTPUT.decode('utf-8') for x in['\.:','::',':.:'])
if not CHECK:
	OK('PATH 환경변수에 “.” 이 맨 앞이나 중간에 포함되지 않은 경우\n')
else:
	WARN('PATH 환경변수에 “.” 이 맨 앞이나 중간에 포함되지 않은 경우\n')

##U-06
CODE('[U-06 파일 및 디렉터리 소유자 설정]')
CHECK = run_msg("find / \( -nouser -o -nogroup \) -print ")
if not CHECK:
	OK('소유자가 존재하지 않는 파일 및 디렉터리가 존재하지 않는 경우\n')
else:
	WARN('소유자가 존재하지 않는 파일 및 디렉터리가 존재하는 경우\n')

##U-07
CODE('[U-07 /etc/passwd 파일 소유자 및 권한 설정]')
OUTPUT1,_ = run_msg('ls -l /etc/passwd')
CHECK1=OUTPUT1.decode('utf-8').split()[2]
OUTPUT2,_= run_msg('stat -c"%a" /etc/passwd')
CHECK2=int(OUTPUT2.decode('utf-8'))
if CHECK1 == 'root' and CHECK2 <= 644:
	OK('/etc/passwd 파일의 소유자가 root이고, 권한이 644인 이하인 경우\n')
else:
	WARN ('/etc/passwd 파일의 소유자가 root가 아니거나, 권한이 644 이상인 경우\n')

##U-08
CODE('[U-08 /etc/shadow 파일 소유자 및 권한 설정]')
OUTPUT1,_ = run_msg('ls -l /etc/shadow')
CHECK1=OUTPUT1.decode('utf-8').split()[2]
OUTPUT2,_= run_msg('stat -c"%a" /etc/shadow')
CHECK2=int(OUTPUT2.decode('utf-8'))
if CHECK1 == 'root' and CHECK2 <= 400:
	OK('/etc/shadow 파일의 소유자가 root이고, 권한이 400인 이하인 경우\n')
else:
	WARN ('/etc/shadow 파일의 소유자가 root가 아니거나, 권한이 400 이상인 경우\n')

##U-09
CODE('[U-09 /etc/hosts 파일 소유자 및 권한 설정]')
OUTPUT1,_ = run_msg('ls -l /etc/hosts')
CHECK1=OUTPUT1.decode('utf-8').split()[2]
OUTPUT2,_= run_msg('stat -c"%a" /etc/hosts')
CHECK2=int(OUTPUT2.decode('utf-8'))
if CHECK1 == 'root' and CHECK2 <= 600:
	OK('/etc/hosts 파일의 소유자가 root이고, 권한이 600인 이하인 경우\n')
else:
	WARN ('/etc/hosts 파일의 소유자가 root가 아니거나, 권한이 600 이상인 경우\n')

##U-10
#CODE('[U-10 /etc/xinetd.conf 파일 소유자 및 권한 설정]')
#OUTPUT1,_ = run_msg('ls -l /etc/xinetd.conf')
#CHECK1=OUTPUT1.decode('utf-8').split()[2]
#OUTPUT2,_= run_msg('stat -c"%a" /etc/xinetd.conf')
#CHECK2=int(OUTPUT2.decode('utf-8'))
#if CHECK1 == 'root' and CHECK2 <= 600:
#	OK('/etc/xinetd.conf 파일의 소유자가 root이고, 권한이 600인 이하인 경우\n')
#else:
#	WARN ('/etc/xinetd.xonf 파일의 소유자가 root가 아니거나, 권한이 600 이상인 경우\n')

##U-11
CODE('[U-11 /etc/rsyslog.conf 파일 소유자 및 권한 설정]')
OUTPUT1,_ = run_msg('ls -l /etc/rsyslog.conf')
CHECK1=OUTPUT1.decode('utf-8').split()[2]
OUTPUT2,_= run_msg('stat -c"%a" /etc/rsyslog.conf')
CHECK2=int(OUTPUT2.decode('utf-8'))
if CHECK1 == 'root' and CHECK2 <= 600:
	OK('/etc/rsyslog.conf 파일의 소유자가 root이고, 권한이 600인 이하인 경우\n')
else:
	WARN ('/etc/rsyslog.conf 파일의 소유자가 root가 아니거나, 권한이 600 이상인 경우\n')

##U-12
CODE('[U-12 /etc/services 파일 소유자 및 권한 설정]')
OUTPUT1,_ = run_msg('ls -l /etc/services')
CHECK1=OUTPUT1.decode('utf-8').split()[2]
OUTPUT2,_= run_msg('stat -c"%a" /etc/services')
CHECK2=int(OUTPUT2.decode('utf-8'))
if CHECK1 == 'root' and CHECK2 <= 600:
	OK('/etc/services 파일의 소유자가 root이고, 권한이 600인 이하인 경우\n')
else:
	WARN ('/etc/services 파일의 소유자가 root가 아니거나, 권한이 600 이상인 경우\n')

##U-13
CODE('[U-13 SUID, SGID, Sticky bit 설정 파일 점검 ]')

##U-14
CODE('[U-14 사용자, 시스템 시작파일 및 환경파일 소유자 및 권한 설정]')

##U-15
CODE('[U-15 world writable 파일 점검]')

##U-16
CODE('[U-16 /dev에 존재하지 않는 deivce 파일 점검]')

##U-17
CODE('[U-17 $HOME/.rhosts, hosts.equiv 사용금지]')

##U-18
CODE('[U-18 접속 IP 및 포트 제한]')

import os
import subprocess
import unicodedata

def NOTICE():
    print('[OK] : 양호')
    print('[WARN] : 취약')

def OK():
    print(f'양호')

def WARN():
    print(f'취약')

def CODE(msg):
    print(f'{msg}')

def divider():
    print("=" * 70)

def run_msg(msg):
        return subprocess.Popen(
                msg, stdout=subprocess.PIPE,stderr=subprocess.PIPE, shell=True).communicate()

#checklinux 폴더 생성
if not os.path.exists("checklinux"):
    os.mkdir("checklinux")

inspection_log_path = os.path.expanduser("~/checklinux/inspection_contents.log")

CODE_MAX_LENGTH = 5  # 'CODE' 요소의 최대 크기
CONTENT_MAX_LENGTH = 30  # 'CONTENT' 요소의 최대 크기
PADDING_CHAR = ' '  # 패딩으로 사용할 문자

data = {
    'CODE': ['U-01', 'U-02', 'U-03', 'U-04', 'U-44', 'U-46', 'U-47', 'U-48', 'U-52'],
    'CONTENT': ['root 계정 원격 접속 제한', '패스워드 복잡성 설정', '계정 임계값 설정', '패스워드 파일 보호', 'root 이외의 UID가 0 금지', '패스워드 최소 길이 설정', '패스워드 최대 사용기간 설정', '패스워드 최소 사용기간 설정', '동일한 UID 금지'],
    'RESULT': ['', '', '', '', '', '', '', '', '']
}

for i in range(len(data['CONTENT'])):
    # 'CONTENT' 요소 크기 조정
    data['CONTENT'][i] = data['CONTENT'][i][:CONTENT_MAX_LENGTH].ljust(CONTENT_MAX_LENGTH, PADDING_CHAR)

    

def get_display_width(text):
    return sum(1 + (unicodedata.east_asian_width(c) in ('F', 'W')) for c in text)

def print_table(data):
    column_width = [max(get_display_width(str(value)) for value in column) for column in data.values()]
    separator = '-' * (sum(column_width) + 3 * (len(data) - 1) + 4)

    print("\n[1. 계정 관리]")
    print(separator)
    for key, width in zip(data.keys(), column_width):
        print(f'| {key:<{width}} ', end='')
    print('|')
    print(separator)

    for i in range(len(data['CODE'])):
        for key, width in zip(data.keys(), column_width):
            value = data[key][i]
            padding = width - get_display_width(str(value))
            print(f'| {value}{" " * padding} ', end='')
        print('|')

    print(separator)

#[1.계정 관리]
#U-01

log_file_path = os.path.expanduser("~/checklinux/U-01.log")

try:
    check = subprocess.check_output(['cat', '/etc/securetty', '|', 'grep', 'pts'], stderr=subprocess.DEVNULL).decode().strip()
except subprocess.CalledProcessError:
    check = ''

try:
    result = subprocess.check_output(['cat', '/etc/securetty'], stderr=subprocess.DEVNULL).decode().strip()
except subprocess.CalledProcessError:
    result = ''

#점검 내용 파일 생성
with open(log_file_path, 'w') as f:
    f.write("="*30 + " U-01 조건 " + "="*30 + "\n")
    f.write('[양호]:원격 서비스를 사용하지 않거나 사용 시 직접 접속을 차단한 경우\n')
    f.write('[취약]:원격 터미널 사용 시 root 직접 접속을 허용한 경우\n')
    if os.path.exists('/etc/securetty'):
        if check == 0:
            data['RESULT'][0] = ' 취약 ' 
        else:
            data['RESULT'][0] = ' 양호 '
        f.write("="*30 + " U-01 점검 내용 " + "="*30 + "\n")
        f.write(f'{result}')

    else:
        data['RESULT'][0] = ' 취약 '
        f.write("="*30 + " U-01 점검 내용 " + "="*30 + "\n")
        f.write("파일이 존재하지 않습니다.")

with open(log_file_path, 'r') as u01_file:
    u01_contents = u01_file.read()

with open(inspection_log_path, 'w') as inspection_file:
    inspection_file.write(u01_contents)
    inspection_file.write('\n\n')

#U-02
log_file_path = os.path.expanduser("~/checklinux/U-02.log")
filename = '/etc/security/pwquality.conf'

minlen = None
credit_lines = []
info_printed = False

if os.path.isfile(filename):
    with open(filename, 'r') as f:
        lines = f.readlines()

    for line in lines:
        if "=" in line:
            if "minlen" in line and "#" in line:
                data['RESULT'][1] = ' 취약 '
                continue

            if "credit" in line and "#" in line:
                data['RESULT'][1] = ' 취약 '
                break

            if "minlen" in line:
                if "#" not in line:
                    minlen = int(line.split()[2])

            if "credit" in line:
                if "#" not in line:
                    credit_value = int(line.split()[2])
                    if credit_value == -1:
                        credit_lines.append(line)

                if minlen is not None and credit_lines is not None:
                    if minlen >= 8:
                        data['RESULT'][1] = ' 양호 '
                        if len(credit_lines) <= 2:
                            data['RESULT'][1] = ' 취약 '
                    elif not info_printed:
                        data['RESULT'][1] = ' 취약 '
                        info_printed = True
                    break

    with open(log_file_path, 'w') as f:
        f.write("="*30 + " U-02 조건 " + "="*30 + "\n")
        f.write('[양호]:패스워드 최소길이 8자리 이상, 영문, 숫자, 특수문자 최소 입력 기능이 설정된 경우\n')
        f.write('[취약]:패스워드 최소길이 8자리 이상, 영문, 숫자, 특수문자 최소 입력 기능이 설정되지 않은 경우\n')

        f.write("="*30 + "U-02 점검 내용" + "="*30 + "\n")
        for line in lines:
            if any(option in line for option in ["minlen", "credit"]):
                if "=" in line:
                    f.write(line)

else:
    data['RESULT'][1] = ' 취약 '
    with open(log_file_path, 'w') as f:
        f.write("="*30 + " U-02 조건 " + "="*30 + "\n")
        f.write('[양호]:패스워드 최소길이 8자리 이상, 영문, 숫자, 특수문자 최소 입력 기능이 설정된 경우\n')
        f.write('[취약]:패스워드 최소길이 8자리 이상, 영문, 숫자, 특수문자 최소 입력 기능이 설정되지 않은 경우\n')
        f.write("="*30 + " U-02 점검 내용 " + "="*30 + "\n")
        f.write(f"파일 '{filename}'이(가) 존재하지 않습니다.")


with open(log_file_path, 'r') as u02_file:
    u02_contents = u02_file.read()

with open(inspection_log_path, 'a') as inspection_file:
    inspection_file.write(u02_contents)
    inspection_file.write('\n\n')

#U-03
log_file_path = os.path.expanduser("~/checklinux/U-03.log")
filelist = ['/etc/pam.d/system-auth', '/etc/pam.d/common-auth']

for file in filelist:
    if os.path.isfile(file):
        with open(file) as f:
            content = f.read()


        with open(log_file_path, 'w') as f:
            f.write("="*30 + " U-03 조건 " + "="*30 + "\n")
            f.write('[양호]:계정 잠금 임계값이 10회 이하의 값으로 설정되어 있는 경우\n')
            f.write('[취약]:계정 잠금 임계값이 설정되어 있지 않거나, 10회 이하의 값으로 설정되지 않은 경우\n')
            if 'pam_tally.so' in content or 'pam_tally2.so' in content:
                LINES = [line for line in content.split('\n') if 'pam_tally.so' in line]
                for line in LINES:
                    PARTS = line.split()
                    for part in PARTS:
                        if part.startswith('deny='):
                            VALUE = int(part.split('=')[1])
                            if VALUE <= 10:
                                data['RESULT'][2] = ' 양호 '
                            else:
                                data['RESULT'][2] = ' 취약 '
            else:
                data['RESULT'][2] = ' 취약 '

            f.write("="*30 + " U-03 점검 내용 " + "="*30 + "\n")
            if 'pam_tally.so' in content or 'pam_tally2.so' in content:
                f.write(line)
            else:
                f.write(f"{file} 내용을 확인하세요\n")
        break

else:
    data['RESULT'][2] = ' 취약 '
    f.write("파일이 존재하지 않습니다.\n")

with open(log_file_path, 'r') as u03_file:
    u03_contents = u03_file.read()

with open(inspection_log_path, 'a') as inspection_file:
    inspection_file.write(u03_contents)
    inspection_file.write('\n\n')

#U-04
log_file_path = os.path.expanduser("~/checklinux/U-04.log")

FILENAME1 = '/etc/shadow'
FILENAME2 = '/etc/passwd'

with open(log_file_path, 'w') as f:
    f.write("="*30 + " U-04 조건 " + "="*30 + "\n")
    f.write('[양호]:쉐도우 패스워드를 사용하거나, 패스워드를 암호화하여 저장하는 경우\n')
    f.write('[취약]:쉐도우 패스워드를 사용하지 않고, 패스워드를 암호화하여 저장하지 않는 경우\n')

    if os.path.isfile(FILENAME1):
        data['RESULT'][3] = ' 양호 '
        with open(FILENAME2, 'r') as f2:
            for line in f2:
                passwd_field = line.split(':')[1]
                if passwd_field != 'x':
                    data['RESULT'][3] = ' 취약 '
                    break
            else:
                data['RESULT'][3] = ' 양호 '
    else:
        data['RESULT'][3] = ' 취약 '

    f.write("="*30 + " U-04 점검 내용 " + "="*30 + "\n")
    with open(FILENAME2, 'r') as f2:
        lines = f2.readlines()
        f.write(''.join(lines[-3:]).rstrip())

with open(log_file_path, 'r') as u04_file:
    u04_contents = u04_file.read()

with open(inspection_log_path, 'a') as inspection_file:
    inspection_file.write(u04_contents)
    inspection_file.write('\n\n')

#U-44

log_file_path = os.path.expanduser("~/checklinux/U-44.log")

FILENAME = "/etc/passwd"

with open(log_file_path, 'w') as f:
    f.write("="*30 + " U-44 조건 " + "="*30 + "\n")
    f.write("[양호]:root 계정과 동일한 UID를 갖는 계정이 존재하지 않는 경우\n")
    f.write("[취약]:root 계정과 동일한 UID를 갖는 걔정이 존재하는 경우\n")

    with open(FILENAME, 'r') as f2:
        check = 0
        for line in f2:
            fields = line.strip().split(':')
            if fields[2] == '0' and fields[0] != 'root':
                check += 1
                data['RESULT'][4] = ' 취약 '
                break
        if check == 0:
            data['RESULT'][4] = ' 양호 '

    f.write("="*30 + " U-44 점검 내용 " + "="*30 + "\n")
    with open(FILENAME, 'r') as f2:
        lines = f2.readlines()
        f.write(''.join(lines[:]).rstrip())

with open(log_file_path, 'r') as u44_file:
    u44_contents = u44_file.read()

with open(inspection_log_path, 'a') as inspection_file:
    inspection_file.write(u44_contents)
    inspection_file.write('\n\n')

#U-46
log_file_path = os.path.expanduser("~/checklinux/U-46.log")

FILENAME = '/etc/login.defs'

with open(log_file_path, 'w') as f:
    f.write("="*30 + " U-46 조건 " + "="*30 + "\n")
    f.write("[양호]:패스워드 최소 길이가 8자 이상으로 설정되어 있는 경우\n")
    f.write("[취약]:패스워드 최소 길이가 8자 미만으로 설정되어 있는 경우\n")

    lenline = None

    with open(FILENAME) as f2:
        for line in f2:
            if line.startswith('PASS_MIN_LEN'):
                lenline = line.strip()
                break

    if lenline:
        if '#' in line:
            data['RESULT'][5] = ' 취약 '
        else:
            parts = lenline.split()
            if len(parts) >= 2 and int(parts[1]) >= 8:
                data['RESULT'][5] = ' 양호 '
            else:
                data['RESULT'][5] = ' 취약 '

        f.write("="*30 + " U-46 점검 내용 " + "="*30 + "\n")
        f.write(lenline + '\n')

    else:
        data['RESULT'][5] = ' 취약 '
        f.write("="*30 + " U-46 점검 내용 " + "="*30 + "\n")
        f.write("설정되어있지 않습니다.\n/etc/login.defs 파일에 PASS_MIN_LEN을 확인해주세요.\n")

with open(log_file_path, 'r') as u46_file:
    u46_contents = u46_file.read()

with open(inspection_log_path, 'a') as inspection_file:
    inspection_file.write(u46_contents)
    inspection_file.write('\n\n')

#U-47
log_file_path = os.path.expanduser("~/checklinux/U-47.log")

FILENAME = "/etc/login.defs"

with open(log_file_path, 'w') as f:
    f.write("="*30 + " U-47 조건 " + "="*30 + "\n")
    f.write("[양호]:패스워드 최대 사용기간이 90일(12주) 이하로 설정되어 있는 경우\n")
    f.write("[취약]:패스워드 최대 사용기간이 90일(12주) 이하로 설정되어 있지 않은 경우\n")

    with open(FILENAME) as f2:
        for line in f2:
            if line.startswith('PASS_MAX_DAYS'):
                CHECK = int(line.split()[1])
                break

    if CHECK >= 90:
        data['RESULT'][6] = ' 취약 '
    else:
        data['RESULT'][6] = ' 양호 '

    f.write("="*30 + " U-47 점검 내용 " + "="*30 + "\n")
    with open(FILENAME, 'r') as f2:
        lines = f2.readlines()
        for line in lines:
            if line.startswith('PASS_MAX_DAYS'):
                f.write(line.strip())

with open(log_file_path, 'r') as u47_file:
    u47_contents = u47_file.read()

with open(inspection_log_path, 'a') as inspection_file:
    inspection_file.write(u47_contents)
    inspection_file.write('\n\n')

#U-48
log_file_path = os.path.expanduser("~/checklinux/U-48.log")

FILENAME = "/etc/login.defs"

with open(log_file_path, 'w') as f:
    f.write("="*30 + " U-48 조건 " + "="*30 + "\n")
    f.write("[양호]:패스워드 최소 사용기간이 1일 이상 설정되어 있는 경우\n")
    f.write("[취약]:패스워드 최소 사용기간이 설정되어 있지 않은 경우\n")

    with open(FILENAME) as f2:
        for line in f2:
            if line.startswith('PASS_MIN_DAYS'):
                CHECK = int(line.split()[1])
                break

    if CHECK >= 1:
        data['RESULT'][7] = ' 양호 '
    else:
        data['RESULT'][7] = ' 취약 '

    f.write("="*30 + " U-48 점검 내용 " + "="*30 + "\n")
    with open(FILENAME, 'r') as f2:
        lines = f2.readlines()
        for line in lines:
            if line.startswith('PASS_MIN_DAYS'):
                f.write(line.strip())

with open(log_file_path, 'r') as u48_file:
    u48_contents = u48_file.read()

with open(inspection_log_path, 'a') as inspection_file:
    inspection_file.write(u48_contents)
    inspection_file.write('\n\n')

#U-52
log_file_path = os.path.expanduser("~/checklinux/U-52.log")

FILENAME = "/etc/passwd"

with open(log_file_path, 'w') as f:
    f.write("="*30 + " U-52 조건 " + "="*30 + "\n")
    f.write("[양호]:동일한 UID로 설정된 사용자 계정이 존재하지 않는 경우\n")
    f.write("[취약]:동일한 UID로 설정된 사용자 걔정이 존재하는 경우\n")

    with open(FILENAME, 'r') as f2:
        uid_list = []
        for line in f2:
            uid = line.split(":")[2]
            uid_list.append(uid)

    if len(uid_list) == len(set(uid_list)):
        data['RESULT'][8] = ' 양호 '
    else:
        data['RESULT'][8] = ' 취약 '

    f.write("="*30 + " U-52 점검 내용 " + "="*30 + "\n")
    with open(FILENAME, 'r') as f2:
        lines = f2.readlines()
        f.write(''.join(lines[:]).rstrip())

with open(log_file_path, 'r') as u52_file:
    u52_contents = u52_file.read()

with open(inspection_log_path, 'a') as inspection_file:
    inspection_file.write(u52_contents)
    inspection_file.write('\n\n')

print_table(data)

CODE_MAX_LENGTH = 5  # 'CODE' 요소의 최대 크기
CONTENT_MAX_LENGTH = 35  # 'CONTENT' 요소의 최대 크기
PADDING_CHAR = ' '  # 패딩으로 사용할 문자

data = {'CODE': ['U-05', 'U-06', 'U-07', 'U-08', 'U-09', 'U-10', 'U-11', 'U-12', 'U-13', 'U-14', 'U-15', 'U-16', 'U-17', 'U-18', 'U-56', 'U-57', 'U-58'],
        'CONTENT': ['root 홈, 패스 디렉터리 권한 및 패스 설정', '파일 및 디렉터리 소유자 설정', '/etc/passwd 파일 소유자 및 권한 설정', '/etc/shadow 파일 소유자 및 권한 설정', '/etc/hosts 파일 소유자 및 권한 설정', '/etc/xinetd.conf 파일 소유자 및 권한 설정', '/etc/syslog.conf 파일 소유자 및 권한 설정', '/etc/services 파일 소유자 및 권한 설정', 'SUID, SGID, Sticky bit 설정 파일 점검', '사용자, 시스템 시작파일 및 환경파일 소유자 및 권한 설정', 'world writable 파일 점검', '/dev에 존재하지 않는 deivce 파일 점검', '$HOME/.rhosts, hosts.equiv 사용 금지', '접속 IP 및 포트 제한', 'UMASK 설정 관리', '홈 디렉토리 소유자 및 권한 설정', '홈 디렉토리로 지정한 디렉토리의 존재 관리'],
        'RESULT': ['', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '']}

for i in range(len(data['CONTENT'])):
    # 'CONTENT' 요소 크기 조정
    data['CONTENT'][i] = data['CONTENT'][i][:CONTENT_MAX_LENGTH].ljust(CONTENT_MAX_LENGTH, PADDING_CHAR)

# 표 출력 함수

def print_table(data):
    column_width = [max(get_display_width(str(value)) for value in column) for column in data.values()]
    separator = '-' * (sum(column_width) + 3 * (len(data) - 1) + 4)

    print("\n\n[2. 파일 및 디렉터리 관리]")
    print(separator)
    for key, width in zip(data.keys(), column_width):
        print(f'| {key:<{width}} ', end='')
    print('|')
    print(separator)

    for i in range(len(data['CODE'])):
        for key, width in zip(data.keys(), column_width):
            value = data[key][i]
            padding = width - get_display_width(str(value))
            print(f'| {value}{" " * padding} ' , end='')
        print('|')
        
    print(separator)

#U-05
log_file_path = os.path.expanduser("~/checklinux/U-05.log")

path = os.popen('echo $PATH').read().strip()

with open(log_file_path, 'w') as f:
    f.write("="*30 + " U-05 조건 " + "="*30 + "\n")
    f.write("[양호]:PATH 환경변수에 . 이 맨 앞이나 중간에 포함되지 않은 경우\n")
    f.write("[취약]:PATH 환경변수에 . 이 맨 앞이나 중간에 포함되어 있는 경우\n")

    if path.startswith('.'):
        data['RESULT'][0] = ' 취약 '
    elif '.:' in path or '::' in path:
        data['RESULT'][0] = ' 취약 '
    else:
        data['RESULT'][0] = ' 양호 '

    f.write("="*30 + " U-05 점검 내용 " + "="*30 + "\n")
    f.write(f'{path}')

with open(log_file_path, 'r') as u05_file:
    u05_contents = u05_file.read()

with open(inspection_log_path, 'a') as inspection_file:
    inspection_file.write(u05_contents)
    inspection_file.write('\n\n')

#U-06

log_file_path = os.path.expanduser("~/checklinux/U-06.log")

CHECK = os.popen("find / -type d -nouser -nogroup -print 2>&1").read().strip()
CHECK_LINES = CHECK.count('\n') if CHECK else 0

with open(log_file_path, 'w') as f:
    f.write("="*30 + " U-06 조건 " + "="*30 + "\n")
    f.write("[양호]:소유자가 존재하지 않는 파일 및 디렉터리가 존재하지 않는 경우\n")
    f.write("[취약]:소유자가 존재하지 않는 파일 및 디렉터리가 존재하는 경우\n")

    if CHECK_LINES == 0:
        data['RESULT'][1] = ' 양호 '
    else:
        data['RESULT'][1] = ' 취약 '

    f.write("="*30 + " U-06 점검 내용 " + "="*30 + "\n")
    if CHECK_LINES > 0:
        f.write(f"{CHECK_LINES}개의 소유자가 존재하지 않는 파일 및 디렉터리가 있습니다.\n")
        f.write("find / -type d -nouser - nogroup -print를 통하여 확인하세요.\n")
    else:
        f.write("소유자가 존재하지 않는 파일 및 디렉터리가 없습니다.")

with open(log_file_path, 'r') as u06_file:
    u06_contents = u06_file.read()

with open(inspection_log_path, 'a') as inspection_file:
    inspection_file.write(u06_contents)
    inspection_file.write('\n\n')


#U-07
log_file_path = os.path.expanduser("~/checklinux/U-07.log")

OUTPUT1 = os.popen('ls -l /etc/passwd').read().strip()
CHECK1 = OUTPUT1.split()[2]
OUTPUT2 = os.popen('stat -c"%a" /etc/passwd').read().strip()
CHECK2 = int(OUTPUT2)

with open(log_file_path, 'w') as f:
    f.write("="*30 + " U-07 조건 " + "="*30 + "\n")
    f.write("[양호]:/etc/passwd 파일의 소유자가 root이고, 권한이 644이하인 경우\n")
    f.write("[취약]:/etc/passwd 파일의 소유자가 root가 아니거나, 권한이 644이하가 아닌 경우\n")

    if CHECK1 == 'root' and CHECK2 <= 644:
        data['RESULT'][2] = ' 양호 '
    else:
        data['RESULT'][2] = ' 취약 '

    f.write("="*30 + " U-07 점검 내용 " + "="*30 + "\n")
    f.write(f'{OUTPUT1}')

    if not OUTPUT1:
        data['RESULT'][2] = ' 취약 '
        f.write("해당 파일이 존재하지 않습니다.")

with open(log_file_path, 'r') as u07_file:
    u07_contents = u07_file.read()

with open(inspection_log_path, 'a') as inspection_file:
    inspection_file.write(u07_contents)
    inspection_file.write('\n\n')

#U-08
log_file_path = os.path.expanduser("~/checklinux/U-08.log")

OUTPUT1 = os.popen('ls -l /etc/shadow').read().strip()
CHECK1 = OUTPUT1.split()[2]
OUTPUT2 = os.popen('stat -c"%a" /etc/shadow').read().strip()
CHECK2 = int(OUTPUT2)

with open(log_file_path, 'w') as f:
    f.write("="*30 + " U-08 조건 " + "="*30 + "\n")
    f.write("[양호]:/etc/shadow 파일의 소유자가 root이고, 권한이 400 이하인 경우\n")
    f.write("[취약]:/etc/shadow 파일의 소유자가 root가 아니거나, 권한이 400 이하가 아닌 경우\n")

    if CHECK1 == 'root' and CHECK2 <= 400:
        data['RESULT'][3] = ' 양호 '
    else:
        data['RESULT'][3] = ' 취약 '

    f.write("="*30 + " U-08 점검 내용 " + "="*30 + "\n")
    f.write(f'{OUTPUT1}')
    
    if not OUTPUT1:
        data['RESULT'][3] = ' 취약 '
        f.write("해당 파일이 존재하지 않습니다.")

with open(log_file_path, 'r') as u08_file:
    u08_contents = u08_file.read()

with open(inspection_log_path, 'a') as inspection_file:
    inspection_file.write(u08_contents)
    inspection_file.write('\n\n')


#U-09
log_file_path = os.path.expanduser("~/checklinux/U-09.log")

OUTPUT1 = os.popen('ls -l /etc/hosts').read().strip()
CHECK1 = OUTPUT1.split()[2]
OUTPUT2 = os.popen('stat -c"%a" /etc/hosts').read().strip()
CHECK2 = int(OUTPUT2)

with open(log_file_path, 'w') as f:
    f.write("="*30 + " U-09 조건 " + "="*30 + "\n")
    f.write("[양호]:/etc/hosts 파일의 소유자가 root이고, 권한이 600 이하인 경우\n")
    f.write("[취약]:/etc/hosts 파일의 소유자가 root가 아니거나, 권한이 600 이하가 아닌 경우\n")

    if CHECK1 == 'root' and CHECK2 <= 600:
        data['RESULT'][4] = ' 양호 '
    else:
        data['RESULT'][4] = ' 취약 '

    f.write("="*30 + " U-09 점검 내용 " + "="*30 + "\n")
    f.write(f'{OUTPUT1}')

    if not OUTPUT1:
        data['RESULT'][4] = ' 취약 '
        f.write("해당 파일이 존재하지 않습니다.")

with open(log_file_path, 'r') as u09_file:
    u09_contents = u09_file.read()

with open(inspection_log_path, 'a') as inspection_file:
    inspection_file.write(u09_contents)
    inspection_file.write('\n\n')

#U-10
log_file_path = os.path.expanduser("~/checklinux/U-10.log")

filelist = ['/etc/xinetd.conf', '/etc/inetd.conf']
for file in filelist:
    if os.path.exists(file):
        OUTPUT1 = os.popen('ls -l ' + file).read().strip()
        CHECK1 = OUTPUT1.split()[2]
        OUTPUT2 = os.popen('stat -c"%a" ' + file).read().strip()
        CHECK2 = int(OUTPUT2)

        with open(log_file_path, 'w') as f:
            f.write("="*30 + " U-10 조건 " + "="*30 + "\n")
            f.write("[양호]:/etc/(x)inetd.conf 파일의 소유자가 root이고, 권한이 600 이하인 경우\n")
            f.write("[취약]:/etc/(x)inetd.conf 파일의 소유자가 root가 아니거나, 권한이 600 이하가 아닌 경우\n")


            if CHECK1 == 'root' and CHECK2 <= 600:
                data['RESULT'][5] = ' 양호 '
            else:
                data['RESULT'][5] = ' 취약 '

            f.write("="*30 + " U-10 점검 내용 " + "="*30 + "\n")
            f.write(f'{OUTPUT1}')

            if not OUTPUT1:
                data['RESULT'][5] = ' 취약 '
                f.write("="*30 + " U-10 점검 내용 " + "="*30 + "\n")
                f.write("해당 파일이 존재하지 않습니다.")

with open(log_file_path, 'r') as u10_file:
    u10_contents = u10_file.read()

with open(inspection_log_path, 'a') as inspection_file:
    inspection_file.write(u10_contents)
    inspection_file.write('\n\n')

#U-11
log_file_path = os.path.expanduser("~/checklinux/U-11.log")

filelist = ['/etc/rsyslog.conf', '/etc/syslog.conf']
for file in filelist:
    if os.path.exists(file):
        OUTPUT1 = os.popen('ls -l ' + file).read().strip()
        CHECK1 = OUTPUT1.split()[2]
        OUTPUT2 = os.popen('stat -c"%a" ' + file).read().strip()
        CHECK2 = int(OUTPUT2)

        with open(log_file_path, 'w') as f:
            f.write("="*30 + " U-11 조건 " + "="*30 + "\n")
            f.write("[양호]:/etc/(r)syslog.conf 파일의 소유자가 root(또는 bin, sys)이고, 권한이 640 이하인 경우\n")
            f.write("[취약]:/etc/(r)syslog.conf 파일의 소유자가 root(또는 bin, sys)가 아니거나, 권한이 640 이하가 아닌 경우\n")

            if CHECK1 == 'root' or CHECK1 == 'bin' or CHECK1 == 'sys': 
                if CHECK2 <= 640:
                    data['RESULT'][6] = ' 양호 '
                else:
                    data['RESULT'][6] = ' 취약 '

            else:
                data['RESULT'][6] = ' 취약 '
            
            f.write("="*30 + " U-11 점검 내용 " + "="*30 + "\n")
            f.write(f'{OUTPUT1}')

            if not OUTPUT1:
                data['RESULT'][6] = ' 취약 '
                f.write("="*30 + " U-11 점검 내용 " + "="*30 + "\n")
                f.write("해당 파일이 존재하지 않습니다.")

with open(log_file_path, 'r') as u11_file:
    u11_contents = u11_file.read()

with open(inspection_log_path, 'a') as inspection_file:
    inspection_file.write(u11_contents)
    inspection_file.write('\n\n')

#U-12
log_file_path = os.path.expanduser("~/checklinux/U-12.log")

OUTPUT1 = os.popen('ls -l /etc/services').read().strip()
CHECK1 = OUTPUT1.split()[2]
OUTPUT2 = os.popen('stat -c"%a" /etc/services').read().strip()
CHECK2 = int(OUTPUT2)

with open(log_file_path, 'w') as f:
    f.write("="*30 + " U-12 조건 " + "="*30 + "\n")
    f.write("[양호]:/etc/services 파일의 소유자가 root(또는 bin, sys)이고, 권한이 644 이하인 경우\n")
    f.write("[취약]:/etc/services 파일의 소유자가 root(또는 bin, sys)가 아니거나, 권한이 644 이하가 아닌 경우\n")

    if CHECK1 == 'root' or CHECK1 == 'bin' or CHECK1 == 'sys' and CHECK2 <= 644:
        data['RESULT'][7] = ' 양호 '
    else:
        data['RESULT'][7] = ' 취약 '

    f.write("="*30 + " U-12 점검 내용 " + "="*30 + "\n")
    f.write(f'{OUTPUT1}')

    if not OUTPUT1:
        data['RESULT'][7] = ' 취약 '
        f.write("해당 파일이 존재하지 않습니다.")

with open(log_file_path, 'r') as u12_file:
    u12_contents = u12_file.read()

with open(inspection_log_path, 'a') as inspection_file:
    inspection_file.write(u12_contents)
    inspection_file.write('\n\n')

#U-13

log_file_path = os.path.expanduser("~/checklinux/U-13.log")

CHECK = os.popen(' find / -user root -type f \( -perm -4000 -o -perm -2000 \) -xdev -exec ls -al {} \; 2>/dev/null').read().strip()
CHECK_LINES = CHECK.count('\n') if CHECK else 0

with open(log_file_path, 'w') as f:
    f.write("="*30 + " U-13 조건 " + "="*30 + "\n")
    f.write("[양호]:주요 실행파일의 권한에 SUID와 SGID에 대한 설정이 부여되지 있지 않은 경우\n")
    f.write("[취약]:주요 실행파일의 권한에 SUID와 SGID에 대한 설정이 부여되어 있는 경우\n")

    if CHECK_LINES == 0:
        data['RESULT'][8] = ' 양호 '
    else:
        for line in CHECK.split('\n'):
            if line.startswith('-') and ('s' in line or 'S' in line):
                data['RESULT'][8] = ' 취약 '
                break

    f.write("="*30 + " U-13 점검 내용 " + "="*30 + "\n")
    if CHECK_LINES > 0:
        f.write(f'{CHECK_LINES}개의 파일이 존재합니다.\n')
        f.write(f'주요 실행파일의 권한을 확인하세요.\n')
    else:
        f.write("해당하는 파일이 없습니다.\n")

with open(log_file_path, 'r') as u13_file:
    u13_contents = u13_file.read()

with open(inspection_log_path, 'a') as inspection_file:
    inspection_file.write(u13_contents)
    inspection_file.write('\n\n')

#U-14
log_file_path = os.path.expanduser("~/checklinux/U-14.log")

filelist = [ '.profile', '.kshrc', '.cshrc', '.bashrc', '.bash_profile', '.login', '.exrc', '.netrc']

vul_files = []
sec_files = []

with open(log_file_path, 'w') as f:
    f.write("="*30 + " U-14 조건 " + "="*30 + "\n")
    f.write("[양호]:홈 디렉터리 환경변수 파일 소유자가 root 또는 해당 계정으로 지정되어 있고, 홈 디렉터리 환경변수 파일에 root와 소유자만 쓰기, 권한이 부여된 경우\n")
    f.write("[취약]:홈 디렉터리 환경변수 파일 소유자가 root 또는, 해당 계정으로 지정되지 않고, 홈 디렉터리 환경변수 파일에 root와 소유자 외에 쓰기 권한이 부여된 경우\n")

    f.write("="*30 + " U-14 점검 내용 " + "="*30 + "\n")
    for file in filelist:
        file_path = os.path.expanduser(f"~/{file}")
        if os.path.isfile(file_path):
            file_stat = os.stat(file_path)
            if file_stat.st_uid == os.getuid():
                if file_stat.st_mode & 0o2 != 0:
                    vul_files.append(file)
                else:
                    sec_files.append(file)
            else:
                if file_stat.st_mode & 0o2 != 0 or (file_stat.st_mode & 0o2 == 0 and file_stat.st_mode & 0o20 != 0 and file_stat.st_mode & 0o200 == 0):
                    vul_files.append(file)
                else:
                    sec_files.append(file)

            CHECK = os.popen(f"ls -al {file_path}").read()
            f.write(f"{file_path}\n")
            f.write(CHECK)

if vul_files:
    data['RESULT'][9] = ' 취약 '
else:
    data['RESULT'][9] = ' 양호 '

with open(log_file_path, 'r') as u14_file:
    u14_contents = u14_file.read()

with open(inspection_log_path, 'a') as inspection_file:
    inspection_file.write(u14_contents)
    inspection_file.write('\n\n')

#U-15
log_file_path = os.path.expanduser("~/checklinux/U-15.log")

filelist = ['/etc/passwd', '/etc/shadow', '/var/log']

for file_path in filelist:
    CHECK = os.popen(f"ls -l {file_path} 2>/dev/null").read().strip()
    CHECK1 = os.popen("find / -type f ! -user root -perm /o+w -exec ls -l {file_path} \; 2>/dev/null").read().strip()
    CHECK_LINES = CHECK1.count('\n') if CHECK else 0

with open(log_file_path, 'w') as f:
    f.write("="*30 + " U-15 조건 " + "="*30 + "\n")
    f.write("[양호]:시스템 중요 파일에 wordl writable 파일이 존재하지 않거나, 존재시 설정 이유를 확인하고 있는 경우\n")
    f.write("[취약]:시스템 중요 파일에 world writable 파일이 존재하나 해당 설정 이유를 확인하고 있지 않은 경우\n")

    if CHECK_LINES == 0:
        data['RESULT'][10] = ' 양호 '
    else:
        data['RESULT'][10] = ' 취약 '

    f.write("="*30 + " U-15 점검 내용 " + "="*30 + "\n")
    if CHECK_LINES > 0:
        f.write(f"{CHECK_LINES}개의 파일이 존재합니다.\n")
        f.write("/etc/passwd, /etc/shadow, /var/log 파일의 설정을 확인하세요.\n")
        f.write(f'{CHECK_LINES}')
    else:
        f.write("해당하는 파일이 없습니다.\n")

with open(log_file_path, 'r') as u15_file:
    u15_contents = u15_file.read()

with open(inspection_log_path, 'a') as inspection_file:
    inspection_file.write(u15_contents)
    inspection_file.write('\n\n')

#U-16
log_file_path = os.path.expanduser("~/checklinux/U-16.log")

CHECK = os.popen('find /dev -type f -exec ls -l {} \;').read().strip()

with open(log_file_path, 'w') as f:
    f.write("="*30 + " U-16 조건 " + "="*30 + "\n")
    f.write("[양호]:dev에 대한 파일 점검 후 존재하지 않은 device 파일을 제거한 경우\n")
    f.write("[취약]:dev에 대한 파일 점검 후 존재하지 않은 device 파일은 제거하지 않은 경우\n")

    if CHECK == 0:
        data['RESULT'][11] = ' 취약 '
        f.write("="*30 + " U-16 점검 내용 " + "="*30 + "\n")
        f.write(f'{CHECK}')

    else:
        data['RESULT'][11] = ' 양호 '
        f.write("="*30 + " U-16 점검 내용 " + "="*30 + "\n")
        f.write("파일이 존재하지 않습니다.")

with open(log_file_path, 'r') as u16_file:
    u16_contents = u16_file.read()

with open(inspection_log_path, 'a') as inspection_file:
    inspection_file.write(u16_contents)
    inspection_file.write('\n\n')

#U-17
log_file_path = os.path.expanduser("~/checklinux/U-17.log")

def check_file(file_path, mode, uid):
    if os.path.exists(file_path):
        file_stat = os.stat(file_path)
        if file_stat.st_mode == mode and file_stat.st_uid == uid:
            with open(file_path, 'r') as file:
                file_content = file.read()
                if '+' in file_content:
                    return True
    return False

filename1 = '/etc/hosts.equiv'
filename2 = os.path.expanduser('~/.rhosts')

with open(log_file_path, 'w') as f:
    f.write("="*30 + " U-17 조건 " + "="*30 + "\n")
    f.write("[양호]:login, shell, exec 서비스를 사용하지 않거나, 사용 시 아래와 같은 설정이 적용된 경우\n1./etc/hosts.equiv 및 $HOME/.rhosts 파일 소유자가 root 또는, 해당 계정인 경우\n2. /etc/hosts.equiv 및 $HOME/.rhosts 파일 권한이 600 이하인 경우\n3./etc/hosts.equiv 및 $HOME/.rhosts 파일설정에 '+' 설정이 없는 경우\n")
    f.write("[취약]:login, shell, exec 서비스를 사용하고, 위와 같은 설정이 적용되지 않은 경우\n")

    f.write("=" * 30 + " U-17 점검 내용 " + "=" * 30 + "\n")
   
    if os.path.exists(filename1):
        f.write(f"{filename1}\n")
        file1_exists = True
        file1_stat = os.stat(filename1)
        if file1_stat.st_mode == 0o600 and file1_stat.st_uid == 0:
            with open(filename1, 'r') as file1:
                file1_content = file1.read()
                if '+' in file1_content:
                    data['RESULT'][12] = ' 양호 '
                else:
                    data['RESULT'][12] = ' 취약 '
        else:
            data['RESULT'][12] = ' 취약 '

    else:
        data['RESULT'][12] = ' 양호 '
        f.write(f"{filename1} 파일이 존재하지 않습니다.\n")
        file1_exists = False

    if os.path.exists(filename2):
        f.write(f"{filename2}\n")
        file2_exists = True
        file2_stat = os.stat(filename2)
        if file2_stat.st_mode == 0o600 and file2_stat.st_uid == os.getuid():
            with open(filename2, 'r') as file2:
                file2_content = file2.read()
                if '+' in file2_content:
                    data['RESULT'][12] = ' 양호 '
                else:
                    data['RESULT'][12] = ' 취약 '
        else:
             data['RESULT'][12] = ' 취약 '
    else:
        data['RESULT'][12] = ' 취약 '
        f.write(f"{filename2} 파일이 존재하지 않습니다.\n")
        file2_exists = False

with open(log_file_path, 'r') as u17_file:
    u17_contents = u17_file.read()

with open(inspection_log_path, 'a') as inspection_file:
    inspection_file.write(u17_contents)
    inspection_file.write('\n\n')

#U-18
log_file_path = os.path.expanduser("~/checklinux/U-18.log")

filelist = ['/etc/hosts.allow', '/etc/hosts.deny']

CHECK1 = os.popen('cat /etc/hosts.allow 2>/dev/null').read().strip()
CHECK2 = os.popen('cat /etc/hosts.deny 2>/dev/null').read().strip()

for file in filelist:
    with open(log_file_path, 'w') as f:
        f.write("="*30 + " U-18 조건 " + "="*30 + "\n")
        f.write("[양호]:접속을 허용할 특정 호스트에 대한 IP 주소 및 포트 제한을 설정한 경우\n")
        f.write("[취약]:접속을 허용할 특정 호스트에 대한 IP 주소 및 포트 제한을 설정하지 않은 경우\n")
    if os.path.isfile(file):
        with open(file) as f:
            content = f.read()

        with open(log_file_path, 'w') as f:
            f.write("="*30 +" U-18 조건 " + "="*30 + "\n")
            f.write("[양호]:접속을 허용할 특정 호스트에 대한 IP 주소 및 포트 제한을 설정한 경우\n")
            f.write("[취약]:접속을 허용할 특정 호스트에 대한 IP 주소 및 포트 제한을 설정하지 않은 경우\n")
            if "#" not in file:
                if CHECK1 == 0 or CHECK2 == 0:
                    data['RESULT'][13] = ' 양호 '
                    f.write("="*30 + " U-18 점검 내용 " + "="*30 + "\n")
                    f.write(f'{CHECK1}')
                    f.write(f'{CHECK2}')
                else:
                    data['RESULT'][13] = ' 취약 '
                    f.write("="*30 + " U-18 점검 내용 " + "="*30 + "\n")
                    f.write("제한을 설정하지 않았습니다.\n")

            break

    else:
        data['RESULT'][13] = ' 취약 '
        f.write("="*30 + " U-18 점검 내용 " + "="*30 + "\n")
        f.write("파일이 존재하지 않습니다.\n")

with open(log_file_path, 'r') as u18_file:
    u18_contents = u18_file.read()

with open(inspection_log_path, 'a') as inspection_file:
    inspection_file.write(u18_contents)
    inspection_file.write('\n\n')
#U-56
log_file_path = os.path.expanduser("~/checklinux/U-56.log")

CHECK = os.popen('cat /etc/profile | grep -i umask | awk \'{print $2}\' | grep 022').read().strip()

with open(log_file_path, 'w') as f:
    f.write("="*30 + " U-56 조건 " + "="*30 + "\n")
    f.write("[양호]:UMASK값이 022 이상으로 설정된 경우\n")
    f.write("[취약]:uMASK값이 022 이상으로 설정되지 않은 경우\n")

    f.write("="*30 + " U-56 점검 내용 " + "="*30 + "\n")
    if CHECK:
        data['RESULT'][14] = ' 양호 '
        with open('/etc/profile', 'r') as profile:
            for line in profile:
                if CHECK in line:
                    f.write(line)
                    break
    else:
        data['RESULT'][14] = ' 취약 '
        f.write("UMASK가 설정되지 않았습니다.\n")
        f.write("/etc/profile 파일을 확인하세요.\n")

with open(log_file_path, 'r') as u56_file:
    u56_contents = u56_file.read()

with open(inspection_log_path, 'a') as inspection_file:
    inspection_file.write(u56_contents)
    inspection_file.write('\n\n')

#U-57
log_file_path = os.path.expanduser("~/checklinux/U-57.log")

USERS = os.popen("cat /etc/passwd | grep 'sh$' | awk -F: '{print $1}'").read().strip().split('\n')

with open(log_file_path, 'w') as f:
    f.write("="*30 + " U-57 조건 " + "="*30 + "\n")
    f.write("[양호]:홈 디렉터리 소유자가 해당 계정이고, 타 사용자 쓰기 권한이 제거된 경우\n")
    f.write("[취약]:홈 디렉터리 소유자가 해당 계정이 아니고, 타 사용자 쓰기 권한이 부여된 경우\n")

    for user in USERS:
        HOME_DIR = os.path.expanduser(f"~{user}")
        STAT_INFO = os.popen(f"ls -ald {HOME_DIR}").read().strip()
        CHECK = os.path.basename(HOME_DIR)
        OWN = STAT_INFO.split()[2]
        PERMISSION = STAT_INFO.split()[0]
        CHECK1 = os.popen('stat -c"%a" /home').read().strip()
        CHECK2 = int(CHECK1) if CHECK1 else -1

        if CHECK == OWN or CHECK2 == 700:
            data['RESULT'][15] = ' 양호 '
        else:
            data['RESULT'][15] = ' 취약 '

        f.write("="*30 + " U-57 점검 내용 " + "="*30 + "\n")
        f.write(f"{STAT_INFO}\n")

        break  # 첫 번째 사용자에 대한 결과만 기록하고 종료

with open(log_file_path, 'r') as u57_file:
    u57_contents = u57_file.read()

with open(inspection_log_path, 'a') as inspection_file:
    inspection_file.write(u57_contents)
    inspection_file.write('\n\n')

#U-58
log_file_path = os.path.expanduser("~/checklinux/U-58.log")

with open(log_file_path, 'w') as f:
    f.write("="*30 + " U-58 조건 " + "="*30 + "\n")
    f.write("[양호]:홈 디렉터리가 존재하지 않는 계정이 발견되지 않은 경우\n")
    f.write("[취약]:홈 디렉터리가 존재하지 않는 계정이 발견된 경우\n")

    with open('/etc/passwd') as f2:
        has_empty_home = False
        for line in f2:
            name, home = line.strip().split(":")[0], line.strip().split(":")[5]
            if not home:
                has_empty_home = True
                data['RESULT'][16] = ' 취약 '
                f.write(f"홈 디렉터리가 없는 계정: {name}\n")

            else:
                data['RESULT'][16] = ' 양호 '
                break

        f.write("="*30 + " U-58 점검 내용 " + "="*30 + "\n")
        f2.seek(0)
        if not has_empty_home:
            f.write("홈 디렉터리가 없는 계정이 존재하지 않습니다.\n")
        f.write(f2.read())

with open(log_file_path, 'r') as u58_file:
    u58_contents = u58_file.read()

with open(inspection_log_path, 'a') as inspection_file:
    inspection_file.write(u58_contents)
    inspection_file.write('\n\n')

print_table(data)

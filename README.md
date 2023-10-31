# linux check
1.  Check SSH server installation (ssh server 설치 확인)
   sudo systemctl status openssh
2.  If not installed, then install it (설치 되어 있지 않다면 설치)
   sudo apt-get update -> sudo apt-get install openssh-server
3.  Check the status if installation is complete (설치 완료시 상태 확인)
   sudo systemctl status openssh
4.  Enter your Linux information (IP, ID, PASSWORD) (자신의 리눅스에 대한 정보 입력 (IP, ID, PASSWD))

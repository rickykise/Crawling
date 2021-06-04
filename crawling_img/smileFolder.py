import paramiko
import datetime

def makeMain():
    ssh = paramiko.SSHClient()
    ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
    ssh.connect('49.247.5.169', username = "root", password = "sms@unionc")
    stdin, stdout, stderr = ssh.exec_command('mkdir /usr/local/img/'+datetime.datetime.now().strftime('%Y-%m-%d'))
    ssh.close()

if __name__=='__main__':
        print('폴더생성')
        makeMain()
        print('폴더생성완료')

# def mkdir():
#     ssh = paramiko.SSHClient()
#     ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
#     ssh.connect('49.247.5.169', username = "root", password = "sms@unionc")
#     stdin, stdout, stderr = ssh.exec_command('mkdir /usr/local/img/'+datetime.datetime.now().strftime('%Y-%m-%d'))
#     ssh.close()


	# dirname = 'D:\img\\'+datetime.datetime.now().strftime('%Y-%m-%d')
    # path = 'D:\img\\'
    # yester = '2019-04-17'
    # print("pscp -pw sms@unionc "+path+yester+"\daum_6420287420190416.jpg"+" root@49.247.5.169:/usr/local/img/")
    # dis = subprocess.call("pscp -pw sms@unionc "+path+yester+"\daum_6420287420190416.jpg"+" root@49.247.5.169:/usr/local/img/", shell=True)
    # print(dis)



    # print(dis2)
    # dis = os.system("pscp " + path+datetime.datetime.now().strftime('%Y-%m-%d') + "\daum_6420287420190416.jpg" + " root@49.247.5.169:/usr/local/img")
    # dis2 = os.system("sms@unionc")
    # dis = subprocess.run("ls -al", shell=True)
    # print(dis)
    # ssh = paramiko.SSHClient()
    # ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
    # ssh.connect('49.247.5.169', username = "root", password = "sms@unionc")
    # sftp = paramiko.SFTPClient.from_transport(ssh)
    # path = "D:\img\2019-04-17"
    # filepath = os.listdir(path)
    # localpath = '/usr/local/img/'
    # sftp.put(localpath, filepath)
    # ssh.exec_command('mkdir sg_test')
    # stdin, stdout, stderr = ssh.exec_command('mkdir /usr/local/img/'+datetime.datetime.now().strftime('%Y-%m-%d'))
    # stdin, stdout, stderr = ssh.exec_command('dir')
    # print(stdout.readlines())
    # sftp.close()
    # ssh.close()

    # dis = subprocess.call("sms@unionc", shell=True)
    # print(dis)
    # subprocess.run("sms@unionc", shell=True)
    # print(dis).
    # subprocess.call("sms@unionc", shell=True)
    # print(dis)



    # sftp = paramiko.SFTPClient.from_transport(ssh)
    # localpath = '/usr/local/img'



	# ssh = paramiko.SSHClient()
	# ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
	# ssh.connect('49.247.5.169', 22, username="root", password="sms@unionc")
    #
    # sftp = paramiko.SFTPClient.from_transport(ssh)
    # localpath = '/usr/local/img'
    #
    # print(sftp.get(localpath=))

	# sftp = paramiko.SFTPClient.from_transport(ssh)
	#
	# file_list = sftp.listdir(path='/usr/local/img/')

	# dirname = 'D:\img\\'+datetime.datetime.now().strftime('%Y-%m-%d')
	# if not os.path.isdir(dirname):
	# 	os.mkdir(dirname)

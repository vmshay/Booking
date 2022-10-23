# TODO: Отправляем календарь на сервер
#
import paramiko
import bot.config as cnf

file = 'calendar.ics'


async def send():
    with paramiko.SSHClient() as ssh:
        ssh.load_system_host_keys()
        ssh.connect(hostname=cnf.SSH_HOST, username=cnf.SSH_USER, password=cnf.SSH_PASS)

        sftp = ssh.open_sftp()

        sftp.chdir('/var/www/vmshay')
        sftp.put(file, file)

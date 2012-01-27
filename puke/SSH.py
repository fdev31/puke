import paramiko
import logging

class SSH (paramiko.SSHClient):

	def __init__(self):
		logger = paramiko.util.logging.getLogger('paramiko')
		logger.setLevel(logging.ERROR)
		super(SSH, self).__init__()
		

	def execute(self, cmd):
		chan = self.get_transport().open_session()
		chan.exec_command(cmd)

		return (chan.makefile('rb', -1).read(),  chan.makefile_stderr('rb', -1).read(),chan.recv_exit_status())
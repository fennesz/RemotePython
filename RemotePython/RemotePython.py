'''
Created on Mar 6, 2016

@author: allexveldman
'''

from subprocess import call, check_output, CalledProcessError
import getpass

class RemotePython(object):
    '''
    Class for executing commands and scripts on a remote machine, needs SSH on system level to work.
    '''
    def __init__(self, remote_script=None, ip='localhost', user=getpass.getuser(), port=22):
        '''Default values result in <username>@localhost port:22'''
        self.script = remote_script
        self.port = port
        self.__ip = ip
        self.__user = user
        self.__remote_client = '%s@%s' % (self.__user, self.__ip)
    
    @property
    def ip(self):
        return self.__ip
    @ip.setter
    def ip(self, value):
        self.__ip = value
        self.__remote_client = '%s@%s' % (self.__user, self.__ip)
    @property
    def user(self):
        return self.__user
    @user.setter
    def user(self, value):
        self.__user = value
        self.__remote_client = '%s@%s' % (self.__user, self.__ip)
        
    def __str__(self):
        '''print the info in a RemotePython instance'''
        return '\
        ip:\t\t%s\n\
        user:\t\t%s\n\
        remote_client:\t%s\n\
        port:\t\t%s\n\
        remote_script:\t%s' % (self.__ip, self.__user, self.__remote_client, self.port, self.script)
     
    def __copyScript(self, script=None):
        ''' Copy the to-be-executed script to the target machine, returns 'None is no script is specified.'''
        if not script:
            if self.script != None:
                script = self.script
            else:
                print "No script specified"
                return None
        try:
            call(['scp', script, '%s:%s' % (self.__remote_client, script)])
        except:
            print "Call failed: scp %s %s:%s" % (script, self.__remote_client, script)
            raise
        #TODO: Add check if call is successful
    
    def __removeScript(self, script=None):
        ''' Remove the used script from the target machine, returns 'None' is script is not specified.'''
        if not script:
            if self.script != None:
                script = self.script
            else:
                print "No script specified"
                return None
        call(['ssh', self.__remote_client, '-p %s' % (self.port), 'rm %s' % (script)])
        #TODO: Add check if call is successful
        
    def getEnv(self):
        '''
        Determine the machine type of the target machine.
        Return the correct command to load the environment on the target machine.
        This can be useful to run commands or scripts that need the environment normally loaded when starting a shell
        '''
        
        ret = self.runCommand('uname', '-s')
        if ret == 'Linux': #Linux
            profile = '~/.bashrc'
        elif ret == 'Darwin': #OSX
            profile = '~/.bash_profile'
        else: #Solaris / rest
            profile = '~/.login' 
        return profile

    def runScript(self, script=None):
        #TODO: Quit method if any call fails with proper error handling
        '''
        Run a python script on a remote machine.
        The script should either be passed as an argument or predefined in the RemotePython object
        Return 'None' if no script is specified.
        '''
        #TODO: remove this check and raise a proper exeption in __copyScript(), check is now performed twice
        if not script:
            if self.script != None:
                script = self.script
            else:
                print "No script specified"
                return None
        
        try:
            # Copy script to remote machine
            self.__copyScript(script)
            profile = self.getEnv()
            # pre-load the environment, Run the python script and return its stdout
            ret = check_output(['ssh',
                                self.__remote_client,
                                '-p %s' % (self.port),
                                '%s %s; python %s' % ('source', profile, script)])
            self.__removeScript(script)
            return ret.strip()
        except CalledProcessError as e:
            print "Call failed: %s" % (script)
            raise

    def runCommand(self, *command):
        '''Call a single command on the remote machine, returns it's stdout'''
        try:
            ret = check_output(['ssh', self.__remote_client, '-p %s' % (self.port)] + list(command))
            return ret.strip()
        except CalledProcessError as e:
            print "Call failed: ssh %s -p %s " % (self.__remote_client, self.port) + str(list(command))
            raise

def main():
    obj = RemotePython()
    print obj.runScript('remote_script.py')
    return 0

if __name__ == '__main__':
    main()

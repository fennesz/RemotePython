'''
Created on Mar 6, 2016

@author: allexveldman
'''
import os
from subprocess import call, check_output, CalledProcessError
import getpass
import sys


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

        #Use sshpass if available ... Should only be used for testing purposes.
        if (os.environ.get('SSHPASS', 'None') != 'None'):
            self.__ssh_string = ['sshpass', '-e']
        else:
            self.__ssh_string = ''
    
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
    @property
    def ssh_string(self):
        return self.__ssh_string

    def __str__(self):
        '''print the info in a RemotePython instance'''
        return '\
        ip:\t\t%s\n\
        user:\t\t%s\n\
        remote_client:\t%s\n\
        port:\t\t%s\n\
        remote_script:\t%s' % (self.__ip, self.__user, self.__remote_client, self.port, self.script)
     
    def __copyScript(self, script):
        ''' Copy the to-be-executed script to the target machine, returns 'None is no script is specified.'''
        try:
            call(list(self.__ssh_string) + ['scp', script, '%s:%s' % (self.__remote_client, script)])
        except:
            print "Call failed: scp %s %s:%s" % (script, self.__remote_client, script)
            raise
    
    def __removeScript(self, script=None):
        ''' Remove the used script from the target machine, returns 'None' is script is not specified.'''
        if not script:
            if self.script != None:
                script = self.script
            else:
                print "No script specified"
                return None
        try:
            call(list(self.__ssh_string) + ['ssh', self.__remote_client, '-p %s' % (self.port), 'rm %s' % (script)])
        except CalledProcessError:
            print "Could not remove script: ssh %s -p %s rm %s" % (self.__remote_client, self.port, script) 
            raise
        
    def getEnv(self):
        '''
        Determine the machine type of the target machine.
        Return the correct command to load the environment on the target machine.
        This can be useful to run commands or scripts that need the environment normally loaded when starting a shell
        '''
        #TODO: make a better way of loading the proper environment
        profile = 'source '
        ret = self.runCommand(['uname', '-s'])
        if ret == 'Linux': #Linux
            profile += '~/.profile;'
        elif ret == 'Darwin': #OSX
            profile += '~/.bash_profile;'
        else: #Solaris / rest
            profile += '~/.login;'
        return profile

    def runScript(self, script=None, load_env=False):
        #TODO: Quit method if any call fails with proper error handling
        '''
        Run a python script on a remote machine.
        The script should either be passed as an argument or predefined in the RemotePython object
        Return 'None' if no script is specified.
        if load_env=True it will check the environment and source the corresponding file on the remote machine
        '''
        if not script:
            if self.script != None:
                script = self.script
            else:
                raise ValueError("A script should be specified in either the object or the function call")      
        try:
            # Copy script to remote machine
            self.__copyScript(script)
            load_profile = self.getEnv() if load_env == True else ''
            # pre-load the environment, Run the python script and return its stdout
            ret = check_output(list(self.__ssh_string) + ['ssh',
                                self.__remote_client,
                                '-p %s' % (self.port),
                                load_profile,
                                'python %s' % (script)])
            self.__removeScript(script)
            return ret.strip()
        except CalledProcessError:
            print "Call failed: %s" % (script)
            raise
        except ValueError:
            print "Could not copy the script"
            raise

    def runCommand(self, command=[], load_env=False):
        '''Call a single command on the remote machine, returns it's stdout'''

        load_profile = self.getEnv() if load_env == True else ''
        try:
            ret = check_output(list(self.ssh_string) + ['ssh',
                                self.__remote_client,
                                '-p %s' % (self.port),
                                load_profile] + list(command))
            return ret.strip()
        except CalledProcessError as e:
            sys.stdout.write("Call failed: %s %s -p %s %s" % (self.__ssh_string, self.__remote_client, self.port, load_profile))
            #Make sure command is written correctly in console:
            for s in command:
                sys.stdout.write(s + " ")
            raise

def main():
    pass


if __name__ == '__main__':
    main()

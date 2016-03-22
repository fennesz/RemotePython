'''
Created on Mar 6, 2016

@author: allexveldman
'''
from getpass import getuser
from subprocess import CalledProcessError
from RemotePython import RemotePython
import mock
import unittest
import sys


# Change these to your remote machine keys to execute the testRunScript() test on your remote machine
IP = 'ssh.fedthund.dk'
USER = 'pi'


# LOCAL_UNAME should be the result you get from running 'uname -s' on your local machine
if sys.platform.startswith('linux'):
    LOCAL_UNAME = 'Linux'
elif sys.platform.startswith('darwin'):
    LOCAL_UNAME = 'Darwin'

# To avoid all the password requests, install sshpass on your local system
# and set the environment variable SSHPASS to your password. In Linux, this is done like so:
# $ export SSHPASS=password

class Test(unittest.TestCase):
    ''' Class containing unittests for the RemotePython module '''

    def testRunScript(self):
        ''' Test execution of a python script on a remote machine'''
#         print self.testRunScript.__doc__
        obj = RemotePython('remote_script.py', ip=IP, user=USER)
        ret = obj.runScript(load_env=True)
        self.assertIn('the call worked', ret)

    def testRunScriptRaisesValueError(self):
        ''' Test that ValueError is raised when RemotePython doesn't receive a script'''
        obj = RemotePython()
        with self.assertRaises(ValueError):
            obj.runScript()

    def testRunScriptRaisesCalledProcessError(self):
        '''Test that CalledProcessError is raised when RemotePython attempts to execute nonexistant script.'''
        obj = RemotePython()
        with self.assertRaises(CalledProcessError):
            obj.runScript('wrong_script.py')

    def testRunCommand(self):
        ''' Run uname on localhost, for OSX this is Darwin, for linux this is Linux.'''
        obj = RemotePython()
        ret = obj.runCommand(['uname', '-s'])
        self.assertEqual(ret, LOCAL_UNAME)

    def testRunCommandRaisesCalledProcessError(self):
        '''Test that CalledProcessError is raised when RemotePython attempts to execute invalid command.'''
        obj = RemotePython()
        with self.assertRaises(CalledProcessError):
            obj.runCommand(['invalid', 'command'])
     
       
    def testLoadEnv(self):
        ''' Run a command on target which has been symbolically linked to /bin/ls - and cleans up afterwards.
            If it fails, it might be because your load environment file isn't found by RemotePython, or because
            the unix system in question has an unorthodox file structure.'''
        
        obj = RemotePython(ip=IP, user=USER)
        try:
            delete_bin = obj.runCommand(["[ -d ./bin ]"]) # returns None if ./bin exists
        except CalledProcessError: # raises CalledProcessError if ./bin doen not exist
            delete_bin = True # ./bin did not exist yet so delete it afterwards
        #Set-up:                 
        obj.runCommand(['mkdir', '-p', 'bin;', # create folder if not there
                        'ln', '-s', '/bin/ls', '~/bin/testingCommand;', # Symbolic link  to ls command
                        'touch', 'TemporaryTestFile']) #create temporary file to look for
        #Test:
        ret = obj.runCommand(['testingCommand'], load_env=True) # Environment command execution
        #Break-down:
        if delete_bin:
            obj.runCommand(['rm -r','./bin/', 'TemporaryTestFile'])
        else:
            obj.runCommand(['rm', '~/bin/testingCommand TemporaryTestFile']) # Cleanup
        self.assertIn('TemporaryTestFile', ret)

    def testLoadEnvUnkownBashRaisesValueError(self):
        with mock.patch.object(RemotePython, 'runCommand', create=True, return_value='crazyFish bash'):
            obj = RemotePython()
            with self.assertRaises(ValueError):
                obj.getEnv()

    def testLoadEnvUnkownBashRaisesValueError(self):
        with mock.patch.object(RemotePython, 'runCommand', create=True, return_value='crazyFish'):
            obj = RemotePython()
            with self.assertRaises(ValueError):
                obj.getEnv()

    def testLoadEnvBashProfile(self):
        with mock.patch.object(RemotePython, 'runCommand', create=True, return_value='.bash_profile bash'):
            obj = RemotePython()
            self.assertEquals(obj.getEnv(), 'source .bash_profile;')

    def testLoadEnvBashLogin(self):
        with mock.patch.object(RemotePython, 'runCommand', create=True, return_value='.bash_login bash'):
            obj = RemotePython()
            self.assertEquals(obj.getEnv(), 'source .bash_login;')

    def testLoadEnvProfile(self):
        with mock.patch.object(RemotePython, 'runCommand', create=True, return_value='.profile bash'):
            obj = RemotePython()
            self.assertEquals(obj.getEnv(), 'source .profile;')

    def testLoadEnvCsh(self):
        with mock.patch.object(RemotePython, 'runCommand', create=True, return_value='.login csh'):
            obj = RemotePython()
            self.assertEquals(obj.getEnv(), 'source .login;')

    def testRemoveScript(self):
        ''' Test if hidden function '__removeScript' works '''
#         print self.testRemoveScript.__doc__
        obj = RemotePython()
        before = int(obj.runCommand(['ls', '-l', '|', 'wc', '-l']))
        obj.runCommand(['touch', 'test.txt'])
        middle = int(obj.runCommand(['ls', '-l', '|', 'wc', '-l']))
        self.assertEqual(middle, before+1, "No file created, file already existed") # Check if we created a new file
        obj._RemotePython__removeScript('test.txt')
        after = int(obj.runCommand(['ls', '-l', '|', 'wc', '-l']))
        self.assertEqual(before, after) # Check if we removed the created file

    def testPrint(self):
        ''' Print the default object '''
        print RemotePython()

if __name__ == "__main__":
    #import sys;sys.argv = ['', 'Test.testMain']
    unittest.main()

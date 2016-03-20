'''
Created on Mar 6, 2016

@author: allexveldman
'''

from subprocess import CalledProcessError
from RemotePython import RemotePython
from getpass import getuser
import unittest


# Change these to your remote machine keys to execute the testRunScript() test on your remote machine
IP = 'localhost'
USER = getuser()


# LOCAL_UNAME should be the result you get from running 'uname -s' on your local machine
LOCAL_UNAME = 'Linux'

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
        ''' Run uname on localhost, for OSX this is Darwin.'''
        obj = RemotePython()
        ret = obj.runCommand(['uname', '-s'])
        self.assertEqual(ret, LOCAL_UNAME)

    def testRunCommandRaisesCalledProcessError(self):
        '''Test that CalledProcessError is raised when RemotePython attempts to execute invalid command.'''
        obj = RemotePython()
        with self.assertRaises(CalledProcessError):
            obj.runCommand(['invalid', 'command'])
     
    @unittest.skipIf(IP == 'localhost', "Needs a remote machine with symbolic link to work")   
    def testLoadEnv(self):
        ''' Run a command with loading the environment, needs a command named 'testCommand' on the target 
        I created a symbolic link in my /home/allex/bin to the ls command in /bin
        Also create a file or object called ArdPi in the user home dir.'''
        #TODO: change this test so it creates a file and cleans up afterward on the target machine
        obj = RemotePython(ip=IP, user=USER)
        ret = obj.runCommand(['testCommand'],load_env=True)
        self.assertIn('ArdPi', ret)

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
#         print self.testPrint.__doc__
        print RemotePython()

if __name__ == "__main__":
    #import sys;sys.argv = ['', 'Test.testMain']
    unittest.main()

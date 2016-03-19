'''
Created on Mar 6, 2016

@author: allexveldman
'''

from subprocess import CalledProcessError
from RemotePython import RemotePython
from getpass import getuser
import unittest
import StringIO
import sys


# Change these to your remote machine keys to execute the testRunScript() test on your remote machine
IP = 'localhost'
USER = getuser()

# LOCAL_UNAME should be the result you get from running 'uname -s' on your local machine
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

    def testRunScriptCalledProcessErrorPrints(self):
        '''Test to see if an errormessage is printed to the screen when CalledProcessError is raised.
            this is done by temporarily redirecting IO to capturedOutput, and checking to see if it's empty
            after runScript is called. If the test isn't succesful, it's because the CalledProcessError exception isn't caught
            in RemotePython, or because nothing is printed when it is.'''
        rpy = RemotePython()
        capturedOutput = StringIO.StringIO()            # Create StringIO object
        sys.stdout = capturedOutput                     # redirect stdout.
        try:
            rpy.runScript('wrong_script.py')            # Call function, Provoking CalledProcessError
        except CalledProcessError:
            pass                                        # Drop exception, as it's not needed for testing.
        sys.stdout = sys.__stdout__                     # Reset redirect.
        self.assertIsNot('', capturedOutput.getvalue()) # Assert there is output.

    def testRunScriptValueErrorPrints(self):
        '''Test to see if an errormessage is printed to the screen when ValueError is raised.
            this is done by temporarily redirecting IO to capturedOutput, and checking to see if it's empty
            after runScript is called. If the test isn't succesful, it's because the ValueError exception isn't caught
            in RemotePython, or because nothing is printed when it is'''
        rpy = RemotePython()
        capturedOutput = StringIO.StringIO()               # Create StringIO object
        sys.stdout = capturedOutput                        # redirect stdout.
        try:
            rpy.runScript()                                # Call function, provoking ValueError
        except ValueError:
            pass
        sys.stdout = sys.__stdout__                        # Reset redirect.
        self.assertIsNot('', capturedOutput.getvalue())    # Assert there is output.


    def testRunCommand(self):
        ''' Run uname on localhost, for OSX this is Darwin.'''
        obj = RemotePython()
        ret = obj.runCommand(['uname', '-s'])
        self.assertEqual(ret, LOCAL_UNAME)
     
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

''' Remote script to execute '''
from subprocess import check_output, CalledProcessError

print "the call worked"
# print os.listdir('./')
try:
    RET = check_output('uname')
    if RET.strip('\n') == 'Linux':
        print "it's a Linux machine!!"
    else:
        print RET
except CalledProcessError as err:
    print err.returncode
    print err.output
    
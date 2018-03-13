# file operation exercise
import sys
import os

def test1():
    # need to handle file closing
    file = open("textfile.txt", "r")
    content = file.read()
    file.close

    print(content)
    print("\r\n")


def test2():
    # file closing handled automatically
    with open("textfile.txt") as f:
        content = f.read()

    print(content)


def test3():
    print(sys.argv[0])
    indir = '.\\'
    for root, dirs, filenames in os.walk(indir):
        for f in filenames:
            print(os.path.join(root, f))
            if f != sys.argv[0]:
                doFileOps(os.path.join(root, f))


def wipe():
    if len(sys.argv) == 1:
        curpath = ".\\"
    else:
        curpath = sys.argv[1]
    for root, _, files in os.walk(curpath):
        for f in files:
            fname = os.path.join(root, f)
            print(fname)
            if f != sys.argv[0]:
                doFileOps(os.path.join(root, f))
                #print("Do fileop : " + fname)



def doFileOps(fname):
    x = b"The quick brown fox jumps over the lazy dog"
    print(len(x))
    f = r"{}".format(fname)
    size = os.stat(f).st_size
    fp = open(f, "rb+") # open file for update
    fp.seek(0)
    print(size)
    while size > 0:
        fp.write(x)
        size = size - len(x)
        #print(size)
    fp.close()



def test4():
    if len(sys.argv) == 1:
        curpath = ".\\"
    else:
        curpath = sys.argv[1]
    for root, _, files in os.walk(curpath):
        for f in files:
            fname = os.path.join(root, f)
            print(fname)
            # Remove *.pyc files, compress images, count lines of code
            # calculate folder size, check for repeated files, etc.
            # A lot of nice things can be done here
            # credits: m_tayseer @reddit



wipe()
# test3()



# mm = list(os.walk('./'))
# mm[0] is 1 tuple of [root],[subdirs],[files]
# mm[1] is next tuple..

# joining dir path to filenames:-
# fn= map(lambda l: os.path.join(mm[3][0], l), [k for k in mm[3][2]])
# list(fn)



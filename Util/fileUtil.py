
# don't catch the exception, raise the exceptionw

def writeFile(filename, data):
    with open(filename, "w") as f:
        f.write(data)
        return True

def readFile(filename):
    with open(filename, "r") as f:
        res = f.readline()
        return True, res


# writeFile("test.txt", "hello world!")
# res = readFile("test.txt")
# print res
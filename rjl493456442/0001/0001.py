import string
import random
CODE_FILE = "code.txt"
CODE_LENGTH = 15
CODE_NUMBER = 200
def generate_activation_code(code_file, code_length, code_number):
    try:
        f = open(code_file, "w")
    except IOError:
        print "open file failed"
        return
    avaiable_letter = string.letters + "0123456789"
    for count in range(code_number):
        code = ""
        for _ in range(code_length):
            code += random.choice(avaiable_letter)
        code += '\n'
        # save to file
        f.write(code)
    f.close()

if __name__ == "__main__":
    generate_activation_code(CODE_FILE, CODE_LENGTH, CODE_NUMBER)


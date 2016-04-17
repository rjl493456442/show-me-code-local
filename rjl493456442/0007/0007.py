"""
    author : gary rong
    date : 2016/04/17
    description: code line statistic
    note: only for python code
"""
import sys
import os
root_directory = ''
mode = 0
annotation_num = 0
empty_line_num = 0
code_line_num = 0
class Table:
    def __init__(self):
        self._info = []
    def insert(self, dirpath, fname, code_line_num, annotation_num, empty_line_num):
        self._info.append({
            "dirpath" : dirpath,
            "fname" : fname,
            "code_line_num" : code_line_num,
            "annotation_num" : annotation_num,
            "empty_line_num" : empty_line_num
        })
    def display(self):
        for trace in self._info:
            n_layer_trace = len(trace['dirpath'].split('/'))
            n_layer_root = len(root_directory.split('/'))
            print ' ' * 2 * (n_layer_trace - n_layer_root) + trace['dirpath'] + '/' +  trace['fname']
            print "code: %d, annotation: %d, empty: %d" % (trace['code_line_num'], trace['annotation_num'], trace['empty_line_num'])

def run():
    global result
    for dirpath, dirnames, filenames in os.walk(root_directory):
        for fname in filenames:
            if fname.endswith(".py"):
                code_line_num, annotation_num, empty_line_num = analyse(dirpath, fname)
                if code_line_num:
                    result.insert(dirpath, fname, code_line_num, annotation_num, empty_line_num)

def analyse(dirpath, fname):
    global annotation_num
    global empty_line_num
    global code_line_num
    local_annotation_num = 0
    local_empty_line_num = 0
    local_code_line_num = 0

    multi_annotation_symbol = ['"""',"'''"]
    single_annotation_symbol = '#'
    empty_line_symbol = ""
    filepath = os.path.join(dirpath, fname)
    try:
        with open(filepath, 'r') as f:
            lines = f.readlines()
            index = 0
            while index < len(lines):
                # remove the space in the begin and end of the line
                line = lines[index].strip()
                if line.startswith(single_annotation_symbol):
                    local_annotation_num += 1
                elif line.startswith(multi_annotation_symbol[0]) or line.startswith(multi_annotation_symbol[1]):
                    # annotation like """ something """
                    if line[3:].endswith(multi_annotation_symbol[0]) or line[3:].endswith(multi_annotation_symbol[1]):
                        local_annotation_num += 1
                        index += 1
                        continue
                    index += 1
                    temp_count = 1
                    while True:
                        if index == len(lines):
                            print "invalid format code file: %s" % filepath
                            return None, None, None
                        line = lines[index].strip()
                        if line.startswith(multi_annotation_symbol[0]) or line.startswith(multi_annotation_symbol[1]):
                            temp_count += 1
                            break
                        else:
                            temp_count += 1
                            index += 1
                    local_annotation_num += temp_count
                elif line == empty_line_symbol:
                    local_empty_line_num += 1
                else:
                    local_code_line_num += 1
                index += 1
        code_line_num += local_code_line_num
        annotation_num += local_annotation_num
        empty_line_num += local_empty_line_num
        return local_code_line_num, local_annotation_num, local_empty_line_num
    except IOError, e:
        print e
if __name__ == "__main__":
    result = Table()
    index = 1
    while index < len(sys.argv):
        if sys.argv[index].startswith("--"):
            options = sys.argv[index][2:]
            if options == "dir":
                root_directory = sys.argv[index+1]
                index  += 2
                continue
            else:
                print "invalid parameters"
                sys.exit()
        if sys.argv[index].startswith("-"):
            options = sys.argv[index][1:]
            if options == "v":
                mode = 1
                index += 1
            else:
                print "invalid parameters"
                sys.exit()
    if root_directory == "":
        print "Attention: no path for project has been specified"
        print "           the current path will be used for analysis"
        root_directory = '.'

    run()
    if mode == 1:
        result.display()
    print "total statistic:"
    print "code: %d, annotation: %d, empty: %d" % (code_line_num, annotation_num, empty_line_num)

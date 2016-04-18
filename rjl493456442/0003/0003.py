"""
    author : gary rong
    date : 2016/4/18
    description: save text into redisDB
"""
import redis
hostname = "localhost"
port = 6379
redis_cli = None
set_name = "active_code"
def get_handler():
    global redis_cli
    redis_cli = redis.StrictRedis(host = hostname, port = port)

def save_to_set(set_name, value):
    redis_cli.sadd(set_name, value)


def get_all_members_from_set(set_name):
    return redis_cli.smembers(set_name)

def remove_set(set_name):
    redis_cli.delete(set_name)

def read_big_file(file_object, chunk_size = 1024):
    """ lazy function to read a file piece by piece
        default chunk size is 1kB
    Args:
        1) file_object: the handler of file
    Returns:
        1) data: a generator which contain the chunk info
    """

    while True:
        data = file_object.read(chunk_size)
        if data:
            yield data
        else:
            break

def save_active_code(filename):
    try:
        with open(filename, 'r') as f:
            data = read_big_file(f)
            if data:
                for piece in data:
                    all_lines = piece.split('\n')
                    for line in all_lines:
                        if line != '':
                            save_to_set(set_name, line)
    except IOError, e:
        print e

if __name__ == "__main__":
    get_handler()
    save_active_code("code.txt")

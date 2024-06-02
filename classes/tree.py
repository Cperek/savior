class GitTreeLeaf (object):
    def __init__(self, mode, path, sha):
        self.mode = mode
        self.path = path
        self.sha = sha


def parse_one(raw, start=0):
    # Find the space terminator of the mode
    x = raw.find(b' ', start)
    assert x-start == 5 or x-start==6

    # Read the mode
    mode = raw[start:x]
    if len(mode) == 5:
        # Normalize to six bytes.
        mode = b" " + mode

    # Find the NULL terminator of the path
    y = raw.find(b'\x00', x)
    # and read the path
    path = raw[x+1:y]

    # Read the SHA and convert to a hex string
    sha = format(int.from_bytes(raw[y+1:y+21], "big"), "040x")
    return y+21, GitTreeLeaf(mode, path.decode("utf8"), sha)

def parse(raw):
    pos = 0
    max = len(raw)
    ret = list()
    while pos < max:
        pos, data = parse_one(raw, pos)
        ret.append(data)

    return ret

def leaf_sort_key(leaf):
    if leaf.mode.startswith(b"10"):
        return leaf.path
    else:
        return leaf.path + "/"
    
def serialize(obj):
    obj.items.sort(key=leaf_sort_key)
    ret = b''
    for i in obj.items:
        ret += i.mode
        ret += b' '
        ret += i.path.encode("utf8")
        ret += b'\x00'
        sha = int(i.sha, 16)
        ret += sha.to_bytes(20, byteorder="big")
    return ret


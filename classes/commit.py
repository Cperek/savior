import collections

def parse(raw, start = 0, dct = None):
    if not dct:
        dct = collections.OrderedDict()

    spc = raw.find(b' ', start)
    nl = raw.find(b'\n', start)


    if (spc < 0) or (nl < spc):
        assert nl == start
        dct[None] = raw[start+1:]
        return dct
    
    key = raw[start:spc]

    end = start
    while True:
        end = raw.find(b'\n', end+1)
        if raw[end+1] != ord(' '):
            break

    value = raw[spc+1:end].replace(b'\n ', b'\n')

    if key in dct:
        if type(dct[key]) == list:
            dct[key].append(value)
        else:
            dct[key] = [dct[key], value]
    else:
        dct[key] = value

    return parse(raw, start=end+1, dct=dct)


def serialize(commit):
    ret = b''

    # Output fields
    for k in commit.keys():
        # Skip the message itself
        if k == None: continue
        val = commit[k]
        # Normalize to a list
        if type(val) != list:
            val = [ val ]

        for v in val:
            ret += k + b' ' + (v.replace(b'\n', b'\n ')) + b'\n'

    # Append message
    ret += b'\n' + commit[None] + b'\n'

    return ret

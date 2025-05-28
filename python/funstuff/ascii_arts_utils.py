import re

color_mappings = {
    'RED': '\x1b[31;1m',
    'GREEN': '\x1b[32;1m',
    'YELLOW': '\x1b[33;1m',
    'BLUE': '\x1b[34;1m',
    'GRAPE': '\x1b[38;2;104;83;156;1m',
    'CLEAR': '\x1b[0m'
}

def parse_tags(ascii_art):
    ans = ''
    last = 0
    for res in re.finditer(r'\[(%s)\]' % '|'.join(color_mappings.keys()), ascii_art):
        span = res.span()
        code = (color_mappings['CLEAR'] if last else '') + color_mappings[ascii_art[span[0]+1:span[1]-1]]
        ans += ascii_art[last:span[0]] + code
        last = span[1]
    return ans + ascii_art[last:] + color_mappings['CLEAR']

def clear_ansi_codes(s, collect = True):
    ans = re.sub('\x1b\\[[\\d;]+m', '', s)
    if collect:
        dic = dict()
        for i, line in enumerate(s.splitlines()):
            l = 0
            last = None
            for res in re.finditer('\x1b\\[[\\d;]+m', line):
                span = res.span()
                last = (i, span[0] - l)
                dic[last] = line[span[0]:span[1]]
                l += span[1] - span[0]
            if last is not None and span[1] == len(line.rstrip()) - 1:
                dic[(i, -1)] = dic.pop(last)
        return ans, dic
    return ans

def overlap(*args, overlap_margin = 1):    # (str1, i1, j1), (str2, i2, j2), ...
    h = 0
    w = 0
    for ascii_art, i, j in args:
        s = clear_ansi_codes(ascii_art, False)
        h = max(h, len(s.splitlines()) + i)
        for line in s.splitlines():
            w = max(w, len(line.rstrip()) + j)
    canvas = [list(' '*w) for _ in range(h)]
    for ascii_art, i, j in args:
        s, dic = clear_ansi_codes(ascii_art)
        for si, line in enumerate(s.splitlines()):
            for sj, ss in enumerate(line):
                if ss.strip():
                    lb = max(0, sj+j-overlap_margin)
                    rb = min(w, sj+j+overlap_margin+1)
                    ub = max(0, si+i-overlap_margin)
                    bb = min(h, si+i+overlap_margin+1)
                    for ci in range(ub, bb):
                        canvas[ci][lb:rb] = ' '*(rb-lb)
        code = '%s'
        for si, line in enumerate(s.splitlines()):
            for sj, ss in enumerate(line):
                if (si, sj) in dic:
                    tmp = dic[(si, sj)]
                    code = '%s' if tmp == color_mappings['CLEAR'] else tmp + '%s' + color_mappings['CLEAR']
                if ss.strip():
                    canvas[si+i][sj+j] = code % ss
            if (si, -1) in dic:
                code = dic[(si, -1)] + '%s' + color_mappings['CLEAR']
    return '\n'.join(''.join(line) for line in canvas)

import re
import warnings


# Fomater Tool
class FT:
    VARIABLE = "[a-zA-Z_][a-zA-Z0-9_]*"
    NUMBER = "[0-9]*\.?[0-9]+"
    ALPHA = "[a-zA-Z_][a-zA-Z]*"
    INTEGER = "[0-9]+"
    COMMA = ","
    COLON = ":"
    SEMICOLON = ";"
    EQUAL = "="
    PLUS = "\+"
    MINUS = "-"
    MULTIPLY = "\*"
    DIVIDE = "/"
    POWER = "\^"
    LBRACKET = "\("
    RBRACKET = "\)"
    LBRACE = "\{"
    RBRACE = "\}"
    LBRACKET_S = "\["
    RBRACKET_S = "\]"
    LANGLE = "<"
    RANGLE = ">"
    DOLLAR = "\$"
    DOT = "\."
    QUESTION = "\?"

    # RE Special
    BLANK_CHAR = "\s"
    DIGIT_CHAR = "\d"
    WORD_CHAR = "\w"
    NBLANK_CHAR = "\S"
    NDIGIT_CHAR = "\D"
    NWORD_CHAR = "\W"
    ANY_CHAR = "[.\n]"
    OP_ANYMORE = "*"
    OP_ATLEAST = "+"
    OP_MAYBE = "?"

    # #
    BLANK_ANYMORE = BLANK_CHAR + OP_ANYMORE
    BLANK_ATLEAST = BLANK_CHAR + OP_ATLEAST
    BLANK_MAYBE = BLANK_CHAR + OP_MAYBE

    def __init__(self):
        self.funcs = []  # list of functions
        self.groupss = []  # list of groups
        self.hts = []  # list of (head, tail)
        self.areass = []  # list of areas

        # current
        self.func = None  # current function
        self.groups = None  # current group
        self.ht = None  # current (head, tail)
        self.areas = None

    @staticmethod
    def _check_bracket(txt: str):
        """
        Check if any brackets in txt
        :param txt:
        :return:
        """
        if txt.find('(') != -1 and txt.find(')') != -1:
            warnings.warn(f'Should not use brackets in {txt}')
            return True
        return False

    @staticmethod
    def _expand_area(areas, size) -> list:
        """
        Expand area to a list
        :param areas:
        :param size: max value. If index over size, will raise Exception
        :return:
        """
        res = []
        for area in areas:
            if isinstance(area, int):
                res += [area]
            elif isinstance(area, tuple):
                if len(area) != 2:
                    raise Exception(f'Area {area} should be a tuple of (start, end)')
                start, end = area
                if start < 0 or start >= size:
                    raise Exception(f'Area {area} start {start} out of range')
                if end < 0 or end >= size:
                    raise Exception(f'Area {area} end {end} out of range')
                if start > end:
                    raise Exception(f'Area {area} start {start} should less than end {end}')
                res += list(range(start, end))
            else:
                raise Exception(f'Area {area} should be a tuple of (start, end) or a index')
        return res

    def login(self, fn, *groups: str, start: bool = False, end: bool = False, areas: list = None):
        """
        Login a function
        :param fn:
        :param groups:
        :param start:
        :param end:
        :param areas: list of area, each area is a tuple of (start, end) or a index
        :return:
        """
        for group in groups:
            self._check_bracket(group)

        # check exists
        if fn in self.funcs:
            warnings.warn(f'Function {fn} already exists')

        # check groups
        if groups in self.groupss:
            warnings.warn(f'Groups {groups} already exists')

        # head and tail
        if start:
            start = '^'
        else:
            start = ''
        if end:
            end = '$'
        else:
            end = ''

        # areas
        if areas is None:
            areas = list(range(len(groups)))
        else:
            areas = self._expand_area(areas, len(groups))

        # add
        self.funcs.append(fn)
        self.groupss.append(groups)
        self.hts.append((start, end))
        self.areass.append(areas)

    def logout(self, *items):
        """
        logout fn or groups
        :param items: a fn or groups
        :return:
        """
        if len(items) == 0:
            warnings.warn('Logout nothing')
            return

        if isinstance(items[0], str):
            if not items in self.groupss:
                warnings.warn(f'Groups {items} not exists')
                return
            self.groupss.remove(items)
        else:
            if not items[0] in self.funcs:
                warnings.warn(f'Function {items} not exists')
                return
            self.funcs.remove(items[0])

    def _sub_fn(self, matched):
        # get each groups
        cares = matched.groups()
        # create params
        params = []
        for area in self.areas:
            if not isinstance(area, int):
                raise Exception(f'Area {self.areas} should be a list[int].')
            params.append(cares[area])
        # call
        return self.func(*params)

    def handle(self, txt: str):
        lens = len(self.funcs), len(self.groupss), len(self.hts)
        assert lens[0] == lens[1] == lens[2], f'Length of funcs, groups, hts not equal: {lens}'
        for i in range(lens[0]):
            self.func = self.funcs[i]
            self.groups = self.groupss[i]
            self.areas = self.areass[i]
            head, tail = self.hts[i]
            self.ht = (head, tail)

            # Build pattern
            pat = head
            for group in self.groups:
                pat += f'({group})'
            pat += tail

            # Replace
            txt = re.sub(pat, self._sub_fn, txt)

        return txt

    # call
    def __call__(self, txt: str):
        return self.handle(txt)


class FRemove(FT):
    """
    Remove data by format
    """

    def __init__(self):
        super().__init__()

    def login(self, val_id: int, *groups: str, start: bool = False, end: bool = False, areas: list = None):
        super().login(lambda *args: "", *groups, start=start, end=end, areas=areas)


class FDict(FT):
    """
    Get Dict data by format
    """

    def __init__(self):
        super().__init__()
        self.dict = {}

    def _hook_key_val(self, *args, key_id=None, val_id=None, val_default=None):
        assert key_id is not None, f'key_id should not be None'
        key = args[key_id]
        if val_id is None:
            val = val_default
        else:
            val = args[val_id]
        self.dict[key] = val
        return ''.join(args)

    def login(self, key_id, val_id, *groups: str, start: bool = False, end: bool = False, areas: list = None, val_default=None):
        fn = lambda *args: self._hook_key_val(*args, key_id=key_id, val_id=val_id, val_default=val_default)
        super().login(fn, *groups, start=start, end=end, areas=areas)

    # dict functions
    def keys(self):
        return self.dict.keys()

    def values(self):
        return self.dict.values()

    def items(self):
        return self.dict.items()

    def __getitem__(self, item):
        return self.dict[item]

    def __setitem__(self, key, value):
        self.dict[key] = value

    def __contains__(self, item):
        return item in self.dict

    def __len__(self):
        return len(self.dict)

    def __iter__(self):
        return self.dict.__iter__()

    def __str__(self):
        return self.dict.__str__()

    def clear(self):
        self.dict.clear()

    def pop(self, key):
        return self.dict.pop(key)

    def get(self, key, default=None):
        return self.dict.get(key, default)

    def todict(self):
        return self.dict.copy()


class FSet(FT):
    """
    Get Set data by format
    """

    def __init__(self):
        super().__init__()
        self.set = set()

    def _hook_set(self, *args, val_id=None):
        assert val_id is not None, f'val_id should not be None'
        self.set.add(args[val_id])
        return ''.join(args)

    def login(self, val_id: int, *groups: str, start: bool = False, end: bool = False, areas: list = None):
        fn = lambda *args: self._hook_set(*args, val_id=val_id)
        super().login(fn, *groups, start=start, end=end, areas=areas)

    # set functions
    def add(self, item):
        self.set.add(item)

    def remove(self, item):
        self.set.remove(item)

    def discard(self, item):
        self.set.discard(item)

    def pop(self):
        return self.set.pop()

    def clear(self):
        self.set.clear()

    def __contains__(self, item):
        return item in self.set

    def __len__(self):
        return len(self.set)

    def __iter__(self):
        return self.set.__iter__()

    def __str__(self):
        return self.set.__str__()

    def toset(self):
        return self.set.copy()


class FList(FT):
    """
    Get List data by format
    """

    def __init__(self):
        super().__init__()
        self.list = []

    def _hook_list(self, *args, val_id=None):
        assert val_id is not None, f'val_id should not be None'
        self.list.append(args[val_id])
        return ''.join(args)

    def login(self, val_id: int, *groups: str, start: bool = False, end: bool = False, areas: list = None):
        fn = lambda *args: self._hook_list(*args, val_id=val_id)
        super().login(fn, *groups, start=start, end=end, areas=areas)

    # list functions
    def append(self, item):
        self.list.append(item)

    def remove(self, item):
        self.list.remove(item)

    def pop(self, index=-1):
        return self.list.pop(index)

    def clear(self):
        self.list.clear()

    def __contains__(self, item):
        return item in self.list

    def __len__(self):
        return len(self.list)

    def __getitem__(self, item):
        return self.list[item]

    def __setitem__(self, key, value):
        self.list[key] = value

    def __iter__(self):
        return self.list.__iter__()

    def __str__(self):
        return self.list.__str__()

    def tolist(self):
        return self.list.copy()


if __name__ == '__main__':
    test = """
        Pip 和 Conda 是 Python 的两大软件包管理工具，它们的官方源在国内访问困难，下载速度非常慢。一般情况下我们使用的都是国内的镜像源，例如清华大学的 TUNA 镜像站、阿里云的镜像站。
    
    但是有些软件包体积非常大，安装的时候从镜像站下载下来仍然需要等待很长时间，如果正巧遇到镜像站负载高峰导致下载速度缓慢，那更是雪上加霜。
    
    为了防止配环境的时候软件包下载等待时间过长，$SINGLE:1$可行的方法就是搭建$SINGLE1:1$本地镜像源，在下载的时候直接从本地镜像源下载，速度能够达到内网带宽。如果是千兆内网，那么理论可以达到 125MB/s，这个速度即使是$SINGLE2:9$ GB 的软件包，也能在半分钟内装好。
    """
    ft = FDict()
    ft.login(0, 1, FT.DOLLAR, FT.VARIABLE, FT.COLON, FT.NUMBER, FT.DOLLAR, areas=[1, 3])
    ft(test)
    print(ft)

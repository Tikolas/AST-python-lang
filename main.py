class SMP:
    def __init__(self, func, *args) -> None:
        self.func = func
        self.args = list(args)

class AST20_CONF:
    """
    Нужен ли prev
    и нужно ли управлять потоком символов

    while 1

    """
    def __init__(self) -> None:
        self.prevNeed = False # если надо -
        self.needConf = False # если функция +
        self.funcEnd = False # если надо end -
        self.isWhile = False # если цикл -
        self.whileSum = 0 # если цикл считать -
        self.whileFree = False # если inf -
        self.whileCond = False # если условия -

        self.prev: str = "" # прошлый символ
        self.r1 = 1
        self.res = ""
        self.ptr = 0 # указатель на isWhile char
        self.ptrCon = 0 # указатель на функцию
    def refresh(self):
        self.__init__()

class AST20_INST:
    def __init__(self) -> None:
        self.con: list[SMP] = []
        self.conf = AST20_CONF()

    def enter(self, text):
        if self.conf.isWhile:
            self.whiled(text)
        else:
            self.fored(text)
    
    def fored(self, text):
        if self.conf.prevNeed:
            self.conf.prev = text[0]
        for char in text[int(self.conf.prevNeed):]:
            self.callFunc(char)

            if self.conf.prevNeed:
                self.conf.prev = char
        # End func
        self.endFunc()

    def whiled(self, text):
        if self.conf.prevNeed:
            self.conf.prev = text[0]
            self.conf.ptr = 1
        while self.conf.whileFree or self.conf.whileCond and self.conf.ptr < len(text):
            self.callFunc(text[self.conf.ptr])

            if self.conf.prevNeed:
                self.conf.prev = text[self.conf.ptr]
            if self.conf.whileSum > 0:
                self.conf.ptr += self.conf.whileSum
        # End func
        self.endFunc()

    def endFunc(self):
        con = self.con[self.conf.ptrCon]
        if self.conf.funcEnd and self.conf.needConf:
            con.func(self.conf, None, *con.args)
        elif self.conf.funcEnd:
            con.func(None, *con.args)
    
    def callFunc(self, char):
        con = self.con[self.conf.ptrCon]

        if self.conf.needConf:
            con.func(self.conf, char, *con.args)
        else:
            con.func(char, *con.args)

class AST20:
    def __init__(self) -> None:
        self.inst: AST20_INST = AST20_INST()

    def append(self, func, *args):
        self.inst.con.append(SMP(func, *args))

    def enter(self, text):
        if type(text) == str and len(text) > 0:
            self.inst.enter(text)
        else:
            print("Error")
    
    def onConf(self):
        self.inst.conf.needConf = not self.inst.conf.needConf

    @property
    def result(self):
        return self.inst.conf.res

a = AST20()
a.onConf()

def count(ctx: AST20_CONF, char):
    if char == ctx.prev:
        ctx.r1+=1
    else:
        if ctx.r1 == 1:
            ctx.res+=f"{ctx.prev}"
        else:
            ctx.res+=f"{ctx.prev}{ctx.r1}"
        ctx.r1 = 1
    ctx.prev = char

a.append(count)
a.enter("aaaaaabbbbbbCCCCddfqwordfff")
print(a.result)

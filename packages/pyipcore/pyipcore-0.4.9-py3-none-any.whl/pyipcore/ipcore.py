import re

from pyipcore.ipc_utils import *
from files3 import files

VAR_PARAM_TYPE = "param"
VAR_PORT_TYPE = 'port'


class IpCore:
    """
    维护IP核文本
    """

    def __init__(self, dir, name):
        self.fdir = os.path.abspath(dir)
        self.key = name
        self.f = files(self.fdir, IPC_SUFFIX)
        if not self.f[self.key]:
            raise Exception("IP core not found: {}".format(name))

        self._built = None
        self._last_icode = None

    def GetICode(self):
        """Get the instance code of the IP core."""
        return self.icode

    @staticmethod
    def FromVerilog(dir, name, vpath):
        """Trasform a Verilog file into an IP core."""
        f = files(dir, IPC_SUFFIX)
        with open(vpath, encoding='utf-8') as vf:
            content = vf.read()
        f[name] = content

    VERILOG_NUMBER = f"({FT.DIGIT_CHAR}+'{FT.ALPHA})?[0-9_]+"

    @staticmethod
    def _auto_type_change(params_dict):
        """
        自动转换参数类型，会自动检查str类型的int, float数据，并转换为int, float。
        :param params_dict: 包含参数的字典，其中值可能是str, int, float等类型
        :return: 转换后的字典
        """
        for key, value in params_dict.items():
            # 尝试将值转换为整数
            if isinstance(value, str) and value.isdigit():
                params_dict[key] = int(value)
            # 尝试将值转换为浮点数
            elif isinstance(value, str):
                try:
                    # 尝试转换为浮点数
                    params_dict[key] = float(value)
                except ValueError:
                    # 如果转换失败，保留原始字符串
                    pass
        return params_dict

    @staticmethod
    def _handle_eval(txt, params_dict):
        """
        处理EVAL表达式。
        要求格式为'$(表达式)'，最后将结果的str替换原表达式。
        能使用的环境只有params_dict。
        :param txt: 原始文本
        :param params_dict: 包含变量名和值的字典
        :return: 替换后的文本
        """

        # 定义一个函数，用于计算表达式并返回结果
        def eval_expr(match):
            # 获取匹配到的表达式部分
            expr = match.group(1)
            try:
                # 使用eval函数计算表达式，传入params_dict作为局部变量环境
                result = eval(expr, {}, params_dict)
                # 返回计算结果的字符串形式
                return str(result)
            except Exception as e:
                # 如果表达式计算出错，返回原始表达式
                return '$EVAL({})'.format(expr)

        # 使用re.sub函数替换文本中的所有EVAL表达式
        return re.sub(r'\$\((.*?)\)', eval_expr, txt)

    def build(self, **params) -> str:
        """Build the IP core with the given parameters."""
        content = self.content
        ft = FT()
        ft.login(lambda key: str(params[key]), *IPC_W_VAL_GS, areas=[IPC_W_VAL_VID])
        ft.login(lambda k, v: (v if params[k] else ""), *IPC_REMOVE_GS, areas=list(IPC_REMOVE_KVID))
        _content = ft.handle(content)
        _content = self._handle_eval(_content, self._auto_type_change(params))
        self._built = _content
        return self._built

    # ----------------------------------------- Following are properties -----------------------------------------

    @property
    def content(self):
        """Return the content of the IP core."""
        return self.f[self.key]

    # 获取参数默认值
    @property
    def defaults(self):
        """Return the parameters and values of the IP core."""
        fdict = FDict()
        fdict.login(*IPC_VAL_KVID, *IPC_VAL_GS)  # 参数默认值     \\ $a = 1
        fdict.handle(self.content)
        return fdict

    # 获取参数名称
    @property
    def keys(self):
        """Return the parameters of the IP core."""
        fset = FSet()
        fset.login(IPC_REMOVE_KVID[0], *IPC_REMOVE_GS)  # 分支控制变量   \\ $$a ... $$
        fset.login(IPC_VAL_KVID[0], *IPC_VAL_GS)  # 参数默认值     \\ $a = 1
        fset.handle(self.content)
        return fset

    @property
    def dict(self):
        """Return the parameters of the IP core."""
        fdict = FDict()
        fdict.login(*IPC_VAL_KVID, *IPC_VAL_GS)
        fdict.login(IPC_REMOVE_KVID[0], None, *IPC_REMOVE_GS, val_default=False)
        fdict.handle(self.content)
        return fdict

    @property
    def types(self) -> dict:
        d = self.dict
        return {k: VAR_PARAM_TYPE if d[k] else VAR_PORT_TYPE for k in d}

    @property
    def icode(self):
        """
        Get the instance code of the IP core.
        * Cost lots of time.
        :return:
        """
        _ = create_module_inst_code(self.built)
        self._last_icode = _
        return _

    @property
    def last_icode(self):
        return self._last_icode

    @property
    def built(self):
        if self._built is None:
            self.build(**self.dict)
        return self._built


if __name__ == '__main__':
    IpCore.FromVerilog("", 'test', r'H:\FPGA_Learns\00 IPC\_raw\counter.v2.v')
    # raise
    ip = IpCore("", 'test')
    d = ip.dict
    # d['WIDTH'] = 32
    # d['add_clr'] = False
    t = ip.build(**d)
    # save to a counter~.v file
    # with open('counter~.v', 'w', encoding='utf-8') as f:
    #     f.write(t)
    # test = "module Counter #(parameter WIDTH=16,parameter RCO_WIDTH=4"
    # txt = ip.decorate_paragraph(test, 30, 35, "WIDTH", 0)
    # print(txt)
    # txt = ip.decorate_paragraph(txt, 33, 35, "WIDTH", 0)
    print(ip.dict)
    print(ip.types)
    print(ip.icode)
    print(ip._built)

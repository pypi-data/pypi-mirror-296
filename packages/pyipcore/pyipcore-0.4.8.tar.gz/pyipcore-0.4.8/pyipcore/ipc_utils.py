import os
import re
import typing

from PyQt5.QtCore import QThread
from reft import *
from files3 import files, F3False

IPC_SUFFIX = '.ipc'

V_SUFFIXS = ['.v', '.sv']

OPEN_TYPE = "Verilog (*.v);;SystemVerilog (*.sv);;IP Core (*.ipc)"
SAVE_TYPE = "IP Core (*.ipc);;Verilog (*.v);;SystemVerilog (*.sv)"

VERILOG_TYPE = "Verilog (*.v);;SystemVerilog (*.sv)"

# 读取变量默认值的正则表达式参数, 例如: // $a = 1
IPC_VAL_GS = [
    "//+\s*\$",  # 0 "// $"
    FT.VARIABLE,  # 1 "a"
    "\s*=\s*",  # 2 " = "
    "[^;/\s]+",  # 3 "1"
]
IPC_VAL_KVID = (1, 3)  # (key, value) index in IPC_VAL_GS

# 读取分支控制的正则表达式参数, 例如: // $$a ... ... $$
IPC_REMOVE_GS = [
    "//+\s*\$\$",  # 0 "// $$"
    FT.VARIABLE,  # 1 "a"
    "[^\$]+",  # 2 " ... ... "
    "\$\$"  # 3 "$$"
]
IPC_REMOVE_KVID = (1, 2)  # (key, value) index in IPC_REMOVE_GS

# 写变量的正则表达式参数, 例如: $XXX$
IPC_W_VAL_GS = [
    FT.DOLLAR,  # 0 "$"
    FT.VARIABLE,  # 1 "XXX"
    FT.DOLLAR  # 2 "$$"
]
IPC_W_VAL_VID = 1  # value index in IPC_W_VAL_GS


def get_lib_path():
    """Return the absolute path of the library."""
    # read lib_path from files
    f = files(os.getcwd())
    lib_path = f.get("lib_path")
    if lib_path is F3False:
        return os.getcwd()
    return lib_path


from pyverilog.vparser.parser import parse as verilog_parse
from pyverilog.vparser.ast import ModuleDef, Input, Inout, Output, IntConst, Minus, Plus


def get_str_value(var):
    """
    获取str类型的值
    :param var: IntConst
    :return: str
    """
    if var is None:
        return ""
    elif isinstance(var, IntConst):
        return var.value
    elif isinstance(var, Minus):
        return "-" + get_str_value(var.left)


def get_module_parameters(param_s) -> dict:
    """
    获取module的参数
    :param param_s: module.paramlist.show() txt
        @example:
        parameter WIDTH = GLOBAL_SET * 1,
        parameter RCO_WIDTH = 4
    :return: dict {name: value}
    """
    rslt = {}

    def _sub_fn(matched):
        # get groups
        name, value = matched.group(1), matched.group(2)
        rslt[name] = value

    # group1: name, group2: value
    pat = re.compile(fr"parameter\s+({FT.VARIABLE})\s*=\s*([^,^\n,^(parameter)]+)")

    re.sub(pat, _sub_fn, param_s)

    return rslt


def get_module_ports(ports_s) -> dict:
    """
    获取module的端口
    :param ports_s: module.portlist.show() txt
        @example:
        input clk,
        input nrst,
        input en,
        input [WIDTH-1:0] i_cmp,
        output reg [WIDTH-1:0] o_cnt,
        output o_rco
    :return: dict {name: (direction:str, prefix:str, width:str)}
    """
    rslt = {}

    def _sub_fn(matched):
        # get groups
        direction, prefix, width, name = matched.group(1), matched.group(2), matched.group(3), matched.group(4)
        # 除了name和direction, 其他都可能为None
        if prefix is None:
            prefix = ""
        if width is None:
            width = ""
        # 移除每个元素末尾的\s*
        prefix = prefix.rstrip()
        width = width.rstrip()

        rslt[name] = (direction, prefix, width)

    # group1: direction, group2: prefix, group3: width, group4: name
    pat = re.compile(fr"(input|output|inout)\s+(reg|wire|logic)?\s*(\[[^\]]+\]\s+)?({FT.VARIABLE})(,\s*)?")

    re.sub(pat, _sub_fn, ports_s)

    return rslt


class StdoutString:
    def __init__(self):
        self.content = ""

    def write(self, txt):
        self.content += txt

    def flush(self):
        pass

    def __str__(self):
        return self.content

    def __repr__(self):
        return self.conten


def show(node) -> StdoutString:
    """
    显示ast的内容
    :param node: ast
    :return: StdoutString
    """
    ss = StdoutString()
    node.show(buf=ss, attrnames=True, showlineno=False)
    return ss


from pyverilog.ast_code_generator.codegen import ASTCodeGenerator


def create_module_inst_code(txt: str) -> str:
    """
    生成verilog module模块的实例代码
    :param txt: 整个module的代码
    :return: module的实例代码
    """

    current_idx = 0
    spec_sv = {}  # 把不属于verilog的部分放到这里，$SPEC_SV_{i}$: sv code
    new_txt = ""
    for line in txt.split("\n"):
        # 1. remove typedef
        if line.find("typedef") != -1:
            key = f"$SPEC_SV_{current_idx}$"
            spec_sv[key] = line
            # new_txt += key + "\n"  # 暂时不添加
            current_idx += 1
            continue
        new_txt += line + "\n\n"
    txt = new_txt

    # remove all between ');' and 'endmodule'
    pat = re.compile("\)\s*;")
    new_txt = ""
    left_txt = txt
    while True:
        matched = pat.search(left_txt)
        if matched is None:
            break
        start, end = matched.span()

        # find the endmodule
        endmodule_idx = left_txt.find("endmodule")
        if endmodule_idx == -1:
            raise ValueError("Can't find 'endmodule' after ');'.")
        new_txt += left_txt[:end] + "\nendmodule\n"
        left_txt = left_txt[endmodule_idx + len("endmodule"):]
    new_txt += left_txt
    txt = new_txt

    # remove more \n
    txt = re.sub(r"\n\n+", "\n", txt)

    # logic -> reg
    txt = re.sub(r"\blogic\b", "reg", txt)

    # WRITE TO FILE # DEBUG
    # open("temp.v", "w").write(txt)

    try:
        ast, _ = verilog_parse([txt])
    except FileNotFoundError as err:
        pre_found_error = "[WinError 2]"
        if str(err).find(pre_found_error) != -1:
            raise Exception("Please retry after install 'iverilog' from 'http://bleyer.org/icarus/' and add it to path.")
        raise err
    for description in ast.children():
        if description.definitions:
            for part_code in description.definitions:
                if isinstance(part_code, ModuleDef):
                    # print(get_module_parameters(part_code))
                    # print("module_name:", part_code.name)
                    # # print("module_parameter:", part_code.paramlist)
                    # print("module_port:", get_module_ports(part_code))
                    # ss = show(part_code.paramlist)
                    # print(ss)
                    codegen = ASTCodeGenerator()
                    rslt = codegen.visit(part_code.paramlist)
                    # print(rslt)
                    params = get_module_parameters(rslt)
                    codegen = ASTCodeGenerator()
                    rslt = codegen.visit(part_code.portlist)
                    # print(rslt)
                    ports = get_module_ports(rslt)
                    # ss = show(part_code.portlist)
                    # print(ss)
                    # /// build inst code
                    ic = ""
                    ic += f"{part_code.name} " + ("#(\n" if params else "")  # module name
                    # /// add parameters
                    for k, v in params.items():
                        ic += f"\t.{k}({v}),\n"
                    if params:
                        ic = ic[:-2] + "\n"
                    ic += (") " if params else "") + f"{part_code.name.lower()}_inst (\n"
                    # /// add ports
                    for k, v in ports.items():
                        ic += f"\t.{k}({k}),\n"

                    ic = ic[:-2] + "\n"
                    ic += ");"
                    return ic
    return ""






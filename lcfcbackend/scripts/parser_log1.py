import subprocess

# windbg 可执行文件路径
windbgx_path = r"C:\Program Files\Windows Kits\10\Debuggers\x64\windbg.exe"
# windbg 后台程序路径
kdX86_path = r"C:\Program Files\Windows Kits\10\Debuggers\x64\kd.exe"

"""
当前脚本执行会先打开windbg界面,之后执行命令，命令完成之后关闭界面
"""


def parser_dump(dump_path):
    # winddbg.exe -z C:\Users\wzb\Downloads\msedge.DMP -c .logopen 3.log -c !analyze  -v
    args = [windbgx_path,
            "-z", dump_path,  # load dump
            "-logo", "1.log",  # 输出保存文件
            # "-y", f'{SYMBOL_PATH}',   # 加载pdb文件
            "-c", "!analyze  -v; q",  # 执行命令，多条命令使用;号分割
            ]

    result = subprocess.run(
        args=args,
        stdin=subprocess.PIPE,
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
        text=True,
        encoding='utf-8'
    )
    print(result.returncode)


if __name__ == '__main__':
    # 批量处理 Dump 文件
    dump_file = r"C:\Users\wzb\Downloads\msedge.DMP"
    parser_dump(dump_file)

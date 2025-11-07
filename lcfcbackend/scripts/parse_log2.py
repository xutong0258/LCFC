import subprocess


windbgx_path = r"C:\Program Files\Windows Kits\10\Debuggers\x64\windbg.exe"
kdX86_path = r"C:\Program Files\Windows Kits\10\Debuggers\x64\kd.exe"

"""
第二中方式执行，后端运行，可以增加命令，获取解析的结果,无需将解析结果保存到日志中,更符合多步执行
这种方式运行更优
"""

if __name__ == "__main__":
    import psutil

    dump_file = r"C:\Users\wzb\Downloads\msedge.DMP"

    args = [kdX86_path,
            "-z", dump_file,
            "-logo", "4.log",
            # "-y", f'{SYMBOL_PATH}',
            # "-c", "!analyze  -v",
            # "-c", ".logclose",
            # "-c", "qqd"
            ]

    process = subprocess.Popen(
        args=args,
        stdin=subprocess.PIPE,
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
        text=True,
        encoding='utf-8'
    )
    # 提供输入
    input_data = "!analyze  -v\nq\n"
    # input_data = "!analyze  -v\n"
    stdout, stderr = process.communicate(input=input_data)
    print(stdout)



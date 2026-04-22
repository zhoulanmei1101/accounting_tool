#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
命令解析模块
负责解析命令行参数、验证用户输入和提供命令帮助
"""

import sys
from typing import Dict, Any, Optional, List


class CLIParser:
    """命令行解析器类"""

    # 支持的命令列表
    VALID_COMMANDS = ['add', 'list', 'total', 'help']

    def __init__(self):
        """初始化命令行解析器"""
        self.command = None
        self.args = {}

    def parse_arguments(self) -> Dict[str, Any]:
        """
        解析命令行参数

        返回:
            包含命令和参数的字典，格式为:
            {
                'command': 命令名称 (str),
                'args': {参数名: 参数值} (dict)
            }
        """
        if len(sys.argv) < 2:
            self._show_help()
            sys.exit(0)

        # 获取命令
        self.command = sys.argv[1].lower()

        # 验证命令
        if self.command not in self.VALID_COMMANDS:
            print(f"错误: 无效的命令 '{self.command}'")
            print(f"有效命令: {', '.join(self.VALID_COMMANDS)}")
            sys.exit(1)

        # 解析各命令的参数
        if self.command == 'add':
            self.args = self._parse_add_args()
        elif self.command == 'list':
            self.args = self._parse_list_args()
        elif self.command == 'total':
            self.args = self._parse_total_args()
        elif self.command == 'help':
            self._show_help()
            sys.exit(0)

        return {
            'command': self.command,
            'args': self.args
        }

    def _parse_add_args(self) -> Dict[str, Any]:
        """
        解析 add 命令的参数

        add 命令格式:
            add --type <收入/支出> --amount <金额> --description <描述>
            或使用短选项: -t, -a, -d

        返回:
            包含 add 命令参数的字典
        """
        args = {
            'type': None,
            'amount': None,
            'description': None
        }

        i = 2
        while i < len(sys.argv):
            arg = sys.argv[i]

            if arg in ('--type', '-t'):
                if i + 1 < len(sys.argv):
                    args['type'] = sys.argv[i + 1]
                    i += 2
                else:
                    print("错误: --type 选项需要一个参数")
                    sys.exit(1)

            elif arg in ('--amount', '-a'):
                if i + 1 < len(sys.argv):
                    try:
                        args['amount'] = float(sys.argv[i + 1])
                    except ValueError:
                        print(f"错误: 金额必须是数字，收到 '{sys.argv[i + 1]}'")
                        sys.exit(1)
                    i += 2
                else:
                    print("错误: --amount 选项需要一个参数")
                    sys.exit(1)

            elif arg in ('--description', '-d'):
                if i + 1 < len(sys.argv):
                    args['description'] = sys.argv[i + 1]
                    i += 2
                else:
                    print("错误: --description 选项需要一个参数")
                    sys.exit(1)

            else:
                # 尝试将位置参数映射到对应的选项
                if args['type'] is None:
                    args['type'] = arg
                elif args['amount'] is None:
                    try:
                        args['amount'] = float(arg)
                    except ValueError:
                        print(f"错误: 金额必须是数字，收到 '{arg}'")
                        sys.exit(1)
                elif args['description'] is None:
                    args['description'] = arg
                else:
                    print(f"错误: 无法识别的参数 '{arg}'")
                    sys.exit(1)
                i += 1

        # 验证必填参数
        if args['type'] is None:
            print("错误: 缺少 --type 参数，请指定 '收入' 或 '支出'")
            sys.exit(1)

        if args['amount'] is None:
            print("错误: 缺少 --amount 参数，请指定金额")
            sys.exit(1)

        # 验证类型
        if args['type'] not in ['收入', '支出']:
            print(f"错误: --type 必须是 '收入' 或 '支出'，收到 '{args['type']}'")
            sys.exit(1)

        # 验证金额为正数
        if args['amount'] <= 0:
            print(f"错误: 金额必须大于 0，收到 '{args['amount']}'")
            sys.exit(1)

        # 提供默认描述
        if args['description'] is None:
            if args['type'] == '收入':
                args['description'] = '其他收入'
            else:
                args['description'] = '其他支出'

        return args

    def _parse_list_args(self) -> Dict[str, Any]:
        """
        解析 list 命令的参数

        list 命令格式:
            list [--limit <数量>] [--type <收入/支出>]
            或使用短选项: -l, -t

        返回:
            包含 list 命令参数的字典
        """
        args = {
            'limit': None,
            'type': None
        }

        i = 2
        while i < len(sys.argv):
            arg = sys.argv[i]

            if arg in ('--limit', '-l'):
                if i + 1 < len(sys.argv):
                    try:
                        args['limit'] = int(sys.argv[i + 1])
                    except ValueError:
                        print(f"错误: --limit 必须是整数，收到 '{sys.argv[i + 1]}'")
                        sys.exit(1)

                    if args['limit'] <= 0:
                        print(f"错误: --limit 必须大于 0，收到 '{args['limit']}'")
                        sys.exit(1)
                    i += 2
                else:
                    print("错误: --limit 选项需要一个参数")
                    sys.exit(1)

            elif arg in ('--type', '-t'):
                if i + 1 < len(sys.argv):
                    args['type'] = sys.argv[i + 1]
                    if args['type'] not in ['收入', '支出']:
                        print(f"错误: --type 必须是 '收入' 或 '支出'，收到 '{args['type']}'")
                        sys.exit(1)
                    i += 2
                else:
                    print("错误: --type 选项需要一个参数")
                    sys.exit(1)

            else:
                print(f"错误: 无法识别的参数 '{arg}'")
                sys.exit(1)

        return args

    def _parse_total_args(self) -> Dict[str, Any]:
        """
        解析 total 命令的参数

        total 命令格式:
            total [--type <收入/支出>]
            或使用短选项: -t

        返回:
            包含 total 命令参数的字典
        """
        args = {
            'type': None
        }

        i = 2
        while i < len(sys.argv):
            arg = sys.argv[i]

            if arg in ('--type', '-t'):
                if i + 1 < len(sys.argv):
                    args['type'] = sys.argv[i + 1]
                    if args['type'] not in ['收入', '支出']:
                        print(f"错误: --type 必须是 '收入' 或 '支出'，收到 '{args['type']}'")
                        sys.exit(1)
                    i += 2
                else:
                    print("错误: --type 选项需要一个参数")
                    sys.exit(1)

            else:
                print(f"错误: 无法识别的参数 '{arg}'")
                sys.exit(1)

        return args

    def _show_help(self) -> None:
        """显示帮助信息"""
        help_text = """
📒 简易记账工具 - 使用帮助

命令格式:
    python main.py <命令> [选项]

可用命令:
    add     新增收支记录
    list    查看账单列表
    total   统计收支总额
    help    显示此帮助信息

各命令详细说明:

1. add - 新增收支记录
   用法:
       python main.py add --type <收入/支出> --amount <金额> --description <描述>
   或使用短选项:
       python main.py add -t <收入/支出> -a <金额> -d <描述>
   或使用位置参数（按顺序）:
       python main.py add 支出 50.0 午餐

   示例:
       python main.py add --type 收入 --amount 5000 --description "工资"
       python main.py add 支出 100.5 水果
       python main.py add -t 支出 -a 200

   说明:
       - --type: 必填，只能是 "收入" 或 "支出"
       - --amount: 必填，必须是大于 0 的数字
       - --description: 可选，默认为 "其他收入" 或 "其他支出"

2. list - 查看账单列表
   用法:
       python main.py list [--limit <数量>] [--type <收入/支出>]
   或使用短选项:
       python main.py list [-l <数量>] [-t <收入/支出>]

   示例:
       python main.py list
       python main.py list --limit 10
       python main.py list --type 支出
       python main.py list -l 5 -t 收入

   说明:
       - --limit: 可选，限制显示的记录数量（默认显示全部）
       - --type: 可选，只显示 "收入" 或 "支出" 记录

3. total - 统计收支总额
   用法:
       python main.py total [--type <收入/支出>]
   或使用短选项:
       python main.py total [-t <收入/支出>]

   示例:
       python main.py total
       python main.py total --type 收入
       python main.py total -t 支出

   说明:
       - 不带参数时，显示总收入、总支出和结余
       - --type: 可选，只统计 "收入" 或 "支出" 的总额

数据存储:
    - 数据保存在当前目录下的 data/records.json 文件中
    - JSON 格式，可手动编辑（但请注意格式正确性）
    - 程序重启后数据不会丢失

错误处理:
    - 无效命令或参数时会显示清晰的错误提示
    - 数据文件损坏时会自动重置为空列表并显示警告
    - 权限不足时会提示无法读写文件
        """
        print(help_text)

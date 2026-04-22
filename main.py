#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
简易记账工具 - 主程序入口
负责整合各个模块，协调命令解析和业务逻辑执行
"""

import sys
from pathlib import Path

# 确保可以找到同目录下的模块
sys.path.insert(0, str(Path(__file__).parent))

from cli_parser import CLIParser
from account_book import AccountBook


def main():
    """主函数"""
    try:
        # 初始化组件
        parser = CLIParser()
        account_book = AccountBook()

        # 解析命令行参数
        cmd_data = parser.parse_arguments()
        command = cmd_data['command']
        args = cmd_data['args']
        command='help'
        

        # 执行相应的命令
        if command == 'add':
            # 新增记录
            success = account_book.add_record(
                record_type=args['type'],
                amount=args['amount'],
                description=args['description']
            )
            sys.exit(0 if success else 1)

        elif command == 'list':
            # 查看列表
            account_book.list_records(
                limit=args['limit'],
                record_type=args['type']
            )
            sys.exit(0)

        elif command == 'total':
            # 统计总额
            account_book.calculate_total(
                record_type=args['type']
            )
            sys.exit(0)

        elif command == 'help':
            # 显示帮助（实际上在解析阶段已经处理）
            print('help11')
            pass

    except KeyboardInterrupt:
        print("\n\n操作已取消")
        sys.exit(0)

    except Exception as e:
        print(f"\n❌ 程序运行时发生错误: {str(e)}")
        print("请使用 'python main.py help' 查看帮助信息")
        sys.exit(1)


if __name__ == "__main__":
    main()

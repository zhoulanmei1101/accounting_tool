#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
业务逻辑模块
负责实现记账的核心业务逻辑：新增记录、查看列表、统计总额
"""

import sys
import os
from datetime import datetime
from typing import List, Dict, Any, Optional

# 确保可以导入同目录下的模块
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

try:
    from data_handler import DataHandler
except ImportError:
    from .data_handler import DataHandler


class AccountBook:
    """记账本类，实现核心业务逻辑"""

    def __init__(self, data_file: str = "records.json"):
        """
        初始化记账本

        参数:
            data_file: 数据存储文件名
        """
        self.data_handler = DataHandler(data_file)
        self.records = []

    def add_record(self, record_type: str, amount: float, description: str) -> bool:
        """
        新增一条收支记录

        参数:
            record_type: 记录类型，'收入' 或 '支出'
            amount: 金额，必须大于 0
            description: 描述信息

        返回:
            添加成功返回 True，失败返回 False
        """
        # 验证参数
        if record_type not in ['收入', '支出']:
            print(f"错误: 记录类型必须是 '收入' 或 '支出'，收到 '{record_type}'")
            return False

        if amount <= 0:
            print(f"错误: 金额必须大于 0，收到 '{amount}'")
            return False

        if not description:
            # 使用默认描述
            if record_type == '收入':
                description = '其他收入'
            else:
                description = '其他支出'

        # 构建记录对象
        record = {
            'type': record_type,
            'amount': amount,
            'description': description,
            'date': datetime.now().strftime('%Y-%m-%d'),
            'time': datetime.now().strftime('%H:%M:%S')
        }

        # 调用数据处理模块保存
        success = self.data_handler.add_record(record)

        if success:
            # 显示添加成功的信息
            sign = '+' if record_type == '收入' else '-'
            print(f"✅ 记录添加成功!")
            print(f"   类型: {record_type}")
            print(f"   金额: {sign}¥{amount:.2f}")
            print(f"   描述: {description}")
            print(f"   时间: {record['date']} {record['time']}")
        else:
            print("❌ 记录添加失败，请检查错误信息")

        return success

    def list_records(self, limit: Optional[int] = None, record_type: Optional[str] = None) -> None:
        """
        查看账单列表

        参数:
            limit: 限制显示的记录数量，None 表示显示全部
            record_type: 筛选记录类型，'收入'、'支出' 或 None（显示全部）
        """
        # 加载所有记录
        records = self.data_handler.load_records()

        if not records:
            print("📭 暂无账单记录")
            return

        # 根据类型筛选
        if record_type:
            records = [r for r in records if r.get('type') == record_type]

        if not records:
            if record_type:
                print(f"📭 暂无 {record_type} 记录")
            else:
                print("📭 暂无账单记录")
            return

        # 按时间倒序排列（最新的在前面）
        records = sorted(
            records,
            key=lambda x: x.get('created_at', ''),
            reverse=True
        )

        # 限制显示数量
        if limit and len(records) > limit:
            records = records[:limit]
            print(f"📋 显示最近 {limit} 条记录 (共 {len(records)} 条)")
        else:
            print(f"📋 共 {len(records)} 条记录")

        print("-" * 80)

        # 格式化输出
        for i, record in enumerate(records, 1):
            rec_type = record.get('type', '未知')
            amount = record.get('amount', 0.0)
            description = record.get('description', '')
            date = record.get('date', '未知日期')
            time = record.get('time', '未知时间')

            # 颜色区分收入和支出
            sign = '+' if rec_type == '收入' else '-'
            amount_str = f"{sign}¥{amount:.2f}"

            # 格式化输出
            print(f"{i:3}. [{date} {time}] {rec_type:4} | {amount_str:>12} | {description}")

        print("-" * 80)

        # 显示当前筛选的统计
        if record_type:
            total = sum(r.get('amount', 0.0) for r in records)
            sign = '+' if record_type == '收入' else '-'
            print(f"当前筛选 {record_type} 总额: {sign}¥{total:.2f}")
        else:
            total_income = sum(r.get('amount', 0.0) for r in records if r.get('type') == '收入')
            total_expense = sum(r.get('amount', 0.0) for r in records if r.get('type') == '支出')
            balance = total_income - total_expense
            print(f"总收入: +¥{total_income:.2f} | 总支出: -¥{total_expense:.2f} | 结余: ¥{balance:.2f}")

    def calculate_total(self, record_type: Optional[str] = None) -> Dict[str, float]:
        """
        统计收支总额

        参数:
            record_type: 筛选记录类型，'收入'、'支出' 或 None（统计全部）

        返回:
            包含统计结果的字典
            - 当 record_type 为 None 时: {'收入': 总收入, '支出': 总支出, '结余': 结余}
            - 当 record_type 为 '收入' 或 '支出' 时: {'总额': 指定类型总额}
        """
        records = self.data_handler.load_records()

        if record_type:
            # 统计指定类型
            total = sum(
                r.get('amount', 0.0)
                for r in records
                if r.get('type') == record_type
            )
            result = {'总额': total}

            # 显示统计结果
            print(f"\n📊 {record_type}统计")
            print("-" * 40)

            count = len([r for r in records if r.get('type') == record_type])
            sign = '+' if record_type == '收入' else '-'

            print(f"记录数量: {count} 条")
            print(f"总额: {sign}¥{total:.2f}")
            print("-" * 40)

        else:
            # 统计全部
            total_income = sum(
                r.get('amount', 0.0)
                for r in records
                if r.get('type') == '收入'
            )
            total_expense = sum(
                r.get('amount', 0.0)
                for r in records
                if r.get('type') == '支出'
            )
            balance = total_income - total_expense

            result = {
                '收入': total_income,
                '支出': total_expense,
                '结余': balance
            }

            # 显示统计结果
            print("\n📊 收支统计")
            print("-" * 60)

            count_income = len([r for r in records if r.get('type') == '收入'])
            count_expense = len([r for r in records if r.get('type') == '支出'])

            print(f"收入记录: {count_income} 条 | 总收入: +¥{total_income:.2f}")
            print(f"支出记录: {count_expense} 条 | 总支出: -¥{total_expense:.2f}")
            print("-" * 60)

            # 结余颜色区分
            if balance >= 0:
                print(f"💰 当前结余: +¥{balance:.2f}")
            else:
                print(f"💸 当前结余: ¥{balance:.2f} (超支)")
            print("-" * 60)

        return result

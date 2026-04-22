#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
数据读写模块
负责 JSON 文件的读取、写入和数据持久化操作
"""

import json
import os
from pathlib import Path
from datetime import datetime
from typing import List, Dict, Any, Optional


class DataHandler:
    """数据处理器类"""

    def __init__(self, data_file: str = "records.json"):
        """
        初始化数据处理器

        参数:
            data_file: 数据存储文件名，默认为 records.json
        """
        # 数据文件路径（存储在当前脚本所在目录的 data 子目录下）
        self.data_dir = Path(__file__).parent / "data"
        self.data_file = self.data_dir / data_file

    def _ensure_data_dir_exists(self) -> None:
        """确保数据存储目录存在，如果不存在则创建"""
        try:
            if not self.data_dir.exists():
                self.data_dir.mkdir(parents=True, exist_ok=True)
        except PermissionError:
            raise PermissionError(f"无法创建数据目录: {self.data_dir}，权限不足")
        except Exception as e:
            raise RuntimeError(f"创建数据目录时发生错误: {str(e)}")

    def load_records(self) -> List[Dict[str, Any]]:
        """
        从 JSON 文件加载账单记录

        返回:
            账单记录列表，如果文件不存在或为空则返回空列表
        """
        try:
            self._ensure_data_dir_exists()

            if not self.data_file.exists():
                return []

            with open(self.data_file, 'r', encoding='utf-8') as f:
                content = f.read().strip()
                if not content:
                    return []
                return json.loads(content)

        except json.JSONDecodeError as e:
            print(f"警告: 数据文件格式错误，将重置为空列表。错误详情: {str(e)}")
            return []
        except PermissionError:
            print(f"错误: 无法读取数据文件 {self.data_file}，权限不足")
            return []
        except Exception as e:
            print(f"错误: 加载数据时发生未知错误: {str(e)}")
            return []

    def save_records(self, records: List[Dict[str, Any]]) -> bool:
        """
        将账单记录保存到 JSON 文件

        参数:
            records: 账单记录列表

        返回:
            保存成功返回 True，失败返回 False
        """
        try:
            self._ensure_data_dir_exists()

            with open(self.data_file, 'w', encoding='utf-8') as f:
                json.dump(records, f, ensure_ascii=False, indent=2, default=str)

            return True

        except PermissionError:
            print(f"错误: 无法写入数据文件 {self.data_file}，权限不足")
            return False
        except Exception as e:
            print(f"错误: 保存数据时发生未知错误: {str(e)}")
            return False

    def add_record(self, record: Dict[str, Any]) -> bool:
        """
        添加一条新的账单记录

        参数:
            record: 账单记录字典

        返回:
            添加成功返回 True，失败返回 False
        """
        try:
            records = self.load_records()

            # 为记录添加唯一ID（使用时间戳）
            if 'id' not in record:
                record['id'] = int(datetime.now().timestamp() * 1000)

            # 确保有创建时间
            if 'created_at' not in record:
                record['created_at'] = datetime.now().isoformat()

            records.append(record)
            return self.save_records(records)

        except Exception as e:
            print(f"错误: 添加记录时发生未知错误: {str(e)}")
            return False

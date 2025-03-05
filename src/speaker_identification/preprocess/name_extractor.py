import re
import json
from typing import List, Set

class NameExtractor:
    def __init__(self, name_file: str):
        """初始化人名提取器
        Args:
            name_list: 预定义的人名列表
        """
        self.name_list = self.load_name_list(name_file)  # 修改这里，使用 self 调用

    def extract_names(self, pre_context: str = "", post_context: str = "") -> List[str]:
        """从前后文中提取人名
        Args:
            pre_context: 前文内容
            post_context: 后文内容
        Returns:
            List[str]: 提取出的人名列表
        """
        try:
            # 合并前后文
            context = f"{pre_context}\n{post_context}"
            
            # 从预定义名单中查找匹配的人名
            names = set()
            for name in self.name_list:
                # 使用正则表达式进行精确匹配
                pattern = re.compile(re.escape(name))
                if pattern.search(context):
                    names.add(name)
            
            # 始终添加"其他人"作为候选项
            names.add("其他人")
            
            return list(names)
        except Exception as e:
            print(f"处理文本时发生错误：{str(e)}")
            return ["其他人"]

    @staticmethod
    def load_name_list(name_file: str) -> Set[str]:  # 移除多余的 self 参数，添加返回类型注解
        """从JSON文件加载人名列表
        Args:
            name_file: JSON文件路径，文件应包含名字列表
        Returns:
            Set[str]: 人名集合
        """
        try:
            with open(name_file, 'r', encoding='utf-8') as f:
                data = json.load(f)
                # 支持多种JSON格式：列表、字典中的列表或单个字段
                if isinstance(data, list):
                    return {name.strip() for name in data if name.strip()}
                elif isinstance(data, dict) and any(isinstance(v, list) for v in data.values()):
                    # 尝试从字典中找到第一个列表值
                    for value in data.values():
                        if isinstance(value, list):
                            return {name.strip() for name in value if name.strip()}
                    return set()
                else:
                    print("警告：JSON文件格式不正确，应为名字列表或包含名字列表的字典")
                    return set()
        except json.JSONDecodeError as e:
            print(f"JSON解析错误：{str(e)}")
            return set()
        except Exception as e:
            print(f"加载人名列表时发生错误：{str(e)}")
            return set()
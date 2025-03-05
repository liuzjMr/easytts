import re
from typing import List, Tuple, Dict, Set
from pathlib import Path
import argparse
from .name_extractor import NameExtractor

class TextPreprocessor:
    def __init__(self, name_file: str, context_size: int = 3, max_context_size: int = 1024):
        """初始化预处理器
        Args:
            context_size: 初始上下文窗口大小（单侧），表示句子数量，默认为3句
            max_context_size: 最大上下文窗口大小（单侧），表示token数量，默认为1024个token
        """
        self.context_size = context_size
        self.max_context_size = max_context_size
        
        self.name_extractor = NameExtractor(name_file)

    def extract_quotes(self, text: str) -> List[Tuple[str, int, int]]:
        """提取文本中的引文
        Args:
            text: 输入文本
        Returns:
            List[Tuple[str, int, int]]: 引文列表，每个元素为(引文内容, 开始位置, 结束位置)
        """
        # 支持中英文引号：""''「」『』
        quotes = []
        # 定义不同类型的引号对
        quote_pairs = [
            ('"', '"'),
            ('“', '”'),
            (''', '''),
            ('‘', '’'),
            ('「', '」'),
            ('『', '』')
        ]
        
        for start_quote, end_quote in quote_pairs:
            # 为每对引号构建正则表达式
            pattern = f"{start_quote}([^{start_quote}{end_quote}]*){end_quote}"
            for match in re.finditer(pattern, text):
                quotes.append((match.group(1), match.start(), match.end()))
        
        return quotes

    @staticmethod
    def split_sentences(text: str) -> Tuple[List[Tuple[str, int, int, int]], List[int]]:
        """将文本分割成句子，同时提取引文
        Args:
            text: 输入文本
        Returns:
            Tuple[List[Tuple[str, int, int, int]], List[int]]: 
                - 句子列表，每个元素为(句子内容, 开始位置, 结束位置, 句子编号)
                - 引文句子的索引列表
        """
        sentences = []
        quotes_idx = []
        
        # 首先提取所有引文
        quote_pairs = [
            ('"', '"'),
            ('“', '”'),
            (''', '''),
            ('’', '‘'),
            ('「', '」'),
            ('『', '』')
        ]
        
        # 记录所有引文的位置
        quote_positions = []
        for start_quote, end_quote in quote_pairs:
            pattern = f"{start_quote}([^{start_quote}{end_quote}]*){end_quote}"
            for match in re.finditer(pattern, text):
                quote_positions.append((match.start(), match.end(), match.group(1)))
        
        # 按位置排序引文
        quote_positions.sort(key=lambda x: x[0])
        
        # 处理文本，将引文和非引文部分分别处理
        current_pos = 0
        for quote_start, quote_end, quote_content in quote_positions:
            # 处理引文前的文本
            if current_pos < quote_start:
                non_quote_text = text[current_pos:quote_start]
                pattern = r'([。！？])\s*'
                start = 0
                for match in re.finditer(pattern, non_quote_text):
                    end = match.end()
                    sentence = non_quote_text[start:end].strip()
                    if sentence:
                        abs_start = current_pos + start
                        abs_end = current_pos + end
                        sentences.append((sentence, abs_start, abs_end, len(sentences)))
                    start = end
                # 处理最后一个非完整句子
                if start < len(non_quote_text):
                    remaining = non_quote_text[start:].strip()
                    if remaining:
                        abs_start = current_pos + start
                        abs_end = quote_start
                        sentences.append((remaining, abs_start, abs_end, len(sentences)))
            
            # 处理引文
            quote_sentence = text[quote_start:quote_end]
            sentences.append((quote_sentence, quote_start, quote_end, len(sentences)))
            quotes_idx.append(len(sentences) - 1)
            current_pos = quote_end
        
        # 处理最后一段非引文文本
        if current_pos < len(text):
            remaining_text = text[current_pos:]
            pattern = r'([。！？])\s*'
            start = 0
            for match in re.finditer(pattern, remaining_text):
                end = match.end()
                sentence = remaining_text[start:end].strip()
                if sentence:
                    abs_start = current_pos + start
                    abs_end = current_pos + end
                    sentences.append((sentence, abs_start, abs_end, len(sentences)))
                start = end
            # 处理最后一个句子
            if start < len(remaining_text):
                sentence = remaining_text[start:].strip()
                if sentence:
                    abs_start = current_pos + start
                    abs_end = len(text)
                    sentences.append((sentence, abs_start, abs_end, len(sentences)))
        
        return sentences, quotes_idx

    @staticmethod
    def get_context(sentences: List[Tuple[str, int, int, int]], 
                    quote_idx: int,
                    pre_size: int = 3,
                    post_size: int = 3) -> Tuple[str, str, str]:
        """获取引文的上下文
        Args:
            sentences: 句子列表
            quote_idx: 引文所在句子的索引
            pre_size: 前文句子数量
            post_size: 后文句子数量
        Returns:
            Tuple[str, str, str]: (前文内容, 引文内容, 后文内容)
        """
        if quote_idx < 0 or quote_idx >= len(sentences):
            return "", "", ""

        # 获取引文所在句子
        quote_sentence = sentences[quote_idx][0]
        
        # 获取前文
        pre_context = []
        for i in range(max(0, quote_idx - pre_size), quote_idx):
            pre_context.append(sentences[i][0])

        # 获取后文
        post_context = []
        for i in range(quote_idx + 1, min(len(sentences), quote_idx + post_size + 1)):
            post_context.append(sentences[i][0])
        
        return pre_context, quote_sentence, post_context
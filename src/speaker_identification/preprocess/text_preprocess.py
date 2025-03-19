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


    @staticmethod
    def _split_by_regex(text: str, pattern: str, times: int = 1) -> List[Tuple[str, int, int]]:
        """使用正则表达式进行分句
        Args:
            text: 输入文本
            pattern: 分句的正则表达式
            times: 匹配次数，每匹配到第times个才进行分句，默认为1
        Returns:
            List[Tuple[str, int, int]]: 分句结果，每个元素为(句子内容, 开始位置, 结束位置)
        """
        sentences = []
        start = 0
        count = 0
        
        for match in re.finditer(pattern, text):
            count += 1
            # 只有当匹配次数是times的倍数时才进行分句
            if count % times == 0:
                end = match.end()
                if (end-start) > times:
                    sentence = text[start:end].strip()
                    sentences.append((sentence, start, end))
                start = end
                
        # 处理最后一个句子
        if start < len(text):
            sentence = text[start:].strip()
            if sentence:
                sentences.append((sentence, start, len(text)))
                
        # 删除全是标点符号的句子
        punctuation_pattern = r'^[，。！？：；、''"",.!?:;\s\n]+$'
        filtered_sentences = []
        
        # 过滤全是标点符号的句子
        for sent_text, start_pos, end_pos in sentences:
            if not re.match(punctuation_pattern, sent_text):
                filtered_sentences.append((sent_text, start_pos, end_pos))
        
        return filtered_sentences

    @staticmethod
    def split_sentences(text: str, split_rule: str) -> Tuple[List[Tuple[str, int, int, int, bool]], List[int]]:
        """将文本分割成句子，同时提取引文
        Args:
            text: 输入文本
            split_rule: 分句规则
        Returns:
            Tuple[List[Tuple[str, int, int, int]], List[int]]: 
                - 句子列表，每个元素为(句子内容, 开始位置, 结束位置, 句子编号)
                - 引文句子的索引列表
        """
        sentences = []
        quotes_idx = []
        
        # 首先提取所有引文和非引文部分
        text_segments = []  # [(文本内容, 是否为引文, 开始位置, 结束位置)]
        current_pos = 0
        
        quote_pairs = [
            ('"', '"'),
            ('“', '”'),
            (''', '''),
            ('‘', '’'),
            ('「', '」'),
            ('『', '』')
        ]
        
        # 记录所有引文的位置
        quote_positions = []
        for start_quote, end_quote in quote_pairs:
            pattern = f"{start_quote}([^{start_quote}{end_quote}]*){end_quote}"
            for match in re.finditer(pattern, text):
                quote_positions.append((match.start(), match.end()))
        
        # 按位置排序引文
        quote_positions.sort(key=lambda x: x[0])
        
        # 删除被包含在其他引文内的引文
        quote_filtered_positions = []
        for i, (start, end) in enumerate(quote_positions):
            # 检查当前引文是否被其他引文包含
            is_contained = False
            for j, (other_start, other_end) in enumerate(quote_positions):
                if i != j and other_start <= start and end <= other_end:
                    is_contained = True
                    break
            if not is_contained:
                quote_filtered_positions.append((start, end))
        
        # 将文本分割成引文和非引文部分
        last_end = 0
        for quote_start, quote_end in quote_filtered_positions:
            if last_end < quote_start:
                text_segments.append((text[last_end:quote_start], False, last_end, quote_start))
            text_segments.append((text[quote_start:quote_end], True, quote_start, quote_end))
            last_end = quote_end
        
        if last_end < len(text):
            text_segments.append((text[last_end:], False, last_end, len(text)))
        
        # 根据split_rule选择分句模式
        times = 1
        if split_rule == '遇到类句号标点一分':
            pattern = r'([。！？.!?])'
        elif split_rule == '遇到标点一分':
            pattern = r'([，。！？：；、,.!?:;])'
        elif split_rule == '遇到标点2句一分':
            pattern = r'([，。！？：；、,.!?:;])'
            times = 2
        elif split_rule == '遇到标点4句一分':
            pattern = r'([，。！？：；、,.!?:;])'
            times = 4
        elif split_rule == '遇到回车一分':
            pattern = r'(\n)'
        elif split_rule == '遇到空格一分':
            pattern = r'(\s)'
        
        punctuation_pattern = r'^[，。！？：；、‘’”“,.!?:;\s\n]+$'
        # 处理每个文本段
        sentence_idx = 0
        for segment_text, is_quote, start_pos, end_pos in text_segments:
            if re.match(punctuation_pattern, segment_text):
                continue
            if is_quote:
                # 引文作为单独的句子
                sentences.append((segment_text, start_pos, end_pos, sentence_idx, True))
                quotes_idx.append(sentence_idx)
                sentence_idx += 1
            else:
                # 对非引文部分进行分句
                segment_sentences = TextPreprocessor._split_by_regex(segment_text, pattern, times)
                for sent_text, rel_start, rel_end in segment_sentences:
                    abs_start = start_pos + rel_start
                    abs_end = start_pos + rel_end
                    sentences.append((sent_text, abs_start, abs_end, sentence_idx, False))
                    sentence_idx += 1
        
        return sentences, quotes_idx
    
    @staticmethod
    def get_context(sentences: List[Tuple[str, int, int, int, bool]], 
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
        pre_context = ""
        for i in range(max(0, quote_idx - pre_size), quote_idx):
            pre_context += sentences[i][0]
        pre_context = pre_context.strip()

        # 获取后文
        post_context = ""
        for i in range(quote_idx + 1, min(len(sentences), quote_idx + post_size + 1)):
            post_context += sentences[i][0]
        post_context = post_context.strip()
        
        question_context = ""
        if quote_idx > 0 and not sentences[quote_idx-1][4]:
            question_context += sentences[quote_idx-1][0]
            question_context += quote_sentence
        elif quote_idx < len(sentences)-1 and not sentences[quote_idx+1][4]:
            question_context += quote_sentence
            question_context += sentences[quote_idx+1][0]
        else:
            question_context += quote_sentence
        question_context = question_context.strip()
        
        
        return pre_context, quote_sentence, post_context, question_context
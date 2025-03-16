import os
import json
from tqdm import tqdm
import torch
import collections
import argparse
from torch.utils.data import TensorDataset, DataLoader

from src.speaker_identification.csi.models.pytorch_modeling import BertConfig, BertForQuestionAnswering
from src.speaker_identification.csi.evaluate.cmrc2018_output import write_predictions
from src.speaker_identification.csi.tokenizations import official_tokenization as tokenization
from src.speaker_identification.csi.preprocess.cmrc2018_preprocess import json2features
from src.speaker_identification.csi.preprocess import utils
from src.utils import WebSocketTqdm


def evaluate(model, args, eval_examples, eval_features, device, socketio=None, task_id=None):
    """评估函数：计算模型预测结果并输出到文件
    Args:
        model: BERT问答模型
        args: 参数配置
        eval_examples: 验证集原始样例
        eval_features: 验证集特征
        device: 计算设备
    """
    print("***** Eval *****")
    RawResult = collections.namedtuple("RawResult",
                                     ["unique_id", "start_logits", "end_logits"])
    if not os.path.exists(args.checkpoint_dir):
        os.makedirs(args.checkpoint_dir)
    output_prediction_file = os.path.join(args.checkpoint_dir, "predictions.json")
    output_nbest_file = output_prediction_file.replace('predictions', 'nbest')

    all_input_ids = torch.tensor([f['input_ids'] for f in eval_features], dtype=torch.long)
    all_input_mask = torch.tensor([f['input_mask'] for f in eval_features], dtype=torch.long)
    all_segment_ids = torch.tensor([f['segment_ids'] for f in eval_features], dtype=torch.long)
    all_example_index = torch.arange(all_input_ids.size(0), dtype=torch.long)

    eval_data = TensorDataset(all_input_ids, all_input_mask, all_segment_ids, all_example_index)
    eval_dataloader = DataLoader(eval_data, batch_size=args.n_batch, shuffle=False)

    model.eval()
    all_results = []
    print("Start evaluating")
    # 使用WebSocketTqdm替代普通tqdm
    for input_ids, input_mask, segment_ids, example_indices in WebSocketTqdm(eval_dataloader, desc="Evaluating", socketio=socketio, task_id=task_id):
        input_ids = input_ids.to(device)
        input_mask = input_mask.to(device)
        segment_ids = segment_ids.to(device)
        with torch.no_grad():
            batch_start_logits, batch_end_logits = model(input_ids, segment_ids, input_mask)

        for i, example_index in enumerate(example_indices):
            start_logits = batch_start_logits[i].detach().cpu().tolist()
            end_logits = batch_end_logits[i].detach().cpu().tolist()
            eval_feature = eval_features[example_index.item()]
            unique_id = int(eval_feature['unique_id'])
            all_results.append(RawResult(unique_id=unique_id,
                                       start_logits=start_logits,
                                       end_logits=end_logits))

    write_predictions(eval_examples, eval_features, all_results,
                     n_best_size=args.n_best, max_answer_length=args.max_ans_length,
                     do_lower_case=True, output_prediction_file=output_prediction_file,
                     output_nbest_file=output_nbest_file)

    print(f"Predictions saved to {output_prediction_file}")


if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('--gpu_ids', type=str, default='0')

    # evaluation parameters
    parser.add_argument('--n_batch', type=int, default=32)
    parser.add_argument('--max_ans_length', type=int, default=50)
    parser.add_argument('--n_best', type=int, default=6)
    parser.add_argument('--vocab_size', type=int, default=21128)

    # data paths
    parser.add_argument('--dev_dir1', type=str, required=True,
                        help='Path to the dev examples file')
    parser.add_argument('--dev_dir2', type=str, required=True,
                        help='Path to the dev features file')
    parser.add_argument('--dev_file', type=str, required=True,
                        help='Path to the original dev file')
    parser.add_argument('--bert_config_file', type=str, required=True,
                        help='Path to the bert config file')
    parser.add_argument('--vocab_file', type=str, required=True,
                        help='Path to the vocab file')
    parser.add_argument('--init_restore_dir', type=str, required=True,
                        help='Path to the model checkpoint file')
    parser.add_argument('--checkpoint_dir', type=str, required=True,
                        help='Directory to save the predictions')

    args = parser.parse_args()
    
    # 设置GPU
    os.environ["CUDA_VISIBLE_DEVICES"] = args.gpu_ids
    device = torch.device("cuda" if torch.cuda.is_available() else "cpu")
    n_gpu = torch.cuda.device_count()
    print(f"device: {device} n_gpu: {n_gpu}")

    # 加载BERT配置
    bert_config = BertConfig.from_json_file(args.bert_config_file)

    # 加载分词器
    print('Loading tokenizer...')
    tokenizer = tokenization.BertTokenizer(vocab_file=args.vocab_file, do_lower_case=True)
    assert args.vocab_size == len(tokenizer.vocab)

    # 如果特征文件不存在，则进行特征提取
    if not os.path.exists(args.dev_dir1) or not os.path.exists(args.dev_dir2):
        print('Converting examples to features...')
        json2features(args.dev_file, [args.dev_dir1, args.dev_dir2], tokenizer, is_training=False,
                     max_seq_length=bert_config.max_position_embeddings)

    # 加载开发集数据
    print('Loading development data...')
    dev_examples = json.load(open(args.dev_dir1, 'r'))
    dev_features = json.load(open(args.dev_dir2, 'r'))

    # 初始化模型
    print('Initializing model...')
    model = BertForQuestionAnswering(bert_config)
    utils.torch_show_all_params(model)
    utils.torch_init_model(model, args.init_restore_dir)
    model.to(device)
    if n_gpu > 1:
        model = torch.nn.DataParallel(model)

    # 进行评估
    evaluate(model, args, dev_examples, dev_features, device)
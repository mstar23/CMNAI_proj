#!/usr/bin/env python
"""Django's command-line utility for administrative tasks."""
import os
import sys
import torch
from torch import nn
import numpy as np
import torch.nn.functional as F
import torch.optim as optim
from torch.utils.data import Dataset, DataLoader
import gluonnlp as nlp
import copy

from kobert.utils import get_tokenizer
from kobert.pytorch_kobert import get_pytorch_kobert_model




def main():
    """Run administrative tasks."""
    os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'config.settings')
    try:
        from django.core.management import execute_from_command_line
    except ImportError as exc:
        raise ImportError(
            "Couldn't import Django. Are you sure it's installed and "
            "available on your PYTHONPATH environment variable? Did you "
            "forget to activate a virtual environment?"
        ) from exc
    execute_from_command_line(sys.argv)


if __name__ == '__main__':
    class BERTDataset(Dataset):
        def __init__(self, dataset, sent_idx, label_idx, bert_tokenizer, max_len,
                     pad, pair):
            transform = nlp.data.BERTSentenceTransform(
                bert_tokenizer, max_seq_length=max_len, pad=pad, pair=pair)

            self.sentences = [transform([i[sent_idx]]) for i in dataset]
            self.labels = [np.int32(i[label_idx]) for i in dataset]

        def __getitem__(self, i):
            return (self.sentences[i] + (self.labels[i],))

        def __len__(self):
            return (len(self.labels))

        # 모델 정의


    class BERTClassifier(nn.Module):
        def __init__(self,
                     bert,
                     hidden_size=768,
                     num_classes=6,
                     dr_rate=None,
                     params=None):
            super(BERTClassifier, self).__init__()
            self.bert = bert
            self.dr_rate = dr_rate

            self.classifier = nn.Linear(hidden_size, num_classes)
            if dr_rate:
                self.dropout = nn.Dropout(p=dr_rate)

        def gen_attention_mask(self, token_ids, valid_length):
            attention_mask = torch.zeros_like(token_ids)
            for i, v in enumerate(valid_length):
                attention_mask[i][:v] = 1
            return attention_mask.float()

        def forward(self, token_ids, valid_length, segment_ids):
            attention_mask = self.gen_attention_mask(token_ids, valid_length)

            _, pooler = self.bert(input_ids=token_ids, token_type_ids=segment_ids.long(),
                                  attention_mask=attention_mask.float().to(token_ids.device))
            if self.dr_rate:
                out = self.dropout(pooler)
            return self.classifier(out)
    main()

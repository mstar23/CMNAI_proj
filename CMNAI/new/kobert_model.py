import torch
from torch import nn
import numpy as np
import torch.nn.functional as F
import torch.optim as optim
from torch.utils.data import Dataset, DataLoader
import gluonnlp as nlp
import copy

#kobert
from kobert.utils import get_tokenizer
from kobert.pytorch_kobert import get_pytorch_kobert_model

#Dataset 정의
class BERTDataset(Dataset):
    def __init__(self, dataset, sent_idx, label_idx, bert_tokenizer, max_len,
                 pad, pair):
        transform = nlp.data.BERTSentenceTransform(
            bert_tokenizer, max_seq_length=max_len, pad=pad, pair=pair)

        self.sentences = [transform([i[sent_idx]]) for i in dataset]
        self.labels = [np.int32(i[label_idx]) for i in dataset]

    def __getitem__(self, i):
        return (self.sentences[i] + (self.labels[i], ))

    def __len__(self):
        return (len(self.labels))

#모델 정의
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


def predict(predict_sentence):
    data = [predict_sentence, '0']
    dataset_another = [data]

    another_test = BERTDataset(dataset_another, 0, 1, tok, max_len, True, False)
    test_dataloader = torch.utils.data.DataLoader(another_test, batch_size=batch_size)

    model.eval()

    for batch_id, (token_ids, valid_length, segment_ids, label) in enumerate(test_dataloader):
        token_ids = token_ids.long().to(device)
        segment_ids = segment_ids.long().to(device)

        valid_length = valid_length
        label = label.long().to(device)

        out = model(token_ids, valid_length, segment_ids)
        # {'불안':0,'당황':1,'슬픔':2,'분노':3,'상처':4,'기쁨':5})
        test_eval = []
        for i in out:
            logits = i
            logits = logits.detach().cpu().numpy()

            if np.argmax(logits) == 0:
                test_eval.append("불안")
            elif np.argmax(logits) == 1:
                test_eval.append("당황")
            elif np.argmax(logits) == 2:
                test_eval.append("슬픔")
            elif np.argmax(logits) == 3:
                test_eval.append("분노")
            elif np.argmax(logits) == 4:
                test_eval.append("상처")
            elif np.argmax(logits) == 5:
                test_eval.append("기쁨")

        # print(test_eval[0])
        return test_eval[0]

# BERT 모델, Vocabulary 불러오기
bertmodel, vocab = get_pytorch_kobert_model()

# 토큰화
tokenizer = get_tokenizer()
tok = nlp.data.BERTSPTokenizer(tokenizer, vocab, lower=False)

# 파라미터 정의
max_len = 70
batch_size = 64

# device 정의
device = torch.device('cpu')

# 모델 불러오기
# model = torch.load('../totaldata_model.pt', map_location=device)  # 전체 모델을 통째로 불러옴, 클래스 선언 필수
# model.load_state_dict(torch.load('../model_state_dict2.pt', map_location=device))  # state_dict를 불러 온 후, 모델에 저장

model = torch.load('C:/Users/mjy30/CMNAI/new/totaldata_model.pt',
                   map_location=device)  # 전체 모델을 통째로 불러옴, 클래스 선언 필수
# model = BERTClassifier('C:/Users/mjy30/Django_Prac/totaldata_model.pt').to(device)
model.load_state_dict(torch.load('C:/Users/mjy30/CMNAI/new/model_state_dict2.pt',
                                 map_location=device))  # state_dict를 불러 온 후, 모델에 저장
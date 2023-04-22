import json
import nltk
import torch
import torch.nn as nn
import torch.optim as optim
from nltk.corpus import stopwords
from sklearn.feature_extraction.text import CountVectorizer
from sklearn.model_selection import train_test_split
from torch.utils.data import Dataset, DataLoader


# 数据加载和预处理
def load_data(file_path):
    with open(file_path, 'r', encoding='utf-8') as f:
        data = json.load(f)
    texts = []
    labels = []
    for item in data:
        text = item['text']
        label = item['label']
        texts.append(text)
        labels.append(label)
    return texts, labels


def preprocess_text(texts):
    stop_words = set(stopwords.words('english'))
    processed_texts = []
    for text in texts:
        # 分词
        tokens = nltk.word_tokenize(text)
        # 去除停用词和标点符号
        tokens = [token.lower() for token in tokens if token.isalpha() and token.lower() not in stop_words]
        # 词干化
        stemmer = nltk.PorterStemmer()
        tokens = [stemmer.stem(token) for token in tokens]
        # 将词汇表连接成文本
        processed_text = ' '.join(tokens)
        processed_texts.append(processed_text)
    return processed_texts


# 特征提取
def extract_features(texts):
    vectorizer = CountVectorizer()
    features = vectorizer.fit_transform(texts)
    return features.toarray()


# 定义数据集类
class TextDataset(Dataset):
    def __init__(self, texts, labels):
        self.texts = texts
        self.labels = labels

    def __len__(self):
        return len(self.texts)

    def __getitem__(self, index):
        text = self.texts[index]
        label = self.labels[index]
        return text, label


# 定义模型类
class TextClassifier(nn.Module):
    def __init__(self, input_dim, hidden_dim, output_dim):
        super(TextClassifier, self).__init__()
        self.fc1 = nn.Linear(input_dim, hidden_dim)
        self.fc2 = nn.Linear(hidden_dim, output_dim)

    def forward(self, x):
        x = torch.relu(self.fc1(x))
        x = self.fc2(x)
        return x


# 训练模型
def train_model(model, dataloader, criterion, optimizer, device):
    model.train()
    total_loss = 0.0
    for texts, labels in dataloader:
        texts = texts.to(device)
        labels = labels.to(device)
        optimizer.zero_grad()
        outputs = model(texts)
        loss = criterion(outputs, labels)
        loss.backward()
        optimizer.step()
        total_loss += loss.item()
    return total_loss / len(dataloader)


# 测试模型
def test_model(model, dataloader, criterion, device):
    model.eval()
    total_loss = 0.0
    correct = 0
    with torch.no_grad():
        for texts, labels in dataloader:
            texts = texts.to(device)
            labels = labels.to(device)
            outputs = model(texts)
            loss = criterion(outputs, labels)
            total_loss += loss.item()
            _, predicted = outputs.max(1)
            correct += predicted.eq(labels).sum().item()

---
title: "Tutorial 24 · Redes Neurais de Zero a Hero · Implementação Python"
subtitle: "Como implementar MLP, CNN, RNN e Transformer do zero com PyTorch"
author: "Equipo Nexus · Sir. Nexus Alencar + Ravi (CTO/AI)"
version: "1.0.0"
date: 2026-07-29
pattern: "MMN_IA"
---

**Tutorial 24 · Redes Neurais de Zero a Hero · Implementação Python**

*Tutorial completo de 4 redes neurais fundamentais: MLP, CNN, RNN, Transformer. Implementação do zero com PyTorch, explicações visuais, e deploy.*

**Por Equipo Nexus · Academ'IA**

---

## 🎯 O que Você Vai Conquistar

Em 2h30, você vai:

1. Entender matematicamente como uma rede neural aprende
2. Implementar MLP (Multi-Layer Perceptron) do zero
3. Implementar CNN (Convolutional) para imagens
4. Implementar RNN (Recurrent) para séries temporais
5. Implementar Transformer (atenção) para texto
6. Treinar, avaliar, deployar

**Pré-requisitos:**
- Python intermediário
- PyTorch instalado
- Álgebra linear básica (vetores, matrizes)
- Cálculo básico (derivadas)

---

## 🧠 Parte 1: Conceitos Fundamentais

### 1.1 — O que é uma Rede Neural

**Definição simples:** função matemática que aprende padrões em dados.

**Analogia:** pense em uma rede neural como uma criança aprendendo a reconhecer cães.

1. Você mostra 10.000 fotos de cães (input)
2. A criança erra no começo (output errado)
3. Você corrige: "isso NÃO é um cachorro" (loss)
4. A criança ajusta o que olha (backpropagation)
5. Repete até acertar quase sempre (convergência)

### 1.2 — Anatomia de um Neurônio

```
inputs (x)     weights (w)      bias (b)      activation (σ)
   x1 ──── w1 ───┐
   x2 ──── w2 ───┤
   x3 ──── w3 ───┼───→ z = Σ(wi·xi) + b ──→ σ(z) ──→ output
   x4 ──── w4 ───┤
   x5 ──── w5 ───┘
```

**Matemática:**
```
z = w · x + b = Σ(wi · xi) + b
a = σ(z) = 1 / (1 + e^(-z))
```

**Onde:**
- `x` = input (1-5 features)
- `w` = pesos (o que a rede aprende)
- `b` = bias (offset)
- `σ` = função de ativação (ReLU, sigmoid, tanh)

### 1.3 — Funções de Ativação

**ReLU (Rectified Linear Unit) — mais comum**
```python
def relu(z):
    return max(0, z)
```
- Saída: 0 a +∞
- Vantagem: simples, sem saturação
- Uso: camadas escondidas

**Sigmoid — classificação binária**
```python
def sigmoid(z):
    return 1 / (1 + np.exp(-z))
```
- Saída: 0 a 1 (probabilidade)
- Vantagem: interpretável
- Uso: output binário

**Softmax — classificação multiclasse**
```python
def softmax(z):
    exp_z = np.exp(z - np.max(z))  # estabilidade numérica
    return exp_z / exp_z.sum()
```
- Saída: 0 a 1, soma = 1 (distribuição)
- Uso: output multiclasse

**Tanh — centralizado em 0**
```python
def tanh(z):
    return np.tanh(z)
```
- Saída: -1 a 1
- Vantagem: centrada em 0
- Uso: RNN (evita gradient bias)

### 1.4 — Forward e Backward Propagation

**Forward (predição):**
```
x → z1 = w1·x + b1 → a1 = σ(z1) → z2 = w2·a1 + b2 → a2 = σ(z2) → ŷ
```

**Backward (aprender):**
```
L (loss) → ∂L/∂w2, ∂L/∂b2 → ∂L/∂w1, ∂L/∂b1 → update w, b
```

**Regra de atualização (Gradient Descent):**
```
w_new = w - α · ∂L/∂w
b_new = b - α · ∂L/∂b
```

**Onde α (learning rate):** 0.001 a 0.1 (ajustável).

### 1.5 — Loss Functions

**MSE (Mean Squared Error) — regressão**
```python
def mse(y_true, y_pred):
    return np.mean((y_true - y_pred) ** 2)
```

**Binary Cross-Entropy — classificação binária**
```python
def binary_ce(y_true, y_pred):
    return -np.mean(y_true * np.log(y_pred) + (1 - y_true) * np.log(1 - y_pred))
```

**Categorical Cross-Entropy — classificação multiclasse**
```python
def categorical_ce(y_true, y_pred):
    return -np.mean(np.sum(y_true * np.log(y_pred), axis=1))
```

### 1.6 — Otimizadores

**SGD (Stochastic Gradient Descent):**
```python
w = w - lr * grad
```

**Adam (Adaptive Moment Estimation) — padrão em deep learning:**
```python
m = β1 * m + (1 - β1) * grad  # média móvel do gradiente
v = β2 * v + (1 - β2) * grad²  # média móvel do gradiente²
m_hat = m / (1 - β1**t)  # correção de viés
v_hat = v / (1 - β2**t)
w = w - lr * m_hat / (sqrt(v_hat) + ε)
```

**Learning rate schedulers:**
- StepLR: reduz lr a cada N epochs
- ReduceLROnPlateau: reduz quando loss para de cair
- CosineAnnealing: lr segue cosseno

---

## 🔢 Parte 2: MLP (Multi-Layer Perceptron)

### 2.1 — Implementação do Zero (NumPy)

```python
"""
MLP from scratch com NumPy.
2 camadas escondidas, classificação binária.
"""
import numpy as np


class MLP:
    def __init__(self, input_dim, hidden_dims, output_dim, learning_rate=0.01):
        """
        input_dim: nº features de entrada
        hidden_dims: lista de neurônios por camada escondida
        output_dim: nº classes de saída
        """
        self.lr = learning_rate
        layer_dims = [input_dim] + hidden_dims + [output_dim]
        self.weights = []
        self.biases = []

        # Inicialização Xavier
        for i in range(len(layer_dims) - 1):
            w = np.random.randn(layer_dims[i], layer_dims[i+1]) * np.sqrt(2 / layer_dims[i])
            b = np.zeros((1, layer_dims[i+1]))
            self.weights.append(w)
            self.biases.append(b)

    def relu(self, z):
        return np.maximum(0, z)

    def relu_derivative(self, z):
        return (z > 0).astype(float)

    def sigmoid(self, z):
        return 1 / (1 + np.exp(-np.clip(z, -500, 500)))

    def forward(self, X):
        """Forward pass"""
        self.activations = [X]
        self.zs = []

        # Camadas escondidas (ReLU)
        for i in range(len(self.weights) - 1):
            z = self.activations[-1] @ self.weights[i] + self.biases[i]
            self.zs.append(z)
            a = self.relu(z)
            self.activations.append(a)

        # Camada de saída (sigmoid para binário)
        z = self.activations[-1] @ self.weights[-1] + self.biases[-1]
        self.zs.append(z)
        output = self.sigmoid(z)
        self.activations.append(output)

        return output

    def binary_cross_entropy(self, y_true, y_pred):
        return -np.mean(y_true * np.log(y_pred + 1e-8) + (1 - y_true) * np.log(1 - y_pred + 1e-8))

    def backward(self, X, y_true, y_pred):
        """Backward pass"""
        m = X.shape[0]
        dL_dz = (y_pred - y_true) / (y_pred * (1 - y_pred) + 1e-8)

        # Backprop através de todas as camadas
        for i in reversed(range(len(self.weights))):
            dL_dw = self.activations[i].T @ dL_dz / m
            dL_db = np.sum(dL_dz, axis=0, keepdims=True) / m

            # Atualizar pesos
            self.weights[i] -= self.lr * dL_dw
            self.biases[i] -= self.lr * dL_db

            # Gradiente para camada anterior
            if i > 0:
                dL_da = dL_dz @ self.weights[i].T
                dL_dz = dL_da * self.relu_derivative(self.zs[i-1])

    def train(self, X, y, epochs=1000, batch_size=32, verbose=True):
        """Treinamento"""
        history = []
        for epoch in range(epochs):
            # Mini-batch
            indices = np.random.permutation(X.shape[0])
            for start in range(0, X.shape[0], batch_size):
                batch_idx = indices[start:start + batch_size]
                X_batch, y_batch = X[batch_idx], y[batch_idx]

                y_pred = self.forward(X_batch)
                self.backward(X_batch, y_batch, y_pred)

            # Loss por epoch
            y_pred_full = self.forward(X)
            loss = self.binary_cross_entropy(y, y_pred_full)
            history.append(loss)

            if verbose and epoch % 100 == 0:
                print(f"Epoch {epoch}, Loss: {loss:.4f}")

        return history

    def predict(self, X, threshold=0.5):
        y_pred = self.forward(X)
        return (y_pred > threshold).astype(int)


# =====================
# Teste
# =====================
if __name__ == "__main__":
    # Dataset sintético: XOR-like
    np.random.seed(42)
    X = np.random.randn(1000, 2)
    y = ((X[:, 0] * X[:, 1]) > 0).astype(int).reshape(-1, 1)

    # Split
    split = 800
    X_train, X_test = X[:split], X[split:]
    y_train, y_test = y[:split], y[split:]

    # Modelo
    mlp = MLP(
        input_dim=2,
        hidden_dims=[8, 4],
        output_dim=1,
        learning_rate=0.01
    )

    # Treinar
    history = mlp.train(X_train, y_train, epochs=500, batch_size=32)

    # Avaliar
    y_pred = mlp.predict(X_test)
    acc = np.mean(y_pred == y_test)
    print(f"\nAcurácia: {acc * 100:.2f}%")
```

### 2.2 — Versão PyTorch (Recomendada)

```python
import torch
import torch.nn as nn
import torch.optim as optim
from torch.utils.data import DataLoader, TensorDataset


class MLPNet(nn.Module):
    def __init__(self, input_dim, hidden_dims, output_dim, dropout=0.2):
        super().__init__()
        layers = []
        prev_dim = input_dim

        for h_dim in hidden_dims:
            layers.extend([
                nn.Linear(prev_dim, h_dim),
                nn.BatchNorm1d(h_dim),
                nn.ReLU(),
                nn.Dropout(dropout),
            ])
            prev_dim = h_dim

        layers.append(nn.Linear(prev_dim, output_dim))
        layers.append(nn.Sigmoid())

        self.net = nn.Sequential(*layers)

    def forward(self, x):
        return self.net(x)


# Treinamento
def train_mlp(X_train, y_train, X_test, y_test, hidden_dims=[64, 32], epochs=50):
    # Tensores
    X_train_t = torch.FloatTensor(X_train)
    y_train_t = torch.FloatTensor(y_train).reshape(-1, 1)
    X_test_t = torch.FloatTensor(X_test)
    y_test_t = torch.FloatTensor(y_test).reshape(-1, 1)

    # DataLoader
    train_dataset = TensorDataset(X_train_t, y_train_t)
    train_loader = DataLoader(train_dataset, batch_size=32, shuffle=True)

    # Modelo
    model = MLPNet(X_train.shape[1], hidden_dims, 1)
    criterion = nn.BCELoss()
    optimizer = optim.Adam(model.parameters(), lr=0.001, weight_decay=1e-5)
    scheduler = optim.lr_scheduler.ReduceLROnPlateau(optimizer, patience=5)

    # Loop
    for epoch in range(epochs):
        model.train()
        train_loss = 0
        for X_batch, y_batch in train_loader:
            optimizer.zero_grad()
            y_pred = model(X_batch)
            loss = criterion(y_pred, y_batch)
            loss.backward()
            optimizer.step()
            train_loss += loss.item()

        # Validação
        model.eval()
        with torch.no_grad():
            y_pred_test = model(X_test_t)
            test_loss = criterion(y_pred_test, y_test_t).item()
            acc = ((y_pred_test > 0.5) == y_test_t).float().mean().item()

        scheduler.step(test_loss)

        if epoch % 5 == 0:
            print(f"Epoch {epoch}: Train Loss={train_loss/len(train_loader):.4f}, "
                  f"Test Loss={test_loss:.4f}, Acc={acc:.4f}")

    return model


# Uso
model = train_mlp(X_train, y_train, X_test, y_test)
```

### 2.3 — Quando Usar MLP

✅ **Bom para:**
- Dados tabulares (features estruturadas)
- Pequeno/médio volume de dados (< 100k samples)
- Features numéricas e categóricas (one-hot)
- Baseline rápido

❌ **Não usar para:**
- Imagens (use CNN)
- Texto sequencial (use RNN ou Transformer)
- Áudio (use CNN ou RNN)
- Dados com estrutura espacial/temporal

---

## 🖼️ Parte 3: CNN (Convolutional Neural Network)

### 3.1 — Conceito

**Problema com MLP para imagens:**
- Imagem 224×224×3 = 150.528 features
- MLP com 1 camada = 150.528 × 1.000 = 150M parâmetros
- Overfitting garantido

**CNN resolve com:**
- **Convolução:** filtros compartilhados (detecta padrões locais)
- **Pooling:** reduz dimensionalidade (subamostragem)
- **Camadas densas no final:** classifica features extraídas

### 3.2 — Arquitetura Típica (ResNet-like)

```
Input (224×224×3)
    ↓
[Conv 7×7, 64, stride=2] → BatchNorm → ReLU
    ↓
MaxPool 3×3, stride=2
    ↓
[Conv 3×3, 64] × 3
[Conv 3×3, 64]
    ↓
[Conv 3×3, 128, stride=2] → [Conv 3×3, 128] × 3
    ↓
[Conv 3×3, 256, stride=2] → [Conv 3×3, 256] × 3
    ↓
[Conv 3×3, 512, stride=2] → [Conv 3×3, 512] × 3
    ↓
AvgPool 7×7
    ↓
FC 1000 → Softmax
```

### 3.3 — Implementação PyTorch

```python
import torch
import torch.nn as nn
import torch.nn.functional as F


class ConvBlock(nn.Module):
    """Bloco convolucional: Conv → BatchNorm → ReLU"""
    def __init__(self, in_channels, out_channels, kernel_size=3, stride=1, padding=1):
        super().__init__()
        self.conv = nn.Conv2d(
            in_channels, out_channels,
            kernel_size, stride, padding, bias=False
        )
        self.bn = nn.BatchNorm2d(out_channels)
        self.relu = nn.ReLU(inplace=True)

    def forward(self, x):
        return self.relu(self.bn(self.conv(x)))


class SimpleCNN(nn.Module):
    """CNN simples para classificação de imagens (CIFAR-10)"""
    def __init__(self, num_classes=10):
        super().__init__()

        # Blocos convolucionais
        self.features = nn.Sequential(
            # Input: 3×32×32
            ConvBlock(3, 64),  # 64×32×32
            ConvBlock(64, 64),
            nn.MaxPool2d(2, 2),  # 64×16×16

            ConvBlock(64, 128),  # 128×16×16
            ConvBlock(128, 128),
            nn.MaxPool2d(2, 2),  # 128×8×8

            ConvBlock(128, 256),  # 256×8×8
            ConvBlock(256, 256),
            nn.MaxPool2d(2, 2),  # 256×4×4
        )

        # Classificador
        self.classifier = nn.Sequential(
            nn.Flatten(),
            nn.Dropout(0.5),
            nn.Linear(256 * 4 * 4, 512),
            nn.ReLU(inplace=True),
            nn.Dropout(0.5),
            nn.Linear(512, num_classes),
        )

    def forward(self, x):
        x = self.features(x)
        x = self.classifier(x)
        return x


# Uso
model = SimpleCNN(num_classes=10)
x = torch.randn(32, 3, 32, 32)  # batch de 32 imagens
y = model(x)
print(f"Output shape: {y.shape}")  # [32, 10]
```

### 3.4 — Transfer Learning (Usar Modelo Pré-treinado)

```python
import torchvision.models as models


def create_resnet50(num_classes=10, pretrained=True):
    """ResNet50 com transfer learning"""
    model = models.resnet50(weights='DEFAULT' if pretrained else None)

    # Congelar camadas convolucionais
    for param in model.parameters():
        param.requires_grad = False

    # Substituir última camada (fully connected)
    num_features = model.fc.in_features
    model.fc = nn.Sequential(
        nn.Linear(num_features, 512),
        nn.ReLU(),
        nn.Dropout(0.3),
        nn.Linear(512, num_classes),
    )

    return model


# Treinar
model = create_resnet50(num_classes=10, pretrained=True)
# Otimizador só treina a última camada
optimizer = torch.optim.Adam(model.fc.parameters(), lr=0.001)
```

### 3.5 — Quando Usar CNN

✅ **Bom para:**
- Imagens (classificação, detecção, segmentação)
- Áudio (espectrograma)
- Qualquer dado com estrutura espacial local

---

## ⏱️ Parte 4: RNN (Recurrent Neural Network)

### 4.1 — Conceito

**Problema com MLP para sequências:**
- Sequência variável
- Não compartilha parâmetros ao longo do tempo
- Sem memória

**RNN resolve com:**
- Estado oculto (hidden state) mantido entre timesteps
- Mesmos parâmetros compartilhados
- Processa sequência timestep por timestep

```
h_t = σ(W_h · h_{t-1} + W_x · x_t + b)
y_t = V · h_t + c
```

### 4.2 — Problema: Vanishing Gradient

**RNN simples tem dificuldade com sequências longas (> 50 timesteps).**

**Solução: LSTM (Long Short-Term Memory)**

```
f_t = σ(W_f · [h_{t-1}, x_t] + b_f)  # forget gate
i_t = σ(W_i · [h_{t-1}, x_t] + b_i)  # input gate
C̃_t = tanh(W_C · [h_{t-1}, x_t] + b_C)
C_t = f_t * C_{t-1} + i_t * C̃_t  # cell state
o_t = σ(W_o · [h_{t-1}, x_t] + b_o)  # output gate
h_t = o_t * tanh(C_t)
```

### 4.3 — Implementação PyTorch

```python
import torch
import torch.nn as nn


class LSTMPredictor(nn.Module):
    """LSTM para previsão de série temporal"""
    def __init__(self, input_size, hidden_size, num_layers, output_size, dropout=0.2):
        super().__init__()
        self.hidden_size = hidden_size
        self.num_layers = num_layers

        self.lstm = nn.LSTM(
            input_size=input_size,
            hidden_size=hidden_size,
            num_layers=num_layers,
            batch_first=True,
            dropout=dropout if num_layers > 1 else 0,
        )

        self.fc = nn.Sequential(
            nn.Linear(hidden_size, 64),
            nn.ReLU(),
            nn.Dropout(dropout),
            nn.Linear(64, output_size),
        )

    def forward(self, x):
        # x: [batch, seq_len, input_size]
        h0 = torch.zeros(self.num_layers, x.size(0), self.hidden_size).to(x.device)
        c0 = torch.zeros(self.num_layers, x.size(0), self.hidden_size).to(x.device)

        out, (hn, cn) = self.lstm(x, (h0, c0))

        # Usar apenas último timestep
        out = out[:, -1, :]
        out = self.fc(out)
        return out


# Uso: prever próximo valor de série temporal
model = LSTMPredictor(
    input_size=1,      # 1 feature (valor)
    hidden_size=64,    # 64 neurônios
    num_layers=2,      # 2 camadas LSTM
    output_size=1,     # prever 1 valor
)
x = torch.randn(32, 30, 1)  # batch=32, seq=30, features=1
y = model(x)
print(f"Output shape: {y.shape}")  # [32, 1]
```

### 4.4 — Quando Usar RNN/LSTM

✅ **Bom para:**
- Séries temporais (previsão, classificação)
- Texto (modelagem de linguagem, geração)
- Áudio (síntese de voz, reconhecimento)
- Vídeo (processamento de frames)

❌ **Limitações:**
- Sequências muito longas (> 1000) são lentas
- Transformer é melhor para a maioria dos casos (2024+)

---

## 🤖 Parte 5: Transformer

### 5.1 — Conceito

**RNN/LSTM processa sequência em ordem** (lento, perde informação de longo alcance).

**Transformer processa tudo em paralelo** com **mecanismo de atenção**:

```
Attention(Q, K, V) = softmax(Q · K^T / √d_k) · V
```

**Intuição:** cada palavra "olha" para todas as outras e decide quais importam.

### 5.2 — Self-Attention Explicada

**Para cada palavra (token):**
1. Calcule 3 vetores: Query (Q), Key (K), Value (V)
2. Score: Q · K^T (similaridade)
3. Scale: / √d_k
4. Mask: ignore tokens futuros (em geração)
5. Softmax: probabilidade de atenção
6. Output: soma ponderada de V

### 5.3 — Implementação PyTorch

```python
import torch
import torch.nn as nn
import math


class MultiHeadAttention(nn.Module):
    def __init__(self, d_model, num_heads, dropout=0.1):
        super().__init__()
        assert d_model % num_heads == 0

        self.d_model = d_model
        self.num_heads = num_heads
        self.d_k = d_model // num_heads

        self.W_q = nn.Linear(d_model, d_model)
        self.W_k = nn.Linear(d_model, d_model)
        self.W_v = nn.Linear(d_model, d_model)
        self.W_o = nn.Linear(d_model, d_model)
        self.dropout = nn.Dropout(dropout)

    def forward(self, x, mask=None):
        batch_size, seq_len, d_model = x.shape

        # Projeções
        Q = self.W_q(x).view(batch_size, seq_len, self.num_heads, self.d_k).transpose(1, 2)
        K = self.W_k(x).view(batch_size, seq_len, self.num_heads, self.d_k).transpose(1, 2)
        V = self.W_v(x).view(batch_size, seq_len, self.num_heads, self.d_k).transpose(1, 2)

        # Attention scores
        scores = (Q @ K.transpose(-2, -1)) / math.sqrt(self.d_k)

        # Mask (opcional)
        if mask is not None:
            scores = scores.masked_fill(mask == 0, -1e9)

        # Softmax
        attn = torch.softmax(scores, dim=-1)
        attn = self.dropout(attn)

        # Aplicar atenção aos valores
        context = attn @ V

        # Concatenar cabeças
        context = context.transpose(1, 2).contiguous().view(batch_size, seq_len, d_model)

        return self.W_o(context)


class TransformerBlock(nn.Module):
    def __init__(self, d_model, num_heads, d_ff, dropout=0.1):
        super().__init__()
        self.attention = MultiHeadAttention(d_model, num_heads, dropout)
        self.norm1 = nn.LayerNorm(d_model)
        self.norm2 = nn.LayerNorm(d_model)

        self.ff = nn.Sequential(
            nn.Linear(d_model, d_ff),
            nn.ReLU(),
            nn.Dropout(dropout),
            nn.Linear(d_ff, d_model),
        )
        self.dropout = nn.Dropout(dropout)

    def forward(self, x, mask=None):
        # Self-attention com residual
        attn_out = self.attention(x, mask)
        x = self.norm1(x + self.dropout(attn_out))

        # Feed-forward com residual
        ff_out = self.ff(x)
        x = self.norm2(x + self.dropout(ff_out))

        return x


class MiniTransformer(nn.Module):
    """Transformer para classificação de texto"""
    def __init__(self, vocab_size, d_model=128, num_heads=4, num_layers=3,
                 d_ff=512, max_seq_len=512, num_classes=2, dropout=0.1):
        super().__init__()

        self.embedding = nn.Embedding(vocab_size, d_model)
        self.pos_encoding = nn.Parameter(torch.randn(1, max_seq_len, d_model))

        self.transformer_blocks = nn.ModuleList([
            TransformerBlock(d_model, num_heads, d_ff, dropout)
            for _ in range(num_layers)
        ])

        self.classifier = nn.Sequential(
            nn.AdaptiveAvgPool1d(1),
            nn.Flatten(),
            nn.Linear(d_model, num_classes),
        )

        self.dropout = nn.Dropout(dropout)

    def forward(self, x, mask=None):
        # x: [batch, seq_len]
        seq_len = x.size(1)

        x = self.embedding(x) + self.pos_encoding[:, :seq_len, :]
        x = self.dropout(x)

        for block in self.transformer_blocks:
            x = block(x, mask)

        # Pool + classificar
        x = x.transpose(1, 2)  # [batch, d_model, seq_len]
        x = self.classifier(x)

        return x


# Uso
model = MiniTransformer(
    vocab_size=10000,
    d_model=128,
    num_heads=4,
    num_layers=3,
    num_classes=2,
)
x = torch.randint(0, 10000, (32, 100))  # batch=32, seq=100 tokens
y = model(x)
print(f"Output shape: {y.shape}")  # [32, 2]
```

### 5.4 — Usar Modelo Pré-treinado (BERT, GPT)

```python
from transformers import AutoTokenizer, AutoModel


def use_pretrained():
    """Usar BERT pré-treinado para classificação"""
    model_name = "bert-base-multilingual-cased"
    tokenizer = AutoTokenizer.from_pretrained(model_name)
    model = AutoModel.from_pretrained(model_name)

    # Texto
    text = "Adorei o produto, recomendo muito!"
    inputs = tokenizer(text, return_tensors="pt", padding=True, truncation=True)

    # Inferência
    with torch.no_grad():
        outputs = model(**inputs)
        # last_hidden_state: [batch, seq_len, hidden_size]
        # pooler_output: [batch, hidden_size]
        embedding = outputs.pooler_output
        print(f"Embedding shape: {embedding.shape}")
        # [1, 768] — vetor de 768 dimensões representando a frase

    return embedding


use_pretrained()
```

### 5.5 — Quando Usar Transformer

✅ **Estado da arte para:**
- NLP (texto, classificação, tradução, geração)
- Visão (ViT, Swin)
- Áudio (Whisper, AudioLM)
- Multi-modal (CLIP, Flamingo)
- Qualquer sequência (substituiu LSTM em 2024+)

---

## 📊 Comparativo: Qual Arquitetura Usar?

| Problema | Arquitetura | Modelo Recomendado |
|----------|-------------|-------------------|
| **Dados tabulares** | MLP | XGBoost (não NN) ou MLP |
| **Imagens** | CNN | ResNet, EfficientNet, ViT |
| **Texto (classificação)** | Transformer | BERT, RoBERTa, XLM-R |
| **Texto (geração)** | Transformer (decoder) | GPT, Llama, Mistral |
| **Séries temporais curtas** | LSTM | LSTM ou Transformer |
| **Séries temporais longas** | Transformer | Informer, Autoformer |
| **Áudio** | CNN + Transformer | Whisper, Wav2Vec |
| **Vídeo** | CNN + Transformer | TimeSformer, Video Swin |
| **Multi-modal** | Transformer | CLIP, Flamingo, GPT-4V |

---

## 🚀 Deploy de Modelo

### Salvar Modelo Treinado

```python
# Salvar
torch.save({
    'model_state_dict': model.state_dict(),
    'optimizer_state_dict': optimizer.state_dict(),
    'epoch': epoch,
    'loss': loss,
}, 'model_checkpoint.pth')

# Carregar
checkpoint = torch.load('model_checkpoint.pth')
model.load_state_dict(checkpoint['model_state_dict'])
```

### Exportar para ONNX (Deploy Cross-platform)

```python
# Modelo em modo eval
model.eval()
dummy_input = torch.randn(1, 3, 224, 224)

# Exportar
torch.onnx.export(
    model,
    dummy_input,
    "model.onnx",
    export_params=True,
    opset_version=11,
    input_names=['input'],
    output_names=['output'],
    dynamic_axes={'input': {0: 'batch'}, 'output': {0: 'batch'}},
)
```

### Servir com FastAPI

```python
# app.py
from fastapi import FastAPI, UploadFile, File
import torch
from PIL import Image
import io
from torchvision import transforms

app = FastAPI()
model = SimpleCNN()
model.load_state_dict(torch.load("model.pth"))
model.eval()

transform = transforms.Compose([
    transforms.Resize((32, 32)),
    transforms.ToTensor(),
])

@app.post("/predict")
async def predict(file: UploadFile = File(...)):
    image = Image.open(io.BytesIO(await file.read()))
    image = transform(image).unsqueeze(0)

    with torch.no_grad():
        output = model(image)
        pred = output.argmax(dim=1).item()

    return {"class": pred}


# Rodar: uvicorn app:app --reload
```

### Deploy em Cloud (AWS SageMaker)

```python
# estimator.py
from sagemaker.pytorch import PyTorch

estimator = PyTorch(
    entry_point='train.py',
    role='arn:aws:iam::...:role/SageMakerRole',
    instance_count=1,
    instance_type='ml.p3.2xlarge',
    framework_version='2.0',
    py_version='py310',
)

estimator.fit({'training': 's3://bucket/data/'})
predictor = estimator.deploy(instance_type='ml.m5.large', initial_instance_count=1)
```

---

## 🧪 Exercícios Práticos

### Exercício 1: MLP para Classificar Flores Iris

```python
from sklearn.datasets import load_iris
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import StandardScaler

# Dataset
iris = load_iris()
X, y = iris.data, (iris.target == 0).astype(int).reshape(-1, 1)  # binário

# Normalizar
scaler = StandardScaler()
X = scaler.fit_transform(X)

# Split
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2)

# Treinar MLP
model = train_mlp(X_train, y_train, X_test, y_test, hidden_dims=[16, 8], epochs=100)
```

### Exercício 2: CNN para MNIST

```python
from torchvision import datasets, transforms
from torch.utils.data import DataLoader

# Dataset
transform = transforms.Compose([transforms.ToTensor()])
train_set = datasets.MNIST('./data', train=True, download=True, transform=transform)
train_loader = DataLoader(train_set, batch_size=64, shuffle=True)

# Modelo
model = SimpleCNN(num_classes=10)
criterion = nn.CrossEntropyLoss()
optimizer = torch.optim.Adam(model.parameters(), lr=0.001)

# Loop
for epoch in range(5):
    for X, y in train_loader:
        optimizer.zero_grad()
        loss = criterion(model(X), y)
        loss.backward()
        optimizer.step()
```

### Exercício 3: Transformer para Análise de Sentimento

```python
from transformers import AutoTokenizer, AutoModelForSequenceClassification
import torch

model = AutoModelForSequenceClassification.from_pretrained(
    "pysentimiento/bertabaporu-large-sentiment"
)
tokenizer = AutoTokenizer.from_pretrained("pysentimiento/bertabaporu-large-sentiment")

text = "Adorei o produto!"
inputs = tokenizer(text, return_tensors="pt")
outputs = model(**inputs)
pred = torch.softmax(outputs.logits, dim=-1)
sentiment = ["negativo", "neutro", "positivo"][pred.argmax().item()]
print(f"Sentimento: {sentiment}")
```

---

## 📚 Materiais Complementares

- `apostilas/39-ia-generativa-avancada.md` — IA generativa
- `apostilas/33-data-stack-agentes-ia.md` — data stack
- `tutoriais/20-fine-tuning-openai-api.md` — fine-tuning
- `Lib-Nexus/best-practices/05-sre-observability.md` — observabilidade
- `producao/INCIDENT-RESPONSE-RUNBOOK.md` — runbook

---

## 🔗 Links Externos

- PyTorch: https://pytorch.org/
- Hugging Face: https://huggingface.co/
- Distill.pub (visualizações): https://distill.pub/
- 3Blue1Brown (deep learning): https://www.3blue1brown.com/topics/neural-networks
- Andrew Ng (Stanford): https://www.coursera.org/learn/machine-learning
- Fast.ai: https://www.fast.ai/

---

*AcademIA · Tutorial 24 · Redes Neurais de Zero a Hero · 2026*
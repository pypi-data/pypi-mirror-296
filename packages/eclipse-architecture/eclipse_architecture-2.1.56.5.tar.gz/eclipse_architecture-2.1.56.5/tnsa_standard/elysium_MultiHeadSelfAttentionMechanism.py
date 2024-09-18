import torch
import torch.nn as nn
import torch.nn.functional as F

class AdvancedMultiHeadAttention(nn.Module):
    def __init__(self, embed_dim, num_heads):
        super(AdvancedMultiHeadAttention, self).__init__()
        self.num_heads = num_heads
        self.embed_dim = embed_dim
        self.head_dim = embed_dim // num_heads

        assert self.head_dim * num_heads == embed_dim, "Embedding dimension must be divisible by number of heads"

        self.q_linear = nn.Linear(embed_dim, embed_dim)
        self.k_linear = nn.Linear(embed_dim, embed_dim)
        self.v_linear = nn.Linear(embed_dim, embed_dim)
        self.out_linear = nn.Linear(embed_dim, embed_dim)

        self.rope = RotaryPositionEmbedding(embed_dim)

    def forward(self, query, key, value, mask=None):
        batch_size = query.size(0)
        
        q = self.q_linear(query).view(batch_size, -1, self.num_heads, self.head_dim).transpose(1, 2)
        k = self.k_linear(key).view(batch_size, -1, self.num_heads, self.head_dim).transpose(1, 2)
        v = self.v_linear(value).view(batch_size, -1, self.num_heads, self.head_dim).transpose(1, 2)

        q, k = self.rope(q, k)

        scores = torch.matmul(q, k.transpose(-2, -1)) / (self.head_dim ** 0.5)

        if mask is not None:
            scores = scores.masked_fill(mask == 0, float('-inf'))

        attn_weights = F.softmax(scores, dim=-1)
        out = torch.matmul(attn_weights, v)

        out = out.transpose(1, 2).contiguous().view(batch_size, -1, self.embed_dim)
        out = self.out_linear(out)

        return out

class RotaryPositionEmbedding(nn.Module):
    def __init__(self, embed_dim):
        super(RotaryPositionEmbedding, self).__init__()
        self.embed_dim = embed_dim

    def forward(self, q, k):
        seq_len = q.size(1)
        position_ids = torch.arange(seq_len, dtype=torch.float32).unsqueeze(0).to(q.device)
        position_embeddings = torch.sin(position_ids / (10000 ** (torch.arange(0, self.embed_dim, 2).float() / self.embed_dim))).unsqueeze(1)
        q = q + position_embeddings
        k = k + position_embeddings
        return q, k

class AdvancedFeedForward(nn.Module):
    def __init__(self, embed_dim, ff_hidden_dim):
        super(AdvancedFeedForward, self).__init__()
        self.fc1 = nn.Linear(embed_dim, ff_hidden_dim)
        self.gated_ff = nn.GatedLinearUnit(embed_dim)
        self.fc2 = nn.Linear(ff_hidden_dim, embed_dim)
        self.layer_norm = nn.LayerNorm(embed_dim)
        self.dropout = nn.Dropout(0.1)

    def forward(self, x):
        residual = x
        x = self.fc1(x)
        x = F.relu(x)
        x = self.gated_ff(x)
        x = self.fc2(x)
        x = self.dropout(x)
        x = self.layer_norm(x + residual)
        return x

class GatedLinearUnit(nn.Module):
    def __init__(self, input_dim):
        super(GatedLinearUnit, self).__init__()
        self.linear = nn.Linear(input_dim, input_dim)
        self.gate = nn.Linear(input_dim, input_dim)

    def forward(self, x):
        return self.linear(x) * torch.sigmoid(self.gate(x))

class DeepAdvancedGPT(nn.Module):
    def __init__(self, vocab_size, embed_dim, num_heads, ff_hidden_dim, num_layers):
        super(DeepAdvancedGPT, self).__init__()
        self.embedding = nn.Embedding(vocab_size, embed_dim)
        self.positional_embedding = nn.Parameter(torch.zeros(1, 512, embed_dim))
        self.layers = nn.ModuleList([
            nn.TransformerEncoderLayer(d_model=embed_dim, nhead=num_heads, dim_feedforward=ff_hidden_dim)
            for _ in range(num_layers)
        ])
        self.attention = AdvancedMultiHeadAttention(embed_dim, num_heads)
        self.feed_forward = AdvancedFeedForward(embed_dim, ff_hidden_dim)
        self.output_layer = nn.Linear(embed_dim, vocab_size)

    def forward(self, x):
        x = self.embedding(x) + self.positional_embedding[:, :x.size(1), :]
        for layer in self.layers:
            x = layer(x)
        x = self.attention(x, x, x)
        x = self.feed_forward(x)
        x = self.output_layer(x)
        return x

# Example usage
vocab_size = 30522
embed_dim = 768
num_heads = 12
ff_hidden_dim = 3072
num_layers = 12

model = DeepAdvancedGPT(vocab_size, embed_dim, num_heads, ff_hidden_dim, num_layers)

# Example input (sequence of token IDs)
input_ids = torch.randint(0, vocab_size, (1, 512))
output = model(input_ids)
print("Output Shape:", output.shape)

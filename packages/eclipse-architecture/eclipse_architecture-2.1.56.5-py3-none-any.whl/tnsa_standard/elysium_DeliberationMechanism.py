import torch
import torch.nn as nn
import torch.nn.functional as F

class AdvancedFeedForward(nn.Module):
    def __init__(self, embed_dim, ff_hidden_dim):
        super(AdvancedFeedForward, self).__init__()
        self.fc1 = nn.Linear(embed_dim, ff_hidden_dim)
        self.gated_ff = nn.Sequential(
            nn.Linear(embed_dim, embed_dim),
            nn.Sigmoid(),
            nn.Linear(embed_dim, embed_dim)
        )
        self.fc2 = nn.Linear(ff_hidden_dim, embed_dim)
        self.layer_norm = nn.LayerNorm(embed_dim)
        self.dropout = nn.Dropout(0.1)

    def forward(self, x):
        residual = x
        x = F.relu(self.fc1(x))
        x = self.gated_ff(x)
        x = self.fc2(x)
        x = self.dropout(x)
        x = self.layer_norm(x + residual)
        return x

class DeliberationLayer(nn.Module):
    def __init__(self, embed_dim, num_heads, ff_hidden_dim):
        super(DeliberationLayer, self).__init__()
        self.multihead_attention = nn.MultiheadAttention(embed_dim, num_heads)
        self.feed_forward = AdvancedFeedForward(embed_dim, ff_hidden_dim)
        self.layer_norm = nn.LayerNorm(embed_dim)
        self.dropout = nn.Dropout(0.1)

    def forward(self, x):
        # Multi-head self-attention
        attn_output, _ = self.multihead_attention(x, x, x)
        attn_output = self.dropout(attn_output)
        x = self.layer_norm(x + attn_output)
        
        # Feed-forward network
        ff_output = self.feed_forward(x)
        return ff_output

class DeliberationMechanism(nn.Module):
    def __init__(self, embed_dim, num_layers, deliberation_depth):
        super(DeliberationMechanism, self).__init__()
        self.num_layers = num_layers
        self.deliberation_depth = deliberation_depth
        self.layers = nn.ModuleList([
            DeliberationLayer(embed_dim, num_layers, embed_dim*4)
            for _ in range(num_layers)
        ])
        self.layer_norm = nn.LayerNorm(embed_dim)

    def forward(self, x):
        for _ in range(self.deliberation_depth):
            for layer in self.layers:
                x = layer(x)
        return self.layer_norm(x)

# Example usage
if __name__ == "__main__":
    embed_dim = 1024
    num_layers = 12
    deliberation_depth = 5  # Adjustable based on task complexity

    model = DeliberationMechanism(embed_dim, num_layers, deliberation_depth)

    # Example input (sequence of token embeddings)
    input_tensor = torch.randn(1, 512, embed_dim)
    output = model(input_tensor)
    print("Output Shape:", output.shape)

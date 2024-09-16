import torch
import torch.nn as nn
import torch.nn.functional as F
from torch.nn import Transformer


class SimpleTransformer(nn.Module):
    def __init__(self, input_size, hidden_size, num_layers, num_heads, output_size):
        super(SimpleTransformer, self).__init__()
        self.transformer = Transformer(d_model=hidden_size,
                                       nhead=num_heads,
                                       num_encoder_layers=num_layers,
                                       num_decoder_layers=num_layers)
        self.fc = nn.Linear(hidden_size, output_size)

    def forward(self, x):
        x = x.unsqueeze(1).transpose(0, 1)  # Add batch dimension and transpose to (batch, seq_len, input_size)
        x = self.transformer(x, x, x)  # Use the same input as query, key, and value
        x = x.transpose(0, 1).squeeze(1)  # Transpose back to (seq_len, batch) and remove batch dimension
        x = self.fc(x)
        return x

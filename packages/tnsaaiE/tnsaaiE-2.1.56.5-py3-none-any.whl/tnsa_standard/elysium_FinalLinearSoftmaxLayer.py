import torch
import torch.nn as nn

class FinalLinearAndSoftmaxLayer(nn.Module):
    def __init__(self, hidden_dim, vocab_size):
        super(FinalLinearAndSoftmaxLayer, self).__init__()
        self.linear = nn.Linear(hidden_dim, vocab_size)  # Linear transformation
        self.softmax = nn.Softmax(dim=-1)  # Softmax activation
    
    def forward(self, x):
        logits = self.linear(x)  # Compute logits
        probabilities = self.softmax(logits)  # Convert logits to probabilities
        return logits, probabilities

# Example usage
hidden_dim = 512
vocab_size = 10000

# Initialize the final linear and softmax layer
final_layer = FinalLinearAndSoftmaxLayer(hidden_dim, vocab_size)

# Dummy input for linear transformation
x = torch.randn(10, hidden_dim)  # (batch_size, hidden_dim)

# Forward pass
logits, probabilities = final_layer(x)

print("Logits Shape:", logits.shape)
print("Probabilities Shape:", probabilities.shape)

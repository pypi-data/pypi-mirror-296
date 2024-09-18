import torch
import torch.nn as nn
import torch.nn.functional as F
import numpy as np

class QValueEstimator(nn.Module):
    def __init__(self, input_dim, hidden_dim):
        super(QValueEstimator, self).__init__()
        # Define the Q-value estimation network
        self.fc1 = nn.Linear(input_dim, hidden_dim)
        self.fc2 = nn.Linear(hidden_dim, hidden_dim)
        self.fc3 = nn.Linear(hidden_dim, 1)  # Output a single Q-value
    
    def forward(self, x):
        # Forward pass through the Q-value network
        x = F.relu(self.fc1(x))
        x = F.relu(self.fc2(x))
        q_value = self.fc3(x)
        return q_value

class HierarchicalAttentionMechanism(nn.Module):
    def __init__(self, input_dim, hidden_dim, num_layers):
        super(HierarchicalAttentionMechanism, self).__init__()
        self.num_layers = num_layers
        self.attention_layers = nn.ModuleList([
            nn.TransformerEncoderLayer(d_model=input_dim, nhead=8, dim_feedforward=hidden_dim)
            for _ in range(num_layers)
        ])
    
    def forward(self, x):
        # Apply hierarchical attention layers
        for layer in self.attention_layers:
            x = layer(x)
        return x

class EnhancedReasoningModule(nn.Module):
    def __init__(self, input_dim, hidden_dim, num_layers):
        super(EnhancedReasoningModule, self).__init__()
        self.q_value_estimator = QValueEstimator(input_dim, hidden_dim)
        self.hierarchical_attention = HierarchicalAttentionMechanism(input_dim, hidden_dim, num_layers)
    
    def forward(self, x):
        # Apply hierarchical attention to input
        hierarchical_output = self.hierarchical_attention(x)
        
        # Estimate Q-values for each step
        q_values = [self.q_value_estimator(step) for step in hierarchical_output]
        q_values = torch.stack(q_values)
        
        return hierarchical_output, q_values

# Example usage
input_dim = 512
hidden_dim = 256
num_layers = 4

# Initialize the Enhanced Reasoning Module
enhanced_reasoning_module = EnhancedReasoningModule(input_dim, hidden_dim, num_layers)

# Dummy input for hierarchical attention and Q-value estimation
x = torch.randn(10, 20, input_dim)  # (batch_size, sequence_length, input_dim)

# Forward pass
hierarchical_output, q_values = enhanced_reasoning_module(x)

print("Hierarchical Output Shape:", hierarchical_output.shape)
print("Q-Values Shape:", q_values.shape)

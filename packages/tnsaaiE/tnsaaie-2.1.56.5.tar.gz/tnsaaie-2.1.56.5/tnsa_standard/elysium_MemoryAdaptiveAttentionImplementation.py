import torch
import torch.nn as nn
import torch.nn.functional as F

class AdaptiveMemoryNetwork(nn.Module):
    def __init__(self, hidden_dim, memory_size):
        super(AdaptiveMemoryNetwork, self).__init__()
        # Memory network components
        self.memory = nn.Parameter(torch.randn(memory_size, hidden_dim))
        self.memory_size = memory_size
        self.fc = nn.Linear(hidden_dim, hidden_dim)
    
    def forward(self, x):
        # Compute attention scores for memory
        attention_scores = torch.matmul(x, self.memory.t())
        attention_weights = F.softmax(attention_scores, dim=-1)
        
        # Compute the weighted sum of memory
        memory_output = torch.matmul(attention_weights, self.memory)
        # Combine memory with input
        combined_output = x + memory_output
        # Transform combined output
        output = self.fc(combined_output)
        return output

class DynamicAttentionMechanism(nn.Module):
    def __init__(self, hidden_dim, num_heads):
        super(DynamicAttentionMechanism, self).__init__()
        self.num_heads = num_heads
        self.head_dim = hidden_dim // num_heads
        
        self.query_fc = nn.Linear(hidden_dim, hidden_dim)
        self.key_fc = nn.Linear(hidden_dim, hidden_dim)
        self.value_fc = nn.Linear(hidden_dim, hidden_dim)
        self.out_fc = nn.Linear(hidden_dim, hidden_dim)
        
    def forward(self, query, key, value, attention_mask=None):
        batch_size = query.size(0)
        
        # Linear projections
        queries = self.query_fc(query).view(batch_size, -1, self.num_heads, self.head_dim)
        keys = self.key_fc(key).view(batch_size, -1, self.num_heads, self.head_dim)
        values = self.value_fc(value).view(batch_size, -1, self.num_heads, self.head_dim)
        
        # Scaled dot-product attention
        scores = torch.matmul(queries, keys.transpose(-2, -1)) / self.head_dim**0.5
        if attention_mask is not None:
            scores += attention_mask
        attention_weights = F.softmax(scores, dim=-1)
        context = torch.matmul(attention_weights, values)
        
        # Concat heads and project
        context = context.view(batch_size, -1, self.num_heads * self.head_dim)
        output = self.out_fc(context)
        return output

class MemoryAndAdaptiveAttention(nn.Module):
    def __init__(self, hidden_dim, memory_size, num_heads):
        super(MemoryAndAdaptiveAttention, self).__init__()
        self.adaptive_memory = AdaptiveMemoryNetwork(hidden_dim, memory_size)
        self.dynamic_attention = DynamicAttentionMechanism(hidden_dim, num_heads)
    
    def forward(self, x, attention_mask=None):
        # Apply adaptive memory network
        memory_output = self.adaptive_memory(x)
        
        # Apply dynamic attention mechanism
        output = self.dynamic_attention(memory_output, memory_output, memory_output, attention_mask)
        return output

# Example usage
hidden_dim = 512
memory_size = 100
num_heads = 8

# Initialize the Memory and Adaptive Attention component
memory_and_adaptive_attention = MemoryAndAdaptiveAttention(hidden_dim, memory_size, num_heads)

# Dummy input
x = torch.randn(10, 20, hidden_dim)  # (batch_size, sequence_length, hidden_dim)
attention_mask = torch.zeros(10, 20, 20)  # (batch_size, sequence_length, sequence_length)

# Forward pass
output = memory_and_adaptive_attention(x, attention_mask)

print("Output Shape:", output.shape)

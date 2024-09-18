import torch
import torch.optim as optim
import torch.nn as nn
from TNSA_StandardFinalLinearSoftmaxLayer import elysium_FinalLinearSoftmaxLayer

class TrainingSetup:
    def __init__(self, model, vocab_size, learning_rate=1e-4):
        self.model = model
        self.loss_function = nn.CrossEntropyLoss()  # Common loss function for classification tasks
        self.optimizer = optim.AdamW(self.model.parameters(), lr=learning_rate)  # Optimizer with weight decay
        self.learning_rate = learning_rate
    
    def train_step(self, input_data, target_data):
        self.model.train()
        self.optimizer.zero_grad()
        
        # Forward pass
        logits, _ = self.model(input_data)
        
        # Compute loss
        loss = self.loss_function(logits.view(-1, logits.size(-1)), target_data.view(-1))
        
        # Backward pass and optimization
        loss.backward()
        self.optimizer.step()
        
        return loss.item()

# Example usage
class DummyModel(nn.Module):
    def __init__(self, hidden_dim, vocab_size):
        super(DummyModel, self).__init__()
        self.final_layer = elysium_FinalLinearSoftmaxLayer(hidden_dim, vocab_size)
    
    def forward(self, x):
        return self.final_layer(x)

hidden_dim = 512
vocab_size = 10000
dummy_model = DummyModel(hidden_dim, vocab_size)
training_setup = TrainingSetup(dummy_model, vocab_size)

# Dummy input and target
input_data = torch.randn(10, hidden_dim)
target_data = torch.randint(0, vocab_size, (10,))

# Training step
loss = training_setup.train_step(input_data, target_data)
print("Training Loss:", loss)

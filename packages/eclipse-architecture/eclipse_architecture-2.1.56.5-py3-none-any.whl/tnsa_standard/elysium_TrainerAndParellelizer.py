# elysium_Training.py

import torch
import torch.nn as nn
import torch.optim as optim
from torch.nn.parallel import DataParallel, DistributedDataParallel
import torch.distributed as dist
from torch.optim.lr_scheduler import StepLR
from torch.utils.data import DataLoader

class TrainingAndParallelizationSetup:
    def __init__(self, model, vocab_size, learning_rate=1e-4, batch_size=256, sequence_length=2048):
        self.model = model
        self.vocab_size = vocab_size
        self.learning_rate = learning_rate
        self.batch_size = batch_size
        self.sequence_length = sequence_length
        
        # Setup loss function and optimizer
        self.loss_function = nn.CrossEntropyLoss()
        self.optimizer = optim.AdamW(self.model.parameters(), lr=self.learning_rate)
        
        # Setup learning rate scheduler
        self.scheduler = StepLR(self.optimizer, step_size=10000, gamma=0.95)
        
        # Setup DataParallel or DistributedDataParallel
        self.use_distributed = False
        self.setup_parallelization()
    
    def setup_parallelization(self):
        if torch.cuda.device_count() > 1:
            # Check if distributed training is required
            if dist.is_available() and dist.is_initialized():
                self.model = DistributedDataParallel(self.model)
                self.use_distributed = True
            else:
                self.model = DataParallel(self.model)
    
    def train_step(self, input_data, target_data):
        self.model.train()
        self.optimizer.zero_grad()
        
        # Forward pass
        logits = self.model(input_data)
        
        # Compute loss
        loss = self.loss_function(logits.view(-1, logits.size(-1)), target_data.view(-1))
        
        # Backward pass and optimization
        loss.backward()
        self.optimizer.step()
        self.scheduler.step()
        
        return loss.item()

    def configure_dataloader(self, dataset, shuffle=True):
        return DataLoader(dataset, batch_size=self.batch_size, shuffle=shuffle)

# Example usage
class ExampleModel(nn.Module):
    def __init__(self, hidden_dim, vocab_size):
        super(ExampleModel, self).__init__()
        self.final_layer = nn.Linear(hidden_dim, vocab_size)
    
    def forward(self, x):
        return self.final_layer(x)

hidden_dim = 512
vocab_size = 10000
batch_size = 256
sequence_length = 2048

# Initialize the model and training setup
example_model = ExampleModel(hidden_dim, vocab_size)
training_setup = TrainingAndParallelizationSetup(example_model, vocab_size, batch_size=batch_size, sequence_length=sequence_length)

# Dummy dataset and dataloader
class DummyDataset(torch.utils.data.Dataset):
    def __init__(self, size, vocab_size):
        self.data = torch.randn(size, hidden_dim)
        self.labels = torch.randint(0, vocab_size, (size,))
    
    def __len__(self):
        return len(self.data)
    
    def __getitem__(self, idx):
        return self.data[idx], self.labels[idx]

dataset = DummyDataset(size=10000, vocab_size=vocab_size)
dataloader = training_setup.configure_dataloader(dataset)

# Training loop (simplified)
for epoch in range(1):  # Example for one epoch
    for batch in dataloader:
        input_data, target_data = batch
        loss = training_setup.train_step(input_data, target_data)
        print("Training Loss:", loss)

import torch
import torch.nn as nn
import torch.nn.functional as F
from torch_geometric.nn import GATConv
import time

class EnhancedFashionGAT(nn.Module):
    """
    Enhanced Graph Attention Network for fashion item recommendations
    
    This model processes a heterogeneous graph with items and their attributes
    to learn representations that can predict compatible fashion item pairs.
    Supports the expanded set of fashion attributes.
    """
    def __init__(self, pyg_graph, hidden_channels=64, out_channels=32, heads=4, dropout=0.2):
        super().__init__()
        
        # Save the original node mappings
        self.node_types = pyg_graph.node_types
        
        # Initial embeddings for each node type
        self.node_embeddings = nn.ModuleDict()
        for node_type in self.node_types:
            num_nodes = pyg_graph[node_type].x.size(0)
            self.node_embeddings[node_type] = nn.Embedding(num_nodes, hidden_channels)
        
        # First GAT layer
        self.conv1 = nn.ModuleDict()
        for edge_type in pyg_graph.edge_types:
            src, _, dst = edge_type
            self.conv1[str(edge_type)] = GATConv(
                (hidden_channels, hidden_channels), 
                hidden_channels // heads, 
                heads=heads,
                dropout=dropout
            )
        
        # Second GAT layer
        self.conv2 = nn.ModuleDict()
        for edge_type in pyg_graph.edge_types:
            src, _, dst = edge_type
            self.conv2[str(edge_type)] = GATConv(
                (hidden_channels, hidden_channels), 
                out_channels, 
                heads=1,
                dropout=dropout
            )
        
        # Compatibility scoring module - input size is 2 * hidden_channels
        self.scorer = nn.Sequential(
            nn.Linear(2 * hidden_channels, hidden_channels),
            nn.ReLU(),
            nn.Dropout(dropout),
            nn.Linear(hidden_channels, 1),
            nn.Sigmoid()
        )
        
        # Print scorer network structure for debugging
        print("Scorer network structure:")
        for i, layer in enumerate(self.scorer):
            if isinstance(layer, nn.Linear):
                print(f"Layer {i}: Linear(in_features={layer.in_features}, out_features={layer.out_features})")
        
        # Attribute attention for explainability - now using shared layers and softmax
        self.attr_shared_layer = nn.Sequential(
            nn.Linear(2 * hidden_channels, hidden_channels),
            nn.Tanh()
        )
        
        # Include all attribute types with separated color attributes
        self.attr_types = [
            'color_value',  # Actual color
            'color_master', # Color luminance/brightness
            'appearance', 
            'fabric', 
            'sleeve', 
            'length', 
            'neckline'
        ]
        
        # Single attention layer for all attributes
        self.attr_attention = nn.Linear(hidden_channels, len(self.attr_types))
    
    def forward(self, x_dict, edge_index_dict):
        """
        Forward pass through the model
        
        Args:
            x_dict: Dictionary of node features for each node type
            edge_index_dict: Dictionary of edge indices for each edge type
            
        Returns:
            Dictionary of node embeddings for each node type
        """
        # Initialize embeddings for each node type
        h_dict = {}
        for node_type in self.node_types:
            h_dict[node_type] = self.node_embeddings[node_type].weight
        
        # First GAT layer
        h_dict1 = {}
        for edge_type, edge_index in edge_index_dict.items():
            src, _, dst = edge_type
            h_dict1[dst] = self.conv1[str(edge_type)]((h_dict[src], h_dict[dst]), edge_index)
        
        # Apply non-linearity
        for node_type in h_dict1:
            h_dict1[node_type] = F.relu(h_dict1[node_type])
            h_dict1[node_type] = F.dropout(h_dict1[node_type], p=0.2, training=self.training)
        
        # Second GAT layer
        h_dict2 = {}
        for edge_type, edge_index in edge_index_dict.items():
            src, _, dst = edge_type
            src_x = h_dict1.get(src, h_dict[src])  # Use updated embeddings if available
            dst_x = h_dict1.get(dst, h_dict[dst])
            h_dict2[dst] = self.conv2[str(edge_type)]((src_x, dst_x), edge_index)
        
        # Apply non-linearity
        for node_type in h_dict2:
            h_dict2[node_type] = F.relu(h_dict2[node_type])
        
        # Combine with first layer embeddings
        for node_type in self.node_types:
            if node_type in h_dict2:
                continue  # Already updated
            elif node_type in h_dict1:
                h_dict2[node_type] = h_dict1[node_type]
            else:
                h_dict2[node_type] = h_dict[node_type]
        
        return h_dict2
    
    def predict_compatibility(self, item1_idx, item2_idx, item_embeddings):
        """
        Predict compatibility score between two items
        
        Args:
            item1_idx: Index of first item
            item2_idx: Index of second item
            item_embeddings: Embeddings of all items
            
        Returns:
            Compatibility score between 0 and 1
        """
        # Get embeddings for items
        emb1 = item_embeddings[item1_idx]
        emb2 = item_embeddings[item2_idx]
        
        # Concatenate embeddings
        pair_emb = torch.cat([emb1, emb2], dim=0)
        
        # Compute compatibility score
        score = self.scorer(pair_emb)
        
        return score.item()
    
    def batch_predict_compatibility(self, item_indices1, item_indices2, item_embeddings):
        """Predict compatibility scores for a batch of item pairs"""
        if isinstance(item_indices1, list):
            item_indices1 = torch.tensor(item_indices1)
        if isinstance(item_indices2, list):
            item_indices2 = torch.tensor(item_indices2)
            
        # Get embeddings for items
        emb1 = item_embeddings[item_indices1]
        emb2 = item_embeddings[item_indices2]
        
        # Concatenate embeddings along the feature dimension
        pair_emb = torch.cat([emb1, emb2], dim=1)
        
        # Compute compatibility scores
        scores = self.scorer(pair_emb)
        
        return scores.squeeze()

    def compute_attribute_importance(self, item1_idx, item2_idx, item_embeddings):
        """
        Compute importance scores for different attributes to explain compatibility.
        Now returns normalized scores that sum to 1, representing percentage of influence.
        
        Args:
            item1_idx: Index of first item
            item2_idx: Index of second item
            item_embeddings: Embeddings of all items
            
        Returns:
            Dictionary of importance scores for each attribute type, summing to 1
        """
        # Get embeddings for items
        emb1 = item_embeddings[item1_idx]
        emb2 = item_embeddings[item2_idx]
        
        # Concatenate embeddings
        pair_emb = torch.cat([emb1, emb2], dim=0).unsqueeze(0)
        
        # Pass through shared layer
        shared_features = self.attr_shared_layer(pair_emb)
        
        # Get attention scores for all attributes at once
        raw_scores = self.attr_attention(shared_features)
        
        # Apply softmax to get normalized scores
        normalized_scores = F.softmax(raw_scores, dim=1)
        
        # Convert to dictionary
        attribute_scores = {
            attr_type: score.item()
            for attr_type, score in zip(self.attr_types, normalized_scores[0])
        }
        
        return attribute_scores

def train_gat_model(model, pyg_graph, positive_pairs, negative_pairs, epochs=50, batch_size=128, verbose=True):
    """Train the GAT model using positive and negative pairs"""
    import torch.optim as optim
    import time
    
    device = torch.device('cpu')
    model = model.to(device)
    
    # Prepare training data
    x_dict = {node_type: data.x.to(device) for node_type, data in pyg_graph.items()}
    edge_index_dict = {
        edge_type: data.edge_index.to(device) 
        for edge_type, data in pyg_graph.items() 
        if hasattr(data, 'edge_index')
    }
    
    # Combine positive and negative pairs
    all_pairs = torch.cat([positive_pairs, negative_pairs], dim=0)
    # Extract scores (third column)
    all_scores = all_pairs[:, 2]
    # Extract just the indices (first two columns)
    all_pairs = all_pairs[:, :2].long()
    
    # Create optimizer
    optimizer = optim.Adam(model.parameters(), lr=0.001)
    
    # Training loop
    model.train()
    best_loss = float('inf')
    patience = 5
    patience_counter = 0
    
    if verbose:
        print("\nTraining GAT model...")
        print(f"Total pairs: {len(all_pairs)}")
        print(f"Batch size: {batch_size}")
        print(f"Number of epochs: {epochs}\n")
    
    for epoch in range(epochs):
        start_time = time.time()
        total_loss = 0
        num_batches = 0
        
        # Shuffle pairs for each epoch
        indices = torch.randperm(len(all_pairs))
        all_pairs_shuffled = all_pairs[indices]
        all_scores_shuffled = all_scores[indices]
        
        # Process in batches
        for i in range(0, len(all_pairs), batch_size):
            batch_pairs = all_pairs_shuffled[i:i+batch_size]
            batch_scores = all_scores_shuffled[i:i+batch_size]
            
            # Zero gradients
            optimizer.zero_grad()
            
            # Forward pass
            node_embeddings = model(x_dict, edge_index_dict)
            item_embeddings = node_embeddings['item']
            
            # Get predictions for batch
            pred_scores = model.batch_predict_compatibility(
                batch_pairs[:, 0],
                batch_pairs[:, 1],
                item_embeddings
            )
            
            # Compute loss using MSE since we now have continuous scores
            loss = torch.nn.functional.mse_loss(pred_scores, batch_scores)
            
            # Backward pass
            loss.backward()
            optimizer.step()
            
            total_loss += loss.item()
            num_batches += 1
        
        # Compute average loss for epoch
        avg_loss = total_loss / num_batches
        epoch_time = time.time() - start_time
        
        if verbose and (epoch + 1) % 5 == 0:
            print(f"Epoch {epoch+1}/{epochs}, Loss: {avg_loss:.4f}, Time: {epoch_time:.2f}s")
        
        # Early stopping
        if avg_loss < best_loss:
            best_loss = avg_loss
            patience_counter = 0
        else:
            patience_counter += 1
            
        if patience_counter >= patience:
            if verbose:
                print(f"\nEarly stopping at epoch {epoch+1}")
            break
    
    if verbose:
        print("\nTraining completed!")
        print(f"Best loss: {best_loss:.4f}")
    
    return model


def save_model_and_data(model, fashion_graph, pyg_graph, node_mapping, fashion_data, output_dir="fashion_model"):
    """Save model and graph data for later use"""
    import os
    import pickle
    import torch
    
    # Create output directory if it doesn't exist
    os.makedirs(output_dir, exist_ok=True)
    
    # Save model
    torch.save(model.state_dict(), os.path.join(output_dir, "gat_model.pt"))
    
    # Save graph data using pickle
    with open(os.path.join(output_dir, "fashion_graph.pkl"), "wb") as f:
        pickle.dump(fashion_graph, f)
    
    with open(os.path.join(output_dir, "node_mapping.pkl"), "wb") as f:
        pickle.dump(node_mapping, f)
    
    # Save PyG graph tensors
    torch.save(pyg_graph, os.path.join(output_dir, "pyg_graph.pt"))
    
    # Save a sample of the original fashion data (for lookups)
    fashion_data_sample = fashion_data.sample(min(5000, len(fashion_data)), random_state=42)
    fashion_data_sample.to_csv(os.path.join(output_dir, "fashion_data_sample.csv"), index=False)
    
    print(f"Model and data saved to {output_dir}/")

def load_model_and_data(model_class, output_dir="fashion_model"):
    """Load saved model and graph data"""
    import os
    import pickle
    import torch
    import pandas as pd
    
    # Load model
    model_path = os.path.join(output_dir, "gat_model.pt")
    if not os.path.exists(model_path):
        raise FileNotFoundError(f"Model file not found at {model_path}")
    
    # Load PyG graph
    pyg_graph = torch.load(os.path.join(output_dir, "pyg_graph.pt"))
    
    # Create model
    model = model_class(pyg_graph)
    model.load_state_dict(torch.load(model_path))
    model.eval()
    
    # Load graph data
    with open(os.path.join(output_dir, "fashion_graph.pkl"), "rb") as f:
        fashion_graph = pickle.load(f)
    
    with open(os.path.join(output_dir, "node_mapping.pkl"), "rb") as f:
        node_mapping = pickle.load(f)
    
    # Load fashion data sample
    fashion_data = pd.read_csv(os.path.join(output_dir, "fashion_data_sample.csv"))
    
    print(f"Model and data loaded from {output_dir}/")
    
    return model, fashion_graph, pyg_graph, node_mapping, fashion_data
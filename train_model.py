import os
import cv2
import torch
import numpy as np
import torch.nn as nn
import torch.nn.functional as F
from torch_geometric.data import Data, DataLoader
from torch_geometric.nn import GCNConv, global_mean_pool

DATASET_DIR = "dataset"
IMG_SIZE = 64   
BATCH_SIZE = 8
EPOCHS = 15


def image_to_graph(image):
    h, w, c = image.shape
    nodes = []
    edges = []

    for i in range(h):
        for j in range(w):
            nodes.append(image[i, j] / 255.0)

            node_id = i * w + j

            if i > 0:
                edges.append([node_id, (i-1)*w + j])
            if j > 0:
                edges.append([node_id, i*w + (j-1)])

    x = torch.tensor(nodes, dtype=torch.float)
    edge_index = torch.tensor(edges, dtype=torch.long).t().contiguous()

    return x, edge_index


def load_dataset():
    data_list = []
    class_names = sorted(os.listdir(DATASET_DIR))
    class_to_idx = {cls:i for i, cls in enumerate(class_names)}

    for cls in class_names:
        class_path = os.path.join(DATASET_DIR, cls)

        for img_name in os.listdir(class_path):
            img_path = os.path.join(class_path, img_name)

            image = cv2.imread(img_path)
            image = cv2.resize(image, (IMG_SIZE, IMG_SIZE))

            x, edge_index = image_to_graph(image)

            y = torch.tensor([class_to_idx[cls]], dtype=torch.long)

            data = Data(x=x, edge_index=edge_index, y=y)
            data_list.append(data)

    return data_list, len(class_names)

dataset, NUM_CLASSES = load_dataset()

train_loader = DataLoader(dataset, batch_size=BATCH_SIZE, shuffle=True)


class GNNModel(nn.Module):
    def __init__(self, num_node_features, num_classes):
        super().__init__()

        self.conv1 = GCNConv(num_node_features, 64)
        self.conv2 = GCNConv(64, 128)

        self.fc1 = nn.Linear(128, 64)
        self.fc2 = nn.Linear(64, num_classes)

    def forward(self, x, edge_index, batch):
        x = self.conv1(x, edge_index)
        x = F.relu(x)

        x = self.conv2(x, edge_index)
        x = F.relu(x)

        x = global_mean_pool(x, batch)

        x = F.relu(self.fc1(x))
        x = self.fc2(x)

        return F.log_softmax(x, dim=1)


device = torch.device("cuda" if torch.cuda.is_available() else "cpu")

model = GNNModel(num_node_features=3, num_classes=NUM_CLASSES).to(device)
optimizer = torch.optim.Adam(model.parameters(), lr=0.001)

for epoch in range(EPOCHS):
    model.train()
    total_loss = 0

    for data in train_loader:
        data = data.to(device)

        optimizer.zero_grad()

        out = model(data.x, data.edge_index, data.batch)
        loss = F.nll_loss(out, data.y)

        loss.backward()
        optimizer.step()

        total_loss += loss.item()

    print(f"Epoch {epoch+1}, Loss: {total_loss:.4f}")


torch.save(model.state_dict(), "gnn_disease_model.pth")

print("✅ GNN TRAINING COMPLETE")
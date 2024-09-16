from transformers import CLIPProcessor, CLIPModel
import torch


model = CLIPModel.from_pretrained("openai/clip-vit-base-patch32")
processor = CLIPProcessor.from_pretrained("openai/clip-vit-base-patch32")

def get_text_embedding(text):
    inputs = processor(text=text, return_tensors="pt")
    with torch.no_grad():
        embedding = model.get_text_features(**inputs).numpy()
    return embedding.squeeze()

def TextEmbeddingEngine(text):
    text_embeddings=get_text_embedding(text)
    return text_embeddings
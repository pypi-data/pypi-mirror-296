from transformers import CLIPProcessor, CLIPModel
from PIL import Image
import requests
import torch
from io import BytesIO
model = CLIPModel.from_pretrained("openai/clip-vit-base-patch32")
processor = CLIPProcessor.from_pretrained("openai/clip-vit-base-patch32")


def get_image_embedding(image_path):
    imagebytes=requests.get(image_path).content
    image = Image.open(BytesIO(imagebytes))
    inputs = processor(images=image, return_tensors="pt")
    with torch.no_grad():
        embedding = model.get_image_features(**inputs).numpy()
    return embedding.squeeze()


def ImageEmbeddingEngine(image_urls):
        embeddings=[]
        for image in image_urls:
                image_embedding=get_image_embedding(image)
                embeddings.append(image_embedding)
        return embeddings , image_urls
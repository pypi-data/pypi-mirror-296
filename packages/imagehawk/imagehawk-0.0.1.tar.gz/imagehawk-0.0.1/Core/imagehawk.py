from Core.Engines.image_embeddings import ImageEmbeddingEngine
from Core.Engines.text_embeddings import TextEmbeddingEngine
from Core.VectorStores.qdrantvectorstore import SaveEmbeddings
from qdrant_client import QdrantClient


class ImageHawk():
    def _init_(self,new_collection,image_urls,query_text,qdrant_url,qdrant_pass,userid,project):
        self.new_collection=new_collection
        self.image_urls=image_urls
        self.query_text=query_text
        self.qdrant_url=qdrant_url
        self.qdrant_pass=qdrant_pass
        self.userid=userid
        self.project=project

    def generate_image_embeddings(self):
        embeddings,image_urls=ImageEmbeddingEngine(self.image_urls)
        save_result=SaveEmbeddings(
            new=bool(self.new_collection),qdrant_url=self.qdrant_url,qdrant_api_key=self.qdrant_pass,
            embeddings=embeddings,image_urls=image_urls,userid=self.userid,
            agent=self.project
        )
        if save_result==True:
            return True
        elif save_result==False:
            return False


    def search_similar_images(self):

        text_embedding =TextEmbeddingEngine(self.query_text)
        client = QdrantClient(url=self.qdrant_url, api_key=self.qdrant_api_key,prefer_grpc=True)
        search_result = client.search(
        collection_name="image_embeddings",
        query_vector=text_embedding.tolist(),
        limit=1
        )

        #Display the search results
        for result in search_result:
            output={
                "id":result.id,
                "similarity_score":result.score,
                "metadata":result.payload
            }
            return output

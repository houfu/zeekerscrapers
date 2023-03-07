# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://docs.scrapy.org/en/latest/topics/item-pipeline.html
import os

import weaviate
# useful for handling different item types with a single interface
from itemadapter import ItemAdapter

import dotenv

dotenv.load_dotenv()

class_obj = {
    "class": "ZeekerArticle",
    "description": "A generic article",
    "properties": [
        {
            "dataType": ["text"],
            "description": "Content of the article",
            "name": "content"
        },
        {
            "dataType": ["date"],
            "description": "Date when article was published",
            "name": "date_pub"
        },
        {
            "dataType": ["text"],
            "description": "Title of the article",
            "name": "title"
        },
        {
            "dataType": ["string"],
            "description": "Category of the article",
            "name": "category"
        },
    ],
    "vectorizer": "text2vec-openai"
}


class SaveZeekerArticletoWeaviatePipeline:

    def __init__(self):
        resource_owner_config = weaviate.AuthClientPassword(
            username=os.getenv('WEAVIATE_USER'),
            password=os.getenv('WEAVIATE_PASSWORD'),
        )

        self.client = weaviate.Client(
            os.getenv('WEAVIATE_URL'),
            auth_client_secret=resource_owner_config,
            additional_headers={
                "X-OpenAI-Api-Key": os.getenv('OPENAI_KEY')
            }
        )

    def open_spider(self, spider):
        """
        When spider is opened,
        remove all and recreate schema.
        """
        self.client.batch.configure(batch_size=5, dynamic=True)

        # TODO: Make sure it is possible to keep existing data in a database in a production environment
        self.client.schema.delete_all()

        self.client.schema.create_class(class_obj)

    def process_item(self, item, spider):
        adapter = ItemAdapter(item)
        texts = adapter.get('text')
        from langchain.text_splitter import RecursiveCharacterTextSplitter
        splitter = RecursiveCharacterTextSplitter.from_tiktoken_encoder(chunk_size=300, chunk_overlap=50)
        chunks = splitter.split_text(texts)
        with self.client.batch as batch:
            for chunk in chunks:
                batch.add_data_object({
                    "content": chunk,
                    "date_pub": adapter.get('date_published'),
                    "title": adapter.get('title'),
                    "category": spider.name,
                }, "ZeekerArticle")
        return item

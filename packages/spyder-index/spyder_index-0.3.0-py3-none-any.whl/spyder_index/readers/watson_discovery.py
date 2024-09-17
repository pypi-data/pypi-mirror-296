import logging

from datetime import datetime
from typing import List, Optional

from spyder_index.core.readers import BaseReader
from spyder_index.core.document import Document


class WatsonDiscoveryReader(BaseReader):
    """Provides functionality to load documents from IBM Watson Discovery.

    See https://cloud.ibm.com/docs/discovery-data?topic=discovery-data-getting-started for more info.

    Args:
        url (str): Watson Discovery instance url.
        api_key (str): Watson Discovery apikey.
        project_id (str): Watson Discovery project ID.
        version (str, optional): Watson Discovery version. Defaults to ``2023-03-31``.
        batch_size (int, optional): Batch size for bulk operations. Defaults to ``50``.
        date_gte (str, optional): Load Watson Discovery documents uploaded/created after given date, expected format ``YYYY-MM-DD``. Defaults to ``datetime.today()``.

    **Example**

    .. code-block:: python

        from spyder_index.readers import WatsonDiscoveryReader

        reader = WatsonDiscoveryReader(url="<your_url>",
                                          api_key="<your_api_key>",
                                          project_id="<your_project_id>")
    """

    def __init__(self,
                 url: str,
                 api_key: str,
                 project_id: str,
                 version: str = '2023-03-31',
                 batch_size: int = 50,
                 date_gte: str = datetime.today().strftime('%Y-%m-%d')
                 ) -> None:
        try:
            from ibm_watson import DiscoveryV2
            from ibm_cloud_sdk_core.authenticators import IAMAuthenticator

        except ImportError:
            raise ImportError("ibm-watson package not found, please install it with `pip install ibm-watson`")

        self.project_id = project_id
        self.batch_size = batch_size
        self.date_gte = date_gte

        try:
            authenticator = IAMAuthenticator(api_key)
            self._client = DiscoveryV2(authenticator=authenticator,
                                       version=version)

            self._client.set_service_url(url)
        except Exception as e:
            logging.error(f"Error connecting to IBM Watson Discovery: {e}")
            raise

    def load_data(self, extra_info: Optional[dict] = None) -> List[Document]:
        """Loads documents from the Watson Discovery.

        **Example**

        .. code-block:: python

            docs = reader.load_data()
        """
        from ibm_watson.discovery_v2 import QueryLargePassages
        last_batch_size = self.batch_size
        offset_len = 0
        documents = []

        while last_batch_size == self.batch_size:
            results = self._client.query(
                project_id=self.project_id,
                count=self.batch_size,
                offset=offset_len,
                return_=["extracted_metadata.filename", "extracted_metadata.file_type", 'text'],
                filter="extracted_metadata.publicationdate>={}".format(self.date_gte),
                passages=QueryLargePassages(enabled=False)).get_result()

            last_batch_size = len(results['results'])
            offset_len = offset_len + last_batch_size

            # Make sure all retrieved document 'text' exist
            results_documents = [doc for doc in results['results'] if 'text' in doc]

            documents.extend([Document(doc_id=doc['document_id'],
                                       text=' '.join(doc['text']),
                                       metadata={'collection_id': doc['result_metadata']['collection_id']} | doc[
                                           'extracted_metadata'])
                              for doc in results_documents])

        return documents

"""Module that contains utility functions, as well as tooling for manual parsing of data contained in Nyx."""

import logging
import os
import sqlite3
from io import StringIO
from typing import Any, List, Literal, Optional

import pandas as pd
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity
from sqlalchemy import create_engine, engine
from sqlalchemy.pool import StaticPool

from nyx_client.data import Data

logging.basicConfig(format="%(asctime)s %(levelname)s [%(module)s] %(message)s", level=logging.INFO)

log = logging.getLogger(__name__)


class VectorResult:  # noqa: D101
    def __init__(self, chunks: List[str], similarities: List[float], success: bool, message: str = ""):  # noqa: D107
        self.chunks = chunks
        self.similarities = similarities
        self.success = success
        self.message = message

    def __repr__(self):
        return (
            f"VectorResult(chunks={repr(self.chunks)}, similarities={repr(self.similarities)},"
            f"success={repr(self.success)})"
        )


class Utils:
    """Utility methods for query (system) prompt modification."""

    @staticmethod
    def with_sources(prompt: str, **kwargs) -> str:
        """Expand prompt with clause to request the data sources considered to be included in the response."""
        return Utils.build_query(
            prompt
            + (
                "and also using the table nyx_subscriptions where table_name is the name of the table the "
                "information came from, retrieve the source and url of the relevant table queried."
                "When you go to say table, actually say sources. Output in markdown list format."
                "You must include sources for all requests,where the table the results came from"
                " matches the table_name in nyx_subscriptions, and the "
                "relevant url from that table"
            ),
            **kwargs,
        )

    @staticmethod
    def build_query(prompt: str, **kwargs) -> str:
        """Base prompt builder."""
        return (
            prompt
            + " "
            + (
                "Do not talk as if you are getting the results from a database, each table in the database is "
                "a file from a source. If there are no tables "
                "in the schema, or you can't see relevant ones, JUST RESPOND WITH the text 'I don't know', "
                "nothing else. \n"
                "all urls should be left in the same format, do not strip query params from the urls"
                "if you cannot find an exact match when looking for relevant tables, attempt to answer the query"
                "using the most relevant table, only provide the answer if it answers the users query"
                "Database information: \n {}".format(kwargs if kwargs else "")
            )
        )

    @staticmethod
    def with_confidence(prompt: str) -> str:
        """Like `with_sources` but also requests for a confidence score to be included in the result."""
        return prompt + (
            "Do not talk as if you are getting the results from a database, each table in the database is "
            "a file from a source. Do not make mention of any sources in your answer. If there are no tables "
            "in the schema, or you can't see relevant ones, JUST RESPOND WITH the text 'I don't know', nothing else."
            "Also, provide a confidence score between 0 and 1 for your answer. The response should be of the format: "
            '{"content": "<your response>", "confidence": <your confidence score>}'
        )


class Parser:
    """A class for processing and querying datasets from Data instances.

    This class provides methods to convert data into SQL databases or vector representations,
    and to perform queries on the processed data.

    Attributes:
        vectors: The TF-IDF vector representations of the processed content.
        vectorizer: The TfidfVectorizer instance used for creating vectors.
        chunks: The text chunks created from the processed content.
    """

    _excel_mimes = [
        # xlsx
        "vnd.openxmlformats-officedocument.spreadsheetml.sheet",
        # xls
        "vnd.ms-excel",
    ]

    def __init__(self):
        """Initialize a Parser instance."""
        self.vectors = None
        self.vectorizer = None
        self.chunks = None

    @staticmethod
    def data_as_db(
        data: List[Data],
        additional_information: List[str] = None,
        sqlite_file: Optional[str] = None,
        if_exists: Literal["fail", "replace", "append"] = "fail",
    ) -> "engine.Engine":
        """Process the content of multiple Data instances into an in-memory SQLite database.

        This method downloads the content of each Data (if it's a CSV) and converts it to an in-memory
        SQLite database. The resulting database engine is then returned for use with language models.

        Args:
            data: A list of Data instances to process.
            additional_information: List of additional information to be stored in the DB as a fallback
            sqlite_file: Provide a file for the database to reside in
            if_exists: What to do if a table already exists Defaults to "fail" can be "fail", "append", "replace"

        Returns:
            An SQLAlchemy `engine.Engine` instance for the in-memory SQLite database.

        Note:
            If the list of data is empty, an empty database engine is returned.
        """
        connection_str = ":memory:"
        if sqlite_file:
            # Ensure the directory exists
            os.makedirs(os.path.dirname(sqlite_file), exist_ok=True)
            connection_str = sqlite_file

        connection = sqlite3.connect(connection_str, check_same_thread=False)
        db_engine = create_engine(
            "sqlite://",
            creator=lambda: connection,
            poolclass=StaticPool,
            connect_args={"check_same_thread": False},
        )

        if len(data) == 0:
            return db_engine
        tables = []
        for d in data:
            content = d.download()
            if content is None:
                log.debug("Not adding table for %s as no content was found", d.title)
                continue
            tables.append([d.title, d.url, d.title.replace(" ", "_"), d.description])
            if content:
                try:
                    if d.content_type == "csv":
                        data = pd.read_csv(StringIO(content))
                    elif d.content_type in Parser._excel_mimes:
                        data = pd.read_excel(StringIO(content))
                    elif d.content_type == "json":
                        data = pd.read_json(StringIO(content))
                    else:
                        log.warning("%s is unsupported type %s", d.title, d.content_type)
                        continue
                    data.columns = Parser.normalise_values(data.columns)
                    table_name = Parser.normalise_values([d.title])[0]
                    data.to_sql(table_name, db_engine, index=False)
                except pd.errors.ParserError:
                    if d.content_type in ["csv", "json", *Parser._excel_mimes]:
                        log.warning("%s could not be processed as a %s", d.title, d.content_type)
                except Exception as e:
                    log.warning("Unexpected error for %s: %s", d.title, e)
        if len(tables) > 0:
            df = pd.DataFrame(tables)
            df.columns = ["file_title", "url", "table_name", "description"]
            df.to_sql("nyx_subscriptions", db_engine, index=False, if_exists=if_exists)

        if additional_information:
            df = pd.DataFrame(additional_information)
            df.columns = ["context"]
            df.to_sql("additional_information", db_engine, index=False, if_exists=if_exists)
        return db_engine

    @staticmethod
    def normalise_values(values: List[str]) -> List[str]:
        """Normalise names in a list of values.

        Args:
            values (List[str]): A list of values to normalise.

        Returns:
            List[str]: A list of normalised values.
        """
        return [
            value.lower().replace(" ", "_").replace(".", "_").replace("-", "_").replace("(", "_").replace(")", "_")
            for value in values
            if value
        ]

    def data_as_vectors(self, data: List[Data], chunk_size: int = 1000):
        """Process the content of multiple Data instances into vector representations.

        This method downloads the content of each Data, combines it, chunks it,
        and creates a TF-IDF vectorizer for the chunks.

        Args:
            data (List[Data]): A list of Data instances to process.
            chunk_size (int, optional): The size of each chunk when splitting the content. Defaults to 1000.

        Returns:
            Parser: The current Parser instance with updated vectors, vectorizer, and chunks.

        Note:
            If no content is found in any of the data, the method returns without processing.
        """
        contents = ""
        for d in data:
            content = d.download()
            if content:
                contents += content
        if contents == "":
            return

        self.chunks = self._chunk_text(contents, chunk_size)
        if len(self.chunks) == 0:
            return

        self.vectorizer = TfidfVectorizer()
        self.vectors = self.vectorizer.fit_transform(self.chunks)

        return self

    @staticmethod
    def _chunk_text(text: str, chunk_size: int) -> List[str]:
        """Split a text into chunks of a specified size.

        Args:
            text (str): The text to be chunked.
            chunk_size (int): The maximum number of words in each chunk.

        Returns:
            List[str]: A list of text chunks.
        """
        words = text.split()
        return [" ".join(words[i : i + chunk_size]) for i in range(0, len(words), chunk_size)]

    def find_matching_chunk(self, query_vector: Any, k: int = 3) -> VectorResult:
        """Find the best matching chunks for a given query vector.

        Args:
            query_vector (Any): The vector representation of the query.
            k (int): The number of top matches to return. Defaults to 3.

        Returns:
            VectorResult: An object containing the best matching chunks, their similarity scores, and success status.

        Raises:
            ValueError: If the content has not been processed yet.
        """
        if self.vectors is None:
            return VectorResult(
                chunks=[],
                similarities=[],
                success=False,
                message="content has either not been processed, or you have no plain text",
            )

        similarities = cosine_similarity(query_vector, self.vectors)
        top_indices = similarities[0].argsort()[-k:][::-1]  # Get indices of top k similarities

        top_chunks = [self.chunks[i] for i in top_indices]
        top_similarities = similarities[0][top_indices].tolist()

        return VectorResult(
            chunks=top_chunks,
            similarities=top_similarities,
            success=True,
        )

    def query(self, text: str, k: int = 3) -> VectorResult:
        """Query the processed content with a text string.

        Args:
            text (str): The query text.
            k (int): The number of top matches to return. Defaults to 3.

        Returns:
            VectorResult: An object containing the best matching chunks and related information,
                          or an error message if the content has not been processed.
        """
        if self.vectorizer is None:
            return VectorResult(
                chunks=[],
                similarities=[],
                success=False,
                message="content not processed, or not present on the data (do you have access?)",
            )
        query_vector = self.vectorizer.transform([text])
        return self.find_matching_chunk(query_vector, k)

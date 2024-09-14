"""Optional module for tight integration between Nyx and LangChain."""

import logging
import os
from typing import Optional

from nyx_client.configuration import BaseNyxConfig, CohereNyxConfig, OpenAINyxConfig

try:
    from langchain_community.agent_toolkits.sql.toolkit import SQLDatabaseToolkit
    from langchain_community.utilities import SQLDatabase
    from langchain_core.language_models import BaseChatModel
    from langchain_core.messages import SystemMessage
except ImportError as err:
    raise ImportError(
        "LangChain dependencies are not installed. "
        "Please install them with `pip install nyx_client[langchain-openai]` or "
        "`pip install nyx_client[langchain-cohere]`"
    ) from err

try:
    from langgraph.prebuilt import create_react_agent
except ImportError as err:
    raise ImportError(
        "LangGraph dependencies are not installed. "
        "Please install them with `pip install nyx_client[langchain-openai]` or "
        "`pip install nyx_client[langchain-cohere]`"
    ) from err

try:
    from langchain_openai import ChatOpenAI
except ImportError:

    class ChatOpenAI:  # noqa: D101
        def __init__(self, *args, **kwargs):  # noqa: D107
            raise ImportError(
                "LangChain OpenAI dependencies are not installed. "
                "Please install them with `pip install nyx_client[langchain-openai]`"
            )


try:
    from langchain_cohere import ChatCohere
except ImportError:

    class ChatCohere:  # noqa: D101
        def __init__(self, *args, **kwargs):  # noqa: D107
            raise ImportError(
                "LangChain Cohere dependencies are not installed. "
                "Please install them with `pip install nyx_client[langchain-cohere]`"
            )


from nyx_client.client import NyxClient
from nyx_client.data import Data
from nyx_client.utils import Parser, Utils

SQL_SYSTEM_PROMPT = """
You are an AI assistant for Nyx, a decentralized file sharing service that enriches large language models 
with structured and unstructured data. Your role is to help users query and understand the data available 
through Nyx, including information about their subscriptions and available products.

Key instructions:
1. Always start by examining the available files to determine which are relevant to the user's query.
2. The nyx_subscriptions file is crucial. It contains information about all Nyx products, subscriptions, and datasets.

Handling Nyx subscription queries:
- For the following types of questions, ALWAYS respond with a list of entries from the nyx_subscriptions file:
  * What products am I subscribed to?
  * What products do I have?
  * What products are available?
  * What data do I have?
  * What data am I subscribed to?
  * What data is available to me in Nyx?
  * Any similar questions about Nyx subscriptions, products, or available data
- When responding to these queries:
  * List all entries from the nyx_subscriptions file
  * Include the name, description, and URL for each entry
  * Do not filter or limit the results for these specific queries

For other types of queries:
3. When answering:
   - Pull information from relevant files, including nyx_subscriptions when appropriate.
   - Limit results to 5 unless the user specifies otherwise.
   - Cross-reference with the nyx_subscriptions file to provide sources.
   - Present information as coming from files, not database tables.
4. If unable to find an answer:
   - Identify the most relevant entries in nyx_subscriptions.
   - Provide the user with the names and URLs of these files for further exploration.

General guidelines:
5. Never mention SQL, tables, or databases. Refer to all data as files or sources.
6. Always include sources for your responses, listing the file name and URL from nyx_subscriptions
   ONLY where the queried tables match the table_name from the nyx_subscription.
7. Preserve all URLs in their original format, including query parameters.
8. Format your responses in markdown, using lists for clarity when appropriate.

Remember:
- Users may refer to nyx_subscription entries as "products", "data", "datasets", or similar terms.
- They may mention having access, being subscribed, or simply having products from Nyx.
- Never make any changes to the files (no INSERT, UPDATE, DELETE, DROP, etc.).
- Always provide thoughtful, accurate responses based on the available information.
- For Nyx subscription queries, always provide a complete list from nyx_subscriptions.
"""

DEFAULT_COHERE_MODEL = "command-r"
DEFAULT_OPENAI_MODEL = "gpt-4o-mini"


class NyxLangChain(NyxClient):
    """An opinionated client wrapping langChain to evaluate user queries against contents of a Nyx network.

    This class extends NyxClient to provide LangChain-based functionality for querying Nyx network contents.

    Note:
        The LLM must support tool calling.
    """

    def __init__(
        self,
        config: Optional[BaseNyxConfig] = None,
        env_file: Optional[str] = None,
        llm: Optional[BaseChatModel] = None,
        log_level: int = logging.WARN,
        system_prompt: str = SQL_SYSTEM_PROMPT,
    ):
        """Initialise a new langChain client.

        Args:
            config: Configuration for the Nyx client.
            env_file: Path to the environment file.
            llm: Language model to use.
            log_level: the logging level to use for nyx client, and langchain modules
            system_prompt: provide an override for the system prompt
        """
        super().__init__(env_file, config)
        logging.basicConfig(format="%(asctime)s %(levelname)s [%(module)s] %(message)s", level=log_level)

        # Disable langchain network requests log
        logging.getLogger("httpx").setLevel(log_level)
        logging.getLogger("httpcore").setLevel(log_level)

        self.log = logging.getLogger(__name__)
        self.log.setLevel(log_level)

        if llm:
            self.llm = llm
        else:
            if isinstance(self.config, CohereNyxConfig):
                self.llm = ChatCohere(model=DEFAULT_COHERE_MODEL, cohere_api_key=self.config.api_key)
            elif isinstance(self.config, OpenAINyxConfig):
                self.llm = ChatOpenAI(model=DEFAULT_OPENAI_MODEL, api_key=self.config.api_key)
            else:
                raise ValueError("No language model provided and no valid config found")

        self.system_message = SystemMessage(system_prompt)

    def query(
        self,
        prompt: str,
        data: Optional[list[Data]] = None,
        include_own: bool = False,
        sqlite_file: Optional[str] = None,
        update_subscribed: bool = True,
        k: int = 3,
    ) -> str:
        """Query the LLM with a user prompt and context from Nyx.

        This method takes a user prompt and invokes it against the LLM associated with this instance,
        using context from Nyx.

        Args:
            prompt (str): The user prompt.
            data (Optional[list[Data]], optional): List of products to use for context.
                If None, uses all subscribed data. Defaults to None.
            include_own (bool): Include your own data, created in Nyx, in the query.
            sqlite_file (Optional[str]): A file location to write the sql_lite file to.
            update_subscribed (bool): if set to true this will re-poll Nyx for subscribed data
            k (int): Max number of vector matches to include

        Returns:
            str: The answer from the LLM.

        Note:
            If the data list is not provided, this method updates subscriptions and retrieves all subscribed data.
        """
        if update_subscribed:
            self.update_subscriptions()
        if data is None:
            data = self.get_subscribed_data()
        if include_own:
            data.extend(self.get_data_for_creators(creators=[self.config.org]))
        self.log.debug("using products: %s", [d.title for d in data])

        parser = Parser()
        parser.data_as_vectors([d for d in data if d.content_type != "csv"], chunk_size=100)
        matching_vectors = parser.query(prompt, k)

        engine = Parser.data_as_db(data, matching_vectors.chunks, sqlite_file=sqlite_file, if_exists="replace")
        db = SQLDatabase(engine=engine)

        # Optionally provide extra context to the model system prompt
        table_context = {
            "tables": db.get_usable_table_names(),
            "schemas": db.get_table_info(),
        }

        toolkit = SQLDatabaseToolkit(db=db, llm=self.llm, dialect=db.dialect)
        agent_executor = create_react_agent(self.llm, toolkit.get_tools(), state_modifier=self.system_message)
        events = agent_executor.stream(
            {"messages": [("user", Utils.with_sources(prompt, **table_context))]},
            stream_mode="values",
        )

        last_content: str = ""
        for event in events:
            last_content = event["messages"][-1].content

        if sqlite_file:
            os.remove(sqlite_file)

        return last_content

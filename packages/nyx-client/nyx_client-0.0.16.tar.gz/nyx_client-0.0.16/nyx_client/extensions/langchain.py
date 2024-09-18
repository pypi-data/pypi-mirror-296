"""Optional module for tight integration between Nyx and LangChain."""

import logging
import os
from typing import Optional

from nyx_client.configuration import BaseNyxConfig, CohereNyxConfig, OpenAINyxConfig

try:
    from langchain_community.agent_toolkits import create_sql_agent
    from langchain_community.utilities import SQLDatabase
    from langchain_core.language_models import BaseChatModel
except ImportError as err:
    raise ImportError(
        "LangChain dependencies are not installed. "
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
    from langchain_cohere.sql_agent.agent import create_sql_agent as create_cohere_sql_agent
except ImportError:

    class ChatCohere:  # noqa: D101
        def __init__(self, *args, **kwargs):  # noqa: D107
            raise ImportError(
                "LangChain Cohere dependencies are not installed. "
                "Please install them with `pip install nyx_client[langchain-cohere]`"
            )


from langchain.agents.mrkl import prompt as react_prompt
from langchain_core.prompts import (
    ChatPromptTemplate,
    FewShotChatMessagePromptTemplate,
    PromptTemplate,
)

from nyx_client.client import NyxClient
from nyx_client.data import Data
from nyx_client.utils import Parser, Utils

EXAMPLES = [
    {
        "input": "List all the characters in Anna Karenina",
        "query": "SELECT DISTINCT characterNames FROM novels WHERE novelName = 'Anna Karenina'",
    },
]

SYSTEM_PREFIX = """
    You are an agent designed to interact with a SQL database.
    Given an input question, create a syntactically correct query to run, then look at the results of the query and 
    return the answer. Unless the user specifies a specific number of examples they wish to obtain.
    You can order the results by a relevant column to return the most interesting examples in the database.
    Never query for all the columns from a specific table, only ask for the relevant columns given the question.
    You have access to tools for interacting with the database.
    Only use the given tools. Only use the information returned by the tools to construct your final answer.
    You MUST double check your query before executing it. If you get an error while executing a query,
    rewrite the query and try again.

    DO NOT make any DML statements (INSERT, UPDATE, DELETE, DROP etc.) to the database.
    
    If the question does not seem related to the database, just return "I don't know" as the answer.
    
    For the following types of questions, ALWAYS respond with a list of entries from the nyx_subscriptions file:
      * What products am I subscribed to?
      * What products do I have?
      * What products are available?
      * What data do I have?
      * What data am I subscribed to?
      * What data is available to me in Nyx?
      * Any similar questions about Nyx subscriptions, products, or available data
    When responding to these queries:
      * List all entries from the nyx_subscriptions file
      * Include the name, description, and URL for each entry
      * Do not filter or limit the results for these specific queries
"""

BASIC_PREFIX = """
    Begin!

    Question: {input}
    Thought: I should look at the tables in the database to see what I can query.
    Then I should query the schema of the most relevant tables.
    {agent_scratchpad}

"""

EXAMPLE_PROMPT = ChatPromptTemplate.from_messages(
    messages=[
        ("human", "Hello, I am going to ask you a question now which you will need to answer using SQL."),
        ("ai", "OK, I will do my best to answer your question using SQL."),
        ("human", "{query}"),
    ]
)

FEW_SHOT_PROMPT = FewShotChatMessagePromptTemplate(
    examples=EXAMPLES,
    example_prompt=EXAMPLE_PROMPT,
    input_variables=["input", "agent_scratchpad"],
)

FORMAT_INSTRUCTIONS = (
    f"{react_prompt.FORMAT_INSTRUCTIONS}\n "
    f"Here are some examples of user inputs and "
    f"their corresponding SQL queries:\n"
)

TEMPLATE = "\n\n".join([SYSTEM_PREFIX, FORMAT_INSTRUCTIONS, FEW_SHOT_PROMPT.format(), BASIC_PREFIX])

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
        system_prompt: Optional[str] = None,
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

        self.verbose = False
        if log_level <= logging.DEBUG:
            self.verbose = True
        self.create_agent_func = create_sql_agent

        if llm:
            self.llm = llm
            if isinstance(self.llm, ChatCohere):
                self.create_agent_func = create_cohere_sql_agent
        else:
            if isinstance(self.config, CohereNyxConfig):
                self.llm = ChatCohere(model=DEFAULT_COHERE_MODEL, cohere_api_key=self.config.api_key)
                self.create_agent_func = create_cohere_sql_agent
            elif isinstance(self.config, OpenAINyxConfig):
                self.llm = ChatOpenAI(model=DEFAULT_OPENAI_MODEL, api_key=self.config.api_key)
            else:
                raise ValueError("No language model provided and no valid config found")

        self.template = "\n\n".join([system_prompt if system_prompt else "", TEMPLATE])
        self.prompt = PromptTemplate.from_template(template=self.template)

    def query(
        self,
        query: str,
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
            query (str): The user input.
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
        matching_vectors = parser.query(query, k)

        engine = Parser.data_as_db(data, matching_vectors.chunks, sqlite_file=sqlite_file, if_exists="replace")
        db = SQLDatabase(engine=engine)
        agent_executor = self.create_agent_func(self.llm, db=db, agent_type="tool-calling", verbose=self.verbose)

        res = agent_executor.invoke(
            {
                "input": self.prompt.format(
                    input=Utils.with_sources(query), agent_scratchpad="", tool_names=agent_executor.tools
                )
            }
        )

        if sqlite_file:
            os.remove(sqlite_file)

        return res["output"]

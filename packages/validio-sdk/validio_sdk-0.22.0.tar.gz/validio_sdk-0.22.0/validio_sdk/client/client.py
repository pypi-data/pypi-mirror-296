"""A client used to send GraphQL requests with sensible defaults for Validio."""

from typing import Any

from gql import Client as GqlClient
from gql import gql
from gql.transport.aiohttp import AIOHTTPTransport

import validio_sdk.metadata
from validio_sdk.config import Config, ValidioConfig

USER_AGENT = f"validio-sdk@{validio_sdk.metadata.version()}"


class Client:
    """A GraphQL client with sensible defaults for Validio.

    It will be created by reading the Validio configuration just like the CLI
    tool and ensure the correct headers are passed.

    If no `ValidioConfig` is passed when constructing the client, it will
    fallback to first look for required environment variables:
        - `VALIDIO_ENDPOINT`
        - `VALIDIO_ACCESS_KEY`
        - `VALIDIO_CONFIG_PATH`
    If not all of them are found, it will look for a configuration file. It will
    first look in the path set in `VALIDIO_CONFIG_PATH` and if that one is empty
    it will look in the default OS dependant system directory.
    """

    def __init__(
        self,
        config: ValidioConfig | None = None,
        user_agent: str = USER_AGENT,
        headers: dict[str, str] = {},
    ):
        """Constructor.

        :param config: Optional `ValidioConfig` to use to set config.
        :param user_agent: The `User-Agent` header to use for the requests
        :param headers: Additional headers to set.
        :returns: A client that can execute GraphQL operations
        """
        if config is None:
            config = Config().read()

        headers = {
            "User-Agent": user_agent,
            "Authorization": f"{config.access_key}:{config._access_secret}",
            **headers,
        }
        api_url = f"{config.endpoint.rstrip('/')}/api"
        transport = AIOHTTPTransport(url=api_url, headers=headers)

        self.client = GqlClient(transport=transport, fetch_schema_from_transport=True)

    def execute(
        self,
        query: str,
        variable_values: dict[str, Any] | None = None,
    ) -> Any:
        """Execute a GraphQL request.

        :param query: The query to be executed
        :variable_values: Variable values if the query contains such
        :returns: The API response
        """
        graphql_query = gql(query)
        return self.client.execute(graphql_query, variable_values=variable_values)

    async def execute_async(
        self,
        query: str,
        variable_values: dict[str, Any] | None = None,
    ) -> Any:
        """Execute a GraphQL request async.

        :param query: The query to be executed
        :variable_values: Variable values if the query contains such
        :returns: The API response
        """
        graphql_query = gql(query)
        return await self.client.execute_async(
            graphql_query, variable_values=variable_values
        )

# AlphaSense API SDK

## Installation

Before installing; you should create the virtual environment

```bash
pip install alphasense-api-sdk
```

or specify the version

```bash
pip install alphasense-api-sdk==0.1.0
```

Or adding the `alphasense-api-sdk` to the `pyproject.toml` file

```toml
dependencies = [
  "alphasense-api-sdk==0.1.0"
]
```

or `requirements.txt` file

```txt
alphasense-api-sdk==0.1.0
```

## Usage

- Create `pyproject.toml` file
- Add the following to the `pyproject.toml` file

```toml
[alphasense.auth]
username = "<your username>"
password = "<your password>"
api_key = "<your api key>"
client_id = "<your client id>"
client_secret = "<your client secret>"
```

- Writing the code to fetch the watchlists with raw GraphQL query

```python
from alphasense_api_sdk.client import Client, GraphQLField

async def main():
    client = Client()
    w = await client.query(
        GraphQLField("user { watchlists { id name }}"), operation_name="user_watchlists"
    )
    print("Watchlists: ", w)


if __name__ == "__main__":
    import asyncio

    asyncio.run(main())
```

- Or using the `Query` object to search for documents

```python
from alphasense_api_sdk.client import Client, GraphQLField
from alphasense_api_sdk.custom_queries import Query, SearchResponseFields


async def main():
    client = Client()
    df = SearchResponseFields.documents()
    search_query = Query.search(limit=5).fields(
        SearchResponseFields.documents().fields(
            df.id,
            df.title,
            df.released_at,
            GraphQLField("type { ids }"),
        )
    )
    docs = await client.query(search_query, operation_name="searchDocs")
    print("> docs: ", docs)


if __name__ == "__main__":
    import asyncio

    asyncio.run(main())

```

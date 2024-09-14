import aiohttp

class Sumarizer:
    def __init__(self, url: str, verbose: bool = False):
        self.url = url
        self.verbose = verbose
        self.session = None

    async def __aenter__(self):
        """Async context manager."""
        # Create a new session when entering the context manager.
        self.session = aiohttp.ClientSession()
        return self

    async def __aexit__(self, exc_type, exc, tb):
        """Async context manager."""
        # Close the session when exiting the context manager.
        await self.session.close()

    async def fetch(self, url: str) -> str:
        async with self.session.get(url) as response:
            return await response.text()

    async def request_llm(self):
        """Request the LLM page."""
        if self.verbose:
            print("Requesting the LLM page...")
        payload = {
            "message": "get_llm",
        }
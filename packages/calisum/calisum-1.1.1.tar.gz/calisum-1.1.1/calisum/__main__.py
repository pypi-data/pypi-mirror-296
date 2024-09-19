""" calisum.__main__: executed when calisum directory is called as script. """
import asyncio
from calisum.cli import main

if __name__ == "__main__":
    asyncio.run(main())
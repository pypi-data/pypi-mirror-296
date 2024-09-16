
<h1 align="center">apininjas.py</h1>
<p align="center">An easy-to-use and async-ready Python wrapper for the API-Ninjas APIs.</p>

<p align="center">
    <a href="https://pypi.org/project/apininjas.py/"><img alt="PyPi version" src="https://img.shields.io/pypi/v/apininjas.py?style=flat-square&color=016dad"></a>
    <a href="https://pypi.org/project/apininjas.py/"><img alt="Python version" src="https://img.shields.io/pypi/pyversions/apininjas.py?style=flat-square&color=016dad"></a>
    <a href="https://github.com/Puncher1/apininjas.py/blob/main/LICENSE"><img alt="License" src="https://img.shields.io/github/license/puncher1/apininjas.py?style=flat-square"></a>
</p>

## Key Features

* Pythonic and modern API
* Asynchronous using `async` and `await`
* Fully type-hinted
* Easy to use with an object oriented design


## Installing

**Python 3.9 or higher is required**

To install the latest stable version, use
```cmd
pip install -U apininjas.py
```

To install the development version (**may be unstable**), use
```cmd
pip install -U git+https://github.com/puncher1/apininjas.py
```


## Example

```python
import asyncio
from apininjas import Client

async def main():
    client = Client("api_key")

    stock = await client.fetch_stock("AAPL")
    print(f"{stock.name} is trading at ${stock.price}")

    await client.close()

if __name__ == "__main__":
    asyncio.run(main())
```
### Example with Context Manager
Or use the context manager, which automatically cleans up.
```python
import asyncio
from apininjas import Client

async def main():
    async with Client("api_key") as client:
        stock = await client.fetch_stock("AAPL")
        print(f"{stock.name} is trading at ${stock.price}")

if __name__ == "__main__":
    asyncio.run(main())
```


## Links
* [Documentation][1] <br>
* [API-Ninjas][2]


[1]: https://apininjaspy.rtfd.org/latest
[2]: https://api-ninjas.com

import aiohttp,asyncio

async def aioioio():
    async with aiohttp.ClientSession() as ses:
        url = 'http://siamchart.com/stock-chart/itd'
        async with ses.get(url) as r:
            print('url: ',r.url)
            print('status: ', r.status)
            print('charset: ', r.charset)

asyncio. run(aioioio())
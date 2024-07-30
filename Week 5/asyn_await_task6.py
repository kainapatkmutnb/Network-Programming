import asyncio, time

async def ioioio(wela, chue_ngan):
    print('Start%s Time has passed %.6f Second'%(chue_ngan,time.time()-t0))
    await asyncio.sleep(wela)
    print('%sDone Time has passed %.6f Second'%(chue_ngan,time.time()-t0))

async def main():
    cococoru = [ioioio (1.5, 'Downloading Music'), ioioio(2.5, 'Downloading Anime'), ioioio(0.5, 'Downloading Movie'), ioioio (2, 'Downloading Game')]
    await asyncio.wait(cococoru)

t0 = time.time()
asyncio.run(main())



#async def download_item(duration, name):
#    """Downloads an item asynchronously with a specified duration."""
#    print(f'Start: {name} (Time elapsed: {time.time() - t0:.6f} seconds)')
#    await asyncio.sleep(duration)
#    print(f'Done: {name} (Time elapsed: {time.time() - t0:.6f} seconds)')

#async def main():
#    """Downloads various items concurrently using asyncio."""
#    tasks = [
#        download_item(1.5, 'Downloading Music'),
#        download_item(2.5, 'Downloading Anime'),
#       download_item(0.5, 'Downloading Movie'),
#        download_item(2, 'Downloading Game')
#    ]
#    await asyncio.gather(*tasks)  # Use asyncio.gather for efficient waiting

#t0 = time.time()
#asyncio.run(main())

import aiohttp
import asyncio
import aiofiles
import os

last_page = None
arr_err = []

async def img(name_dir, url_img):
    global arr_err
    dir = name_dir
    async with aiohttp.ClientSession() as session:
        url = url_img
        try:
            async with session.get(url) as resp:
                if resp.status == 200:
                    f = await aiofiles.open(str(os.path.dirname(__file__))+'/image/'+dir+'/'+url.split('/')[-1], mode='wb')
                    await f.write(await resp.read())
                    await f.close()
                else:
                    arr_err.append(url)
        except Exception as ex:
            pass


async def get_url_data(name_dir, urls):
    tasks = []
    for i in range(len(urls)):
        tasks.append(asyncio.create_task(img(name_dir, urls[i])))
    return await asyncio.gather(*tasks)


def start_parse(name_dir, urls):
    global last_page
    dir = name_dir
    loop = asyncio.get_event_loop()
    loop.run_until_complete(get_url_data(dir, urls))


def parse_image(name_dir, download_err=False, parse_error=[]):
    dir = name_dir
    path = str(os.path.dirname(__file__))
    try:
        os.makedirs(path+'/image/'+dir)
        print("Папка создана:", path+'/image/'+dir)
    except Exception:
        print("Папка существует:", path+'/image/'+dir)
    
    if download_err == False:
        urls = open(path+'/text/'+dir+'.txt', 'r').read().split('\n')
        start_parse(dir, urls)
    
    elif len(parse_error) >= 1:
        urls = parse_error.copy()
        global arr_err
        arr_err = []
        start_parse(dir, urls)
    else:
        pass



def main(dir):
    global arr_err
    print('Начинаю работу с проектом ' + dir)
    parse_image(name_dir=dir)
    j = 0
    print('Всего ошибочных:', len(arr_err))
    while len(arr_err) >= 1 and j < 5:
        print('Попытка скачать нужные файлы:', j)
        parse_image(name_dir=dir, download_err=True, parse_error=arr_err)
        j += 1
    print('Скачалось всё')
    print(arr_err)


if __name__ == "__main__":
    dirs = [
        'test'
    ]
    for dir in dirs:
        main(dir)

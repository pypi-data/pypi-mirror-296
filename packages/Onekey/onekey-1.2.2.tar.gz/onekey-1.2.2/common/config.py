import os
import sys
import asyncio
import ujson as json
import aiofiles

from .stack_error import stack_error
from .log import log


async def gen_config_file():
    qa1 = "温馨提示：Github_Personal_Token可在Github设置的最底下开发者选项找到，详情看教程"
    tutorial = "https://ikunshare.com/Onekey_tutorial"
    default_config ={
                    "Github_Personal_Token": "",
                    "Custom_Steam_Path": "",
                    "QA1": qa1,
                    "教程": tutorial
                    }
    async with aiofiles.open("./config.json",
                             mode="w",
                             encoding="utf-8") as f:
        await f.write(json.dumps(default_config,
                                 indent=2,
                                 ensure_ascii=False,
                                 escape_forward_slashes=False))
        await f.close()
    log.info(' 🖱️ 程序可能为第一次启动，请填写配置文件后重新启动程序')


async def load_config():
    if not os.path.exists('./config.json'):
        await gen_config_file()
        os.system('pause')
        sys.exit()
    else:
        try:
            async with aiofiles.open("./config.json",
                                     mode="r",
                                     encoding="utf-8") as f:
                config = json.loads(await f.read())
                return config
        except Exception as e:
            log.error(f"配置文件加载失败，原因: {stack_error(e)}")
            os.remove("./config.json")
            os.system('pause')

        
config = asyncio.run(load_config())

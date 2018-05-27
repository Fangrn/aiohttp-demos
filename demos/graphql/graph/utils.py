import pathlib
import argparse

from aiohttp import web
from trafaret_config import commandline
import trafaret


PATH = pathlib.Path(__file__).parent.parent
DEFAULT_CONFIG_PATH = PATH / 'config' / 'api.yml'


CONFIG_TRAFARET = trafaret.Dict({
    trafaret.Key('postgres'):
        trafaret.Dict({
            'user': trafaret.String(),
            'password': trafaret.String(),
            'database': trafaret.String(),
            'host': trafaret.String(),
            'port': trafaret.Int(),
        }),
    trafaret.Key('redis'):
        trafaret.Dict({
            'port': trafaret.Int(),
        }),
    trafaret.Key('app'):
        trafaret.Dict({
            'host': trafaret.IP,
            'port': trafaret.Int(),
        }),
})


def get_config() -> dict:
    ap = argparse.ArgumentParser()
    commandline.standard_argparse_options(
        ap,
        default_config=DEFAULT_CONFIG_PATH,
    )
    options = ap.parse_args()

    return commandline.config_from_options(options, CONFIG_TRAFARET)


def init_config(app: web.Application) -> None:
    app['config'] = get_config()

"""客户端代码生成"""

import json
import logging
from pathlib import Path

from mtmai.mtlibs import mtutils
from mtmlib.mtutils import bash


def register_gen_commands(cli):
    logger = logging.getLogger()

    @cli.command()
    def gen():
        from mtmai.cli.serve import app
        from mtmai.core.config import settings

        openapi = app.openapi()
        with Path(settings.OPENAPI_JSON_PATH).open("w") as f:
            logger.info(
                "openapi.json exported %s to %s",
                openapi.get("openapi", "unknown version"),
                settings.OPENAPI_JSON_PATH,
            )
            json.dump(openapi, f, indent=2)
        # dev_helper.gen()
        if not mtutils.command_exists("openapi-python-client"):
            bash(
                "pip install openapi-python-client && openapi-python-client --install-completion"
            )
        bash(
            "openapi-python-client generate --path mtmai/mtmai/openapi.json --overwrite"
        )

        # typescript 客户端库
        bash("cd packages/mtmaiapi && bun run gen")

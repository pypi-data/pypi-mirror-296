"""
# Welcome to Lynq
### This documentation including its installation guide may only be applicable to Lynq 9(.6)

**Documentation for Lynq**

Lynq is a Python-based framework designed to simplify the development and management of web applications. It provides a set of tools and utilities to streamline the development process, enhance security, and improve performance.

**Installation**

To install Lynq, you can use either pip or git.

Using pip:
```
pip install lynq
```

Using git:
```
git clone https://github.com/elemenom/lynq.git
```

**Upgrade**

To upgrade Lynq, you can use either pip or git.

Using pip:
```
pip install lynq --upgrade
```

Using git:
```
rm -rf lynq; git clone https://github.com/elemenom/lynq.git
```

**Links**

- PyPI: https://pypi.org/project/lynq/
- GitHub: https://github.com/elemenom/lynq/

**Author**

- Name: Elekk aka Elemenom
- User: elemenom
- Mail: pixilreal@gmail.com
- GitHub: https://github.com/elemenom/
- PyPI: https://pypi.org/user/elemenom/

**Command-Line Interface (CLI) Usage**

Lynq provides a command-line interface (CLI) to perform various tasks such as running the application, cleaning pycache files, and running processes directly from the CLI.

To use the CLI, you can run the following commands:

- Run the application with GUI:
```
python -m lynq --lq.rungui
```

- Clean pycache files:
```
python -m lynq --lq.clean
```

- Run a process directly from the CLI:
```
python -m lynq --lq.run_process "<process_command>"
```

**Lynq Configuration**

Lynq supports different types of configuration files, such as JSON, BASIN, and PYTHON. You can specify the configuration file and type using command-line arguments.

To use a JSON configuration file:
```
python myproject.py --lq.cfile "path_to_config_file.json" --lq.ctype "JSON"
```

To use a BASIN configuration file:
```
python myproject.py --lq.cfile "path_to_config_file.basin" --lq.ctype "BASIN"
```

To use a PYTHON configuration file:
```
python myproject.py lq.cfile "" --lq.ctype "PYTHON"
```

(i) The `lq.cfile` argument is ignored and can be blank when PYTHON is used as `lq.ctype`.

**Lynq Error Handling**

Lynq offers a total of 4 modes you can use to handle errors:
- 'disable' (errors will not show and lynq will try to recover as best as it can)
- 'legacy' (python's default error handling)
- 'external (uses lynq's modern external window handling)
- 'default' (default option when the argument isn't provided, provides a user-friendly error handling experience)

To select a handling type,

We recommend using the 'default' option.

**Lynq Components**

Lynq consists of several components that provide various functionalities. Some of the key components are:

- `launch`: A module for launching web applications.
- `directlaunch`: A module for launching web applications directly without having to explicitly define a `Server`.
- `app`: An app decorator for managing web application objects.
- `jsonapp`: An app decorator for managing web application objects using JSON.
- `basinapp`: An app decorator for managing web application objects using BASIN.
- `InternetExplorerInstance`: A class for managing Internet Explorer instances.
- `Server`: A class for managing standard Lynq servers.
- `ConfigurableServer`: A class for managing customizable Lynq servers.
- `JsonServer`: A class for managing Lynq servers using JSON.
- `BasinServer`: A class for managing Lynq servers using BASIN.
- `App`: A class for representing web application objects.
- `ExportedApp`: A class for representing exported web application objects.

**Important Note**

Please note that the `backendutils` directory is not intended to be accessed directly. It contains internal utilities and modules used by Lynq. Any code within this directory should not be modified or accessed directly.

This file is part of VexilPy (elemenom/vexilpy).

VexilPy is free software: you can redistribute it and/or modify
it under the terms of the GNU General Public License as published by
the Free Software Foundation, either version 3 of the License, or
(at your option) any later version.

VexilPy is distributed in the hope that it will be useful,
but WITHOUT ANY WARRANTY; without even the implied warranty of
MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE. See the
GNU General Public License for more details.

You should have received a copy of the GNU General Public License
along with VexilPy. If not, see <https://www.gnu.org/licenses/>.
"""

import atexit, os, argparse, logging, inspect

from typing import Final

from .backendutils.vexilpy.pycache_remover import remove_pycache_from as _remove_pycache_from

from .backendutils.basin.getval import getval
from .backendutils.basin.object import BasinObject

from .backendutils.safety.logger import init_logger
from .backendutils.yaml.loader import load_yaml_config
from .backendutils.yaml.validator import validate_config

SYSVER: Final[float] = 11.1

run: bool = True

verbose: bool = False

print(f"Running from '{inspect.stack()[-1].filename}'")

# Checking if pypi_upload_setup.py is running this:
if "pypi_upload_setup.py" in inspect.stack()[-1].filename:
    run = False

# UPDATE RELEASE FOR PYPI (PIP)
# PWSH ONLY
# ```
# python -m vexilpy --Clean
# git commit --all
# git push
# rm dist build vexilpy.egg-info
# python pypi_upload_setup.py sdist bdist_wheel
# twine upload dist/*
# rm dist build vexilpy.egg-info
# ```

class LowercaseFormatter(logging.Formatter):
    def format(self, record):
        result = super().format(record)
        return result.lower()

def main() -> None:
    parser: argparse.ArgumentParser = argparse.ArgumentParser(description="Basic config")

    parser.add_argument("-F", "--File", type=str, help="Path to your vexilconfig.yaml file.")

    parser.add_argument("--Rungui", action="store_true", help="Start a new instance of VexilPy RUNGUI and exit the program.")
    parser.add_argument("--Clean", action="store_true", help="Clean pycache files and exit the program.")

    parser.add_argument("--Verbose", action="store_true", help="Disable VexilPy's error handling (only recommended for debugging purposes).")

    parser.add_argument("--Run-Process", type=str, help="Run a process like from a VexilPy RUNGUI, but presented directly from a CLI.")

    args, _ = parser.parse_known_args()

    vexilconfig = args.File or "vexilconfig.yaml"

    if not os.path.exists(vexilconfig):
        print("WARNING | No vexilconfig.yaml file found. Creating a new one.")

        with open(vexilconfig, "w") as file:
            file.write(
"""logger:
loggingConfig:
loggingLevel:
loggingFormat:

cleanLogger:
cleanPycache:
cleanLogFile:"""
            )

    data = load_yaml_config(vexilconfig)

    logger_ = data.get("logger")
    additional = data.get("loggingConfig")
    level = data.get("loggingLevel")
    format_ = data.get("loggingFormat")

    cleanlogger = data.get("cleanLogger")
    clean = data.get("cleanPycache")
    cleanlogfile = data.get("cleanLogFile")

    PYCACHE_REMOVAL_LOCATIONS: tuple[str, ...] = (
        "",
        *[
            f"backendutils.{d}" for d in os.listdir("./vexilpy/backendutils") if os.path.isdir(os.path.join("./vexilpy/backendutils", d))
        ],
        *[
            f"backendutils.stock.{d}" for d in os.listdir("./vexilpy/backendutils/stock") if os.path.isdir(os.path.join("./vexilpy/backendutils/stock", d))
        ]
    )

    global verbose

    verbose = args.Verbose or False

    format_ = format_ or "%(levelname)s: %(message)s"

    logging.basicConfig(
        level = eval(f"logging.{level}") if level else logging.DEBUG,
        format = format_,
        **additional or {}
    )

    formatter = LowercaseFormatter(format_)
    for handler in logging.root.handlers:
        handler.setFormatter(formatter)

    init_logger(logger_ or logging.getLogger(__name__))

    from .backendutils.safety.logger import logger

    CLEAN_CACHE: bool = clean or False
    CLEAN_LOGGER: bool = cleanlogger or True

    logger().info(f"Started instance of VexilPy {SYSVER}.")

    if args.Rungui:
        from .backendutils.vexilpy.rungui import run_gui

        run_gui("<onstart rungui>")

        exit()

    if args.Clean:
        for path in PYCACHE_REMOVAL_LOCATIONS:
            _remove_pycache_from(f"./vexilpy/{path.replace(".", "/")}")

        exit()

    if args.Run_Process:
        from .backendutils.vexilpy.rungui import run_process

        run_process(args.Run_Process, logger, "<terminal Run-Process instance>")

        exit()

    def _clean_up() -> None:
        logging.shutdown()

        if os.path.exists("throwaway.log") and cleanlogfile:
            try:
                os.remove("throwaway.log")

            except PermissionError:
                logger().error("Failed to delete throwaway.log file.\n"
                               "This could be because it's being used by another program."
                )

    def _clean_up_cache() -> None:
        logger().debug("Commencing pycache clean up process.")

        for path_ in PYCACHE_REMOVAL_LOCATIONS:
            _remove_pycache_from(f"./vexilpy/{path_.replace(".", "/")}")

    def _at_exit_func() -> None:

        logger().debug("Commencing logger deletion and clean up process.")

        if CLEAN_CACHE:
            _clean_up_cache()

        if CLEAN_LOGGER:
            _clean_up()

        print(f"[Exiting...] Program ended successfully. All active servers terminated.")

    atexit.register(_at_exit_func)

if run:
    main()

from .backendutils.launcher.launch import launch
from .backendutils.launcher.direct import directlaunch
from .backendutils.app.app import app, WebApp
from .backendutils.app.jsonapp import jsonapp, JsonWebApp
from .backendutils.app.basinapp import basinapp, BasinWebApp
from .backendutils.vexilpy.msie import InternetExplorerInstance
from .backendutils.server.standard import Server
from .backendutils.server.custom import ConfigurableServer
from .backendutils.server.json import JsonServer
from .backendutils.server.basin import BasinServer
from .backendutils.app.appobject import AppObject as SelfApp
from .backendutils.app.standardappexportobject import StandardAppExportObject as ExportedApp
from .backendutils.script.ctrl import CTRLScript
from .backendutils.server.yaml import YamlServer
from .backendutils.app.yamlapp import yamlapp, YamlWebApp
from .backendutils.app.remoteapp import rmtapp, RemoteWebApp
from .backendutils.style.inclusion import InclusionMap, SafeInclusionMap
from .backendutils.style.style import StyledAppAttachment as Style
from .backendutils.style.attribute import StyleAttribute as Selector
from .backendutils.vexilpy.importer import stock_import, batch_import

import logging
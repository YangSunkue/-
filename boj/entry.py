import traceback

from boj import args_resolver
from boj.containers import Container
from boj.core import constant
from boj.core.error import BojError
from boj.core.console import BojConsole
from boj.core.fs.util import mkdir


def cli():
    parser = args_resolver.create_parser()
    args = parser.parse_args()

    if args.command is None:
        parser.print_help()
        exit(0)

    console = BojConsole()
    try:
        container = Container()
        dispatcher = container.dispatcher_factory()

        mkdir(constant.boj_cli_path(), True)  # 여기서 세션 저장 디렉터리 만드는 것 같다 (.boj-cli)
        # username 경로를 추가해야 하는데 어디서..?????
        # -> login/command.py 에서 추가했다

        dispatcher.modules[args.command].execute(args)
    except BojError as e:
        SystemExit(e)
        console.log(str(e))
        # print(str(e))
        exit(1)
    except BaseException as e:
        console.log(e.args)
        traceback.print_exc()
        exit(1)

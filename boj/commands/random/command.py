import dataclasses
import random
import webbrowser

from rich.console import Console

import boj.core.crypto
import boj.core.constant
from boj.core import constant
from boj.core.command import Command

from boj.core import http
from boj.core.error import IllegalStatementError, FatalError
from boj.web.solved_ac_search_api import (
    SolvedAcSearchApiRequest,
    make_solved_ac_search_api_params,
)
from boj.core.fs.repository import Repository
from boj.core.http import JsonResponse
from boj.data.credential import Credential


@dataclasses.dataclass
class RandomCommand(Command):
    console: Console
    credential_repository: Repository[Credential]

    # 특정 문제 검색 후 열기
    def execute(self, args):
        with self.console.status("Reading credential...") as status:
            #############
            credential = self.credential_repository.find(cwd=constant.boj_cli_path())  # 여기서 세션 가져온다
            #
            ### 현재 사용자가 누구인지 확인 후 해당하는 credential을 가져와야 하는데 어떻게 하지???###
            ## 근데 이거 random/command.py 인데 필요한 부분인가?


            status.update("Calling solved.ac API...")
            response = JsonResponse(
                http.get(
                    SolvedAcSearchApiRequest(
                        params=make_solved_ac_search_api_params(
                            tags=args.tags,
                            lang="ko",
                            tier=args.tier,
                            user=credential.username,
                        )
                    )
                )
            )

            json = response.json
            if not json or ("items" not in json):
                raise FatalError("error while calling solve.ac API.")

            if len(json["items"]) == 0:
                raise FatalError("no matching problem found.")

            items = json["items"]
            selected_tag = None
            if args.tags:
                selected_tag = random.choice(args.tags)

            for item in items:
                for tag in item["tags"]:
                    if not selected_tag or (tag["key"] == selected_tag):
                        selected_item = item
                        break

            status.update("Opening in browser...")
            webbrowser.open(
                boj.core.constant.boj_problem_url(selected_item["problemId"])
            )

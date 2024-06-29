import dataclasses
import os

from rich.console import Console

from boj.browsers.login_browser import LoginBrowser
from boj.core.error import FatalError
from boj.core.fs.file_object import FileMetadata
from boj.core.fs.repository import Repository, ReadOnlyRepository
from boj.data.config import Config
from boj.data.credential import Credential
from boj.core import constant
from boj.core.command import Command
## 추가
from boj.core.fs.util import mkdir
from boj.core.fs.util import file_exists
## 추가


@dataclasses.dataclass
class LoginCommand(Command):
    console: Console
    config_repository: ReadOnlyRepository[Config]
    credential_repository: Repository[Credential]

    def execute(self, args):
        config = self.config_repository.find()
        if not config.general.selenium_browser:
            raise FatalError("invalid value for 'config.general.login_browser'")

        with self.console.status("Preparing login browser...") as status:
            browser = LoginBrowser(
                constant.boj_login_url(),
                config.general.selenium_browser,
            )

            browser.open()
            credential_dict = browser.wait_for_login()  # 여기서 credential 정보 뽑아왔음( token, username 있음 )
            browser.close()

            status.update("Encrypting the credential...")


            #### ~/.boj_cli 하위에 username 디렉터리가 없을 경우 추가하기
            if not file_exists(constant.boj_cli_path_username(credential_dict["username"])):
                mkdir(constant.boj_cli_path_username(credential_dict["username"]), True)                
            ####

            credential = Credential(
                metadata=FileMetadata.of(
                    os.path.join(constant.boj_cli_path_username(credential_dict["username"]), "credential")  # username 안에 credential 저장
                ),
                username=credential_dict["username"],
                token=credential_dict["token"],
            )

            status.update("Writing to file...")
            self.credential_repository.save(credential)

        self.console.print("[green]Successfully logged in")


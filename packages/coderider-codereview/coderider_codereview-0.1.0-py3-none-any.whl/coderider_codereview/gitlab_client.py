import gitlab

from coderider_codereview import configs


class GitlabClient:
    def __init__(self):
        self._mr = None
        self._project = None
        self._latest_version = None
        self._code_diffs = None

        self._project_path = configs.CR_MR_PROJECT_PATH
        self._mr_iid = configs.CR_MR_IID
        self._gitlab_host = configs.CR_GITLAB_HOST
        self._bot_token = configs.CR_AI_BOT_TOKEN

        self._client = gitlab.Gitlab(url=self._gitlab_host, private_token=self._bot_token, per_page=100)
        if configs.CR_DEBUG:
            self._client.enable_debug()

    def project(self):
        if not self._project:
            self._project = self._client.projects.get(self._project_path)

        return self._project

    def mr(self):
        if not self._mr:
            mr_iid = configs.CR_MR_IID
            self._mr = self.project().mergerequests.get(mr_iid)

        return self._mr

    def latest_version(self):
        if not self._latest_version:
            versions = self.mr().diffs.list(order_by='id', sort='desc', page=1, per_page=1)
            self._latest_version = versions[0]

        return self._latest_version

    def mr_code_diffs(self):
        if not self._code_diffs:
            latest_version = self.latest_version()
            self._code_diffs = self.mr().diffs.get(latest_version.id, unidiff="true")

        return self._code_diffs

    def create_note(self, content):
        resp = self.mr().notes.create({'body': content})
        return resp


if __name__ == '__main__':
    client = GitlabClient()
    mr_code_diffs = client.mr_code_diffs()
    print("end")

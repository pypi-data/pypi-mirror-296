import gitlab

from coderider_codereview import configs


class GitlabClient:
    HIDDEN_TAG_AI_BOT = "<!-- ai-bot -->"

    def __init__(self):
        self._ai_bot_user = None
        self._mr = None
        self._project = None
        self._latest_version = None
        self._code_diffs = None
        self._discussions = None
        self._ai_bot_discussions = None

        self._project_path = configs.CR_MR_PROJECT_PATH
        self._mr_iid = configs.CR_MR_IID
        self._gitlab_host = configs.CR_GITLAB_HOST
        self._bot_token = configs.CR_AI_BOT_TOKEN

        self._client = gitlab.Gitlab(url=self._gitlab_host, private_token=self._bot_token, per_page=100)
        if configs.CR_DEBUG:
            self._client.enable_debug()

    def ai_bot_user(self):
        if not self._ai_bot_user:
            self._client.auth()
            self._ai_bot_user = self._client.user

        return self._ai_bot_user

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

    def create_discussion(self, content):
        resp = self.mr().discussions.create({'body': content})
        return resp

    def discussions(self):
        if not self._discussions:
            self._discussions = self.mr().discussions.list(all=True)

        return self._discussions

    def _is_ai_bot_discussion(self, discussion, tag: str = HIDDEN_TAG_AI_BOT) -> bool:
        try:
            note = discussion.attributes["notes"][0]
            author = note["author"]
            content = note["body"]

            if author["id"] != self.ai_bot_user().id:
                return False

            tag_filter = True if tag is None else content.startswith(tag)
            return tag_filter

        except Exception as e:
            if configs.CR_DEBUG: print(e)
            return False

    def ai_bot_discussions(self, tag: str = HIDDEN_TAG_AI_BOT):
        all_discussions = self.discussions()
        discussions = list(filter(
            lambda d: self._is_ai_bot_discussion(d, tag), all_discussions
        ))

        return discussions

    def edit_or_create_ai_bot_comment(self, content):
        ai_bot_discussions = self.ai_bot_discussions()

        try:
            # edit
            discussion = ai_bot_discussions[0]
            note_id = discussion.attributes["notes"][0]["id"]
            _updated_note = discussion.notes.update(note_id, {'body': content})
            if configs.CR_DEBUG: print(f"Edit the discussion: {discussion.id}")
            updated_discussion = self.mr().discussions.get(discussion.id)
            return updated_discussion
        except IndexError:
            # create
            new_discussion = self.create_discussion(content)
            if configs.CR_DEBUG: print(f"Create new discussion: {new_discussion.id}")
            return new_discussion


if __name__ == '__main__':
    client = GitlabClient()
    res = client.ai_bot_discussions()
    print("end")

import time

from coderider_codereview import configs
from coderider_codereview.coderider_client import CoderiderClient
from coderider_codereview.exceptions import ConfigError
from coderider_codereview.gitlab_client import GitlabClient
from coderider_codereview.litellm_client import LitellmClient
from coderider_codereview.prompt import Prompt


def main():
    try:
        messages = Prompt().all_messages()

        if configs.CR_LLM_MODEL.startswith("coderider/"):
            client = CoderiderClient().login()
        else:
            client = LitellmClient()

        llm_resp = client.chat_completions(messages)
        llm_content = llm_resp["choices"][0]["message"]["content"]
        content = f"{GitlabClient.HIDDEN_TAG_AI_BOT}\n\n{llm_content}"
        if configs.CR_DEBUG: print(content)

        GitlabClient().edit_or_create_ai_bot_comment(content)

    except ConfigError as e:
        print(e)
        exit(1)


if __name__ == '__main__':
    start_at = time.time()
    main()
    delta = time.time() - start_at
    if configs.CR_DEBUG:
        print(f"Time consuming: {delta:.3f} s")

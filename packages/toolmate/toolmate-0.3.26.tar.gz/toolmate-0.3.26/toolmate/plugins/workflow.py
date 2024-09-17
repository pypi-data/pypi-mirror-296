from toolmate import config
from pathlib import Path
import os

workflowDir = os.path.join(config.localStorage, "workflows")

Path(workflowDir).mkdir(parents=True, exist_ok=True)

workflows = {i: None for i in os.listdir(workflowDir) if os.path.isfile(i) and not i.startswith(".")}

config.inputSuggestions.append({"@workflow": workflows if workflows else None})
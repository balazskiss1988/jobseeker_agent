import openai
import memory
from utils import getJobs

from prompts import (
    ACTION_PROMPT,
    PREFIX,
    TASK_PROMPT
)

MODEL = "gpt-3.5-turbo"  # "gpt-4"
openai.api_key = ""

def parse_action(string: str):
    assert string.startswith("action:")
    idx = string.find("action_input=")
    if idx == -1:
        return string[8:], None
    return string[8 : idx - 1], string[idx + 13 :].strip("'").strip('"')

def call_main(purpose, task, action_input):
    resp = run_gpt(
        ACTION_PROMPT,
        stop_tokens=["observation:", "task:"],
        max_tokens=256,
        purpose=purpose,
        task=task,
        memory=memory.permanent_memory
    )
    lines = resp.strip().strip("\n").split("\n")
    print(resp)
    for line in lines:
        if line == "":
            continue
        if line.startswith("thought: "):
            print(line)
        elif line.startswith("action: "):
            action_name, action_input = parse_action(line)
            print(action_name, action_input)
            return action_name, action_input, task
        else:
            assert False, "unknown action: {}".format(line)
    return "MAIN", None, task

def call_set_task(purpose, task, action_input):
    task = run_gpt(
        TASK_PROMPT,
        stop_tokens=[],
        max_tokens=64,
        purpose=purpose,
        task=task,
    ).strip("\n")
    return "MAIN", None, task

def search_task(purpose, task, action_input):
    jobs = getJobs(action_input)
    task = run_gpt(
        TASK_PROMPT,
        stop_tokens=[],
        max_tokens=64,
        purpose=purpose,
        task=task,
    ).strip("\n")
    return "MAIN", None, task

def ask_jobseeker_info(purpose, task, action_input):
    print("Please provide some information about yourself: ", action_input)
    info = input()
    memory.permanent_memory.append("The job seekers' desired " + action_input + " is : " + info)
    return "MAIN", info, task

def run_gpt(
    prompt_template,
    stop_tokens,
    max_tokens,
    purpose,
    **prompt_kwargs,
):
    content = PREFIX.format(
        purpose=purpose,
    ) + prompt_template.format(**prompt_kwargs)
    resp = openai.ChatCompletion.create(
        model=MODEL,
        messages=[
            {"role": "system", "content": content},
        ],
        temperature=0.0,
        max_tokens=max_tokens,
        stop=stop_tokens if stop_tokens else None,
    )["choices"][0]["message"]["content"]
    print("*********")
    print(resp)
    return resp

NAME_TO_FUNC = {
    "MAIN": call_main,
    "UPDATE_TASK": call_set_task,
    "ASK_JOBSEEKER_INFO": ask_jobseeker_info,
    "SEARCH_JOBS": search_task
}

def run_action(purpose, task, action_name, action_input):
    if action_name == "COMPLETE":
        exit(0)

    assert action_name in NAME_TO_FUNC

    print("RUN: ", action_name, action_input)
    return NAME_TO_FUNC[action_name](purpose, task, action_input)


def run(purpose, task=None):
    action_name = "UPDATE_TASK" if task is None else "MAIN"
    action_input = None
    while True:
        print("")
        print("")
        print("---")
        print("purpose:", purpose)
        print("task:", task)
        print("---")

        action_name, action_input, task = run_action(
            purpose,
            task,
            action_name,
            action_input,
        )

def mainLoop():
    keepSearching = True
    while (keepSearching):
        pass
    # read input
    # perform agent call
    # output result
    # switch state
    # loop

# run("help me find a job")


import openai
import memory
import json
from utils import get_jobs, parse_action, format_memory

from prompts import (
    ACTION_PROMPT,
    PREFIX,
    JOB_SUMMARIZE_PROMPT
)

MODEL = "gpt-3.5-turbo"  # "gpt-4"
openai.api_key = ""


def summarize_job(purpose, title, description):
    summary = run_gpt(
        JOB_SUMMARIZE_PROMPT,
        stop_tokens=[],
        max_tokens=64,
        purpose=purpose,
        title=title,
        description=description
    )
    return summary


def call_main(purpose, history, action_input):
    formatted_memory = format_memory(memory.permanent_memory)
    resp = run_gpt(
        ACTION_PROMPT,
        stop_tokens=["observation:"],
        max_tokens=256,
        purpose=purpose,
        history=formatted_memory
    )
    memory.permanent_memory['current_job'] = ''
    memory.permanent_memory['current_user_response'] = ''
    lines = resp.strip().strip("\n").split("\n")
    for line in lines:
        if line == "":
            continue
        if line.startswith("thought: "):
            print(line)
        elif line.startswith("action: "):
            action_name, action_input = parse_action(line)
            print(action_name, action_input)
            history += '\nThe previously picked action is: ' + action_name
            return action_name, action_input, history
        else:
            assert False, "unknown action: {}".format(line)
    return "MAIN", None, history


def search_job(purpose, history, action_input):
    title = "Journalist"
    try:
        parsed_json = json.loads(action_input.replace("'", '"'))
        if "title" in parsed_json:
            title = parsed_json['title']
    except:
        pass
    finally:
        pass
    jobs = get_jobs(title)
    summarized_jobs = list(map(lambda d: summarize_job(purpose, d['title'], d['description']), jobs))
    for job in summarized_jobs:
        memory.permanent_memory['current_job'] = job
        memory.permanent_memory['found_jobs'].append(job)
        history += "\nWe found this job: " + job
        print(job)
    history += "\nobservation: We found " + str(len(summarized_jobs)) + " job(s) for " + title
    return "MAIN", None, history


def ask_jobseeker_info(purpose, history, action_input):
    print("Please provide some information about yourself: ", action_input)
    info = input()
    memory.permanent_memory['title'] = info
    history += "\nobservation: The user provided this information: " + info
    return "MAIN", None, history


def show_job(purpose, history, action_input):
    print("What do you think of this job?")
    print(action_input)
    response = input()
    memory.permanent_memory['current_user_response'] = response
    memory.permanent_memory['current_job'] = action_input
    history += "\nobservation: The user responded with: '" + response + "' when we showed a job with this description: " + action_input
    return "MAIN", None, history


def apply_for_job(purpose, history, action_input):
    exit(0)


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
    print(content)
    resp = openai.ChatCompletion.create(
        model=MODEL,
        messages=[
            {"role": "system", "content": content},
        ],
        temperature=0.0,
        max_tokens=max_tokens,
        stop=stop_tokens if stop_tokens else None,
    )["choices"][0]["message"]["content"]
    return resp


NAME_TO_FUNC = {
    "MAIN": call_main,
    "ASK_JOBSEEKER_INFO": ask_jobseeker_info,
    "SEARCH_JOBS": search_job,
    "SHOW_JOB": show_job,
    "APPLY_FOR_JOB": apply_for_job
}


def run_action(purpose, history, action_name, action_input):
    if action_name == "COMPLETE":
        exit(0)

    assert action_name in NAME_TO_FUNC

    print("RUN: ", action_name, action_input)
    return NAME_TO_FUNC[action_name](purpose, history, action_input)


def run(purpose):
    action_name ="MAIN"
    action_input = None
    history = ""
    while True:
        print("")
        print("---")

        action_name, action_input, history = run_action(
            purpose,
            history,
            action_name,
            action_input,
        )


input_purpose = """
You are searching for jobs in the Netherlands.
When a job is found show it to the jobseeker to see if they want to apply.
The jobseeker will reply with a message.
If the job seeker wants to apply, apply them to the job.
If the user likes the job consider the purpose completed.
No extra information is needed to apply for a job.
"""

run(input_purpose)

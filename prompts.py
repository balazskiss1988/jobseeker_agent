PREFIX = """You are helping a jobseeker find a job by telling them which action to pick

Purpose:
{purpose}
"""

ACTION_PROMPT = """
You have access to the following tools:
- action: UPDATE_TASK action_input=NEW_TASK
- action: ASK_JOBSEEKER_INFO action_input=JOBSEEKER_INFO
- action: SEARCH_JOBS action_input=FILTERS
- action: SHOW_JOB action_input=JOB_INFO
- action: APPLY_FOR_JOB
- action: COMPLETE

Instructions
- Complete the current task as best you can
- When the task is complete, update the task
- You can only use the tools you have access to

Use the following format:
task: the input task you must complete
thought: you should always think about what to do
action: the action to take (should be one of [UPDATE_TASK, ASK_JOBSEEKER_INFO, SEARCH_JOBS, SHOW_JOB, APPLY_FOR_JOB, COMPLETE]) action_input=XXX
observation: the result of the action
thought: you should always think after an observation
... (thought/action/observation/thought can repeat N times)

When ASK_JOBSEEKER_INFO is selected use one of [title] as input.

You are attempting to complete the task.
task: {task}

{history}
"""

TASK_PROMPT = """
You are attempting to complete the task
task: {task}

Tasks should be small, isolated, and independent

What should the task be for us to achieve the purpose?
task: """

JOB_SUMMARIZE_PROMPT = """
Summarize the following job in a single sentence:
Title:
{title}
Description:
{description}
"""


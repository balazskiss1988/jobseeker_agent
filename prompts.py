PREFIX = """You are helping a jobseeker find a job by telling them which action to pick

Purpose:
{purpose}
"""

ACTION_PROMPT = """
You know the following information:
{history}

You have access to the following tools:
- action: ASK_JOBSEEKER_INFO action_input=(should be one of [title])
- action: SEARCH_JOBS action_input=FILTERS
- action: SHOW_JOB action_input=JOB_INFO
- action: APPLY_FOR_JOB
- action: COMPLETE

Instructions
- You can only use the tools you have access to
- Do not choose ASK_JOBSEEKR_INFO if you already know the jobseekers preferred job title
- Pick SHOW_JOB if a job was found previously
- Pick APPLY_FOR_JOB if the jobseeker responds positively for the shown job
- Consider the response of the jobseeker when picking a tool

Use the following format:
thought: you should always think about what to do
action: the action to take (should be one of [ASK_JOBSEEKER_INFO, SEARCH_JOBS, SHOW_JOB, APPLY_FOR_JOB, COMPLETE]) action_input=XXX
observation: the result of the action
thought: you should always think after an observation
... (thought/action/observation/thought can repeat N times)

When ASK_JOBSEEKER_INFO is selected use one of [title] as input.
"""

JOB_SUMMARIZE_PROMPT = """
Summarize the following job in a single sentence:
Title:
{title}
Description:
{description}
"""


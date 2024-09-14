import textwrap


def action_decision_pt(state_chunks: str) -> str:
    '''
    Prompt for Action Decision LLM that predicts the optimal action token.

    Args:
        state_chunks: Sequence of state information chunks formatted as follows:
            ---
            topic: /asr
            ts: 2024-08-31 17:45:23
            data: Hey robot, I'm heading out for the day.
            ---
            topic: /action_response
            ts: 2024-08-31 17:45:25
            data: Robot reply: Certainly! I hope you had a productive day. Is there anything you need help with before you leave?
            ---
            topic: /asr
            ts: 2024-08-31 17:45:32
            data: No, I think I'm all set. Just wanted to say goodbye.
            ---
            topic: /action_response
            ts: 2024-08-31 17:45:34
            data: Robot reply: That's very kind of you, sweetie. Have a wonderful evening and a safe trip home!
            ---

    Returns:

    '''
    state_template = textwrap.dedent('''
        <state_header>
        Current task goal: Follow instructions from the user to help them with their task. Provide information and assistance as needed.

        Robot world state representation description:
        topic: Name of ROS 2 topic publishing message
        ts: Timestamp of message formatted as 'year-month-day hour:minute:seconds'
        data: Message content

        The state information is structured as follows:
        The first part <retrieved_memory> is a summary of task-relevant long-term memories.
        The second part <state_chunks> is a list of most recent state information including perceptual and internal state information.
        </state_header>

        <retrieved_memory>
        </retrieved_memory>

        <state_chunks>
        {}
        </state_chunks>
    ''')

    instruction_template = textwrap.dedent('''
        Output the optimal action you should take in order to achieve the goal based on the following robot world state:
        {}
        The robot outputs what action to take to optimally follow user instructions. The robot should provide information and assistance as needed. Generally the robot pursues conversation with the user but remains quiet unless user is speaking with the robot.

        Output the character of the optimal action you should take among the following list of valid actions:
        Do nothing: a
        Reply: b
    ''')

    state = state_template.format(state_chunks)
    prompt = instruction_template.format(state)

    # Remove leading/trailing line breaks
    prompt = prompt.strip()

    return prompt


if __name__ == '__main__':

    state_chunks = textwrap.dedent('''
        ---
        topic: /asr
        ts: 2024-08-31 17:45:23
        data: Hey robot, I'm heading out for the day.
        ---
        topic: /action_response
        ts: 2024-08-31 17:45:25
        data: Robot reply: Certainly! I hope you had a productive day. Is there anything you need help with before you leave?
        ---
        topic: /asr
        ts: 2024-08-31 17:45:32
        data: No, I think I'm all set. Just wanted to say goodbye.
        ---
        topic: /action_response
        ts: 2024-08-31 17:45:34
        data: Robot reply: That's very kind of you, sweetie. Have a wonderful evening and a safe trip home!
        ---
    ''')

    prompt = action_decision_pt(state_chunks)

    print(prompt)

import textwrap


def state_description_pt() -> str:
    '''
    Description of the state information structure.
    '''
    state_descr = textwrap.dedent('''
        Robot world state representation description:
        topic: Name of ROS 2 topic publishing message
        ts: Timestamp of message formatted as year-month-day hour:minute:seconds
        data: Message content
        
        Topic descriptions:
        /asr: Automatic speech recognition. Talk robot hears from microphone.
        /action_response: Information about actions the robot previously executed.

        The state information is structured as follows:
        The first part <retrieved_memory> is a summary of task-relevant long-term memories.
        The second part <state_chunks> is a list of most recent state information including perceptual and internal state information.
    ''')

    # Remove leading/trailing line breaks
    state_descr = state_descr.strip()

    return state_descr


if __name__ == '__main__':

    print(state_description_pt())

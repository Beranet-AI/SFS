def edge_command_topic(edge_id: str) -> str:
    return f"sfs/edge/{edge_id}/commands"


def command_result_topic(edge_id: str) -> str:
    return f"sfs/edge/{edge_id}/commands/results"

def activity_to_plain_text(activity : dict) -> str:
    """Convert activity dictionary to plain

    Args:
        activity (dict): activity dict from scrapper (single one)

    Returns:
        str: plain
    """
    return f"{activity['title']}\n\tGoal: {activity['goal']}\n\tResults: {activity['results']}\n\tIssue_encountered: {activity['issue_encountered']}\n\tSkills mastered: {activity['skills']}\n\tFacts: {activity['facts']}\n"



def activities_dict_to_items(act_dict: dict) -> list:
    """Convert activity dictionary to plain list of activity items (dict)

    Args:
        act_dict (dict): activity dict from scrapper

    Returns:
        list: list of all activity
    """
    single_activity_list = []
    for activity_list in act_dict.values():
        single_activity_list.extend(activity_list)
    return single_activity_list

def activities_dict_to_plain_text(act_dict: dict) -> str:
    """Convert activity dictionary to plain text

    Args:
        act_dict (dict): activity dict from scrapper

    Returns:
        str: Plain text of all activity contained in dict
    """
    single_text = ""
    for activity in activities_dict_to_items(act_dict):
        single_text += activity_to_plain_text(activity)
    return single_text
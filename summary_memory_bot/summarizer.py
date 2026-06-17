def update_summary(current_summary, user_message):

    summary = current_summary

    if "my name is" in user_message.lower():

        name = user_message.split("is")[-1].strip()

        summary += f"\nUser name: {name}"

    elif "i am learning" in user_message.lower():

        topic = user_message.split("learning")[-1].strip()

        summary += f"\nLearning: {topic}"

    elif "i like" in user_message.lower():

        interest = user_message.split("like")[-1].strip()

        summary += f"\nInterest: {interest}"

    return summary
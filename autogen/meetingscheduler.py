import os
from datetime import datetime, timedelta
from autogen import AssistantAgent, UserProxyAgent

# Configure the LLM
config_list = [{"model": "gpt-4", "api_key": os.environ["OPENAI_API_KEY"]}]

# Simulated Calendar API
calendar = {
    "John": [
        {"start": "2023-06-13T13:00:00", "end": "2023-06-13T14:00:00"},
        {"start": "2023-06-13T15:30:00", "end": "2023-06-13T16:30:00"},
    ]
}

def find_available_slot(attendee, date, duration):
    slots = calendar.get(attendee, [])
    start_time = datetime.strptime(f"{date}T12:00:00", "%Y-%m-%dT%H:%M:%S")
    end_time = datetime.strptime(f"{date}T18:00:00", "%Y-%m-%dT%H:%M:%S")
    
    while start_time + timedelta(minutes=duration) <= end_time:
        if not any(datetime.strptime(slot["start"], "%Y-%m-%dT%H:%M:%S") < start_time + timedelta(minutes=duration) and 
                   start_time < datetime.strptime(slot["end"], "%Y-%m-%dT%H:%M:%S") for slot in slots):
            return start_time.strftime("%Y-%m-%dT%H:%M:%S")
        start_time += timedelta(minutes=30)
    return None

def schedule_meeting(attendee, start_time, end_time):
    calendar.setdefault(attendee, []).append({"start": start_time, "end": end_time})
    return f"Meeting scheduled with {attendee} from {start_time} to {end_time}."

# User Assistant Agent
user_assistant = AssistantAgent(
    name="UserAssistant",
    system_message="You are an assistant that helps the user schedule meetings.",
    llm_config={"config_list": config_list},
)

# Scheduling Assistant Agent
scheduling_assistant = AssistantAgent(
    name="SchedulingAssistant",
    system_message="You are an assistant that interprets meeting requests and proposes available time slots.",
    llm_config={"config_list": config_list},
)

# User Proxy Agent
user_proxy = UserProxyAgent(
    name="UserProxy",
    human_input_mode="TERMINATE",
    is_termination_msg=lambda x: "TERMINATE" in x.get("content", ""),
)

def schedule(meeting_request):
    user_proxy.initiate_chat(user_assistant, message=meeting_request)
    user_assistant.initiate_chat(scheduling_assistant, message=user_proxy.messages[-1]['content'])
    
    attendee, date, duration = "John", "2023-06-13", 30  # Parse from scheduling_assistant's response
    proposed_slot = find_available_slot(attendee, date, duration)
    
    if proposed_slot:
        user_assistant.initiate_chat(user_proxy, message=f"Proposed time slot: {proposed_slot}. Do you confirm?")
        if "yes" in user_proxy.messages[-1]['content'].lower():
            end_time = (datetime.strptime(proposed_slot, "%Y-%m-%dT%H:%M:%S") + timedelta(minutes=duration)).strftime("%Y-%m-%dT%H:%M:%S")
            result = schedule_meeting(attendee, proposed_slot, end_time)
            user_assistant.initiate_chat(user_proxy, message=result)
    else:
        user_assistant.initiate_chat(user_proxy, message="No available time slots found.")

# Example usage
schedule("Schedule a 30 min meeting with John to discuss the Q3 budget sometime next Tue afternoon.")
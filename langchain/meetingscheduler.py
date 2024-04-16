import os
from langchain.agents import initialize_agent, Tool
from langchain.chains import LLMChain
from langchain.llms import OpenAI
from langchain.prompts import PromptTemplate
from datetime import datetime, timedelta

# Set up OpenAI API key
os.environ["OPENAI_API_KEY"] = "your_openai_api_key"

# Dummy calendar data
calendars = {
    "Alice": [
        {"start": "2023-06-01T09:00:00", "end": "2023-06-01T10:30:00"},
        {"start": "2023-06-01T14:00:00", "end": "2023-06-01T15:00:00"}
    ],
    "Bob": [
        {"start": "2023-06-01T11:00:00", "end": "2023-06-01T12:30:00"},
        {"start": "2023-06-01T14:30:00", "end": "2023-06-01T16:00:00"}
    ],
    "Charlie": [
        {"start": "2023-06-01T10:00:00", "end": "2023-06-01T11:30:00"},
        {"start": "2023-06-01T13:00:00", "end": "2023-06-01T14:30:00"}
    ]
}

# Calendar API tool
def get_availability(attendees):
    availability = []
    for attendee in attendees:
        if attendee in calendars:
            availability.append(f"{attendee}'s availability:")
            for event in calendars[attendee]:
                availability.append(f"  - From: {event['start']} To: {event['end']}")
        else:
            availability.append(f"No calendar data found for {attendee}")
    return "\n".join(availability)

# Time slot finder tool
def find_time_slot(attendees, duration):
    duration = int(duration)
    time_slots = []
    
    start_time = datetime(2023, 6, 1, 9, 0)
    end_time = datetime(2023, 6, 1, 17, 0)
    time_step = timedelta(minutes=30)
    
    while start_time + timedelta(minutes=duration) <= end_time:
        available = True
        for attendee in attendees:
            if attendee not in calendars:
                available = False
                break
            for event in calendars[attendee]:
                event_start = datetime.fromisoformat(event["start"])
                event_end = datetime.fromisoformat(event["end"])
                if start_time < event_end and start_time + timedelta(minutes=duration) > event_start:
                    available = False
                    break
            if not available:
                break
        if available:
            time_slots.append(f"{start_time.strftime('%Y-%m-%dT%H:%M:%S')} - {(start_time + timedelta(minutes=duration)).strftime('%Y-%m-%dT%H:%M:%S')}")
        start_time += time_step
    
    if time_slots:
        return "\n".join(time_slots)
    else:
        return "No available time slots found for the given attendees and duration."

# Email tool
def send_invite(attendees, time_slot):
    return f"Sending meeting invite to {', '.join(attendees)} for time slot {time_slot}."

# Create tools list
tools = [
    Tool(name="Get Availability", func=get_availability, description="Useful for retrieving attendees' availability from their calendars."),
    Tool(name="Find Time Slot", func=find_time_slot, description="Useful for finding available time slots for the meeting based on attendees' availability and meeting duration."),
    Tool(name="Send Invite", func=send_invite, description="Useful for sending meeting invites to attendees.")
]

# Initialize agent
agent = initialize_agent(tools, OpenAI(temperature=0), agent="zero-shot-react-description", verbose=True)

# Main loop
while True:
    print("\nWelcome to the Meeting Scheduler Agent!")
    attendees_input = input("Please enter the list of attendees (comma-separated) or type 'exit' to quit: ")
    
    if attendees_input.lower() == "exit":
        print("Thank you for using the Meeting Scheduler Agent. Goodbye!")
        break
    
    attendees = [attendee.strip() for attendee in attendees_input.split(",")]
    duration = input("Please enter the meeting duration in minutes: ")
    
    result = agent.run(f"Attendees: {', '.join(attendees)}\nDuration: {duration} minutes")
    print(f"\nResult: {result}")
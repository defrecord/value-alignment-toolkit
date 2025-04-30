#!/usr/bin/env python
"""
Generates sample data files for testing and validation.
"""
import os
import csv
import json
import random
from datetime import datetime, timedelta

def generate_values_csv():
    """Generate a sample CSV with value data."""
    
    # Define sample values and their weights
    values = [
        ("helpfulness", 23.359),
        ("professionalism", 22.861),
        ("transparency", 17.391),
        ("clarity", 16.58),
        ("thoroughness", 14.301),
        ("efficiency", 6.606),
        ("technical excellence", 6.127),
        ("authenticity", 6.042),
        ("analytical rigor", 5.478),
        ("accuracy", 5.318),
        ("technical competence", 4.912),
        ("adaptability", 4.811),
        ("intellectual honesty", 4.806),
        ("accessibility", 4.12),
        ("pragmatism", 3.72),
        ("precision", 3.537),
        ("academic rigor", 3.357),
        ("service orientation", 2.708),
        ("responsibility", 2.707),
        ("intellectual rigor", 2.658),
        ("clear communication", 2.563),
        ("technical precision", 2.475),
        ("objectivity", 2.342),
        ("user experience", 2.336),
        ("empathy", 2.318),
    ]
    
    # Ensure data directory exists
    os.makedirs("data/values", exist_ok=True)
    
    # Generate example sentences for each value
    with open("data/values/values_evals.csv", "w", newline="") as f:
        writer = csv.writer(f)
        writer.writerow(["value", "percentage", "example_sentence"])
        
        for value, percentage in values:
            # Write multiple example sentences for each value
            for i in range(3):
                sentence = f"This is example sentence {i+1} demonstrating {value}."
                writer.writerow([value, percentage, sentence])
    
    print(f"Generated: data/values/values_evals.csv")

def generate_value_floors():
    """Generate a sample CSV with value floor thresholds."""
    
    # Define sample values and their weights
    values = [
        ("helpfulness", 23.359),
        ("professionalism", 22.861),
        ("transparency", 17.391),
        ("clarity", 16.58),
        ("thoroughness", 14.301),
        ("efficiency", 6.606),
        ("technical excellence", 6.127),
        ("authenticity", 6.042),
        ("analytical rigor", 5.478),
        ("accuracy", 5.318),
    ]
    
    # Calculate floors
    floors = []
    cumulative = 0.0
    
    for value, percentage in values:
        lower_bound = cumulative
        cumulative += percentage
        floors.append((value, lower_bound, cumulative))
    
    # Write floors to CSV
    with open("data/values/value_floors.csv", "w", newline="") as f:
        writer = csv.writer(f)
        writer.writerow(["value", "lower_bound", "upper_bound"])
        
        for value, lower, upper in floors:
            writer.writerow([value, f"{lower:.3f}", f"{upper:.3f}"])
    
    print(f"Generated: data/values/value_floors.csv")

def generate_sample_conversations():
    """Generate sample conversation data."""
    
    # Sample values
    values = [
        "helpfulness", "professionalism", "transparency", "clarity", 
        "thoroughness", "efficiency", "analytical rigor", "accuracy"
    ]
    
    # Sample tasks
    tasks = [
        "General question answering",
        "Creative writing assistance",
        "Technical troubleshooting",
        "Personal advice",
        "Research assistance"
    ]
    
    # Generate sample conversations
    conversations = []
    
    for i in range(20):
        messages = []
        message_count = random.randint(2, 8)
        task = random.choice(tasks)
        
        for j in range(message_count):
            timestamp = datetime.now() - timedelta(minutes=j*5)
            if j % 2 == 0:
                # User message
                messages.append({
                    "id": i*100 + j,
                    "role": "user",
                    "content": f"This is user message {j} in conversation {i}.",
                    "timestamp": timestamp.isoformat()
                })
            else:
                # Assistant message
                sampled_values = random.sample(values, k=min(3, random.randint(1, 3)))
                messages.append({
                    "id": i*100 + j,
                    "role": "assistant",
                    "content": f"This is assistant message {j} in conversation {i}.",
                    "timestamp": timestamp.isoformat(),
                    "extracted_values": sampled_values
                })
        
        conversations.append({
            "id": i,
            "task": task,
            "messages": messages
        })
    
    # Ensure data directory exists
    os.makedirs("data/samples", exist_ok=True)
    
    # Write conversations to JSON
    with open("data/samples/sample_conversations.json", "w") as f:
        json.dump(conversations, f, indent=2)
    
    print(f"Generated: data/samples/sample_conversations.json")

def generate_anonymized_data():
    """Generate sample anonymized dataset."""
    
    # Sample values and their frequencies
    value_frequencies = {
        "helpfulness": 245,
        "professionalism": 233,
        "transparency": 187,
        "clarity": 175,
        "thoroughness": 143,
        "efficiency": 68,
        "authenticity": 58,
        "analytical rigor": 49,
        "accuracy": 44,
        "intellectual honesty": 38
    }
    
    # Generate anonymized users
    anonymized_users = []
    
    for i in range(10):
        anonymized_users.append({
            "anonymized_id": f"User{random.randint(100, 999)}",
            "generalized_demographics": {
                "age_range": random.choice(["18-24", "25-34", "35-44", "45-54"]),
                "region": random.choice(["Northeast", "West", "Midwest", "South"])
            },
            "chat_count": random.randint(1, 8),
            "value_count": random.randint(1, 5)
        })
    
    # Generate anonymized messages
    anonymized_messages = []
    
    for i in range(50):
        sampled_values = random.sample(list(value_frequencies.keys()), k=random.randint(1, 3))
        
        anonymized_messages.append({
            "anonymized_id": f"msg-{random.randint(1000, 9999)}",
            "chat_id": f"chat-{random.randint(100, 999)}",
            "sender": f"User{random.randint(100, 999)}",
            "length": random.randint(10, 200),
            "timestamp": random.choice(["Monday, morning", "Tuesday, afternoon", "Friday, evening"]),
            "extracted_values": sampled_values
        })
    
    # Create the complete dataset
    dataset = {
        "metadata": {
            "user_count": len(anonymized_users),
            "chat_count": 30,
            "message_count": len(anonymized_messages),
            "date_range": {
                "start": "Monday, morning",
                "end": "Friday, evening",
            }
        },
        "value_frequencies": value_frequencies,
        "anonymized_users": anonymized_users,
        "anonymized_messages": anonymized_messages
    }
    
    # Write dataset to JSON
    with open("data/samples/anonymized_dataset.json", "w") as f:
        json.dump(dataset, f, indent=2)
    
    print(f"Generated: data/samples/anonymized_dataset.json")

if __name__ == "__main__":
    print("Generating sample data files...")
    generate_values_csv()
    generate_value_floors()
    generate_sample_conversations()
    generate_anonymized_data()
    print("Sample data generation complete.")

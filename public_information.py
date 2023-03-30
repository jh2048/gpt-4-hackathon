# Import necessary libraries
import openai, json
from GPTKey import api_key

# Set up OpenAI API credentials
openai.api_key = api_key

# Define function to check if a food item has been recalled
def check_food_recall_json(food_item, recalls):
    # Check if the food item has been recalled
    for recall in recalls:
        if food_item in recall["product_description"].lower():
            if recall["status"] == "Ongoing" or recall["status"] == "Completed":
                recall_reason = recall["reason_for_recall"]
                recall_classification = recall["classification"]
                state = recall["state"]
                product_description = recall["product_description"]
                year, month, day = int(recall["recall_initiation_date"][:4]), int(recall["recall_initiation_date"][4:6]), int(recall["recall_initiation_date"][6:])
                return f"Be careful! If you're in {state}, as of {day, month, year}, the {food_item} you consumed has been recalled due to {recall_reason}. The recall classification is {recall_classification}. Here's a full description of the food item: \n {product_description} \n"
    # If the food item has not been recalled, return a message stating that it is safe
    return f"The {food_item} you consumed has not been recalled. It is safe to eat."




# Define function to generate a response to user prompts using ChatGPT
def generate_response(prompt):
    print('Opening dataset...')

    with open("food-enforcement.json") as f:
        recalls = json.load(f)

    print('Getting response...')
    # Generate a response using ChatGPT
    response = openai.ChatCompletion.create(
        model="gpt-4",
        messages=[
            {"role": "system", "content": "Find food items in the text."},
            {"role": "user", "content": f"{prompt}"},
        ],
    )
    print(response)
    food_items = response["choices"][0]["message"]["content"].strip().split(',')
    print(food_items)
    # Extract the food item mentioned in the prompt
    for food_item in food_items:
        # Check if the food item has been recalled
        recall_info = check_food_recall_json(food_item, recalls)
        print(f"You said you ate {food_item}. Here is recall info that might be useful to you: {recall_info}")
        print('\n')

    # Return the recall information along with the original prompt and ChatGPT's response
    return 

# Example usage
print('Starting anaysis...')
prompt = "I ate a burger for lunch today, and it was delicious. The bun was soft, and the meat was juicy. The fries were crispy and salty. Can you tell me more about burgers?"
print('Generating response... ')
response = generate_response(prompt)
print(response)

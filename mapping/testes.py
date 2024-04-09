import json

# Initialize an empty list to store data
data_list = []

# Example loop (replace this with your actual loop)
for i in range(3):
    # Create a dictionary representing data for each iteration
    item_data = {
        "index": i,
        "name": "Item {}".format(i),
        "description": "Description of item {}".format(i)
    }
    
    # Append the dictionary to the list
    data_list.append(item_data)

# Convert the list of dictionaries to a JSON array
json_data = json.dumps(data_list, indent=4)

# Print the JSON array
print(json_data)
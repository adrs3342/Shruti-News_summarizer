from datasets import load_dataset

# Define the local directory where you want to store the dataset
save_path = "./newsroom_data"

# Load the dataset with caching in the specified folder
dataset = load_dataset("newsroom", cache_dir='/Users/adarshsharma/Desktop/project/News-Articles-Summarizer-App-main/project')

# Print dataset structure
print(dataset)

# Save each split as a JSON file
dataset["train"].to_csv(f"{save_path}/newsroom_train.csv")
dataset["validation"].to_csv(f"{save_path}/newsroom_validation.csv")
dataset["test"].to_csv(f"{save_path}/newsroom_test.csv")


print("Dataset saved successfully!")

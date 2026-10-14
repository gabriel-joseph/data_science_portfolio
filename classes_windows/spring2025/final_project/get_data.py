import kagglehub

# Download latest version
path = kagglehub.dataset_download("ahmedgmy/cars-raw-dataset")

print("Path to dataset files:", path)
import re
import matplotlib.pyplot as plt

def analyze_file(file_path):
  
    pattern = r"OK created sql table model (.*?)\s+\.\.+ \[OK in (.*?)s\]"

    with open(file_path, "r") as file:
        log_content = file.read()

    matches = re.findall(pattern, log_content)

    return matches


file_path = "data/dbt_run_logs_2_exec.txt" # CHANGE to file_path of file you want to analyze
file_name = file_path[18:24]

matches = analyze_file(file_path)

# Calculate total execution time for the file
total_time = sum(float(time) for _, time in matches)
total_time_minutes = total_time / 60
print(f"Total time of execution for {file_path} is {total_time_minutes:.2f} min.")


# Sort tables by execution time (descending order)
sorted_tables = sorted(matches, key=lambda x: float(x[1]), reverse=True)

# Print the top 5 longest processed tables
print("\nTop 5 longest processed tables:")
for table, time in sorted_tables[:5]:
    print(f"Table: {table}, Time: {time} seconds")
    
# Aggregate time by layer (demo_bronze, demo_silver, demo_gold)
layer_times = {'demo_bronze': 0, 'demo_silver': 0, 'demo_gold': 0}
for table, time in matches:
    layer = table.split('.')[0]
    if layer in layer_times:
        layer_times[layer] += float(time)

# Convert time to minutes
layer_times = {layer: time / 60 for layer, time in layer_times.items()}

# Plotting
plt.figure(figsize=(8, 5))
plt.bar(layer_times.keys(), layer_times.values())
plt.title(f'Total Execution Time by Layer ~ {file_name}')
plt.xlabel('Layer')
plt.ylabel('Time (minutes)')
plt.xticks(rotation=45)
plt.tight_layout()
plt.show()

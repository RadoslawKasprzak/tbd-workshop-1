import re
import matplotlib.pyplot as plt

def analyze_file(file_path):
  
    pattern = r"OK created sql table model (.*?)\s+\.\.+ \[OK in (.*?)s\]"

    with open(file_path, "r") as file:
        log_content = file.read()

    matches = re.findall(pattern, log_content)

    return matches


file_path = "C:\\Users\\karol\\tbd\\tbd-workshop-1\\dbt_etl_performance_testing\\data\\dbt_run_logs_8_exec.txt" # CHANGE to file_path of file you want to analyze
file_name = file_path[-10:-4]

matches = analyze_file(file_path)

# Calculate total execution time for the file
#total_time = sum(float(time) for _, time in matches)
#total_time_minutes = total_time / 60
#print(f"Total time of execution for {file_path} is {total_time_minutes:.2f} min.")


# Sort tables by execution time (descending order)
sorted_tables = sorted(matches, key=lambda x: float(x[1]), reverse=True)

# Print all tables
'''print("\nTables:")
for table, time in matches:
    print(f"Table: {table}, Time: {time} seconds")'''

time_values = [float(x[1]) for x in matches]

# Plotting
plt.figure(figsize=(8, 5))
plt.bar(range(len(matches)), time_values)
plt.title(f'Time taken per task ~ {file_name}')
plt.xlabel('Task number')
plt.ylabel('Time (seconds)')
plt.ylim(0, 1100)
plt.xticks(rotation=45)
plt.tight_layout()
plt.show()

import pandas as pd
import matplotlib.pyplot as plt

# Load the CSV file
# Replace 'your_file.csv' with the path to your CSV file
data = pd.read_csv('csv.mergeall.py')

# Convert the timestamp to a numeric or datetime format if necessary
data['timestamp'] = pd.to_datetime(data['timestamp'])

# Plot the data
plt.figure(figsize=(12, 6))

# Subplot for bid and ask prices
plt.subplot(2, 1, 1)
plt.plot(data['timestamp'], data['bidPrice'], label='Bid Price', color='blue')
plt.plot(data['timestamp'], data['askPrice'], label='Ask Price', color='red')
plt.xlabel('Timestamp')
plt.ylabel('Price')
plt.title('Bid and Ask Prices Over Time')
plt.legend()

# Subplot for bid and ask volumes
plt.subplot(2, 1, 2)
plt.plot(data['timestamp'], data['bidVolume'], label='Bid Volume', color='green')
plt.plot(data['timestamp'], data['askVolume'], label='Ask Volume', color='orange')
plt.xlabel('Timestamp')
plt.ylabel('Volume')
plt.title('Bid and Ask Volumes Over Time')
plt.legend()

# Adjust layout and show the plot
plt.tight_layout()
plt.show()
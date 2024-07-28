import json
import matplotlib.pyplot as plt
import pandas as pd
import seaborn as sns

charts = ['Pie Chart of Total Time Distribution',
          'Bar Chart of Activity Average Time and Total Logs']

def create_df():
    # create empty dataframe
    df = pd.DataFrame(columns=['Activity', 'Num_Logs', 'Total Time'])
    with open("activities.json", 'r') as file:
        contents = json.load(file)

    # each each activity to the dataframe
    for content in contents['activities']:
        new_row = {
            'Activity': content['activity_name'],
            'Num_Logs': len(content['time_elapsed']),
            'Total Time': sum(content['time_elapsed'])
        }
        df.loc[len(df)] = new_row
    
    df['Average Time'] = df['Total Time'] / df['Num_Logs']

    return df

# draws pie chart of all activities
def draw_pie(df):
    fig, ax = plt.subplots(figsize=(6,6))
    plt.pie(df['Total Time'],labels=df['Activity'], autopct='%.0f%%', radius=0.85)
    ax.legend()
    ax.set_title('Time Elapsed by Activity')
    plt.tight_layout()

    return plt.show()

# draws bar chart of all activities
def draw_barchart(df):
    fig, ax1 = plt.subplots()
    sns.barplot(data=df, x='Activity', y='Average Time')
    ax2 = ax1.twinx()
    ax2.plot(df['Activity'], df['Num_Logs'], color='red', marker='o', linestyle='-', label='Number of Logs')
    ax1.set_title('Time Elapsed by Activity')
    ax1.set_ylabel('Total Time (seconds)')
    ax2.set_ylabel('Number of Logs')
    plt.tight_layout()

    return plt.show()

def PLOT(df):
    try:
        choice = int(input('\nWhich chart would you like to view? ---> '))
        if choice == 1:
            return draw_pie(df)
        elif choice == 2:
            return draw_barchart(df)
        else: raise ValueError
    except ValueError:
        print('Invalid input. Please enter a number that corresponds to a visual.')
        return PLOT(df)

def main():
    df = create_df()

    print(f"\n{'*'*15} Available Charts {'*'*15}")
    for i in range(len(charts)):
        print(f"{i + 1} - {charts[i]}")
    
    PLOT(df)

if __name__ == "__main__":
    main()
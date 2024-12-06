import configparser

# Load configuration file
config = configparser.ConfigParser()
config.read('assets\config.cfg')

# Redshift credentials
host = config.get('redshift', 'host')
port = config.getint('redshift', 'port')
dbname = config.get('redshift', 'dbname')
user = config.get('redshift', 'user')
password = config.get('redshift', 'password')
schema = config.get('redshift', 'schema')  # Read schema from config

# Identify consecutive sequences that match the target set
def find_consecutive_target_sequences(group):
    # Keep track of sequences that match the target set
    target_set = {8782, 8717, 8920, 8870, 9201, 8971, 8546}
    group['is_target'] = group['visit_concept_id'].isin(target_set)
    group['seq_id'] = (group['is_target'] != group['is_target'].shift()).cumsum()
    # display(group[group['is_target']].groupby('seq_id').apply(lambda x: x))
    # display(group)
    # Filter only target sequences
    matching_sequences = (
        group[group['is_target']]
        .groupby('seq_id')
        .filter(lambda x: set(x['visit_concept_id']).issubset(target_set))
    )
    return matching_sequences


def get_first_admission_durations(sub_df):
    # Ensure the dataframe is sorted
    sub_df =sub_df.sort_values(by=["person_id", "visit_start_date"])

    # Apply the function to each person_id
    df_sequences = sub_df.groupby('person_id').apply(find_consecutive_target_sequences).reset_index(drop=True)
    # display(df_sequences)
    # Get the first sequence for each person_id
    df_sequences = df_sequences[df_sequences["seq_id"]==1]
    first_sequences = (
        df_sequences.groupby('person_id')
        .agg(
            first_start=('visit_start_date', 'first'),
            last_end=('visit_end_date', 'last')
        )
        .reset_index()
    )
    first_sequences['duration'] = (first_sequences['last_end'] - first_sequences['first_start'])
    first_sequences['duration'] = first_sequences.duration.apply(lambda x: round(x.total_seconds()/3600/24)) # Convert to number of days
    first_sequences = first_sequences[first_sequences["duration"]<=100]

    average_duration = first_sequences['duration'].mean()
    median_duration = first_sequences['duration'].median()
    mode_duration = first_sequences['duration'].mode()
    std_dev = first_sequences['duration'].std()

    stats = {
        "mean": float(average_duration),
        "median": float(median_duration),
        "mode": int(mode_duration),
        "std": float(std_dev)
    }
    
    return first_sequences, stats
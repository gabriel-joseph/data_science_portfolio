import pandas as pd

def classify_column(col):
    unique_vals = col.dropna().unique()
    num_unique = len(unique_vals)
    if pd.api.types.is_numeric_dtype(col):
        if num_unique == 2:
            return 'binary'
        elif num_unique < 15:
            return 'categorical'
        else:
            return 'number'
    else:
        if num_unique == 2:
            return 'binary'
        else:
            return 'categorical'

def get_sample_rows_for_column(df, column, n=3):
    unique_vals = df[column].dropna().unique()
    sample_vals = unique_vals[:min(len(unique_vals), n)]
    rows = pd.DataFrame()

    for val in sample_vals:
        match = df[df[column] == val]
        if not match.empty:
            rows = pd.concat([rows, match.head(1)])
    return rows

def analyze_dataframe_and_save(csv_path, output_csv_path="sampled_air_quality_rows.csv"):
    df = pd.read_csv(csv_path)
    all_samples = pd.DataFrame()

    for col in df.columns:
        col_type = classify_column(df[col])
        print(f"Column: '{col}' | Type: {col_type}")
        sample_rows = get_sample_rows_for_column(df, col)
        all_samples = pd.concat([all_samples, sample_rows], ignore_index=True)

    # Drop duplicate rows before saving
    all_samples.drop_duplicates(inplace=True)
    
    # Save to CSV
    all_samples.to_csv(output_csv_path, index=False)
    print(f"\nSampled rows saved to '{output_csv_path}'.")

# Run the script
if __name__ == "__main__":
    analyze_dataframe_and_save("air_quality_by_state_county.csv")

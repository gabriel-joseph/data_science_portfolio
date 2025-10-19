# read_and_save_csvs.R
# Reads all CSV files in the working directory and saves each as an .rds file
# Place this script in: c:\Users\Gabe\OneDrive\Documents\GitHub\data_science_classes_windows\fall2025\dsc640_data_viz\week5_6

csv_files <- list.files(pattern = "\\.csv$", full.names = TRUE, ignore.case = TRUE)

if (length(csv_files) == 0) {
  stop("No CSV files found in the working directory.")
}

cat(sprintf("Found %d CSV file(s):\n", length(csv_files)))
print(basename(csv_files))

for (f in csv_files) {
  cat(sprintf("\nReading: %s\n", basename(f)))
  # Use tryCatch to handle irregular files
  df <- tryCatch({
    read.csv(f, stringsAsFactors = FALSE, na.strings = c("", "NA", "NaT"))
  }, error = function(e) {
    warning(sprintf("Failed to read %s: %s", basename(f), e$message))
    return(NULL)
  })

  if (is.null(df)) next

  rds_path <- sub("\\.csv$", ".rds", f, ignore.case = TRUE)
  saveRDS(df, file = rds_path)
  cat(sprintf("Saved RDS: %s (rows=%d, cols=%d)\n", basename(rds_path), nrow(df), ncol(df)))
}

cat("\nDone.\n")




# Combine real and fake dataframes
politics_real_df['real'] = 1
politics_fake_df['real'] = 0
combined_df = pd.concat([politics_real_df, politics_fake_df], ignore_index=True)

# Prepare features and target
X = combined_df['title']
y = combined_df['real']

# Split data
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42, stratify=y)

# Vectorize titles
vectorizer = TfidfVectorizer(stop_words='english', max_features=1000)
X_train_vec = vectorizer.fit_transform(X_train)
X_test_vec = vectorizer.transform(X_test)

# Train classifier
clf = LogisticRegression(max_iter=1000, class_weight="balanced")

clf.fit(X_train_vec, y_train)

# Predict and evaluate
y_pred = clf.predict(X_test_vec)
print(classification_report(y_test, y_pred))



# --- Combine real and fake dataframes ---
politics_real_df['real'] = 1
politics_fake_df['real'] = 0
combined_df = pd.concat([politics_real_df, politics_fake_df], ignore_index=True)

# --- Prepare features and target ---
X = combined_df['title'].astype(str)
y = combined_df['real']

# --- Split data ---
X_train, X_test, y_train, y_test = train_test_split(
    X, y, test_size=0.2, random_state=42, stratify=y
)

# --- Tokenize with DistilBERT tokenizer ---
tokenizer = DistilBertTokenizerFast.from_pretrained('distilbert-base-uncased')

train_encodings = tokenizer(
    list(X_train), truncation=True, padding=True, max_length=64, return_tensors='tf'
)
test_encodings = tokenizer(
    list(X_test), truncation=True, padding=True, max_length=64, return_tensors='tf'
)

# --- Convert to TensorFlow datasets ---
train_dataset = tf.data.Dataset.from_tensor_slices((
    dict(train_encodings),
    y_train.values
)).batch(16)

test_dataset = tf.data.Dataset.from_tensor_slices((
    dict(test_encodings),
    y_test.values
)).batch(16)

# --- Load pre-trained DistilBERT model for classification ---
model = TFDistilBertForSequenceClassification.from_pretrained(
    'distilbert-base-uncased',
    num_labels=2
)

# --- Compile model ---
optimizer = Adam(learning_rate=5e-5)
loss = tf.keras.losses.SparseCategoricalCrossentropy(from_logits=True)
metric = tf.keras.metrics.SparseCategoricalAccuracy('accuracy')

model.compile(optimizer=optimizer, loss=loss, metrics=[metric])

# --- Train model ---
model.fit(train_dataset, epochs=2, validation_data=test_dataset)

# --- Evaluate model ---
preds = model.predict(test_dataset).logits
y_pred = tf.math.argmax(preds, axis=1).numpy()

print(classification_report(y_test, y_pred))
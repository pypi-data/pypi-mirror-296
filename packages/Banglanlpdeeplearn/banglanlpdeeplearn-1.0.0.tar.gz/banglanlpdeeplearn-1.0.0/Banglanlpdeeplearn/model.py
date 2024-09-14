import os
os.environ['TF_ENABLE_ONEDNN_OPTS'] = '0'

from sklearn.preprocessing import LabelEncoder
from tensorflow.keras.preprocessing.text import Tokenizer
from tensorflow.keras.preprocessing.sequence import pad_sequences
from sklearn.model_selection import train_test_split
from tensorflow.keras.models import Sequential
from tensorflow.keras.layers import Embedding, Conv1D, GlobalMaxPooling1D, Dense, Dropout, LSTM, Bidirectional

def model_train(df, text_column, label_column):
    encoder = LabelEncoder()
    df[label_column] = encoder.fit_transform(df[label_column])
    
    tokenizer = Tokenizer()
    tokenizer.fit_on_texts(df[text_column])
    sequences = tokenizer.texts_to_sequences(df[text_column])
    max_length = max([len(x) for x in sequences])
    
    X = pad_sequences(sequences, maxlen=max_length, padding='post')
    y = df[label_column]
    
    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)
    
    vocab_size = len(tokenizer.word_index) + 1
    embedding_dim = 64

    # Model 1: Conv1D-based model
    model_conv1d = Sequential([
        Embedding(input_dim=vocab_size, output_dim=embedding_dim, input_length=max_length),
        Conv1D(128, 5, activation='relu'),
        GlobalMaxPooling1D(),
        Dropout(0.5),
        Dense(64, activation='relu'),
        Dense(len(y.unique()), activation='softmax')
    ])

    model_conv1d.compile(optimizer='adam', loss='sparse_categorical_crossentropy', metrics=['accuracy'])
    model_conv1d.fit(X_train, y_train, epochs=15, validation_data=(X_test, y_test), batch_size=32)

    # Model 2: Bidirectional LSTM-based model
    model_lstm = Sequential([
        Embedding(input_dim=vocab_size, output_dim=embedding_dim, input_length=max_length),
        Bidirectional(LSTM(64, return_sequences=True)),
        GlobalMaxPooling1D(),
        Dropout(0.5),
        Dense(64, activation='relu'),
        Dense(len(y.unique()), activation='softmax')
    ])

    model_lstm.compile(optimizer='adam', loss='sparse_categorical_crossentropy', metrics=['accuracy'])
    model_lstm.fit(X_train, y_train, epochs=15, validation_data=(X_test, y_test), batch_size=32)
    
    return model_conv1d, model_lstm, tokenizer, encoder, X_test, y_test, max_length

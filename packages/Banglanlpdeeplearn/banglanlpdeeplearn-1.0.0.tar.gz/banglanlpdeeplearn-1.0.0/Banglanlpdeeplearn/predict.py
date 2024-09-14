import os
os.environ['TF_ENABLE_ONEDNN_OPTS'] = '0'

from keras.preprocessing.sequence import pad_sequences
from .text_process import preprocess_text


def predict_sentiment(text, model, tokenizer, encoder,max_length):
    text_seq = tokenizer.texts_to_sequences([text])
    text_pad = pad_sequences(text_seq, maxlen=max_length, padding='post')
    prediction = model.predict(text_pad)
    predicted_label = encoder.inverse_transform([prediction.argmax(axis=1)[0]])[0]
    return predicted_label

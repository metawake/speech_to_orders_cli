This is a simple Docker container with an app that
listens to audio and records McDonalds orders, 
recorgnizes items and will suggest a coffee if needed.

The app uses TensorFlow, Keras, SpeechRecognition and pyaudio.
Training the model: train_model.py
Using the model: process_stream.py (CLI app, listens to your voice orders and maps them with McDonalds menu).

![Screenshot](https://github.com/metawake/speech_to_orders_cli/blob/master/speech-to-orders.png)

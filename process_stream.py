import speech_recognition as sr
import json
import numpy as np
import speech_recognition as sr
from keras.models import load_model
from keras.preprocessing.sequence import pad_sequences
from keras.preprocessing.text import Tokenizer

# Load the trained model
model = load_model('order_model.h5')
# Initialize tokenizer - this should be the same tokenizer used in training
# Loading tokenizer for prediction
from keras.preprocessing.text import tokenizer_from_json
with open('tokenizer.json') as f:
    data = json.load(f)
    tokenizer = tokenizer_from_json(data)


def predict_additional_item(order):
    # Preprocess the order for prediction
    sequence = tokenizer.texts_to_sequences([order])
    padded_sequence = pad_sequences(sequence, maxlen=100)
    
    # Predict
    prediction = model.predict(padded_sequence)
    class_index = np.argmax(prediction, axis=1)
    
    # Map class index to item
    if class_index == 1:
        return "Coffee"
    elif class_index == 2:
        return "Tea"
    else:
        return None
    
def listen_and_process_order(order):
    # Your existing code to listen and process order
    # Let's assume it returns a string 'order'

    additional_item = predict_additional_item(order)
    
    if additional_item:
        print(f"AI added {additional_item}")
    else:
        print("No additional item suggested by AI")

# Global dictionary of McDonald's products and their prices
PRODUCTS = {
    "Big Mac": 3.99,
    "Quarter Pounder": 3.79,
    "McChicken": 1.29,
    "Filet-O-Fish": 3.79,
    "Nuggets": 4.49,  # Assuming a 10-piece
    "Big Tasty": 4.89,
    "McDouble": 1.39,
    "McRib": 3.69,
    "Apple Pie": 0.99,
    "Cone": 1.00,
    "Fries": 1.79,
    "Shake": 2.19,
    "Coke": 1.00,
    "Sprite": 1.00,
    "Coffee": 1.00,
    "Latte": 2.00,
    "Cappuccino": 2.00,
    "Hot Chocolate": 1.49,
    "Happy Meal": 3.99,
    "Sausage McMuffin": 1.19
}

def listen_and_transcribe(recognizer, source):
    try:
        recognizer.adjust_for_ambient_noise(source)
        print("Listening...")
        audio = recognizer.listen(source, timeout=10, phrase_time_limit=5)
        text = recognizer.recognize_google(audio).lower()
        print("You said: " + text)
        return text
    except sr.WaitTimeoutError:
        print("No speech detected for 10 seconds, starting a new conversation.")
        return None
    except sr.UnknownValueError:
        print("Google Speech Recognition could not understand audio")
        return None
    except sr.RequestError as e:
        print(f"Could not request results from Google Speech Recognition service; {e}")
        return None

def calculate_total(text):
    total = 0
    items = []
    for product in PRODUCTS:
        if product.lower() in text:
            total += PRODUCTS[product]
            items.append(product)
    return total, items

def main():
    recognizer = sr.Recognizer()
    with sr.Microphone() as source:
        conversation_count = 1
        while True:
            print(f"Conversation {conversation_count}:")
            text = listen_and_transcribe(recognizer, source)

            if text:
                total, items = calculate_total(text)
                print(f'processing text={text}')
                listen_and_process_order(items)

                print(f"Items recognized: {items}")
                print(f"Total price: ${total:.2f}")
                conversation_count += 1
            else:
                end_program = input("End program? (yes/no): ").strip().lower()
                if end_program == "yes":
                    break

if __name__ == "__main__":
    main()

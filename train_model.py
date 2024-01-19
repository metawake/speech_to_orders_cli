import numpy as np
from keras.models import Sequential
from keras.layers import Embedding, Flatten, Dense, Dropout
from keras.regularizers import l1_l2
from keras.preprocessing.text import Tokenizer
from keras.preprocessing.sequence import pad_sequences
from keras.utils import to_categorical
from sklearn.model_selection import train_test_split

# Step 1: Read Data from a Text File
def load_data(filename):
    with open(filename, 'r') as file:
        lines = file.readlines()
        orders, labels = [], []
        for line in lines:
            order, label = line.strip().split('->')
            orders.append(order.strip())
            labels.append(label.strip())
        return orders, labels

# Step 2: Preprocess the Data
def preprocess_data(orders, labels):
    tokenizer = Tokenizer()
    tokenizer.fit_on_texts(orders)

    import json
    tokenizer_json = tokenizer.to_json()
    with open('tokenizer.json', 'w', encoding='utf-8') as f:
        f.write(json.dumps(tokenizer_json, ensure_ascii=False))
    
    sequences = tokenizer.texts_to_sequences(orders)
    data = pad_sequences(sequences, maxlen=100)

    # Convert labels to one-hot encoding
    label_dict = {'No': 0, 'Coffee': 1, 'Tea': 2}
    labels = [label_dict[label] for label in labels]
    labels = to_categorical(labels, num_classes=3)

    return data, labels

# Step 3: Build and Train the Model
def build_and_train_model(data, labels):
    model = Sequential()
    model.add(Embedding(1000, 32, input_length=100))  # Reduced complexity
    model.add(Flatten())
    model.add(Dense(64, activation='relu', kernel_regularizer=l1_l2(l1=1e-5, l2=1e-4)))  # Added regularization
    model.add(Dropout(0.5))  # Added dropout
    model.add(Dense(3, activation='softmax'))

    model.compile(optimizer='adam', loss='categorical_crossentropy', metrics=['accuracy'])

    # Split data into training and validation sets
    X_train, X_val, y_train, y_val = train_test_split(data, labels, test_size=0.2, random_state=42)

    from sklearn.utils.class_weight import compute_class_weight
    class_indices = np.argmax(labels, axis=1)

    # Calculate class weights
    class_weights = compute_class_weight(class_weight='balanced', classes=np.unique(class_indices), y=class_indices)
    class_weights_dict = {i : weight for i, weight in enumerate(class_weights)}



    model.fit(X_train, y_train, validation_data=(X_val, y_val), epochs=10, batch_size=32, class_weight=class_weights_dict)

    return model

# Main execution
if __name__ == "__main__":
    orders, labels = load_data('orders.txt')
    data, labels = preprocess_data(orders, labels)
    model = build_and_train_model(data, labels)
    model.save('order_model.h5')

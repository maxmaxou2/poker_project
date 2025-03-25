import onnxruntime
import numpy as np
import cv2

idx_to_class_cards = ['T', '2', '3', '4', '5', '6', '7', '8', '9', 'A', 'J', 'K', 'Q', 'Unknown']
idx_to_class_colors = ['Unknown', 'c', 'd', 'h', 's']
idx_to_class_nbplayers = ['F', 'P']
def load_model(onnx_path):
    # Load the ONNX model
    return onnxruntime.InferenceSession(onnx_path)

def padCenter(rectangle_array, pad_value=0) :
    max_dim = max(rectangle_array.shape)

    if max_dim == rectangle_array.shape[1] :
        # Calculate the required padding for top/bottom sides
        pad_amount = max_dim - rectangle_array.shape[0]
        v = pad_amount//2
        pad_width = ((v, pad_amount-v), (0, 0))
    else:
        # Calculate the required padding for left/right sides
        pad_amount = max_dim - rectangle_array.shape[1]
        v = pad_amount//2
        pad_width = ((0, 0), (v, pad_amount-v))

    # Pad the array randomly to make it square
    padded_array = np.pad(rectangle_array, pad_width=pad_width, mode='constant', constant_values=pad_value)

    return padded_array

def format_input_OCR(image, thresh=180) :
    # Resize the image
    img = cv2.cvtColor(image, cv2.COLOR_RGB2GRAY)
    if thresh is not None :
        img = np.where(img < thresh, 0, 255)
    return img.astype(np.uint8)

def format_input(image, size=(60,60), thresh=110):
    # Resize the image
    img = cv2.cvtColor(image, cv2.COLOR_RGB2GRAY)
    if thresh is not None :
        img = np.where(img < thresh, 0.0, 1.0)
    img = padCenter(img, pad_value=1.0)
    if size is not None :
        img = cv2.resize(img, size)
    img = img[np.newaxis, np.newaxis, :, :]
    img = np.repeat(img, 3, axis=1)
    img = img.astype(np.float32)
    return img

def normalizeToProbabilities(raw_outputs):
    exp_raw_outputs = np.exp(raw_outputs)
    probabilities = exp_raw_outputs / np.sum(exp_raw_outputs)
    return probabilities

def getLabelFromProbabilities(probabilities, idx_to_class):
    index = np.argmax(probabilities)
    return idx_to_class[index], probabilities[index]

def run_inference(model, input):
    return model.run(None, {'input.1': input})

if __name__ == "__main__" :
    path_cards = "./computer_vision/Resnet18_PokerValue_v1.0.onnx"
    path_colors = "./computer_vision/CustomResnet18_PokerColor_v2.4.onnx"
    image_path = "./Images/testInference6.jpg"

    input = format_input(cv2.imread(image_path))
    model_cards = load_model(path_cards)
    model_colors = load_model(path_colors)
    print(run_inference(model_cards, input)[0])
    proba_cards = normalizeToProbabilities(run_inference(model_cards, input)[0])[0]
    proba_colors = normalizeToProbabilities(run_inference(model_colors, input)[0])[0]
    predicted_card, proba_card = getLabelFromProbabilities(proba_cards, idx_to_class_cards)
    predicted_color, proba_color = getLabelFromProbabilities(proba_colors, idx_to_class_colors)
    print("Predicted card {} with {:.3f} and color {} with probability {:.3f}".format(predicted_card, proba_card, predicted_color, proba_color))
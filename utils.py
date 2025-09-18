import torch
import torch.nn as nn
import torch.nn.functional as F
import matplotlib.pyplot as plt
import numpy as np

def plot_adversarial_examples(original, adversarial, predictions_orig, predictions_adv, labels, n_samples=8):
    """
    Plot original and adversarial examples side by side
    """
    fig, axes = plt.subplots(2, n_samples, figsize=(15, 6))
    
    for i in range(n_samples):
        # Original images
        axes[0, i].imshow(original[i].squeeze(), cmap='gray')
        axes[0, i].set_title(f'Original\nPred: {predictions_orig[i]}\nTrue: {labels[i]}')
        axes[0, i].axis('off')
        
        # Adversarial images
        axes[1, i].imshow(adversarial[i].squeeze(), cmap='gray')
        axes[1, i].set_title(f'Adversarial\nPred: {predictions_adv[i]}\nTrue: {labels[i]}')
        axes[1, i].axis('off')
    
    plt.tight_layout()
    plt.show()

def plot_perturbations(original, adversarial, n_samples=8):
    """
    Plot the perturbations (difference between original and adversarial)
    """
    perturbations = adversarial - original
    
    fig, axes = plt.subplots(1, n_samples, figsize=(15, 3))
    
    for i in range(n_samples):
        axes[i].imshow(perturbations[i].squeeze(), cmap='RdBu', vmin=-0.3, vmax=0.3)
        axes[i].set_title(f'Perturbation {i+1}')
        axes[i].axis('off')
    
    plt.tight_layout()
    plt.show()

def calculate_attack_success_rate(original_preds, adversarial_preds, true_labels):
    """
    Calculate the attack success rate
    """
    # Original predictions should be correct
    original_correct = (original_preds == true_labels)
    
    # Adversarial predictions should be different from original
    attack_successful = (original_preds != adversarial_preds) & original_correct
    
    success_rate = attack_successful.float().mean().item()
    return success_rate * 100  # Return as percentage

def denormalize_image(tensor, mean=[0.485, 0.456, 0.406], std=[0.229, 0.224, 0.225]):
    """
    Denormalize image tensor for display
    """
    mean = torch.tensor(mean).view(3, 1, 1)
    std = torch.tensor(std).view(3, 1, 1)
    return tensor * std + mean

def show_image_with_prediction(image, prediction, confidence, title="Image"):
    """
    Display image with prediction and confidence
    """
    plt.figure(figsize=(8, 6))
    if len(image.shape) == 3 and image.shape[0] == 3:
        # RGB image
        plt.imshow(image.permute(1, 2, 0))
    else:
        # Grayscale image
        plt.imshow(image.squeeze(), cmap='gray')
    
    plt.title(f'{title}\nPrediction: {prediction}\nConfidence: {confidence:.3f}')
    plt.axis('off')
    plt.show()

class ImageClassificationHelper:
    """
    Helper class for image classification tasks
    """
    
    @staticmethod
    def get_top_predictions(outputs, classes, top_k=5):
        """Get top-k predictions from model outputs"""
        probabilities = F.softmax(outputs, dim=1)
        top_prob, top_indices = torch.topk(probabilities, top_k)
        
        results = []
        for i in range(top_k):
            results.append({
                'class': classes[top_indices[0][i]],
                'confidence': top_prob[0][i].item()
            })
        return results
    
    @staticmethod
    def visualize_predictions(predictions, title="Top Predictions"):
        """Visualize top predictions as horizontal bar chart"""
        class_names = [p['class'] for p in predictions]
        confidences = [p['confidence'] for p in predictions]
        
        plt.figure(figsize=(10, 6))
        plt.barh(class_names, confidences)
        plt.title(title)
        plt.xlabel('Confidence')
        plt.tight_layout()
        plt.show()

# Attack evaluation utilities
def evaluate_attack_robustness(model, original_images, adversarial_images, true_labels, classes):
    """
    Comprehensive evaluation of adversarial attack robustness
    """
    model.eval()
    
    with torch.no_grad():
        # Get predictions for original images
        orig_outputs = model(original_images)
        orig_preds = torch.argmax(orig_outputs, dim=1)
        
        # Get predictions for adversarial images
        adv_outputs = model(adversarial_images)
        adv_preds = torch.argmax(adv_outputs, dim=1)
    
    # Calculate metrics
    original_accuracy = (orig_preds == true_labels).float().mean().item()
    adversarial_accuracy = (adv_preds == true_labels).float().mean().item()
    
    # Attack success rate (among correctly classified original samples)
    correctly_classified = (orig_preds == true_labels)
    attack_success = (orig_preds != adv_preds) & correctly_classified
    success_rate = attack_success.float().mean().item() if correctly_classified.sum() > 0 else 0.0
    
    results = {
        'original_accuracy': original_accuracy * 100,
        'adversarial_accuracy': adversarial_accuracy * 100,
        'attack_success_rate': success_rate * 100,
        'robustness_drop': (original_accuracy - adversarial_accuracy) * 100
    }
    
    return results

#!/usr/bin/env python3
"""
KiloTap Junk vs Waste Classifier — Training Script
Uses MobileNetV2 transfer learning on Kaggle garbage dataset.
Outputs TensorFlow.js format for browser deployment.
"""

import tensorflow as tf
from tensorflow import keras
from tensorflow.keras import layers, models
from tensorflow.keras.preprocessing.image import ImageDataGenerator
import os, json, shutil

# ============================================================================
# CONFIGURATION
# ============================================================================
DATASET_PATH = "/root/kilotap-simulation/assets/kaggle/garbage classification/Garbage classification"
OUTPUT_DIR = "/root/kilotap-simulation/model"
IMG_SIZE = (224, 224)
BATCH_SIZE = 32
EPOCHS = 10
LEARNING_RATE = 0.0005

# Philippine junk shop classification:
# JUNK: metal (bakal, tanso, aluminum, yero) — heavy, high value
# WASTE: cardboard, paper, plastic, glass, trash — light, low value
CLASSES = {
    'metal': 'junk',
    'cardboard': 'waste',
    'paper': 'waste',
    'plastic': 'waste',
    'glass': 'waste',
    'trash': 'waste',
}

# ============================================================================
# STEP 1: Organize images into junk/ and waste/ directories
# ============================================================================
print("=" * 60)
print("STEP 1: Organizing training data...")
print("=" * 60)

TRAIN_DIR = "/tmp/kilotap_train"
os.makedirs(f"{TRAIN_DIR}/junk", exist_ok=True)
os.makedirs(f"{TRAIN_DIR}/waste", exist_ok=True)

counts = {'junk': 0, 'waste': 0}
for class_name, category in CLASSES.items():
    src_dir = os.path.join(DATASET_PATH, class_name)
    if not os.path.exists(src_dir):
        print(f"  SKIP: {src_dir} not found")
        continue
    
    files = [f for f in os.listdir(src_dir) if f.lower().endswith(('.jpg','.jpeg','.png'))]
    # Limit to 350 images per class to balance
    files = files[:350]
    
    for f in files:
        dst = os.path.join(TRAIN_DIR, category, f"{class_name}_{f}")
        shutil.copy2(os.path.join(src_dir, f), dst)
        counts[category] += 1
    
    print(f"  {class_name} -> {category}: {len(files)} images")

print(f"\n  TOTAL: junk={counts['junk']}, waste={counts['waste']}")

# ============================================================================
# STEP 2: Create data generators with augmentation
# ============================================================================
print("\n" + "=" * 60)
print("STEP 2: Creating data generators...")
print("=" * 60)

# Split into train/validation
datagen = ImageDataGenerator(
    rescale=1.0/255.0,
    rotation_range=20,
    width_shift_range=0.2,
    height_shift_range=0.2,
    shear_range=0.2,
    zoom_range=0.2,
    horizontal_flip=True,
    fill_mode='nearest',
    validation_split=0.2
)

train_gen = datagen.flow_from_directory(
    TRAIN_DIR,
    target_size=IMG_SIZE,
    batch_size=BATCH_SIZE,
    class_mode='binary',
    subset='training',
    shuffle=True
)

val_gen = datagen.flow_from_directory(
    TRAIN_DIR,
    target_size=IMG_SIZE,
    batch_size=BATCH_SIZE,
    class_mode='binary',
    subset='validation',
    shuffle=False
)

print(f"  Classes: {train_gen.class_indices}")
print(f"  Train batches: {len(train_gen)}, Val batches: {len(val_gen)}")

# ============================================================================
# STEP 3: Build model (MobileNetV2 transfer learning)
# ============================================================================
print("\n" + "=" * 60)
print("STEP 3: Building MobileNetV2 model...")
print("=" * 60)

base_model = tf.keras.applications.MobileNetV2(
    input_shape=(224, 224, 3),
    include_top=False,
    weights='imagenet'
)
base_model.trainable = False  # Freeze base

model = models.Sequential([
    base_model,
    layers.GlobalAveragePooling2D(),
    layers.Dropout(0.3),
    layers.Dense(128, activation='relu'),
    layers.Dropout(0.3),
    layers.Dense(1, activation='sigmoid')  # Binary: 0=waste, 1=junk
])

model.compile(
    optimizer=keras.optimizers.Adam(learning_rate=LEARNING_RATE),
    loss='binary_crossentropy',
    metrics=['accuracy']
)

model.summary()

# ============================================================================
# STEP 4: Train
# ============================================================================
print("\n" + "=" * 60)
print(f"STEP 4: Training ({EPOCHS} epochs)...")
print("=" * 60)

history = model.fit(
    train_gen,
    validation_data=val_gen,
    epochs=EPOCHS,
    verbose=1
)

# ============================================================================
# STEP 5: Fine-tune (unfreeze top layers)
# ============================================================================
print("\n" + "=" * 60)
print("STEP 5: Fine-tuning...")
print("=" * 60)

base_model.trainable = True
# Freeze first 100 layers, fine-tune the rest
for layer in base_model.layers[:100]:
    layer.trainable = False

model.compile(
    optimizer=keras.optimizers.Adam(learning_rate=LEARNING_RATE / 10),
    loss='binary_crossentropy',
    metrics=['accuracy']
)

history_ft = model.fit(
    train_gen,
    validation_data=val_gen,
    epochs=5,
    verbose=1
)

# ============================================================================
# STEP 6: Evaluate
# ============================================================================
print("\n" + "=" * 60)
print("STEP 6: Evaluating...")
print("=" * 60)

loss, acc = model.evaluate(val_gen, verbose=0)
print(f"  Validation accuracy: {acc:.4f} ({acc*100:.1f}%)")
print(f"  Validation loss: {loss:.4f}")

# ============================================================================
# STEP 7: Save model
# ============================================================================
print("\n" + "=" * 60)
print("STEP 7: Saving model...")
print("=" * 60)

os.makedirs(OUTPUT_DIR, exist_ok=True)

# Save Keras model
model.save(f"{OUTPUT_DIR}/kilotap_classifier.keras")
print(f"  Saved: {OUTPUT_DIR}/kilotap_classifier.keras")

# Save class labels
with open(f"{OUTPUT_DIR}/classes.json", 'w') as f:
    json.dump({'0': 'waste', '1': 'junk'}, f)
print(f"  Saved: {OUTPUT_DIR}/classes.json")

# ============================================================================
# STEP 8: Convert to TensorFlow.js
# ============================================================================
print("\n" + "=" * 60)
print("STEP 8: Converting to TensorFlow.js...")
print("=" * 60)

import subprocess, sys

# Install tensorflowjs if needed
subprocess.run([sys.executable, '-m', 'pip', 'install', 'tensorflowjs'], 
               capture_output=True)

# Convert
result = subprocess.run([
    'tensorflowjs_converter',
    '--input_format=keras',
    f'{OUTPUT_DIR}/kilotap_classifier.keras',
    f'{OUTPUT_DIR}/tfjs'
], capture_output=True, text=True)

if result.returncode == 0:
    print(f"  TFJS model saved to: {OUTPUT_DIR}/tfjs/")
    # List files
    for f in os.listdir(f"{OUTPUT_DIR}/tfjs/"):
        size = os.path.getsize(f"{OUTPUT_DIR}/tfjs/{f}")
        print(f"    {f} ({size:,} bytes)")
else:
    print(f"  Conversion failed: {result.stderr}")
    print("  The Keras model is still usable at:", f"{OUTPUT_DIR}/kilotap_classifier.keras")

# ============================================================================
# DONE
# ============================================================================
print("\n" + "=" * 60)
print("TRAINING COMPLETE")
print("=" * 60)
print(f"  Model: {OUTPUT_DIR}/kilotap_classifier.keras")
print(f"  TFJS:  {OUTPUT_DIR}/tfjs/")
print(f"  Val Accuracy: {acc:.1%}")

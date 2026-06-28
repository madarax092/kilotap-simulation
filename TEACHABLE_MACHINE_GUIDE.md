# KiloTap Teachable Machine Training Guide

## Overview

COCO-SSD detects generic objects (person, bottle, chair). It can't distinguish 
Philippine junk shop items like "bakal" (scrap iron) from "karton" (cardboard).

**Solution:** Train a custom image classifier using Google Teachable Machine 
that knows the difference between JUNK and WASTE based on Philippine categories.

---

## Step 1: Prepare Training Images

Your Kaggle dataset provides 2,527 images across 6 classes:

| Source Folder | Count | Classify As | Philippine Term |
|--------------|-------|-------------|-----------------|
| `metal/` | 410 | **JUNK** | Bakal, tanso, aluminum, yero |
| `cardboard/` | 403 | WASTE | Karton |
| `paper/` | 594 | WASTE | Papel, dyaryo |
| `plastic/` | 482 | WASTE | Bote plastic, plastic container |
| `glass/` | 501 | WASTE | Bote, broken glass |
| `trash/` | 137 | WASTE | Mixed trash |

---

## Step 2: Train on Teachable Machine

1. Go to: **https://teachablemachine.withgoogle.com/train/image**

2. **Create two classes:**
   - Class 1: Name it **"JUNK"**
   - Class 2: Name it **"WASTE"**

3. **Upload images for JUNK:**
   - Upload all images from `metal/` folder (410 images)
   - These represent: scrap metal, aluminum, appliances, copper wire, batteries
   
4. **Upload images for WASTE:**
   - Upload 100-200 images each from `cardboard/`, `paper/`, `plastic/`, `glass/`, `trash/`
   - Mix them together so the model generalizes
   - Total: ~500-800 images recommended

5. **Training settings:**
   - Epochs: 50
   - Batch size: 16
   - Learning rate: default

6. **Click "Train Model"** — takes 2-5 minutes

7. **Test:** Use the preview window to test with a few images

8. **Export:**
   - Click "Export Model"
   - Select "TensorFlow.js" tab
   - Click "Download"
   - You'll get: `model.json`, `weights.bin`, and `metadata.json`
   - Send these 3 files to me

---

## Step 3: Integration

Once you send me the model files, I will:
1. Replace COCO-SSD with your custom Teachable Machine model
2. The model will directly classify images as JUNK or WASTE
3. No more generic "bottle"/"chair" labels — actual Philippine categories
4. Detection will be faster and more accurate

---

## File Path Reference

Your Kaggle images are at:
```
kilotap-simulation/assets/kaggle/garbage classification/Garbage classification/
├── cardboard/ (403)
├── glass/     (501)
├── metal/     (410) ← USE FOR JUNK
├── paper/     (594)
├── plastic/   (482)
└── trash/     (137)
```

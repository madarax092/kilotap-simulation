# KiloTap — Available Training Datasets

## Already Downloaded

### 1. Recyclable and Household Waste (30 Classes)
- **Kaggle:** alistairking/recyclable-and-household-waste-classification
- **Size:** 15,000 images (500/class), 920MB
- **Type:** Classification
- **Status:** Downloaded, TFJS model trained (82.5%)
- **Path:** `assets/recyclable_30class/`

### 2. Garbage Classification (6 Classes)
- **Kaggle:** asdasdasasdas/garbage-classification
- **Size:** 2,527 images
- **Type:** Classification
- **Status:** Downloaded
- **Path:** `assets/kaggle/`

---

## Available (Not Yet Downloaded)

### 3. E-Waste Classification (18 Classes) — RECOMMENDED
- **Kaggle:** harshadsgore/e-waste-image-classification-dataset-18-classes
- **Size:** ~9,000 images (500/class)
- **Type:** Classification
- **Why:** Directly matches electronics photos (monitor, CPU, keyboard, mouse, printer)
- **KiloTap fit:** CPU, monitor, keyboard, mouse → Junk (electronics)

### 4. Roboflow E-Waste Detection (54 Classes) — BEST FOR DETECTION
- **Roboflow:** electronic-waste-detection/e-waste-dataset-r0ojc
- **Size:** 7,216 images with bounding box annotations
- **Type:** Object Detection (annotated bounding boxes!)
- **Why:** Has actual bounding box coordinates — enables true object detection
- **KiloTap fit:** Can detect AND locate items in photos

### 5. RealWaste (9 Material Types)
- **GitHub:** AgaMiko/waste-datasets-review
- **Size:** 4,752 images (524x524)
- **Types:** Cardboard, Food Organics, Glass, Metal, Misc Trash, Paper, Plastic, Textile, Vegetation
- **Type:** Classification + detection

### 6. Garbage Classification v2 (10 Classes)
- **Kaggle:** sumn2u/garbage-classification-v2
- **Size:** Unknown
- **Type:** Classification

---

## For Future Object Detection Training

### Recommended Pipeline:
1. Download **Roboflow E-Waste Dataset** (bounding boxes included)
2. Download **E-Waste 18-Class** Kaggle dataset
3. Merge with existing Kaggle data
4. Train a proper object detection model (YOLO/SSD format)
5. Convert to TensorFlow.js for browser

### Classes to Prioritize for KiloTap:
| Class | Type | Source |
|-------|------|--------|
| CPU/Tower | Junk | E-Waste 18-Class |
| Monitor/LCD | Junk | E-Waste 18-Class + Roboflow |
| Keyboard/Mouse | Junk | E-Waste 18-Class |
| Refrigerator | Junk | Need separate dataset |
| Washing Machine | Junk | Need separate dataset |
| Air Conditioner | Junk | Need separate dataset |
| Scrap Metal | Junk | Garbage Classification (metal/) |
| Copper Wire | Junk | Web scraping needed |
| Cardboard | Waste | Recyclable 30-Class |
| Plastic Bottle | Waste | Recyclable 30-Class |
| Plastic Bag | Waste | Recyclable 30-Class |

<div align="center">

# 🌱 KRISHI MITRA  
### AI-Enabled Selective Weed Identification & Removal System

**An autonomous, chemical-free precision agriculture solution powered by AI and robotics**

</div>

---

📖 Abstract

Agriculture remains the backbone of India’s economy, supporting nearly half of the population while contributing significantly to the national GDP. One of the most persistent challenges in crop cultivation is weed infestation, which competes with crops for nutrients, water, and sunlight, resulting in yield losses of **25–40%**.

**KRISHI MITRA** is an AI-driven autonomous robotic rover designed to identify, classify, and selectively remove harmful weeds while preserving crops and beneficial vegetation. By combining computer vision, machine learning, robotics, and real-time decision making, the system provides an efficient, scalable, and environmentally sustainable alternative to conventional weed control practices.

---

## 🎯 Project Objectives

- 🚜 Autonomous navigation in agricultural fields  
- 🧠 AI-based plant classification using deep learning  
- 🌿 Differentiation between **Crop**, **Good Weed**, and **Bad Weed**  
- 🦾 Selective mechanical removal of harmful weeds  
- 🌍 Elimination of chemical herbicides  
- 📈 Improvement in crop yield and soil health  
- 🧑‍🌾 Affordable and accessible solution for farmers  

---

## ✨ Key Innovations

### 🌱 Three-Level Plant Classification
- **Crop** – Main cultivated plant  
- **Good Weed** – Beneficial or low-competition species  
- **Bad Weed** – Aggressive and harmful species  

### 🧠 AI-Powered Vision System
- Custom-trained **Convolutional Neural Network (CNN)**
- Dataset curated from:
  - Real-world field images
  - Public datasets (Kaggle)
  - Agricultural research sources (Plantix)

### 🦾 Selective Robotic Weed Removal
- Robotic manipulator with:
  - Forward & inverse kinematics
  - Jacobian-based trajectory planning
- Precise plucking without disturbing crops

### 🌍 Chemical-Free Agriculture
- Zero herbicide usage  
- Environment-friendly operation  
- Promotes sustainable farming practices  

### 🔗 Integrated Robotics Architecture
- Four-wheel mobile rover
- Real-time vision processing
- ESP32-controlled motor drivers
- Raspberry Pi as central processing unit
- Data transmission to farmer-facing application

🚀 Future-Ready Design
- ROS 2 compatible architecture
- Modular hardware & software upgrades
- Support for GPS / RTK integration

---

## 🧪 Methodology

### 📷 Data Collection & Annotation
- Field images captured from paddy, wheat, and potato crops
- Diverse lighting and environmental conditions
- Supplemented with Kaggle datasets
- Manual annotation using **LabelImg**
- Three-class labeling: Crop / Good Weed / Bad Weed

### 🧠 Machine Learning Model
- CNN trained with:
  - Image resizing & normalization
  - Data augmentation
  - Multi-epoch training and validation
- Optimized for real-time inference on embedded hardware

### 🚜 Robotic Rover
- Four-wheel drive chassis for uneven terrain
- High-torque motors
- Wi-Fi controlled via ESP32
- Expandable for autonomous navigation

### 🦾 Robotic Manipulator
- Designed based on weed height and growth patterns
- DH-parameter based kinematic modeling
- Smooth, collision-free plucking trajectories

### 🔄 System Workflow
1. Camera captures live field frames  
2. CNN classifies plant type  
3. Harmful weed detected  
4. Robotic arm activated  
5. Weed removed and collected  
6. Crops and good weeds left untouched  

---

## 📊 Results

- ✅ Accurate real-time weed detection  
- ✅ Reliable classification into three categories  
- ✅ Selective plucking without crop damage  
- ⏱ Processing time: ~3–5 seconds per plant  
- 🌱 Successfully tested in small-scale field conditions  

---

## 🌾 Field Deployment

KRISHI MITRA has been tested in real agricultural environments, including:
- Paddy fields
- Potato crop fields

Field trials provided valuable insights into terrain variation, weed density, and real-world operational constraints, validating the system’s practical applicability.

---

## 📈 Impact & Benefits

- **25–40% increase** in crop productivity  
- **0% chemical herbicide usage**  
- Reduced labor dependency  
- Improved soil health  
- Sustainable and farmer-friendly solution  

---

## 🔮 Future Scope

- Full autonomous navigation using GPS / RTK  
- Advanced crop health analytics  
- Large-scale field deployment  
- Mobile & web dashboards for farmers  
- ROS 2-based autonomous decision making  

---

## 🤝 Acknowledgements

- Kaggle – Dataset resources  
- Plantix – Agricultural reference and weed research  
- Open-source robotics and ML communities  

---

## 📜 License

This project is developed for academic and research purposes.  
License details will be updated in future releases.

---

<div align="center">

**🌱 Precision Agriculture through Intelligence & Robotics 🌱**

</div>

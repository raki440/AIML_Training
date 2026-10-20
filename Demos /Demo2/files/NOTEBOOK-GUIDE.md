# MLOps Training Hands-On Notebook Guide
## Complete End-to-End ML Pipeline for Freshers

---

## 📋 What's Inside

This Jupyter notebook (`MLOps-Training-Session1to5-Hands-On.ipynb`) is a **complete hands-on tutorial** covering Sessions 1-5 of the MLOps training.

**Total: 12 steps across ~200 lines of well-commented code**

---

## 🎯 Objectives

By running this notebook, you will:

1. ✅ Load and explore real data with **Pandas**
2. ✅ Understand data quality and cleaning
3. ✅ Build a Machine Learning model with **scikit-learn**
4. ✅ Evaluate model performance with multiple metrics
5. ✅ Track experiments with **MLflow**
6. ✅ Make predictions on new data
7. ✅ Understand why MLOps matters

---

## 📊 Dataset: Iris Flower Classification

- **Size:** 150 samples, 4 features, 3 classes
- **Features:** Sepal length, sepal width, petal length, petal width
- **Target:** Flower type (Setosa, Versicolor, Virginica)
- **Why Iris?** Perfect for learning - small, clean, classic dataset

---

## 🔧 Step-by-Step Breakdown

### **Step 1: Install Libraries**
```python
pip install pandas numpy scikit-learn matplotlib seaborn mlflow
```
Import all required packages.

### **Step 2: Load Data with Pandas**
```python
df = pd.read_csv('iris.csv')  # or load_iris()
print(df.head())  # See first 5 rows
```
**Learn:** What is a DataFrame? What are rows and columns?

### **Step 3: Explore Data**
```python
df.describe()      # Statistics
df.info()          # Data types
df.isnull().sum()  # Missing values
df.value_counts()  # Class distribution
```
**Learn:** How to understand data before training.

### **Step 4: Visualize Data**
```python
plt.hist(df['sepal_length'])
sns.heatmap(correlation_matrix)
```
**Learn:** What distributions look like. Find patterns visually.

### **Step 5: Prepare Data**
```python
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.3)
X_scaled = StandardScaler().fit_transform(X_train)
```
**Learn:** 
- **Train/test split:** 70% train, 30% test
- **Feature scaling:** Normalize to [0,1] range
- **Why?** Prevents overfitting, fair evaluation

### **Step 6: Build Model**
```python
model = RandomForestClassifier(n_estimators=100, max_depth=5)
model.fit(X_train_scaled, y_train)
```
**Learn:**
- Random Forest = ensemble of 100 decision trees
- Each tree votes, majority wins
- Hyperparameters: n_estimators, max_depth

### **Step 7: Make Predictions**
```python
y_pred = model.predict(X_test_scaled)
y_pred_proba = model.predict_proba(X_test_scaled)  # Confidence scores
```
**Learn:** Predictions can be class (0,1,2) or probabilities (0.95, 0.04, 0.01)

### **Step 8: Evaluate Model**
```python
accuracy = accuracy_score(y_test, y_pred)
precision = precision_score(y_test, y_pred, average='weighted')
recall = recall_score(y_test, y_pred, average='weighted')
f1 = f1_score(y_test, y_pred, average='weighted')
```
**Learn:** 4 key metrics
- **Accuracy:** Overall correctness
- **Precision:** Of positive predictions, how many were right?
- **Recall:** Of actual positives, how many did we find?
- **F1:** Balanced metric (harmonic mean of precision & recall)

### **Step 9: Confusion Matrix**
```python
cm = confusion_matrix(y_test, y_pred)
# Visualize where model goes wrong
```
**Learn:** Diagonal = correct. Off-diagonal = wrong predictions.

### **Step 10: Feature Importance**
```python
model.feature_importances_
# Which features matter most for predictions?
```
**Learn:** Not all features are equally important.

### **Step 11: Track with MLflow**
```python
mlflow.start_run()
mlflow.log_param('n_estimators', 100)
mlflow.log_metric('accuracy', 0.96)
mlflow.sklearn.log_model(model, 'model')
```
**Learn:** MLflow = logbook for ML experiments. Compare multiple runs.

### **Step 12: Make New Predictions**
```python
new_flower = [[5.1, 3.5, 1.4, 0.2]]
prediction = model.predict(new_flower_scaled)
probabilities = model.predict_proba(new_flower_scaled)
```
**Learn:** Real-world usage - predict on new, unseen data.

---

## 🚀 How to Run

### **Option 1: Local Machine**
```bash
# Install Jupyter
pip install jupyter

# Navigate to notebook folder
cd /path/to/notebooks

# Start Jupyter
jupyter notebook

# Open: MLOps-Training-Session1to5-Hands-On.ipynb
# Click "Kernel" → "Run All" (or run cell by cell)
```

### **Option 2: Google Colab (Free, No Installation)**
```bash
1. Upload notebook to Google Drive
2. Open with Google Colab
3. Runtime → Run All Cells
```

### **Option 3: VS Code**
```bash
# Install extension: "Jupyter" by Microsoft
# Open .ipynb file → Run cells in interactive mode
```

---

## 📈 Expected Output

When you run the complete notebook, you'll see:

1. ✅ Dataset info (150 rows, 4 features)
2. ✅ Statistical summary (mean, std, min, max)
3. ✅ 4 visualizations (distributions, heatmap, class balance)
4. ✅ Train/test split confirmation (105 train, 45 test)
5. ✅ Model metrics (e.g., Accuracy: 0.9556)
6. ✅ Confusion matrix heatmap
7. ✅ Feature importance bar chart
8. ✅ MLflow logging confirmation
9. ✅ Single prediction example
10. ✅ Summary with next steps

---

## 🎓 Key Concepts Explained Simply

### **Pandas**
- Think of it as Excel in Python
- Load data: `pd.read_csv('file.csv')`
- Explore: `df.head()`, `df.describe()`, `df.info()`

### **Train/Test Split**
```
Original data (150)
    ↓
Train (105) → Train model
Test (45)   → Evaluate model
```
**Why?** Can't evaluate on training data (overfitting)

### **Feature Scaling**
```
Before: sepal_length = [4.3, 7.9]  (range: 4.3-7.9)
After:  sepal_length = [0.0, 1.0]  (range: 0-1)
```
**Why?** Some algorithms work better with normalized features

### **Random Forest**
```
100 trees
  Tree 1 → Predicts: Setosa (votes: +1)
  Tree 2 → Predicts: Setosa (votes: +1)
  Tree 3 → Predicts: Versicolor (votes: 0)
  ...
  Final: 67 trees vote Setosa → RESULT: Setosa
```
**Why?** Ensemble = more robust than single tree

### **Confusion Matrix**
```
           Predicted
           Setosa  Versicolor  Virginica
Actual
Setosa       15         0           0      ✓ All correct
Versicolor    0        14           1      ✓ Mostly correct
Virginica     0         1          14      ✓ Mostly correct
```
**Interpretation:** Off-diagonal = misclassifications

---

## 🔍 Customization Ideas

### **Try Different Models**
```python
# Replace RandomForestClassifier with:
from sklearn.svm import SVC
from sklearn.neighbors import KNeighborsClassifier
from sklearn.ensemble import GradientBoostingClassifier

model = GradientBoostingClassifier()  # Try this!
```

### **Change Hyperparameters**
```python
# Original
RandomForestClassifier(n_estimators=100, max_depth=5)

# Try this
RandomForestClassifier(n_estimators=200, max_depth=10)
```

### **Use Different Dataset**
```python
# Instead of Iris:
from sklearn.datasets import load_wine, load_breast_cancer
data = load_wine()  # Wine classification
# Rest of code stays the same!
```

### **Add More Visualizations**
```python
# Scatter plot
plt.scatter(df['sepal_length'], df['sepal_width'], c=df['target'])

# Box plot by class
df.boxplot(column='sepal_length', by='target_name')
```

---

## ⚠️ Common Issues & Solutions

| Issue | Solution |
|-------|----------|
| `ModuleNotFoundError: No module named 'pandas'` | Run: `pip install pandas` |
| `ImportError: cannot import name 'load_iris'` | Ensure scikit-learn is installed: `pip install scikit-learn` |
| `MLflow UI not accessible` | Run: `mlflow ui` in terminal, then visit `localhost:5000` |
| `Model accuracy is low (<70%)` | Try different model or tune hyperparameters |
| `Out of memory` | Use smaller dataset or reduce features |

---

## 📚 Next Steps After This Notebook

1. **Week 1-2:** Run notebook multiple times, modify hyperparameters, see results change
2. **Week 3:** Try on different datasets (Wine, Breast Cancer, Customer Churn)
3. **Week 4:** Build your first data pipeline (DVC)
4. **Week 5:** Deploy model as API (FastAPI)
5. **Week 6:** Containerize with Docker
6. **Week 7:** Deploy to Kubernetes
7. **Week 8+:** Production monitoring, retraining, A/B testing

---

## 🎯 Learning Outcomes

After completing this notebook, you'll understand:

✅ How to load and explore data  
✅ Why train/test split is important  
✅ How to build and train ML models  
✅ What metrics mean (accuracy, precision, recall, F1)  
✅ Why MLflow is essential for reproducibility  
✅ How to make predictions on new data  
✅ Where 95% of production ML effort goes (data + infrastructure)  

---

## 📞 Quick Reference Commands

```python
# Load data
import pandas as pd
df = pd.read_csv('file.csv')

# Explore
df.head()
df.describe()
df.isnull().sum()

# Split
from sklearn.model_selection import train_test_split
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.3)

# Scale
from sklearn.preprocessing import StandardScaler
scaler = StandardScaler()
X_scaled = scaler.fit_transform(X)

# Train
from sklearn.ensemble import RandomForestClassifier
model = RandomForestClassifier()
model.fit(X_train, y_train)

# Evaluate
from sklearn.metrics import accuracy_score
accuracy = accuracy_score(y_test, model.predict(X_test))

# Track
import mlflow
mlflow.log_metric('accuracy', accuracy)
mlflow.sklearn.log_model(model, 'model')

# Predict
prediction = model.predict([[5.1, 3.5, 1.4, 0.2]])
```

---

## ✨ Happy Learning!

This notebook is your gateway to production ML. Master it, then scale it! 🚀

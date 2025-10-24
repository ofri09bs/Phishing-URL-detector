# Phishing URL Detection Project

This project utilizes machine learning to classify URLs as either "legitimate" (good) or "phishing" (bad).

The model is trained on a dataset of URLs and employs a feature engineering process to identify suspicious patterns within the URL string itself, rather than relying on the website's content.

## 🚀 Feature Engineering

The core of this project is the extraction of a robust set of features from each URL. The primary features engineered for each URL include:

* **`length`**: The total length of the URL string.
* **`num_special_chars`**: The count of special characters (e.g., `?`, `&`, `%`, `-`).
* **`suswords_count`**: The number of suspicious keywords found (e.g., 'login', 'paypal', 'security', 'verify').
* **`num_subdomains`**: The count of subdomains.
* **`num_digits`**: The count of numeric digits in the URL.
* **`has_https`**: A binary feature indicating whether the URL uses HTTPS.
* ...and several others.

## 📊 Model and Results

After evaluating several models, a `RandomForestClassifier` from the Scikit-learn library was selected for its superior performance on the engineered features.

Given that the dataset is imbalanced (containing more legitimate URLs than phishing URLs), the `class_weight='balanced'` parameter was used during model training.

**Final Performance on the Test Set:**

            precision   recall   f1-score   support

     bad       0.57      0.73      0.64     31200
    good       0.88      0.78      0.83     78670

accuracy                           0.77    109870
(you can see full resaults in the file)

## 🛠️ Technologies & Libraries

* Python 3
* Pandas (For data manipulation and analysis)
* Scikit-learn (sklearn) (For feature engineering, model training, and evaluation)
* Matplotlib / Seaborn (For data visualization)
* Jupyter Notebook / Google Colab (As the development environment)

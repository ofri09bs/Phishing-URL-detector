import tkinter as tk
from tkinter import font
import joblib
import pandas as pd
from urllib.parse import urlparse

# Load the pre-trained model
model = joblib.load('phishing_model4.pkl')

suswords = [
    'login', 'signin', 'verify', 'account', 'password',
    'secure', 'security', 'update', 'confirm', 'banking',
    'paypal','support', 'admin', 'service', 'webscr','bank'
]

sus_suffixes = [
    '.tk', '.ml', '.ga', '.cf', '.gq', '.zip', '.ru', '.xyz','.php'
]

def count_words(url):
  count = 0
  for word in suswords:
    if word in url.lower():
      count += 1
  return count

def has_sus_suffix(url):
  for suffix in sus_suffixes:
    if url.lower().endswith(suffix):
      return 1
  return 0



def extract_features(url):
  features = {}
  features['length'] = len(url)
  features['count_dots'] = url.count('.')
  features['count_dashes'] = url.count('-')
  features['has_https'] = int(url.startswith('https'))
  features['has_at'] = int('@' in url)
  features['has_www'] = int(url.startswith('www'))
  features['has_ip'] = int(url.replace('.', '').isdigit())
  parsed_url = urlparse(url)
  hostname = parsed_url.hostname if parsed_url.hostname else ''
  parts = hostname.split('.')
  num_subdomains = len(parts) - 2 
  features['num_of_subdomains'] = max(0, num_subdomains)
  features['path_slashes'] = parsed_url.path.count('/')
  features['double_slash_in_path'] = int('//' in parsed_url.path)
  features['suswords_count'] = count_words(url)
  features['has_sus_suffix'] = has_sus_suffix(url)

  features_name = model.feature_names_in_
  features = pd.DataFrame([features], columns=features_name)
  features = features.fillna(0)

  return features

# Create the main window
root = tk.Tk()
root.title("Phishing URL Detector")
root.geometry("500x300")
root.config(bg="#f0f0f0")

title_font = font.Font(family="Arial", size=16, weight="bold")
label_font = font.Font(family="Arial", size=12)
resault_font = font.Font(family="Arial", size=12, weight="bold")

title_label = tk.Label(root, text="Enter URL to check:", font=title_font, bg="#f0f0f0")
title_label.pack(pady=20)

url_entry = tk.Entry(root, width=50, font=label_font,relief='solid', bd=1)
url_entry.pack(pady=5, ipady=5, padx=20)

resault_label = tk.Label(root, text="", font=resault_font, bg="#f0f0f0",height=3)


def predict_url():
    url = url_entry.get()
    if not url:
        resault_label.config(text="Please enter a URL.")
        return
    
    features_df = extract_features(url)
    if features_df is None:
        resault_label.config(text="Invalid URL format.")
        return
    
    print("--- DEBUG: Features sent to model ---")
    print(features_df.to_string())
    print("---------------------------------")
    
    prediction = model.predict(features_df)[0]
    prediction_proba = model.predict_proba(features_df)
    confidence = max(prediction_proba[0]) * 100
    if prediction == 'good':
        resault_label.config(text=f"✅Safe: The URL is Legitimate with {confidence:.2f}% confidence.")
    else:
        resault_label.config(text=f"🚨Danger: The URL is Phishing with {confidence:.2f}% confidence.")



check_button = tk.Button(root, text="Check URL", font=label_font, bg="#4CAF50", fg="white", command=predict_url)
check_button.pack(pady=15)

resault_label.pack(pady=20)

root.mainloop()
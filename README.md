Real Time Video Surveillance And Triggering System
==============================

There is a critical need for an automated surveillance solution that can continuously and accurately monitor environments for signs of emergencies, providing real-time alerts to facilitate rapid intervention. Traditional systems relying on human operators are often slow and prone to errors, which can result in severe consequences, including loss of life and extensive propertydamage. Our project aims to develop a real-time emergency surveillance system that leverages computer vision to detect and respond to critical situations such as fires, violence, and medical emergencies.

![alt text](artifacts/Violence.png)

<img src="artifacts/Telegram_bot.jpg" alt="alt text" width="200"/>


# Project Demonstration Link:

[GDrive Link to Demo: ](https://drive.google.com/file/d/1jGzs83KbJ3c6U2SMFaDQ-q-IfVboSkmB/view)

# Dataset link

https://www.kaggle.com/datasets/mohamedmustafa/real-life-violence-situations-dataset


# STEPS to run the project:

## STEP 01: 
Clone the repository

```bash
git clone https://github.com/Hirak010/Real-time-surveillance-detection.git
```

## STEP 02: 
Create an environment & activate


```bash
conda create -n env python=3.11 -y
```

## STEP 03: 
Install the requirements


```bash
pip install -r requirements.txt
```


## STEP 04: 
To run the webcam app


```bash
python alert.py
```

# Technical Aspects

## Human Fall Detection

- You can check distance between foot C.G and body C.G
- It's body center of gravity
- It's foot center of gravity
- You can check the count of how many times he fell.
- If distance over 90 pixel(tall * 0.75), It displays he falling.
- 1) Body C.G and foot C.G.      2) Only use X axis.      3) I use this distance difference to basis of judgment
- It indicates if he woke up. (This only displays after falling.)
- A count of 1 goes up in the area where you fell (the count is determined by which area your feet are in).



# Authors:
```bash
Authors: Hirakjyoti Medhi, Biswajit Bera, Ashutosh Kumar and Roshan Jha
Email: hirak170802@gmail.com
```

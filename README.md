Real Time Video Surveillance And Triggering System
==============================

There is a critical need for an automated surveillance solution that can continuously and accurately monitor environments for signs of emergencies, providing real-time alerts to facilitate rapid intervention. Traditional systems relying on human operators are often slow and prone to errors, which can result in severe consequences, including loss of life and extensive propertydamage. Our project aims to develop a real-time emergency surveillance system that leverages computer vision to detect and respond to critical situations such as fires, violence, and medical emergencies.

![alt text](https://repository-images.githubusercontent.com/278710262/25d99480-c314-11ea-8e3a-de9b289ab474)

# Project Demonstration Link:

[link](https://www.linkedin.com/posts/hirakjyoti-815195207_deeplearning-machinelearning-ai-activity-7159154656743415809-5Nl_?utm_source=share&utm_medium=member_desktop)

# Download this Udacity's Self-Driving Car Simulator:

[Repo link](https://github.com/udacity/self-driving-car-sim)

# Generating Data:
Open the Udacity simulator and select Training Mode. Then click the record button and start driving. A folder will be created with two files IMG and driving_logs.csv 

# STEPS to run the project:

## STEP 01: 
Clone the repository

```bash
git clone https://github.com/Hirak010/Self-Driving-Car-Simulation
```

## STEP 02: 
Create an environment & activate


```bash
conda create -n env python=3.8 -y
```

## STEP 03: 
Install the requirements


```bash
pip install -r requirements.txt
```


## STEP 06: 
Now to start the drive run the following command


```bash
python app.py
```

Now, open the udacity simulator and select autonomous mode.

Project Organization
------------

    ├── LICENSE
    ├── Makefile           <- Makefile with commands like `make data` or `make train`
    ├── README.md          <- The top-level README for developers using this project.
    ├── data
    │   ├── external       <- Data from third party sources.
    │   ├── interim        <- Intermediate data that has been transformed.
    │   ├── processed      <- The final, canonical data sets for modeling.
    │   └── raw            <- The original, immutable data dump.
    │
    ├── docs               <- A default Sphinx project; see sphinx-doc.org for details
    │
    ├── model             <- Trained and serialized models, model predictions, or model summaries
    │
    ├── notebooks          <- Jupyter notebooks. Naming convention is a number (for ordering),
    │                         the creator's initials, and a short `-` delimited description, e.g.
    │                         `1.0-jqp-initial-data-exploration`.
    │
    ├── references         <- Data dictionaries, manuals, and all other explanatory materials.
    │
    ├── reports            <- Generated analysis as HTML, PDF, LaTeX, etc.
    │   └── figures        <- Generated graphics and figures to be used in reporting
    │
    ├── requirements.txt   <- The requirements file for reproducing the analysis environment, e.g.
    │                         generated with `pip freeze > requirements.txt`
    │
    ├── setup.py           <- makes project pip installable (pip install -e .) so src can be imported
    ├── src                <- Source code for use in this project.
    │   ├── __init__.py    <- Makes src a Python module
    │   │
    │   ├── data           <- Scripts to download or generate data
    │   │   └── make_dataset.py
    │   │
    │   ├── features       <- Scripts to turn raw data into features for modeling
    │   │   └── build_features.py
    │   │
    │   ├── models         <- Scripts to train models and then use trained models to make
    │   │   │                 predictions
    │   │   ├── predict_model.py
    │   │   └── train_model.py
    │   │
    │   └── visualization  <- Scripts to create exploratory and results oriented visualizations
    │       └── visualize.py
    │
    └── tox.ini            <- tox file with settings for running tox; see tox.readthedocs.io


--------

<p><small>Project based on the <a target="_blank" href="https://drivendata.github.io/cookiecutter-data-science/">cookiecutter data science project template</a>. #cookiecutterdatascience</small></p>

# Authors:
```bash
Author: Hirakjyoti Medhi
Email: hirak170802@gmail.com
```

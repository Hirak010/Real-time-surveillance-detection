import cv2
import numpy as np
import tensorflow as tf
from keras.models import load_model
import tkinter as tk
from tkinter import ttk
from PIL import Image, ImageTk
import mediapipe as mp
import os
import threading
import telebot
import time

# Load the pre-trained violence detection model
MoBiLSTM_model = load_model("MoBiLSTM_model.h5")

# Constants for violence detection
IMAGE_HEIGHT, IMAGE_WIDTH = 64, 64
SEQUENCE_LENGTH = 16
CLASSES_LIST = ["NonViolence", "Violence"]

# Load the fire detection cascade model
xml_path = 'fire_detection_cascade_model.xml'
fire_cascade = cv2.CascadeClassifier(xml_path)

# Fall detection function (assuming it's defined in fall_detection.py)
from fall_detection import detect_fall

# Initialize the Telegram bot
bot = telebot.TeleBot("7223589660:AAEmG9nlq8eCLKoGcB0sW_Y9BHJsfBM-sMw")
CHAT_ID = "5286247538"

# Time of the last alert
last_alert_time = 0

class IntegratedSafetyMonitoringApp:
    def __init__(self, window, window_title):
        self.window = window
        self.window.title(window_title)

        self.video_source = 0
        self.vid = cv2.VideoCapture(self.video_source)

        self.canvas = tk.Canvas(window, width=self.vid.get(cv2.CAP_PROP_FRAME_WIDTH), height=self.vid.get(cv2.CAP_PROP_FRAME_HEIGHT))
        self.canvas.pack()

        self.btn_quit = ttk.Button(window, text="Quit", command=self.quit)
        self.btn_quit.pack(anchor=tk.SE, padx=10, pady=10)

        # Create a frame for the bottom labels
        self.bottom_frame = tk.Frame(self.window)
        self.bottom_frame.pack(side=tk.BOTTOM, fill=tk.X)

        # Labels for fall, violence, and fire detection results
        self.fall_label = ttk.Label(self.bottom_frame, text="Status: Standing | Falls: 0", font=("Helvetica", 12))
        self.fall_label.pack(side=tk.LEFT, padx=10)

        self.violence_label = ttk.Label(self.bottom_frame, text="Violence: NonViolence", font=("Helvetica", 12))
        self.violence_label.pack(side=tk.LEFT, padx=10)

        self.fire_label = ttk.Label(self.bottom_frame, text="Fire: Not Detected", font=("Helvetica", 12))
        self.fire_label.pack(side=tk.LEFT, padx=10)

        self.pose = mp.solutions.pose.Pose(min_detection_confidence=0.5, min_tracking_confidence=0.5)

        self.fall_count = 0
        self.fall_status = "Standing"
        self.frames_buffer = []

        self.delay = 15
        self.update()

        # Start the Telegram bot in a separate thread
        self.stop_bot = False
        self.bot_thread = threading.Thread(target=self.run_telegram_bot)
        self.bot_thread.start()

        self.window.protocol("WM_DELETE_WINDOW", self.on_closing)
        self.window.mainloop()

    def update(self):
        ret, frame = self.vid.read()

        if ret:
            # Fall detection
            frame, falling, standing = detect_fall(frame, self.pose)

            if falling:
                self.fall_status = "Falling"
                self.send_telegram_alert(frame, "Fall detected!")
            elif standing and self.fall_status == "Falling":
                self.fall_status = "Standing"
                self.fall_count += 1

            self.fall_label.config(text=f"Status: {self.fall_status} | Falls: {self.fall_count}")

            # Violence detection
            resized_frame = cv2.resize(frame, (IMAGE_HEIGHT, IMAGE_WIDTH))
            normalized_frame = resized_frame / 255.0
            self.frames_buffer.append(normalized_frame)
            if len(self.frames_buffer) > SEQUENCE_LENGTH:
                self.frames_buffer.pop(0)

            violence_prediction = "NonViolence"
            violence_prob = 0

            if len(self.frames_buffer) == SEQUENCE_LENGTH:
                violence_prediction, violence_prob = self.predict_violence(np.array([self.frames_buffer]))

            self.update_violence_label(violence_prediction, violence_prob)

            if violence_prediction == "Violence":
                self.send_telegram_alert(frame, "Violence detected!")

            # Fire detection
            gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
            fires = fire_cascade.detectMultiScale(gray, 1.2, 5)
            fire_detected = len(fires) > 0
            fire_prob = min(len(fires) / 10.0, 1.0) if fire_detected else 0

            self.update_fire_label(fire_detected, fire_prob)

            if fire_detected:
                for (x, y, w, h) in fires:
                    cv2.rectangle(frame, (x, y), (x + w, y + h), (255, 0, 0), 2)
                    cv2.putText(frame, 'Fire', (x, y-10), cv2.FONT_HERSHEY_SIMPLEX, 0.9, (255, 0, 0), 2)
                self.send_telegram_alert(frame, "Fire detected!")

            # Display the frame
            self.photo = ImageTk.PhotoImage(image=Image.fromarray(cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)))
            self.canvas.create_image(0, 0, image=self.photo, anchor=tk.NW)

        self.window.after(self.delay, self.update)

    def predict_violence(self, sequence):
        predicted_labels_probabilities = MoBiLSTM_model.predict(sequence)[0]
        predicted_label = np.argmax(predicted_labels_probabilities)
        predicted_class_name = CLASSES_LIST[predicted_label]
        return predicted_class_name, predicted_labels_probabilities[predicted_label]

    def update_violence_label(self, prediction, probability):
        text = f"Violence: {prediction} ({probability:.2f})"
        color = 'red' if prediction == "Violence" else 'green'
        self.violence_label.config(text=text, foreground=color)

    def update_fire_label(self, detected, probability):
        text = f"Fire: {'Detected' if detected else 'Not Detected'} ({probability:.2f})"
        color = 'red' if detected else 'green'
        self.fire_label.config(text=text, foreground=color)

    def send_telegram_alert(self, frame, message):
        global last_alert_time
        current_time = time.time()
        
        if current_time - last_alert_time >= 60:
            try:
                cv2.imwrite("alert.jpg", frame)
                with open("alert.jpg", 'rb') as photo:
                    bot.send_photo(CHAT_ID, photo, caption=f"🚨 ALERT! 🚨\n{message}")
                bot.send_message(CHAT_ID, f"{message} Please take necessary precautions immediately!")
                last_alert_time = current_time
                print(f"Telegram alert sent: {message}")
            except Exception as e:
                print(f"Error sending Telegram alert: {e}")
        else:
            print("Waiting to send next alert. Time since last alert:", int(current_time - last_alert_time), "seconds")

    def run_telegram_bot(self):
        @bot.message_handler(commands=['start'])
        def handle_start(message):
            bot.reply_to(message, "Integrated Safety Monitoring system is running. Use /stop to terminate the system.")

        @bot.message_handler(commands=['stop'])
        def handle_stop(message):
            bot.reply_to(message, "Stopping the Integrated Safety Monitoring system...")
            self.stop_bot = True
            self.window.quit()

        while not self.stop_bot:
            try:
                bot.polling(none_stop=True, timeout=1)
            except Exception as e:
                print(f"An error occurred with the Telegram bot: {e}")
                time.sleep(5)

    def quit(self):
        self.stop_bot = True
        self.vid.release()
        self.window.quit()

    def on_closing(self):
        self.quit()

if __name__ == "__main__":
    IntegratedSafetyMonitoringApp(tk.Tk(), "Real Time Video Surveillance and Triggering System")
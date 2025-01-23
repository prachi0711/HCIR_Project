import tkinter as tk
from tkinter import scrolledtext
from tkinter import messagebox
import cv2
from PIL import Image, ImageTk
from threading import Thread
import time
import requests
from face_detection import FaceDetection
from behaviour import BehaviourController

class PepperGUI:
    def __init__(self, master):
        self.master = master
        self.master.title("Pepper Career Advisor")
        self.master.configure(bg="#2b2b2b")

        # Initialize Rasa URL and BehaviorController
        self.rasa_url = "http://localhost:5005/webhooks/rest/webhook"
        self.session_id = None
        self.behaviour_controller = BehaviourController.BehaviourController(gui=True)

        # GUI components
        self.initialize_console()
        self.initialize_webcam()

        # Face detection
        self.face_detection = FaceDetection.FaceDetection()
        self.webcam_active = False
        self.user_name = None

    def initialize_console(self):
        """Initialize the console text box and user input field."""
        self.console_frame = tk.Frame(self.master, bg="#2b2b2b")
        self.console_frame.pack(side=tk.LEFT, fill=tk.BOTH, expand=True, padx=10, pady=10)

        self.console_text = scrolledtext.ScrolledText(self.console_frame, wrap=tk.WORD, bg="#1e1e1e", fg="#d4d4d4", insertbackground="white", font=("Consolas", 12))
        self.console_text.pack(fill=tk.BOTH, expand=True)
        self.console_text.insert(tk.END, "Would you like to start the conversation? (Yes/No):\n")

        self.user_input = tk.Entry(self.console_frame, bg="#1e1e1e", fg="#d4d4d4", insertbackground="white", font=("Consolas", 12))
        self.user_input.pack(fill=tk.X, pady=(10, 0))
        self.user_input.bind("<Return>", self.process_input)

    def initialize_webcam(self):
        """Initialize the webcam feed area."""
        self.webcam_frame = tk.Frame(self.master, bg="#2b2b2b", width=400, height=400)
        self.webcam_frame.pack(side=tk.RIGHT, fill=tk.BOTH, expand=True, padx=10, pady=10)

        self.webcam_label = tk.Label(self.webcam_frame, bg="#1e1e1e")
        self.webcam_label.pack(fill=tk.BOTH, expand=True)

    def process_input(self, event):
        user_input = self.user_input.get().strip()
        self.console_text.insert(tk.END, f"You: {user_input}\n")
        self.console_text.see(tk.END)
        self.user_input.delete(0, tk.END)

        if user_input.lower() in ["yes", "y"] and not self.webcam_active:
            self.start_webcam()

        elif user_input.lower() in ["no", "n",] and not self.user_name:
            self.console_text.insert(tk.END, f"You: {self.behaviour_controller.say_goodbye()}\n")
            self.behaviour_controller.stop_simulation()

        elif not self.webcam_active and self.user_name:
            if user_input.lower() in ["exit", "quit", "bye"]:
                self.console_text.insert(tk.END, f"You: {self.behaviour_controller.say_goodbye()}\n")
                self.behaviour_controller.stop_simulation()
            else:
                self.process_user_input(user_input)



        else:
            self.console_text.insert(tk.END, "Invalid input. Please type Yes or No.\n")

    def start_webcam(self):
        self.webcam_active = True
        self.console_text.insert(tk.END, "Starting webcam for authorization...\n")
        cap = cv2.VideoCapture(0, cv2.CAP_V4L)
        counter = 0

        while self.webcam_active:
            ret, frame = cap.read()
            if ret:
                self.update_webcam_feed(frame)
                if counter % 30 == 0:
                    # Pass the frame to FaceDetection for processing
                   # self.user_name = self.face_detection.run_face_detection(frame)
                    self.user_name = "Behrouz"
                counter += 1

                if self.user_name:
                    self.webcam_active = False
                    self.console_text.insert(tk.END, f"Authorized User: {self.user_name}\n")
                    self.console_text.insert(tk.END, "You can now start chatting.\n")
                    self.console_text.insert(tk.END, "-------------------------------------------------\n")
                    message = self.behaviour_controller.greet_user(self.user_name)
                    self.console_text.insert(tk.END, f"{message}\n")
                    self.master.update()
                    break

            self.master.update()

        self.webcam_label.configure(image="")
        cv2.waitKey(1000)
        cap.release()
        cv2.destroyAllWindows()


    def update_webcam_feed(self, frame):
        """Update the webcam feed on the GUI."""
        frame_rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
        if self.user_name:
            cv2.putText(frame_rgb, f"Hi {self.user_name}!", (20, 450), cv2.FONT_HERSHEY_SIMPLEX, 1.5,
                    (0, 255, 0),
                    3)
        img = Image.fromarray(frame_rgb)
        imgtk = ImageTk.PhotoImage(image=img)

        self.webcam_label.imgtk = imgtk
        self.webcam_label.configure(image=imgtk)

    def process_user_input(self, user_input):
        rasa_response = self.send_message_to_rasa(user_input)

        if rasa_response:
            for response in rasa_response:
                if 'text' in response:
                    response_text = response['text']
                    self.behaviour_controller.speak(response_text)
                    self.console_text.insert(tk.END, f"Pepper: {response_text}\n")
                    self.console_text.see(tk.END)

    def send_message_to_rasa(self, message):
        payload = {
            "message": message
        }
        headers = {
            "Content-Type": "application/json"
        }

        if not self.session_id:
            self.session_id = str(int(time.time()))

        payload["sender"] = self.session_id

        response = requests.post(self.rasa_url, json=payload, headers=headers)

        if response.status_code == 200:
            return response.json()
        else:
            return [{"text": "I'm sorry, I couldn't process that request."}]

    def close_app(self):
        if self.webcam_active:
            self.webcam_active = False
        self.master.destroy()

if __name__ == "__main__":
    root = tk.Tk()
    app = PepperGUI(root)
    root.protocol("WM_DELETE_WINDOW", app.close_app)
    root.mainloop()

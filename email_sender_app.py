import smtplib
from email.message import EmailMessage
from tkinter import *
from tkinter import filedialog, messagebox, ttk
import os

# -------------------------
# SMTP CONFIG FOR smtp4dev
# -------------------------
SMTP_SERVER = "localhost"
SMTP_PORT = 1025 # use 25 or 2525 based on smtp4dev settings


# -------------------------
# MAIN APP CLASS
# -------------------------
class EmailSenderApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Email Sender App")
        self.root.geometry("520x600")

        self.dark_mode = False
        self.attached_file = None

        self.create_widgets()

    # -------------------------
    # DARK MODE TOGGLE
    # -------------------------
    def toggle_dark_mode(self):
        self.dark_mode = not self.dark_mode
        bg = "#222222" if self.dark_mode else "#ffffff"
        fg = "#ffffff" if self.dark_mode else "#000000"

        self.root.configure(bg=bg)

        widgets = [
            self.label_sender, self.label_receiver, self.label_subject,
            self.label_message, self.label_status
        ]

        for widget in widgets:
            widget.config(bg=bg, fg=fg)

        entries = [
            self.entry_sender, self.entry_receiver,
            self.entry_subject
        ]

        for entry in entries:
            entry.config(bg="#444444" if self.dark_mode else "#ffffff",
                         fg=fg)

        self.text_message.config(bg="#444444" if self.dark_mode else "#ffffff",
                                 fg=fg)

    # -------------------------
    # ATTACH FILE
    # -------------------------
    def attach_file(self):
        file_path = filedialog.askopenfilename()

        if file_path:
            self.attached_file = file_path
            self.label_status.config(text=f"Attached: {os.path.basename(file_path)}")

    # -------------------------
    # SEND EMAIL
    # -------------------------
    def send_email(self):
        sender = self.entry_sender.get()
        receivers = self.entry_receiver.get().split(",")
        subject = self.entry_subject.get()
        message_body = self.text_message.get("1.0", END)

        if not sender or not receivers or not subject:
            messagebox.showerror("Error", "All fields are required!")
            return

        msg = EmailMessage()
        msg["From"] = sender
        msg["To"] = ", ".join(receivers)
        msg["Subject"] = subject
        msg.set_content(message_body)

        # Attach file
        if self.attached_file:
            with open(self.attached_file, "rb") as f:
                file_data = f.read()
                file_name = os.path.basename(self.attached_file)

            msg.add_attachment(file_data, maintype="application",
                               subtype="octet-stream", filename=file_name)

        try:
            self.progress.start()

            server = smtplib.SMTP(SMTP_SERVER, SMTP_PORT)
            server.send_message(msg)
            server.quit()

            self.progress.stop()
            messagebox.showinfo("Success", "Email sent successfully (via smtp4dev)")
            self.label_status.config(text="Status: Email Sent ✔️")

        except Exception as e:
            self.progress.stop()
            messagebox.showerror("Error", f"Failed to send email:\n{e}")

    # -------------------------
    # GUI WIDGETS
    # -------------------------
    def create_widgets(self):
        self.label_sender = Label(self.root, text="Sender Email:")
        self.label_sender.pack(pady=5)
        self.entry_sender = Entry(self.root, width=40)
        self.entry_sender.pack()

        self.label_receiver = Label(self.root, text="Receiver Email(s):")
        self.label_receiver.pack(pady=5)
        self.entry_receiver = Entry(self.root, width=40)
        self.entry_receiver.pack()
        Label(self.root, text="(use comma for multiple)").pack()

        self.label_subject = Label(self.root, text="Subject:")
        self.label_subject.pack(pady=5)
        self.entry_subject = Entry(self.root, width=40)
        self.entry_subject.pack()

        self.label_message = Label(self.root, text="Message:")
        self.label_message.pack(pady=5)
        self.text_message = Text(self.root, height=8, width=50)
        self.text_message.pack()

        Button(self.root, text="Attach File", command=self.attach_file).pack(pady=5)
        Button(self.root, text="Send Email", bg="green", fg="white",
               command=self.send_email).pack(pady=10)

        self.progress = ttk.Progressbar(self.root, orient=HORIZONTAL, mode="indeterminate", length=300)
        self.progress.pack(pady=5)

        Button(self.root, text="Dark Mode", command=self.toggle_dark_mode).pack(pady=10)

        self.label_status = Label(self.root, text="Status: Waiting...")
        self.label_status.pack(pady=5)


# -------------------------
# RUN THE APP
# -------------------------
root = Tk()
app = EmailSenderApp(root)
root.mainloop()

import tkinter as tk
from pathlib import Path
from tkinter import filedialog, messagebox, ttk

from file_manager import save_baseline, verify_file
from history import load_history, record_verification


class SentinelApp:
    """Main Project Sentinel application."""

    def __init__(self, root):
        self.root = root

        self.root.title("Project Sentinel")
        self.root.geometry("900x620")
        self.root.minsize(760, 520)

        self.selected_file = None

        self.setup_style()
        self.build_interface()

    def setup_style(self):
        """Configure the application appearance."""

        style = ttk.Style()

        try:
            style.theme_use("clam")
        except tk.TclError:
            pass

        self.root.configure(bg="#0d1117")

        style.configure(
            "TFrame",
            background="#0d1117"
        )

        style.configure(
            "Card.TFrame",
            background="#161b22"
        )

        style.configure(
            "TLabel",
            background="#0d1117",
            foreground="#e6edf3",
            font=("Segoe UI", 10)
        )

        style.configure(
            "Title.TLabel",
            background="#0d1117",
            foreground="#f0f6fc",
            font=("Segoe UI", 26, "bold")
        )

        style.configure(
            "Subtitle.TLabel",
            background="#0d1117",
            foreground="#8b949e",
            font=("Segoe UI", 10)
        )

        style.configure(
            "CardTitle.TLabel",
            background="#161b22",
            foreground="#f0f6fc",
            font=("Segoe UI", 12, "bold")
        )

        style.configure(
            "Status.TLabel",
            background="#161b22",
            foreground="#8b949e",
            font=("Segoe UI", 11)
        )

        style.configure(
            "TButton",
            font=("Segoe UI", 10, "bold"),
            padding=(14, 9)
        )

        style.configure(
            "Accent.TButton",
            font=("Segoe UI", 10, "bold"),
            padding=(14, 9)
        )

    def build_interface(self):
        """Build the main application interface."""

        main = ttk.Frame(self.root, padding=30)
        main.pack(fill="both", expand=True)

        header = ttk.Frame(main)
        header.pack(fill="x", pady=(0, 25))

        ttk.Label(
            header,
            text="PROJECT SENTINEL",
            style="Title.TLabel"
        ).pack(anchor="w")

        ttk.Label(
            header,
            text="File Integrity Monitoring System",
            style="Subtitle.TLabel"
        ).pack(anchor="w", pady=(5, 0))

        file_card = ttk.Frame(
            main,
            style="Card.TFrame",
            padding=20
        )
        file_card.pack(fill="x", pady=(0, 15))

        ttk.Label(
            file_card,
            text="FILE SELECTION",
            style="CardTitle.TLabel"
        ).pack(anchor="w")

        self.file_label = ttk.Label(
            file_card,
            text="No file selected",
            style="Status.TLabel"
        )
        self.file_label.pack(anchor="w", pady=(12, 15))

        ttk.Button(
            file_card,
            text="Select File",
            command=self.select_file
        ).pack(anchor="w")

        actions = ttk.Frame(main)
        actions.pack(fill="x", pady=(0, 15))

        ttk.Button(
            actions,
            text="Create Trusted Baseline",
            command=self.create_baseline
        ).pack(side="left", padx=(0, 10))

        ttk.Button(
            actions,
            text="Verify Integrity",
            command=self.verify_integrity
        ).pack(side="left")

        status_card = ttk.Frame(
            main,
            style="Card.TFrame",
            padding=20
        )
        status_card.pack(fill="x", pady=(0, 15))

        ttk.Label(
            status_card,
            text="INTEGRITY STATUS",
            style="CardTitle.TLabel"
        ).pack(anchor="w")

        self.status_label = ttk.Label(
            status_card,
            text="Waiting for file...",
            style="Status.TLabel"
        )
        self.status_label.pack(anchor="w", pady=(12, 0))

        history_card = ttk.Frame(
            main,
            style="Card.TFrame",
            padding=20
        )
        history_card.pack(fill="both", expand=True)

        ttk.Label(
            history_card,
            text="RECENT VERIFICATION HISTORY",
            style="CardTitle.TLabel"
        ).pack(anchor="w", pady=(0, 10))

        self.history_text = tk.Text(
            history_card,
            height=8,
            bg="#0d1117",
            fg="#c9d1d9",
            insertbackground="#ffffff",
            relief="flat",
            font=("Consolas", 9),
            wrap="word"
        )
        self.history_text.pack(fill="both", expand=True)

        self.refresh_history()

    def select_file(self):
        """Open a file picker and select a file."""

        file_path = filedialog.askopenfilename(
            title="Select a file to monitor"
        )

        if not file_path:
            return

        self.selected_file = file_path

        self.file_label.config(
            text=str(Path(file_path).resolve())
        )

        self.status_label.config(
            text="File selected. Choose an action."
        )

    def create_baseline(self):
        """Create a trusted baseline for the selected file."""

        if not self.selected_file:
            messagebox.showwarning(
                "No File Selected",
                "Please select a file first."
            )
            return

        try:
            file_hash = save_baseline(self.selected_file)

            self.status_label.config(
                text="✓ Trusted baseline created successfully."
            )

            messagebox.showinfo(
                "Baseline Created",
                f"Trusted baseline created.\n\nSHA-256:\n{file_hash}"
            )

            self.refresh_history()

        except Exception as error:
            messagebox.showerror(
                "Error",
                f"Could not create baseline:\n\n{error}"
            )

    def verify_integrity(self):
        """Verify the selected file against its trusted baseline."""

        if not self.selected_file:
            messagebox.showwarning(
                "No File Selected",
                "Please select a file first."
            )
            return

        try:
            result = verify_file(self.selected_file)

            record_verification(
                self.selected_file,
                result
            )

            if result["status"] == "verified":
                self.status_label.config(
                    text="✓ INTEGRITY VERIFIED — No changes detected."
                )

            elif result["status"] == "modified":
                self.status_label.config(
                    text="⚠ WARNING — File modification detected."
                )

            elif result["status"] == "not_baselined":
                self.status_label.config(
                    text="No trusted baseline exists for this file."
                )

            elif result["status"] == "missing":
                self.status_label.config(
                    text="Selected file no longer exists."
                )

            self.refresh_history()

        except Exception as error:
            messagebox.showerror(
                "Verification Error",
                f"Could not verify the file:\n\n{error}"
            )

    def refresh_history(self):
        """Display recent verification history."""

        history = load_history()

        self.history_text.config(state="normal")
        self.history_text.delete("1.0", tk.END)

        if not history:
            self.history_text.insert(
                tk.END,
                "No verification records yet."
            )
        else:
            for record in reversed(history[-10:]):
                timestamp = record["timestamp"]
                status = record["status"].upper()
                file_path = record["file"]

                self.history_text.insert(
                    tk.END,
                    f"[{timestamp}]\n"
                    f"Status: {status}\n"
                    f"File: {file_path}\n"
                    f"{record['message']}\n"
                    f"{'-' * 80}\n"
                )

        self.history_text.config(state="disabled")


def main():
    root = tk.Tk()
    SentinelApp(root)
    root.mainloop()


if __name__ == "__main__":
    main()

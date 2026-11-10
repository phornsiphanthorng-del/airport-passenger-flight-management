import customtkinter as ctk
from tkinter import messagebox
from database import create_connection


class SettingsPage(ctk.CTkFrame):

    def __init__(self, parent):
        super().__init__(parent)

        # =========================================================
        # PAGE TITLE
        # =========================================================

        title = ctk.CTkLabel(
            self,
            text="Settings",
            font=("Arial", 28, "bold")
        )

        title.pack(
            padx=30,
            pady=(30, 5),
            anchor="w"
        )

        subtitle = ctk.CTkLabel(
            self,
            text="Manage application settings and system information",
            font=("Arial", 15)
        )

        subtitle.pack(
            padx=30,
            pady=(0, 25),
            anchor="w"
        )

        # =========================================================
        # MAIN SETTINGS AREA
        # =========================================================

        main_frame = ctk.CTkFrame(self)

        main_frame.pack(
            padx=30,
            pady=10,
            fill="both",
            expand=True
        )

        # =========================================================
        # DATABASE INFORMATION
        # =========================================================

        database_frame = ctk.CTkFrame(
            main_frame
        )

        database_frame.pack(
            padx=20,
            pady=20,
            fill="x"
        )

        database_title = ctk.CTkLabel(
            database_frame,
            text="🗄️ Database Information",
            font=("Arial", 19, "bold")
        )

        database_title.pack(
            padx=20,
            pady=(20, 15),
            anchor="w"
        )

        self.create_info_row(
            database_frame,
            "Database Name:",
            "airport_management"
        )

        self.create_info_row(
            database_frame,
            "Server:",
            "localhost"
        )

        self.create_info_row(
            database_frame,
            "Port:",
            "3306"
        )

        self.create_info_row(
            database_frame,
            "Database Type:",
            "MySQL"
        )

        # Connection status

        status_frame = ctk.CTkFrame(
            database_frame,
            fg_color="transparent"
        )

        status_frame.pack(
            padx=20,
            pady=(10, 20),
            fill="x"
        )

        status_title = ctk.CTkLabel(
            status_frame,
            text="Connection Status:",
            font=("Arial", 14, "bold")
        )

        status_title.pack(
            side="left"
        )

        self.connection_status = ctk.CTkLabel(
            status_frame,
            text="Checking...",
            font=("Arial", 14, "bold")
        )

        self.connection_status.pack(
            side="left",
            padx=10
        )

        # =========================================================
        # APPEARANCE SETTINGS
        # =========================================================

        appearance_frame = ctk.CTkFrame(
            main_frame
        )

        appearance_frame.pack(
            padx=20,
            pady=(0, 20),
            fill="x"
        )

        appearance_title = ctk.CTkLabel(
            appearance_frame,
            text="🎨 Appearance",
            font=("Arial", 19, "bold")
        )

        appearance_title.pack(
            padx=20,
            pady=(20, 10),
            anchor="w"
        )

        appearance_description = ctk.CTkLabel(
            appearance_frame,
            text="Choose the appearance mode of the application.",
            font=("Arial", 14)
        )

        appearance_description.pack(
            padx=20,
            pady=(0, 10),
            anchor="w"
        )

        self.appearance_menu = ctk.CTkOptionMenu(
            appearance_frame,
            values=[
                "Light",
                "Dark",
                "System"
            ],
            width=180,
            command=self.change_appearance
        )

        self.appearance_menu.set("Light")

        self.appearance_menu.pack(
            padx=20,
            pady=(0, 20),
            anchor="w"
        )

        # =========================================================
        # APPLICATION INFORMATION
        # =========================================================

        application_frame = ctk.CTkFrame(
            main_frame
        )

        application_frame.pack(
            padx=20,
            pady=(0, 20),
            fill="x"
        )

        application_title = ctk.CTkLabel(
            application_frame,
            text="💻 Application Information",
            font=("Arial", 19, "bold")
        )

        application_title.pack(
            padx=20,
            pady=(20, 15),
            anchor="w"
        )

        self.create_info_row(
            application_frame,
            "Application:",
            "Airport Passenger & Flight Data Management System"
        )

        self.create_info_row(
            application_frame,
            "Version:",
            "1.0"
        )

        self.create_info_row(
            application_frame,
            "Technology:",
            "Python + CustomTkinter + MySQL"
        )

        self.create_info_row(
            application_frame,
            "Project Type:",
            "Airport Data Management System"
        )

        # =========================================================
        # ABOUT PROJECT
        # =========================================================

        about_frame = ctk.CTkFrame(
            main_frame
        )

        about_frame.pack(
            padx=20,
            pady=(0, 20),
            fill="x"
        )

        about_title = ctk.CTkLabel(
            about_frame,
            text="ℹ️ About Project",
            font=("Arial", 19, "bold")
        )

        about_title.pack(
            padx=20,
            pady=(20, 10),
            anchor="w"
        )

        about_text = ctk.CTkLabel(
            about_frame,
            text=(
                "This system manages airport passengers, flights, "
                "bookings, baggage, and database reports."
            ),
            font=("Arial", 14),
            wraplength=850,
            justify="left"
        )

        about_text.pack(
            padx=20,
            pady=(0, 20),
            anchor="w"
        )

        # =========================================================
        # CHECK DATABASE CONNECTION
        # =========================================================

        self.check_database_connection()

    # =========================================================
    # INFORMATION ROW
    # =========================================================

    def create_info_row(
        self,
        parent,
        label_text,
        value_text
    ):

        row = ctk.CTkFrame(
            parent,
            fg_color="transparent"
        )

        row.pack(
            padx=20,
            pady=4,
            fill="x"
        )

        label = ctk.CTkLabel(
            row,
            text=label_text,
            font=("Arial", 14, "bold"),
            width=150,
            anchor="w"
        )

        label.pack(
            side="left"
        )

        value = ctk.CTkLabel(
            row,
            text=value_text,
            font=("Arial", 14),
            anchor="w"
        )

        value.pack(
            side="left",
            padx=10
        )

    # =========================================================
    # CHECK DATABASE CONNECTION
    # =========================================================

    def check_database_connection(self):

        connection = create_connection()

        if connection is not None:

            self.connection_status.configure(
                text="Connected ✓"
            )

            connection.close()

        else:

            self.connection_status.configure(
                text="Not Connected ✗"
            )

    # =========================================================
    # CHANGE APPEARANCE
    # =========================================================

    def change_appearance(
        self,
        selected_mode
    ):

        if selected_mode == "Light":

            ctk.set_appearance_mode("light")

        elif selected_mode == "Dark":

            ctk.set_appearance_mode("dark")

        elif selected_mode == "System":

            ctk.set_appearance_mode("system")



            
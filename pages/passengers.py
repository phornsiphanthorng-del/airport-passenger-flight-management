import customtkinter as ctk
from tkinter import ttk, messagebox
from database import create_connection


class PassengerPage(ctk.CTkFrame):

    def __init__(self, parent):
        super().__init__(parent)

        # =========================================================
        # PAGE TITLE
        # =========================================================

        title = ctk.CTkLabel(
            self,
            text="Passenger Management",
            font=("Arial", 28, "bold")
        )
        title.pack(
            padx=30,
            pady=(30, 5),
            anchor="w"
        )

        subtitle = ctk.CTkLabel(
            self,
            text="View and manage airport passenger information",
            font=("Arial", 15)
        )
        subtitle.pack(
            padx=30,
            pady=(0, 25),
            anchor="w"
        )

        # =========================================================
        # SEARCH AREA
        # =========================================================

        search_frame = ctk.CTkFrame(self)
        search_frame.pack(
            padx=30,
            pady=10,
            fill="x"
        )

        search_label = ctk.CTkLabel(
            search_frame,
            text="Search Passenger:",
            font=("Arial", 15, "bold")
        )
        search_label.pack(
            side="left",
            padx=(15, 10),
            pady=15
        )

        self.search_entry = ctk.CTkEntry(
            search_frame,
            width=300,
            placeholder_text="Name or passport number"
        )
        self.search_entry.pack(
            side="left",
            padx=10,
            pady=15
        )

        search_button = ctk.CTkButton(
            search_frame,
            text="Search",
            width=100,
            command=self.search_passengers
        )
        search_button.pack(
            side="left",
            padx=10
        )

        clear_button = ctk.CTkButton(
            search_frame,
            text="Clear",
            width=80,
            command=self.clear_search
        )
        clear_button.pack(
            side="left",
            padx=5
        )

        add_button = ctk.CTkButton(
            search_frame,
            text="+ Add Passenger",
            width=140,
            command=self.open_add_passenger
        )
        add_button.pack(
            side="right",
            padx=15
        )

        # =========================================================
        # PASSENGER TABLE
        # =========================================================

        table_frame = ctk.CTkFrame(self)
        table_frame.pack(
            padx=30,
            pady=20,
            fill="both",
            expand=True
        )

        columns = (
            "ID",
            "First Name",
            "Last Name",
            "Date of Birth",
            "Gender",
            "Passport",
            "Nationality",
            "Phone",
            "Email"
        )

        self.table = ttk.Treeview(
            table_frame,
            columns=columns,
            show="headings"
        )

        # Table headings
        for column in columns:
            self.table.heading(
                column,
                text=column
            )

        # Table column widths
        self.table.column("ID", width=60, anchor="center")
        self.table.column("First Name", width=120, anchor="center")
        self.table.column("Last Name", width=120, anchor="center")
        self.table.column("Date of Birth", width=110, anchor="center")
        self.table.column("Gender", width=90, anchor="center")
        self.table.column("Passport", width=120, anchor="center")
        self.table.column("Nationality", width=120, anchor="center")
        self.table.column("Phone", width=120, anchor="center")
        self.table.column("Email", width=180, anchor="center")

        self.table.pack(
            side="left",
            fill="both",
            expand=True,
            padx=10,
            pady=10
        )

        # =========================================================
        # SCROLLBAR
        # =========================================================

        scrollbar = ttk.Scrollbar(
            table_frame,
            orient="vertical",
            command=self.table.yview
        )

        scrollbar.pack(
            side="right",
            fill="y"
        )

        self.table.configure(
            yscrollcommand=scrollbar.set
        )

        # =========================================================
        # BOTTOM BUTTONS
        # =========================================================

        button_frame = ctk.CTkFrame(self)
        button_frame.pack(
            padx=30,
            pady=(0, 25),
            fill="x"
        )

        edit_button = ctk.CTkButton(
            button_frame,
            text="✏️ Edit Selected",
            command=self.edit_selected
        )
        edit_button.pack(
            side="left",
            padx=10,
            pady=10
        )

        delete_button = ctk.CTkButton(
            button_frame,
            text="🗑 Delete Selected",
            command=self.delete_selected
        )
        delete_button.pack(
            side="left",
            padx=10,
            pady=10
        )

        # =========================================================
        # LOAD PASSENGERS
        # =========================================================

        self.load_passengers()

    # =============================================================
    # LOAD PASSENGERS
    # =============================================================

    def load_passengers(self, search_text=""):

        # Clear existing rows
        for item in self.table.get_children():
            self.table.delete(item)

        connection = create_connection()

        if connection is None:
            messagebox.showerror(
                "Database Error",
                "Could not connect to the database."
            )
            return

        cursor = None

        try:
            cursor = connection.cursor()

            if search_text:

                query = """
                    SELECT
                        passenger_id,
                        first_name,
                        last_name,
                        date_of_birth,
                        gender,
                        passport_number,
                        nationality,
                        phone,
                        email
                    FROM Passenger
                    WHERE
                        first_name LIKE %s
                        OR last_name LIKE %s
                        OR passport_number LIKE %s
                    ORDER BY passenger_id
                """

                search_value = f"%{search_text}%"

                cursor.execute(
                    query,
                    (
                        search_value,
                        search_value,
                        search_value
                    )
                )

            else:

                query = """
                    SELECT
                        passenger_id,
                        first_name,
                        last_name,
                        date_of_birth,
                        gender,
                        passport_number,
                        nationality,
                        phone,
                        email
                    FROM Passenger
                    ORDER BY passenger_id
                """

                cursor.execute(query)

            passengers = cursor.fetchall()

            for passenger in passengers:
                self.table.insert(
                    "",
                    "end",
                    values=passenger
                )

        except Exception as e:

            messagebox.showerror(
                "Database Error",
                f"Error loading passengers:\n\n{e}"
            )

        finally:

            if cursor is not None:
                cursor.close()

            if connection.is_connected():
                connection.close()

    # =============================================================
    # SEARCH PASSENGERS
    # =============================================================

    def search_passengers(self):

        search_text = self.search_entry.get().strip()

        self.load_passengers(search_text)

    # =============================================================
    # CLEAR SEARCH
    # =============================================================

    def clear_search(self):

        self.search_entry.delete(
            0,
            "end"
        )

        self.load_passengers()

    # =============================================================
    # ADD PASSENGER WINDOW
    # =============================================================

    def open_add_passenger(self):

        self.add_window = ctk.CTkToplevel(self)

        self.add_window.title(
            "Add New Passenger"
        )

        self.add_window.geometry(
            "500x750"
        )

        self.add_window.resizable(
            False,
            False
        )

        # Keep this form above the main application and make it modal.
        parent_window = self.winfo_toplevel()
        self.add_window.transient(parent_window)
        self.add_window.lift()
        self.add_window.focus_force()
        self.add_window.grab_set()
        self.add_window.after(
            100,
            lambda: (
                self.add_window.lift(),
                self.add_window.focus_force()
            ) if self.add_window.winfo_exists() else None
        )



        # =========================================================
        # TITLE
        # =========================================================

        title = ctk.CTkLabel(
            self.add_window,
            text="Add New Passenger",
            font=("Arial", 24, "bold")
        )

        title.pack(
            pady=(25, 20)
        )

        # =========================================================
        # FORM
        # =========================================================

        form_frame = ctk.CTkFrame(
            self.add_window
        )

        form_frame.pack(
            padx=30,
            pady=10,
            fill="both",
            expand=True
        )

        # First Name
        ctk.CTkLabel(
            form_frame,
            text="First Name"
        ).pack(
            anchor="w",
            padx=20,
            pady=(15, 5)
        )

        self.first_name_entry = ctk.CTkEntry(
            form_frame,
            width=400,
            placeholder_text="Enter first name"
        )

        self.first_name_entry.pack(
            padx=20
        )

        # Last Name
        ctk.CTkLabel(
            form_frame,
            text="Last Name"
        ).pack(
            anchor="w",
            padx=20,
            pady=(15, 5)
        )

        self.last_name_entry = ctk.CTkEntry(
            form_frame,
            width=400,
            placeholder_text="Enter last name"
        )

        self.last_name_entry.pack(
            padx=20
        )

        # Date of Birth
        ctk.CTkLabel(
            form_frame,
            text="Date of Birth"
        ).pack(
            anchor="w",
            padx=20,
            pady=(15, 5)
        )

        self.dob_entry = ctk.CTkEntry(
            form_frame,
            width=400,
            placeholder_text="YYYY-MM-DD"
        )

        self.dob_entry.pack(
            padx=20
        )

        # Gender
        ctk.CTkLabel(
            form_frame,
            text="Gender"
        ).pack(
            anchor="w",
            padx=20,
            pady=(15, 5)
        )

        self.gender_entry = ctk.CTkComboBox(
            form_frame,
            width=400,
            values=[
                "Male",
                "Female"
            ]
        )

        self.gender_entry.pack(
            padx=20
        )

        self.gender_entry.set("Male")

        # Passport Number
        ctk.CTkLabel(
            form_frame,
            text="Passport Number"
        ).pack(
            anchor="w",
            padx=20,
            pady=(15, 5)
        )

        self.passport_entry = ctk.CTkEntry(
            form_frame,
            width=400,
            placeholder_text="Enter passport number"
        )

        self.passport_entry.pack(
            padx=20
        )

        # Nationality
        ctk.CTkLabel(
            form_frame,
            text="Nationality"
        ).pack(
            anchor="w",
            padx=20,
            pady=(15, 5)
        )

        self.nationality_entry = ctk.CTkEntry(
            form_frame,
            width=400,
            placeholder_text="Enter nationality"
        )

        self.nationality_entry.pack(
            padx=20
        )

        # Phone
        ctk.CTkLabel(
            form_frame,
            text="Phone"
        ).pack(
            anchor="w",
            padx=20,
            pady=(15, 5)
        )

        self.phone_entry = ctk.CTkEntry(
            form_frame,
            width=400,
            placeholder_text="Enter phone number"
        )

        self.phone_entry.pack(
            padx=20
        )

        # Email
        ctk.CTkLabel(
            form_frame,
            text="Email"
        ).pack(
            anchor="w",
            padx=20,
            pady=(15, 5)
        )

        self.email_entry = ctk.CTkEntry(
            form_frame,
            width=400,
            placeholder_text="Enter email address"
        )

        self.email_entry.pack(
            padx=20
        )

        # =========================================================
        # FORM BUTTONS
        # =========================================================

        button_frame = ctk.CTkFrame(
            self.add_window,
            fg_color="transparent"
        )

        button_frame.pack(
            pady=20
        )

        cancel_button = ctk.CTkButton(
            button_frame,
            text="Cancel",
            width=120,
            command=self.add_window.destroy
        )

        cancel_button.pack(
            side="left",
            padx=10
        )

        save_button = ctk.CTkButton(
            button_frame,
            text="Save Passenger",
            width=150,
            command=self.save_passenger
        )

        save_button.pack(
            side="left",
            padx=10
        )

    # =============================================================
    # SAVE PASSENGER
    # =============================================================

    def save_passenger(self):

        first_name = self.first_name_entry.get().strip()
        last_name = self.last_name_entry.get().strip()
        date_of_birth = self.dob_entry.get().strip()
        gender = self.gender_entry.get().strip()
        passport_number = self.passport_entry.get().strip()
        nationality = self.nationality_entry.get().strip()
        phone = self.phone_entry.get().strip()
        email = self.email_entry.get().strip()

        # Required fields
        if not first_name:
            messagebox.showwarning(
                "Missing Information",
                "Please enter the first name."
            )
            return

        if not last_name:
            messagebox.showwarning(
                "Missing Information",
                "Please enter the last name."
            )
            return

        if not date_of_birth:
            messagebox.showwarning(
                "Missing Information",
                "Please enter the date of birth."
            )
            return

        if not passport_number:
            messagebox.showwarning(
                "Missing Information",
                "Please enter the passport number."
            )
            return

        if not nationality:
            messagebox.showwarning(
                "Missing Information",
                "Please enter the nationality."
            )
            return

        connection = create_connection()

        if connection is None:
            messagebox.showerror(
                "Database Error",
                "Could not connect to the database."
            )
            return

        cursor = None

        try:

            cursor = connection.cursor()

            query = """
                INSERT INTO Passenger
                (
                    first_name,
                    last_name,
                    date_of_birth,
                    gender,
                    passport_number,
                    nationality,
                    phone,
                    email
                )
                VALUES
                (
                    %s,
                    %s,
                    %s,
                    %s,
                    %s,
                    %s,
                    %s,
                    %s
                )
            """

            values = (
                first_name,
                last_name,
                date_of_birth,
                gender,
                passport_number,
                nationality,
                phone,
                email
            )

            cursor.execute(
                query,
                values
            )

            connection.commit()

            messagebox.showinfo(
                "Success",
                "Passenger added successfully!"
            )

            self.add_window.destroy()

            self.load_passengers()

        except Exception as e:

            messagebox.showerror(
                "Database Error",
                f"Error adding passenger:\n\n{e}"
            )

            connection.rollback()

        finally:

            if cursor is not None:
                cursor.close()

            if connection.is_connected():
                connection.close()

    # =============================================================
    # EDIT SELECTED PASSENGER
    # =============================================================

    def edit_selected(self):

        selected = self.table.selection()

        if not selected:
            messagebox.showwarning(
                "No Selection",
                "Please select a passenger to edit."
            )
            return

        item = self.table.item(
            selected[0]
        )

        passenger = item["values"]

        passenger_id = passenger[0]

        edit_window = ctk.CTkToplevel(self)

        edit_window.title(
            "Edit Passenger"
        )

        edit_window.geometry(
            "500x750"
        )

        edit_window.resizable(
            False,
            False
        )

        # Keep this form above the main application and make it modal.
        parent_window = self.winfo_toplevel()
        edit_window.transient(parent_window)
        edit_window.lift()
        edit_window.focus_force()
        edit_window.grab_set()
        edit_window.after(
            100,
            lambda: (
                edit_window.lift(),
                edit_window.focus_force()
            ) if edit_window.winfo_exists() else None
        )



        # =========================================================
        # TITLE
        # =========================================================

        title = ctk.CTkLabel(
            edit_window,
            text="Edit Passenger",
            font=("Arial", 24, "bold")
        )

        title.pack(
            pady=(25, 20)
        )

        # =========================================================
        # FORM
        # =========================================================

        form_frame = ctk.CTkFrame(
            edit_window
        )

        form_frame.pack(
            padx=30,
            pady=10,
            fill="both",
            expand=True
        )

        # First Name
        ctk.CTkLabel(
            form_frame,
            text="First Name"
        ).pack(
            anchor="w",
            padx=20,
            pady=(15, 5)
        )

        first_name_entry = ctk.CTkEntry(
            form_frame,
            width=400
        )

        first_name_entry.pack(
            padx=20
        )

        first_name_entry.insert(
            0,
            passenger[1]
        )

        # Last Name
        ctk.CTkLabel(
            form_frame,
            text="Last Name"
        ).pack(
            anchor="w",
            padx=20,
            pady=(15, 5)
        )

        last_name_entry = ctk.CTkEntry(
            form_frame,
            width=400
        )

        last_name_entry.pack(
            padx=20
        )

        last_name_entry.insert(
            0,
            passenger[2]
        )

        # Date of Birth
        ctk.CTkLabel(
            form_frame,
            text="Date of Birth"
        ).pack(
            anchor="w",
            padx=20,
            pady=(15, 5)
        )

        dob_entry = ctk.CTkEntry(
            form_frame,
            width=400
        )

        dob_entry.pack(
            padx=20
        )

        dob_entry.insert(
            0,
            passenger[3]
        )

        # Gender
        ctk.CTkLabel(
            form_frame,
            text="Gender"
        ).pack(
            anchor="w",
            padx=20,
            pady=(15, 5)
        )

        gender_entry = ctk.CTkComboBox(
            form_frame,
            width=400,
            values=[
                "Male",
                "Female"
            ]
        )

        gender_entry.pack(
            padx=20
        )

        gender_entry.set(
            passenger[4]
        )

        # Passport
        ctk.CTkLabel(
            form_frame,
            text="Passport Number"
        ).pack(
            anchor="w",
            padx=20,
            pady=(15, 5)
        )

        passport_entry = ctk.CTkEntry(
            form_frame,
            width=400
        )

        passport_entry.pack(
            padx=20
        )

        passport_entry.insert(
            0,
            passenger[5]
        )

        # Nationality
        ctk.CTkLabel(
            form_frame,
            text="Nationality"
        ).pack(
            anchor="w",
            padx=20,
            pady=(15, 5)
        )

        nationality_entry = ctk.CTkEntry(
            form_frame,
            width=400
        )

        nationality_entry.pack(
            padx=20
        )

        nationality_entry.insert(
            0,
            passenger[6]
        )

        # Phone
        ctk.CTkLabel(
            form_frame,
            text="Phone"
        ).pack(
            anchor="w",
            padx=20,
            pady=(15, 5)
        )

        phone_entry = ctk.CTkEntry(
            form_frame,
            width=400
        )

        phone_entry.pack(
            padx=20
        )

        phone_entry.insert(
            0,
            passenger[7]
        )

        # Email
        ctk.CTkLabel(
            form_frame,
            text="Email"
        ).pack(
            anchor="w",
            padx=20,
            pady=(15, 5)
        )

        email_entry = ctk.CTkEntry(
            form_frame,
            width=400
        )

        email_entry.pack(
            padx=20
        )

        email_entry.insert(
            0,
            passenger[8]
        )

        # =========================================================
        # BUTTONS
        # =========================================================

        button_frame = ctk.CTkFrame(
            edit_window,
            fg_color="transparent"
        )

        button_frame.pack(
            pady=20
        )

        cancel_button = ctk.CTkButton(
            button_frame,
            text="Cancel",
            width=120,
            command=edit_window.destroy
        )

        cancel_button.pack(
            side="left",
            padx=10
        )

        save_button = ctk.CTkButton(
            button_frame,
            text="Update Passenger",
            width=150,
            command=lambda: self.update_passenger(
                passenger_id,
                first_name_entry.get().strip(),
                last_name_entry.get().strip(),
                dob_entry.get().strip(),
                gender_entry.get().strip(),
                passport_entry.get().strip(),
                nationality_entry.get().strip(),
                phone_entry.get().strip(),
                email_entry.get().strip(),
                edit_window
            )
        )

        save_button.pack(
            side="left",
            padx=10
        )

    # =============================================================
    # UPDATE PASSENGER
    # =============================================================

    def update_passenger(
        self,
        passenger_id,
        first_name,
        last_name,
        date_of_birth,
        gender,
        passport_number,
        nationality,
        phone,
        email,
        edit_window
    ):

        if not first_name:
            messagebox.showwarning(
                "Missing Information",
                "Please enter the first name."
            )
            return

        if not last_name:
            messagebox.showwarning(
                "Missing Information",
                "Please enter the last name."
            )
            return

        if not date_of_birth:
            messagebox.showwarning(
                "Missing Information",
                "Please enter the date of birth."
            )
            return

        if not passport_number:
            messagebox.showwarning(
                "Missing Information",
                "Please enter the passport number."
            )
            return

        if not nationality:
            messagebox.showwarning(
                "Missing Information",
                "Please enter the nationality."
            )
            return

        connection = create_connection()

        if connection is None:
            messagebox.showerror(
                "Database Error",
                "Could not connect to the database."
            )
            return

        cursor = None

        try:

            cursor = connection.cursor()

            query = """
                UPDATE Passenger
                SET
                    first_name = %s,
                    last_name = %s,
                    date_of_birth = %s,
                    gender = %s,
                    passport_number = %s,
                    nationality = %s,
                    phone = %s,
                    email = %s
                WHERE passenger_id = %s
            """

            values = (
                first_name,
                last_name,
                date_of_birth,
                gender,
                passport_number,
                nationality,
                phone,
                email,
                passenger_id
            )

            cursor.execute(
                query,
                values
            )

            connection.commit()

            messagebox.showinfo(
                "Success",
                "Passenger updated successfully!"
            )

            edit_window.destroy()

            self.load_passengers()

        except Exception as e:

            messagebox.showerror(
                "Database Error",
                f"Error updating passenger:\n\n{e}"
            )

            connection.rollback()

        finally:

            if cursor is not None:
                cursor.close()

            if connection.is_connected():
                connection.close()

    # =============================================================
    # DELETE SELECTED PASSENGER
    # =============================================================

    def delete_selected(self):

        selected = self.table.selection()

        if not selected:
            messagebox.showwarning(
                "No Selection",
                "Please select a passenger to delete."
            )
            return

        item = self.table.item(
            selected[0]
        )

        passenger = item["values"]

        passenger_id = passenger[0]

        confirm = messagebox.askyesno(
            "Confirm Delete",
            f"Are you sure you want to delete passenger ID {passenger_id}?"
        )

        if not confirm:
            return

        connection = create_connection()

        if connection is None:
            messagebox.showerror(
                "Database Error",
                "Could not connect to the database."
            )
            return

        cursor = None

        try:

            cursor = connection.cursor()

            query = """
                DELETE FROM Passenger
                WHERE passenger_id = %s
            """

            cursor.execute(
                query,
                (passenger_id,)
            )

            connection.commit()

            messagebox.showinfo(
                "Success",
                "Passenger deleted successfully!"
            )

            self.load_passengers()

        except Exception as e:

            messagebox.showerror(
                "Database Error",
                f"Could not delete passenger.\n\n{e}"
            )

            connection.rollback()

        finally:

            if cursor is not None:
                cursor.close()

            if connection.is_connected():
                connection.close()
import customtkinter as ctk
from tkinter import ttk, messagebox
from database import create_connection


class BookingPage(ctk.CTkFrame):

    def __init__(self, parent):
        super().__init__(parent)

        # =====================================================
        # Page Title
        # =====================================================

        title = ctk.CTkLabel(
            self,
            text="Booking Management",
            font=("Arial", 28, "bold")
        )

        title.pack(
            padx=30,
            pady=(30, 5),
            anchor="w"
        )

        subtitle = ctk.CTkLabel(
            self,
            text="View and manage passenger flight bookings",
            font=("Arial", 15)
        )

        subtitle.pack(
            padx=30,
            pady=(0, 25),
            anchor="w"
        )

        # =====================================================
        # Search Area
        # =====================================================

        search_frame = ctk.CTkFrame(self)

        search_frame.pack(
            padx=30,
            pady=10,
            fill="x"
        )

        search_label = ctk.CTkLabel(
            search_frame,
            text="Search Booking:",
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
            placeholder_text="Booking ID, Passenger ID or Flight ID"
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
            command=self.search_bookings
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
            text="+ Add Booking",
            width=140,
            command=self.open_add_booking
        )

        add_button.pack(
            side="right",
            padx=15
        )

        # =====================================================
        # Booking Table
        # =====================================================

        table_frame = ctk.CTkFrame(self)

        table_frame.pack(
            padx=30,
            pady=20,
            fill="both",
            expand=True
        )

        columns = (
            "ID",
            "Passenger ID",
            "Flight ID",
            "Booking Date",
            "Seat Number",
            "Class",
            "Booking Status"
        )

        self.table = ttk.Treeview(
            table_frame,
            columns=columns,
            show="headings"
        )

        for column in columns:

            self.table.heading(
                column,
                text=column
            )

            self.table.column(
                column,
                width=140,
                anchor="center"
            )

        self.table.pack(
            side="left",
            fill="both",
            expand=True,
            padx=10,
            pady=10
        )

        # =====================================================
        # Vertical Scrollbar
        # =====================================================

        vertical_scrollbar = ttk.Scrollbar(
            table_frame,
            orient="vertical",
            command=self.table.yview
        )

        vertical_scrollbar.pack(
            side="right",
            fill="y"
        )

        self.table.configure(
            yscrollcommand=vertical_scrollbar.set
        )

        # =====================================================
        # Horizontal Scrollbar
        # =====================================================

        horizontal_scrollbar = ttk.Scrollbar(
            self,
            orient="horizontal",
            command=self.table.xview
        )

        horizontal_scrollbar.pack(
            padx=30,
            fill="x"
        )

        self.table.configure(
            xscrollcommand=horizontal_scrollbar.set
        )

        # =====================================================
        # Bottom Buttons
        # =====================================================

        button_frame = ctk.CTkFrame(self)

        button_frame.pack(
            padx=30,
            pady=(10, 25),
            fill="x"
        )

        edit_button = ctk.CTkButton(
            button_frame,
            text="Edit Selected",
            width=160,
            command=self.edit_selected
        )

        edit_button.pack(
            side="left",
            padx=10,
            pady=10
        )

        delete_button = ctk.CTkButton(
            button_frame,
            text="Delete Selected",
            width=160,
            command=self.delete_selected
        )

        delete_button.pack(
            side="left",
            padx=10,
            pady=10
        )

        # =====================================================
        # Load Booking Data
        # =====================================================

        self.load_bookings()

    # =====================================================
    # Load Bookings
    # =====================================================

    def load_bookings(self, search_text=""):

        for item in self.table.get_children():
            self.table.delete(item)

        connection = create_connection()

        if connection is None:
            return

        try:

            cursor = connection.cursor()

            if search_text:

                query = """
                    SELECT
                        booking_id,
                        passenger_id,
                        flight_id,
                        booking_date,
                        seat_number,
                        class,
                        booking_status
                    FROM Booking
                    WHERE
                        CAST(booking_id AS CHAR) LIKE %s
                        OR CAST(passenger_id AS CHAR) LIKE %s
                        OR CAST(flight_id AS CHAR) LIKE %s
                        OR seat_number LIKE %s
                        OR class LIKE %s
                        OR booking_status LIKE %s
                    ORDER BY booking_id
                """

                search_value = f"%{search_text}%"

                cursor.execute(
                    query,
                    (
                        search_value,
                        search_value,
                        search_value,
                        search_value,
                        search_value,
                        search_value
                    )
                )

            else:

                query = """
                    SELECT
                        booking_id,
                        passenger_id,
                        flight_id,
                        booking_date,
                        seat_number,
                        class,
                        booking_status
                    FROM Booking
                    ORDER BY booking_id
                """

                cursor.execute(query)

            bookings = cursor.fetchall()

            for booking in bookings:

                self.table.insert(
                    "",
                    "end",
                    values=booking
                )

            cursor.close()
            connection.close()

        except Exception as e:

            print(f"Error loading bookings: {e}")

            try:
                if connection.is_connected():
                    connection.close()
            except:
                pass

    # =====================================================
    # Search Bookings
    # =====================================================

    def search_bookings(self):

        search_text = self.search_entry.get().strip()

        self.load_bookings(search_text)

    # =====================================================
    # Clear Search
    # =====================================================

    def clear_search(self):

        self.search_entry.delete(
            0,
            "end"
        )

        self.load_bookings()

    # =====================================================
    # Add Booking Window
    # =====================================================

    def open_add_booking(self):

        add_window = ctk.CTkToplevel(self)

        add_window.title(
            "Add New Booking"
        )

        add_window.geometry(
            "550x700"
        )

        add_window.minsize(
            550,
            600
        )

        add_window.resizable(
            True,
            True
        )

        add_window.transient(
            self.winfo_toplevel()
        )

        # =================================================
        # Title
        # =================================================

        title = ctk.CTkLabel(
            add_window,
            text="Add New Booking",
            font=("Arial", 26, "bold")
        )

        title.pack(
            pady=(25, 15)
        )

        # =================================================
        # Scrollable Form
        # =================================================

        form_frame = ctk.CTkScrollableFrame(
            add_window
        )

        form_frame.pack(
            padx=20,
            pady=10,
            fill="both",
            expand=True
        )

        # =================================================
        # Passenger ID
        # =================================================

        ctk.CTkLabel(
            form_frame,
            text="Passenger ID"
        ).pack(
            anchor="w",
            padx=20,
            pady=(10, 5)
        )

        passenger_id_entry = ctk.CTkEntry(
            form_frame,
            width=450,
            placeholder_text="Example: 1"
        )

        passenger_id_entry.pack(
            padx=20
        )

        # =================================================
        # Flight ID
        # =================================================

        ctk.CTkLabel(
            form_frame,
            text="Flight ID"
        ).pack(
            anchor="w",
            padx=20,
            pady=(15, 5)
        )

        flight_id_entry = ctk.CTkEntry(
            form_frame,
            width=450,
            placeholder_text="Example: 1"
        )

        flight_id_entry.pack(
            padx=20
        )

        # =================================================
        # Booking Date
        # =================================================

        ctk.CTkLabel(
            form_frame,
            text="Booking Date"
        ).pack(
            anchor="w",
            padx=20,
            pady=(15, 5)
        )

        booking_date_entry = ctk.CTkEntry(
            form_frame,
            width=450,
            placeholder_text="YYYY-MM-DD"
        )

        booking_date_entry.pack(
            padx=20
        )

        # =================================================
        # Seat Number
        # =================================================

        ctk.CTkLabel(
            form_frame,
            text="Seat Number"
        ).pack(
            anchor="w",
            padx=20,
            pady=(15, 5)
        )

        seat_number_entry = ctk.CTkEntry(
            form_frame,
            width=450,
            placeholder_text="Example: 12A"
        )

        seat_number_entry.pack(
            padx=20
        )

        # =================================================
        # Class
        # =================================================

        ctk.CTkLabel(
            form_frame,
            text="Class"
        ).pack(
            anchor="w",
            padx=20,
            pady=(15, 5)
        )

        class_menu = ctk.CTkOptionMenu(
            form_frame,
            width=450,
            values=[
                "Economy",
                "Premium Economy",
                "Business",
                "First Class"
            ]
        )

        class_menu.pack(
            padx=20
        )

        class_menu.set(
            "Economy"
        )

        # =================================================
        # Booking Status
        # =================================================

        ctk.CTkLabel(
            form_frame,
            text="Booking Status"
        ).pack(
            anchor="w",
            padx=20,
            pady=(15, 5)
        )

        status_menu = ctk.CTkOptionMenu(
            form_frame,
            width=450,
            values=[
                "Confirmed",
                "Cancelled"
            ]
        )

        status_menu.pack(
            padx=20
        )

        status_menu.set(
            "Confirmed"
        )

        # =================================================
        # Buttons
        # =================================================

        button_frame = ctk.CTkFrame(
            add_window,
            fg_color="transparent"
        )

        button_frame.pack(
            pady=20
        )

        cancel_button = ctk.CTkButton(
            button_frame,
            text="Cancel",
            width=120,
            command=add_window.destroy
        )

        cancel_button.pack(
            side="left",
            padx=10
        )

        save_button = ctk.CTkButton(
            button_frame,
            text="Save Booking",
            width=150,
            command=lambda: self.save_booking(
                add_window,
                passenger_id_entry,
                flight_id_entry,
                booking_date_entry,
                seat_number_entry,
                class_menu,
                status_menu
            )
        )

        save_button.pack(
            side="left",
            padx=10
        )

    # =====================================================
    # Save New Booking
    # =====================================================

    def save_booking(
        self,
        add_window,
        passenger_id_entry,
        flight_id_entry,
        booking_date_entry,
        seat_number_entry,
        class_menu,
        status_menu
    ):

        passenger_id = passenger_id_entry.get().strip()
        flight_id = flight_id_entry.get().strip()
        booking_date = booking_date_entry.get().strip()
        seat_number = seat_number_entry.get().strip()
        booking_class = class_menu.get().strip()
        booking_status = status_menu.get().strip()

        # =================================================
        # Validation
        # =================================================

        if not passenger_id:
            messagebox.showwarning(
                "Missing Information",
                "Please enter a Passenger ID."
            )
            return

        if not flight_id:
            messagebox.showwarning(
                "Missing Information",
                "Please enter a Flight ID."
            )
            return

        if not booking_date:
            messagebox.showwarning(
                "Missing Information",
                "Please enter the Booking Date."
            )
            return

        if not seat_number:
            messagebox.showwarning(
                "Missing Information",
                "Please enter the Seat Number."
            )
            return

        try:
            passenger_id = int(passenger_id)
            flight_id = int(flight_id)
        except ValueError:

            messagebox.showwarning(
                "Invalid Information",
                "Passenger ID and Flight ID must be numbers."
            )

            return

        connection = create_connection()

        if connection is None:

            messagebox.showerror(
                "Database Error",
                "Could not connect to the database."
            )

            return

        try:

            cursor = connection.cursor()

            query = """
                INSERT INTO Booking
                (
                    passenger_id,
                    flight_id,
                    booking_date,
                    seat_number,
                    class,
                    booking_status
                )
                VALUES
                (
                    %s,
                    %s,
                    %s,
                    %s,
                    %s,
                    %s
                )
            """

            values = (
                passenger_id,
                flight_id,
                booking_date,
                seat_number,
                booking_class,
                booking_status
            )

            cursor.execute(
                query,
                values
            )

            connection.commit()

            cursor.close()
            connection.close()

            messagebox.showinfo(
                "Success",
                "Booking added successfully!"
            )

            add_window.destroy()

            # Automatic table refresh
            self.load_bookings()

        except Exception as e:

            print(
                f"Error adding booking: {e}"
            )

            messagebox.showerror(
                "Error",
                f"Could not add booking.\n\n{e}"
            )

            try:
                if connection.is_connected():
                    connection.close()
            except:
                pass

    # =====================================================
    # Edit Selected Booking
    # =====================================================

    def edit_selected(self):

        selected = self.table.selection()

        if not selected:

            messagebox.showwarning(
                "No Selection",
                "Please select a booking to edit."
            )

            return

        item = self.table.item(
            selected[0]
        )

        booking = item["values"]

        booking_id = booking[0]

        edit_window = ctk.CTkToplevel(self)

        edit_window.title(
            "Edit Booking"
        )

        edit_window.geometry(
            "550x700"
        )

        edit_window.minsize(
            550,
            600
        )

        edit_window.resizable(
            True,
            True
        )

        edit_window.transient(
            self.winfo_toplevel()
        )

        # =================================================
        # Title
        # =================================================

        title = ctk.CTkLabel(
            edit_window,
            text="Edit Booking",
            font=("Arial", 26, "bold")
        )

        title.pack(
            pady=(25, 15)
        )

        # =================================================
        # Scrollable Form
        # =================================================

        form_frame = ctk.CTkScrollableFrame(
            edit_window
        )

        form_frame.pack(
            padx=20,
            pady=10,
            fill="both",
            expand=True
        )

        # =================================================
        # Passenger ID
        # =================================================

        ctk.CTkLabel(
            form_frame,
            text="Passenger ID"
        ).pack(
            anchor="w",
            padx=20,
            pady=(10, 5)
        )

        passenger_id_entry = ctk.CTkEntry(
            form_frame,
            width=450
        )

        passenger_id_entry.pack(
            padx=20
        )

        passenger_id_entry.insert(
            0,
            str(booking[1])
        )

        # =================================================
        # Flight ID
        # =================================================

        ctk.CTkLabel(
            form_frame,
            text="Flight ID"
        ).pack(
            anchor="w",
            padx=20,
            pady=(15, 5)
        )

        flight_id_entry = ctk.CTkEntry(
            form_frame,
            width=450
        )

        flight_id_entry.pack(
            padx=20
        )

        flight_id_entry.insert(
            0,
            str(booking[2])
        )

        # =================================================
        # Booking Date
        # =================================================

        ctk.CTkLabel(
            form_frame,
            text="Booking Date"
        ).pack(
            anchor="w",
            padx=20,
            pady=(15, 5)
        )

        booking_date_entry = ctk.CTkEntry(
            form_frame,
            width=450
        )

        booking_date_entry.pack(
            padx=20
        )

        booking_date_entry.insert(
            0,
            str(booking[3])
        )

        # =================================================
        # Seat Number
        # =================================================

        ctk.CTkLabel(
            form_frame,
            text="Seat Number"
        ).pack(
            anchor="w",
            padx=20,
            pady=(15, 5)
        )

        seat_number_entry = ctk.CTkEntry(
            form_frame,
            width=450
        )

        seat_number_entry.pack(
            padx=20
        )

        seat_number_entry.insert(
            0,
            str(booking[4])
        )

        # =================================================
        # Class
        # =================================================

        ctk.CTkLabel(
            form_frame,
            text="Class"
        ).pack(
            anchor="w",
            padx=20,
            pady=(15, 5)
        )

        class_menu = ctk.CTkOptionMenu(
            form_frame,
            width=450,
            values=[
                "Economy",
                "Premium Economy",
                "Business",
                "First Class"
            ]
        )

        class_menu.pack(
            padx=20
        )

        class_menu.set(
            str(booking[5])
        )

        # =================================================
        # Booking Status
        # =================================================

        ctk.CTkLabel(
            form_frame,
            text="Booking Status"
        ).pack(
            anchor="w",
            padx=20,
            pady=(15, 5)
        )

        status_menu = ctk.CTkOptionMenu(
            form_frame,
            width=450,
            values=[
                "Confirmed",
                "Cancelled"
            ]
        )

        status_menu.pack(
            padx=20
        )

        status_menu.set(
            str(booking[6])
        )

        # =================================================
        # Buttons
        # =================================================

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
            text="Save Changes",
            width=150,
            command=lambda: self.save_changes(
                edit_window,
                booking_id,
                passenger_id_entry,
                flight_id_entry,
                booking_date_entry,
                seat_number_entry,
                class_menu,
                status_menu
            )
        )

        save_button.pack(
            side="left",
            padx=10
        )

    # =====================================================
    # Save Changes
    # =====================================================

    def save_changes(
        self,
        edit_window,
        booking_id,
        passenger_id_entry,
        flight_id_entry,
        booking_date_entry,
        seat_number_entry,
        class_menu,
        status_menu
    ):

        passenger_id = passenger_id_entry.get().strip()
        flight_id = flight_id_entry.get().strip()
        booking_date = booking_date_entry.get().strip()
        seat_number = seat_number_entry.get().strip()
        booking_class = class_menu.get().strip()
        booking_status = status_menu.get().strip()

        # =================================================
        # Validation
        # =================================================

        if not passenger_id:
            messagebox.showwarning(
                "Missing Information",
                "Please enter a Passenger ID."
            )
            return

        if not flight_id:
            messagebox.showwarning(
                "Missing Information",
                "Please enter a Flight ID."
            )
            return

        if not booking_date:
            messagebox.showwarning(
                "Missing Information",
                "Please enter the Booking Date."
            )
            return

        if not seat_number:
            messagebox.showwarning(
                "Missing Information",
                "Please enter the Seat Number."
            )
            return

        try:

            passenger_id = int(passenger_id)
            flight_id = int(flight_id)

        except ValueError:

            messagebox.showwarning(
                "Invalid Information",
                "Passenger ID and Flight ID must be numbers."
            )

            return

        connection = create_connection()

        if connection is None:

            messagebox.showerror(
                "Database Error",
                "Could not connect to the database."
            )

            return

        try:

            cursor = connection.cursor()

            query = """
                UPDATE Booking
                SET
                    passenger_id = %s,
                    flight_id = %s,
                    booking_date = %s,
                    seat_number = %s,
                    class = %s,
                    booking_status = %s
                WHERE booking_id = %s
            """

            values = (
                passenger_id,
                flight_id,
                booking_date,
                seat_number,
                booking_class,
                booking_status,
                booking_id
            )

            cursor.execute(
                query,
                values
            )

            connection.commit()

            cursor.close()
            connection.close()

            messagebox.showinfo(
                "Success",
                "Booking updated successfully!"
            )

            edit_window.destroy()

            # Automatic table refresh
            self.load_bookings()

        except Exception as e:

            print(
                f"Error updating booking: {e}"
            )

            messagebox.showerror(
                "Error",
                f"Could not update booking.\n\n{e}"
            )

            try:
                if connection.is_connected():
                    connection.close()
            except:
                pass

    # =====================================================
    # Delete Selected Booking
    # =====================================================

    def delete_selected(self):

        selected = self.table.selection()

        if not selected:

            messagebox.showwarning(
                "No Selection",
                "Please select a booking to delete."
            )

            return

        item = self.table.item(
            selected[0]
        )

        booking = item["values"]

        booking_id = booking[0]

        confirm = messagebox.askyesno(
            "Confirm Delete",
            f"Are you sure you want to delete booking {booking_id}?"
        )

        if not confirm:
            return

        connection = create_connection()

        if connection is None:
            return

        try:

            cursor = connection.cursor()

            query = """
                DELETE FROM Booking
                WHERE booking_id = %s
            """

            cursor.execute(
                query,
                (booking_id,)
            )

            connection.commit()

            cursor.close()
            connection.close()

            messagebox.showinfo(
                "Success",
                "Booking deleted successfully!"
            )

            # Automatic table refresh
            self.load_bookings()

        except Exception as e:

            print(
                f"Error deleting booking: {e}"
            )

            messagebox.showerror(
                "Error",
                f"Could not delete booking.\n\n{e}"
            )

            try:
                if connection.is_connected():
                    connection.close()
            except:
                pass


            
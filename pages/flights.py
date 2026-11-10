import customtkinter as ctk
from tkinter import ttk, messagebox
from database import create_connection


class FlightPage(ctk.CTkFrame):

    def __init__(self, parent):
        super().__init__(parent)

        # =========================
        # Page Title
        # =========================

        title = ctk.CTkLabel(
            self,
            text="Flight Management",
            font=("Arial", 28, "bold")
        )

        title.pack(
            padx=30,
            pady=(30, 5),
            anchor="w"
        )

        subtitle = ctk.CTkLabel(
            self,
            text="View and manage airport flight information",
            font=("Arial", 15)
        )

        subtitle.pack(
            padx=30,
            pady=(0, 25),
            anchor="w"
        )

        # =========================
        # Search Area
        # =========================

        search_frame = ctk.CTkFrame(self)

        search_frame.pack(
            padx=30,
            pady=10,
            fill="x"
        )

        search_label = ctk.CTkLabel(
            search_frame,
            text="Search Flight:",
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
            placeholder_text="Flight number or status"
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
            command=self.search_flights
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
            text="+ Add Flight",
            width=140,
            command=self.open_add_flight
        )

        add_button.pack(
            side="right",
            padx=15
        )

        # =========================
        # Flight Table
        # =========================

        table_frame = ctk.CTkFrame(self)

        table_frame.pack(
            padx=30,
            pady=20,
            fill="both",
            expand=True
        )

        columns = (
            "ID",
            "Flight Number",
            "Airline ID",
            "Aircraft ID",
            "Departure Airport",
            "Arrival Airport",
            "Gate ID",
            "Departure Time",
            "Arrival Time",
            "Status"
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
                width=130,
                anchor="center"
            )

        self.table.pack(
            side="left",
            fill="both",
            expand=True,
            padx=10,
            pady=10
        )

        # =========================
        # Vertical Scrollbar
        # =========================

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

        # =========================
        # Horizontal Scrollbar
        # =========================

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

        # =========================
        # Bottom Buttons
        # =========================

        button_frame = ctk.CTkFrame(self)

        button_frame.pack(
            padx=30,
            pady=(10, 25),
            fill="x"
        )

        # Edit Selected Button
        edit_button = ctk.CTkButton(
            button_frame,
            text="Edit Selected",
            width=180,
            command=self.edit_selected
        )

        edit_button.pack(
            side="left",
            padx=10,
            pady=10
        )

        # Delete Selected Button
        delete_button = ctk.CTkButton(
            button_frame,
            text="Delete Selected",
            width=180,
            command=self.delete_selected
        )

        delete_button.pack(
            side="left",
            padx=10,
            pady=10
        )

        # =========================
        # Load Flight Data
        # =========================

        self.load_flights()

    # =====================================================
    # Load Flights
    # =====================================================


    def load_flights(self, search_text=""):
        # Clear existing rows before loading fresh data.
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
                        flight_id,
                        flight_number,
                        airline_id,
                        aircraft_id,
                        departure_airport_id,
                        arrival_airport_id,
                        gate_id,
                        departure_time,
                        arrival_time,
                        status
                    FROM Flight
                    WHERE flight_number LIKE %s
                       OR status LIKE %s
                    ORDER BY flight_id
                """
                search_value = f"%{search_text}%"
                cursor.execute(query, (search_value, search_value))
            else:
                query = """
                    SELECT
                        flight_id,
                        flight_number,
                        airline_id,
                        aircraft_id,
                        departure_airport_id,
                        arrival_airport_id,
                        gate_id,
                        departure_time,
                        arrival_time,
                        status
                    FROM Flight
                    ORDER BY flight_id
                """
                cursor.execute(query)

            flights = cursor.fetchall()
            for flight in flights:
                self.table.insert("", "end", values=flight)

        except Exception as e:
            messagebox.showerror(
                "Database Error",
                f"Error loading flights:\n\n{e}"
            )

        finally:
            # Always release database resources, even if the query fails.
            if cursor is not None:
                try:
                    cursor.close()
                except Exception:
                    pass

            if connection is not None:
                try:
                    connection.close()
                except Exception:
                    pass

    def search_flights(self):

        search_text = self.search_entry.get().strip()

        self.load_flights(search_text)

    # =====================================================
    # Clear Search
    # =====================================================

    def clear_search(self):

        self.search_entry.delete(
            0,
            "end"
        )

        self.load_flights()

    # =====================================================
    # Add Flight Window
    # =====================================================

    def open_add_flight(self):

        add_window = ctk.CTkToplevel(self)

        add_window.title("Add Flight")

        add_window.geometry("550x750")

        add_window.minsize(
            550,
            650
        )

        add_window.resizable(
            True,
            True
        )

        add_window.transient(
            self.winfo_toplevel()
        )

        # =========================
        # Title
        # =========================

        title = ctk.CTkLabel(
            add_window,
            text="Add New Flight",
            font=("Arial", 26, "bold")
        )

        title.pack(
            pady=(25, 15)
        )

        # =========================
        # Scrollable Form
        # =========================

        form_frame = ctk.CTkScrollableFrame(
            add_window
        )

        form_frame.pack(
            padx=20,
            pady=10,
            fill="both",
            expand=True
        )

        # =========================
        # Flight Number
        # =========================

        ctk.CTkLabel(
            form_frame,
            text="Flight Number"
        ).pack(
            anchor="w",
            padx=20,
            pady=(10, 5)
        )

        flight_number_entry = ctk.CTkEntry(
            form_frame,
            width=450,
            placeholder_text="Example: CA123"
        )

        flight_number_entry.pack(
            padx=20
        )

        # =========================
        # Airline ID
        # =========================

        ctk.CTkLabel(
            form_frame,
            text="Airline ID"
        ).pack(
            anchor="w",
            padx=20,
            pady=(15, 5)
        )

        airline_id_entry = ctk.CTkEntry(
            form_frame,
            width=450,
            placeholder_text="Example: 1"
        )

        airline_id_entry.pack(
            padx=20
        )

        # =========================
        # Aircraft ID
        # =========================

        ctk.CTkLabel(
            form_frame,
            text="Aircraft ID"
        ).pack(
            anchor="w",
            padx=20,
            pady=(15, 5)
        )

        aircraft_id_entry = ctk.CTkEntry(
            form_frame,
            width=450,
            placeholder_text="Example: 1"
        )

        aircraft_id_entry.pack(
            padx=20
        )

        # =========================
        # Departure Airport ID
        # =========================

        ctk.CTkLabel(
            form_frame,
            text="Departure Airport ID"
        ).pack(
            anchor="w",
            padx=20,
            pady=(15, 5)
        )

        departure_airport_entry = ctk.CTkEntry(
            form_frame,
            width=450,
            placeholder_text="Example: 1"
        )

        departure_airport_entry.pack(
            padx=20
        )

        # =========================
        # Arrival Airport ID
        # =========================

        ctk.CTkLabel(
            form_frame,
            text="Arrival Airport ID"
        ).pack(
            anchor="w",
            padx=20,
            pady=(15, 5)
        )

        arrival_airport_entry = ctk.CTkEntry(
            form_frame,
            width=450,
            placeholder_text="Example: 2"
        )

        arrival_airport_entry.pack(
            padx=20
        )

        # =========================
        # Gate ID
        # =========================

        ctk.CTkLabel(
            form_frame,
            text="Gate ID"
        ).pack(
            anchor="w",
            padx=20,
            pady=(15, 5)
        )

        gate_id_entry = ctk.CTkEntry(
            form_frame,
            width=450,
            placeholder_text="Example: 1"
        )

        gate_id_entry.pack(
            padx=20
        )

        # =========================
        # Departure Time
        # =========================

        ctk.CTkLabel(
            form_frame,
            text="Departure Time"
        ).pack(
            anchor="w",
            padx=20,
            pady=(15, 5)
        )

        departure_time_entry = ctk.CTkEntry(
            form_frame,
            width=450,
            placeholder_text="YYYY-MM-DD HH:MM:SS"
        )

        departure_time_entry.pack(
            padx=20
        )

        # =========================
        # Arrival Time
        # =========================

        ctk.CTkLabel(
            form_frame,
            text="Arrival Time"
        ).pack(
            anchor="w",
            padx=20,
            pady=(15, 5)
        )

        arrival_time_entry = ctk.CTkEntry(
            form_frame,
            width=450,
            placeholder_text="YYYY-MM-DD HH:MM:SS"
        )

        arrival_time_entry.pack(
            padx=20
        )

        # =========================
        # Status
        # =========================

        ctk.CTkLabel(
            form_frame,
            text="Status"
        ).pack(
            anchor="w",
            padx=20,
            pady=(15, 5)
        )

        status_entry = ctk.CTkEntry(
            form_frame,
            width=450,
            placeholder_text="Example: Scheduled"
        )

        status_entry.pack(
            padx=20,
            pady=(0, 20)
        )

        # =========================
        # Fixed Bottom Buttons
        # =========================

        button_frame = ctk.CTkFrame(
            add_window,
            fg_color="transparent"
        )

        button_frame.pack(
            fill="x",
            padx=20,
            pady=15
        )

        cancel_button = ctk.CTkButton(
            button_frame,
            text="Cancel",
            width=150,
            command=add_window.destroy
        )

        cancel_button.pack(
            side="left",
            padx=10
        )

        save_button = ctk.CTkButton(
            button_frame,
            text="Save Flight",
            width=150,
            command=lambda: self.save_flight(
                add_window,
                flight_number_entry,
                airline_id_entry,
                aircraft_id_entry,
                departure_airport_entry,
                arrival_airport_entry,
                gate_id_entry,
                departure_time_entry,
                arrival_time_entry,
                status_entry
            )
        )

        save_button.pack(
            side="right",
            padx=10
        )

    # =====================================================
    # Save New Flight
    # =====================================================


    def save_flight(
        self,
        add_window,
        flight_number_entry,
        airline_id_entry,
        aircraft_id_entry,
        departure_airport_entry,
        arrival_airport_entry,
        gate_id_entry,
        departure_time_entry,
        arrival_time_entry,
        status_entry
    ):
        flight_number = flight_number_entry.get().strip()
        airline_id = airline_id_entry.get().strip()
        aircraft_id = aircraft_id_entry.get().strip()
        departure_airport_id = departure_airport_entry.get().strip()
        arrival_airport_id = arrival_airport_entry.get().strip()
        gate_id = gate_id_entry.get().strip()
        departure_time = departure_time_entry.get().strip()
        arrival_time = arrival_time_entry.get().strip()
        status = status_entry.get().strip()

        # Check required fields.
        fields = [
            (flight_number, "Flight Number"),
            (airline_id, "Airline ID"),
            (aircraft_id, "Aircraft ID"),
            (departure_airport_id, "Departure Airport ID"),
            (arrival_airport_id, "Arrival Airport ID"),
            (gate_id, "Gate ID"),
            (departure_time, "Departure Time"),
            (arrival_time, "Arrival Time"),
            (status, "Flight Status")
        ]

        for value, label in fields:
            if not value:
                messagebox.showwarning(
                    "Missing Information",
                    f"Please enter the {label}."
                )
                return

        # IDs must be positive integers.
        try:
            airline_id = int(airline_id)
            aircraft_id = int(aircraft_id)
            departure_airport_id = int(departure_airport_id)
            arrival_airport_id = int(arrival_airport_id)
            gate_id = int(gate_id)

            if min(
                airline_id,
                aircraft_id,
                departure_airport_id,
                arrival_airport_id,
                gate_id
            ) <= 0:
                raise ValueError
        except ValueError:
            messagebox.showwarning(
                "Invalid Information",
                "Airline, Aircraft, Airport, and Gate IDs must be positive numbers."
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
                INSERT INTO Flight
                (
                    flight_number,
                    airline_id,
                    aircraft_id,
                    departure_airport_id,
                    arrival_airport_id,
                    gate_id,
                    departure_time,
                    arrival_time,
                    status
                )
                VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s)
            """
            values = (
                flight_number,
                airline_id,
                aircraft_id,
                departure_airport_id,
                arrival_airport_id,
                gate_id,
                departure_time,
                arrival_time,
                status
            )

            cursor.execute(query, values)
            connection.commit()

            messagebox.showinfo(
                "Success",
                "Flight added successfully!"
            )
            add_window.destroy()
            self.load_flights()

        except Exception as e:
            try:
                connection.rollback()
            except Exception:
                pass

            messagebox.showerror(
                "Database Error",
                f"Could not add flight.\n\n{e}"
            )

        finally:
            if cursor is not None:
                try:
                    cursor.close()
                except Exception:
                    pass

            try:
                connection.close()
            except Exception:
                pass

    def edit_selected(self):

        selected = self.table.selection()

        if not selected:

            messagebox.showwarning(
                "No Selection",
                "Please select a flight to edit."
            )

            return

        # Get selected row
        item = self.table.item(
            selected[0]
        )

        flight = item["values"]

        # =========================
        # Get Flight Information
        # =========================

        flight_id = flight[0]
        flight_number = flight[1]
        airline_id = flight[2]
        aircraft_id = flight[3]
        departure_airport_id = flight[4]
        arrival_airport_id = flight[5]
        gate_id = flight[6]
        departure_time = flight[7]
        arrival_time = flight[8]
        status = flight[9]

        # =========================
        # Edit Window
        # =========================

        edit_window = ctk.CTkToplevel(self)

        edit_window.title("Edit Flight")

        edit_window.geometry("550x750")

        edit_window.minsize(
            550,
            650
        )

        edit_window.resizable(
            True,
            True
        )

        edit_window.transient(
            self.winfo_toplevel()
        )

        # =========================
        # Title
        # =========================

        title = ctk.CTkLabel(
            edit_window,
            text="Edit Flight",
            font=("Arial", 26, "bold")
        )

        title.pack(
            pady=(25, 15)
        )

        # =========================
        # Scrollable Form
        # =========================

        form_frame = ctk.CTkScrollableFrame(
            edit_window
        )

        form_frame.pack(
            padx=20,
            pady=10,
            fill="both",
            expand=True
        )

        # =========================
        # Flight Number
        # =========================

        ctk.CTkLabel(
            form_frame,
            text="Flight Number"
        ).pack(
            anchor="w",
            padx=20,
            pady=(10, 5)
        )

        flight_number_entry = ctk.CTkEntry(
            form_frame,
            width=450
        )

        flight_number_entry.pack(
            padx=20
        )

        flight_number_entry.insert(
            0,
            str(flight_number)
        )

        # =========================
        # Airline ID
        # =========================

        ctk.CTkLabel(
            form_frame,
            text="Airline ID"
        ).pack(
            anchor="w",
            padx=20,
            pady=(15, 5)
        )

        airline_id_entry = ctk.CTkEntry(
            form_frame,
            width=450
        )

        airline_id_entry.pack(
            padx=20
        )

        airline_id_entry.insert(
            0,
            str(airline_id)
        )

        # =========================
        # Aircraft ID
        # =========================

        ctk.CTkLabel(
            form_frame,
            text="Aircraft ID"
        ).pack(
            anchor="w",
            padx=20,
            pady=(15, 5)
        )

        aircraft_id_entry = ctk.CTkEntry(
            form_frame,
            width=450
        )

        aircraft_id_entry.pack(
            padx=20
        )

        aircraft_id_entry.insert(
            0,
            str(aircraft_id)
        )

        # =========================
        # Departure Airport ID
        # =========================

        ctk.CTkLabel(
            form_frame,
            text="Departure Airport ID"
        ).pack(
            anchor="w",
            padx=20,
            pady=(15, 5)
        )

        departure_airport_entry = ctk.CTkEntry(
            form_frame,
            width=450
        )

        departure_airport_entry.pack(
            padx=20
        )

        departure_airport_entry.insert(
            0,
            str(departure_airport_id)
        )

        # =========================
        # Arrival Airport ID
        # =========================

        ctk.CTkLabel(
            form_frame,
            text="Arrival Airport ID"
        ).pack(
            anchor="w",
            padx=20,
            pady=(15, 5)
        )

        arrival_airport_entry = ctk.CTkEntry(
            form_frame,
            width=450
        )

        arrival_airport_entry.pack(
            padx=20
        )

        arrival_airport_entry.insert(
            0,
            str(arrival_airport_id)
        )

        # =========================
        # Gate ID
        # =========================

        ctk.CTkLabel(
            form_frame,
            text="Gate ID"
        ).pack(
            anchor="w",
            padx=20,
            pady=(15, 5)
        )

        gate_id_entry = ctk.CTkEntry(
            form_frame,
            width=450
        )

        gate_id_entry.pack(
            padx=20
        )

        gate_id_entry.insert(
            0,
            str(gate_id)
        )

        # =========================
        # Departure Time
        # =========================

        ctk.CTkLabel(
            form_frame,
            text="Departure Time"
        ).pack(
            anchor="w",
            padx=20,
            pady=(15, 5)
        )

        departure_time_entry = ctk.CTkEntry(
            form_frame,
            width=450
        )

        departure_time_entry.pack(
            padx=20
        )

        departure_time_entry.insert(
            0,
            str(departure_time)
        )

        # =========================
        # Arrival Time
        # =========================

        ctk.CTkLabel(
            form_frame,
            text="Arrival Time"
        ).pack(
            anchor="w",
            padx=20,
            pady=(15, 5)
        )

        arrival_time_entry = ctk.CTkEntry(
            form_frame,
            width=450
        )

        arrival_time_entry.pack(
            padx=20
        )

        arrival_time_entry.insert(
            0,
            str(arrival_time)
        )

        # =========================
        # Status
        # =========================

        ctk.CTkLabel(
            form_frame,
            text="Status"
        ).pack(
            anchor="w",
            padx=20,
            pady=(15, 5)
        )

        status_entry = ctk.CTkEntry(
            form_frame,
            width=450
        )

        status_entry.pack(
            padx=20,
            pady=(0, 20)
        )

        status_entry.insert(
            0,
            str(status)
        )

        # =========================
        # Fixed Bottom Buttons
        # =========================

        button_frame = ctk.CTkFrame(
            edit_window,
            fg_color="transparent"
        )

        button_frame.pack(
            fill="x",
            padx=20,
            pady=15
        )

        # Cancel Button
        cancel_button = ctk.CTkButton(
            button_frame,
            text="Cancel",
            width=150,
            command=edit_window.destroy
        )

        cancel_button.pack(
            side="left",
            padx=10
        )

        # Save Changes Button
        save_button = ctk.CTkButton(
            button_frame,
            text="Save Changes",
            width=150,
            command=lambda: self.save_changes(
                edit_window,
                flight_id,
                flight_number_entry,
                airline_id_entry,
                aircraft_id_entry,
                departure_airport_entry,
                arrival_airport_entry,
                gate_id_entry,
                departure_time_entry,
                arrival_time_entry,
                status_entry
            )
        )

        save_button.pack(
            side="right",
            padx=10
        )

    # =====================================================
    # Save Edited Flight
    # =====================================================


    def save_changes(
        self,
        edit_window,
        flight_id,
        flight_number_entry,
        airline_id_entry,
        aircraft_id_entry,
        departure_airport_entry,
        arrival_airport_entry,
        gate_id_entry,
        departure_time_entry,
        arrival_time_entry,
        status_entry
    ):
        flight_number = flight_number_entry.get().strip()
        airline_id = airline_id_entry.get().strip()
        aircraft_id = aircraft_id_entry.get().strip()
        departure_airport_id = departure_airport_entry.get().strip()
        arrival_airport_id = arrival_airport_entry.get().strip()
        gate_id = gate_id_entry.get().strip()
        departure_time = departure_time_entry.get().strip()
        arrival_time = arrival_time_entry.get().strip()
        status = status_entry.get().strip()

        fields = [
            (flight_number, "Flight Number"),
            (airline_id, "Airline ID"),
            (aircraft_id, "Aircraft ID"),
            (departure_airport_id, "Departure Airport ID"),
            (arrival_airport_id, "Arrival Airport ID"),
            (gate_id, "Gate ID"),
            (departure_time, "Departure Time"),
            (arrival_time, "Arrival Time"),
            (status, "Flight Status")
        ]

        for value, label in fields:
            if not value:
                messagebox.showwarning(
                    "Missing Information",
                    f"Please enter the {label}."
                )
                return

        try:
            airline_id = int(airline_id)
            aircraft_id = int(aircraft_id)
            departure_airport_id = int(departure_airport_id)
            arrival_airport_id = int(arrival_airport_id)
            gate_id = int(gate_id)

            if min(
                airline_id,
                aircraft_id,
                departure_airport_id,
                arrival_airport_id,
                gate_id
            ) <= 0:
                raise ValueError
        except ValueError:
            messagebox.showwarning(
                "Invalid Information",
                "Airline, Aircraft, Airport, and Gate IDs must be positive numbers."
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
                UPDATE Flight
                SET
                    flight_number = %s,
                    airline_id = %s,
                    aircraft_id = %s,
                    departure_airport_id = %s,
                    arrival_airport_id = %s,
                    gate_id = %s,
                    departure_time = %s,
                    arrival_time = %s,
                    status = %s
                WHERE flight_id = %s
            """
            values = (
                flight_number,
                airline_id,
                aircraft_id,
                departure_airport_id,
                arrival_airport_id,
                gate_id,
                departure_time,
                arrival_time,
                status,
                flight_id
            )

            cursor.execute(query, values)
            connection.commit()

            messagebox.showinfo(
                "Success",
                "Flight updated successfully!"
            )
            edit_window.destroy()
            self.load_flights()

        except Exception as e:
            try:
                connection.rollback()
            except Exception:
                pass

            messagebox.showerror(
                "Database Error",
                f"Could not update flight.\n\n{e}"
            )

        finally:
            if cursor is not None:
                try:
                    cursor.close()
                except Exception:
                    pass

            try:
                connection.close()
            except Exception:
                pass


    def delete_selected(self):
        selected = self.table.selection()
        if not selected:
            messagebox.showwarning(
                "No Selection",
                "Please select a flight to delete."
            )
            return

        item = self.table.item(selected[0])
        flight = item["values"]
        flight_id = flight[0]

        confirm = messagebox.askyesno(
            "Confirm Delete",
            f"Are you sure you want to delete flight {flight[1]}?"
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
                DELETE FROM Flight
                WHERE flight_id = %s
            """
            cursor.execute(query, (flight_id,))
            connection.commit()

            messagebox.showinfo(
                "Success",
                "Flight deleted successfully!"
            )
            self.load_flights()

        except Exception as e:
            try:
                connection.rollback()
            except Exception:
                pass

            messagebox.showerror(
                "Database Error",
                f"Could not delete flight. This flight may have existing bookings.\n\n{e}"
            )

        finally:
            if cursor is not None:
                try:
                    cursor.close()
                except Exception:
                    pass

            try:
                connection.close()
            except Exception:
                pass


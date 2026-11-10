import customtkinter as ctk
from tkinter import ttk, messagebox

from database import create_connection


class ReportsPage(ctk.CTkFrame):

    def __init__(self, parent):
        super().__init__(parent)

        # =====================================================
        # Page Title
        # =====================================================

        title = ctk.CTkLabel(
            self,
            text="Reports",
            font=("Arial", 28, "bold")
        )

        title.pack(
            padx=30,
            pady=(30, 5),
            anchor="w"
        )

        subtitle = ctk.CTkLabel(
            self,
            text="View reports and statistics from the airport database",
            font=("Arial", 15)
        )

        subtitle.pack(
            padx=30,
            pady=(0, 25),
            anchor="w"
        )

        # =====================================================
        # Statistics Cards
        # =====================================================

        stats_frame = ctk.CTkFrame(
            self,
            fg_color="transparent"
        )

        stats_frame.pack(
            padx=30,
            pady=10,
            fill="x"
        )

        # Passenger Card
        self.passenger_card = self.create_stat_card(
            stats_frame,
            "Total Passengers"
        )

        self.passenger_card.pack(
            side="left",
            padx=5,
            fill="x",
            expand=True
        )

        # Flight Card
        self.flight_card = self.create_stat_card(
            stats_frame,
            "Total Flights"
        )

        self.flight_card.pack(
            side="left",
            padx=5,
            fill="x",
            expand=True
        )

        # Booking Card
        self.booking_card = self.create_stat_card(
            stats_frame,
            "Total Bookings"
        )

        self.booking_card.pack(
            side="left",
            padx=5,
            fill="x",
            expand=True
        )

        # Baggage Card
        self.baggage_card = self.create_stat_card(
            stats_frame,
            "Total Baggage"
        )

        self.baggage_card.pack(
            side="left",
            padx=5,
            fill="x",
            expand=True
        )

        # =====================================================
        # Report Selection
        # =====================================================

        report_frame = ctk.CTkFrame(self)

        report_frame.pack(
            padx=30,
            pady=20,
            fill="x"
        )

        report_label = ctk.CTkLabel(
            report_frame,
            text="Select Report",
            font=("Arial", 15, "bold")
        )

        report_label.pack(
            side="left",
            padx=(15, 10),
            pady=15
        )

        self.report_combo = ctk.CTkComboBox(
            report_frame,
            width=310,
            values=[
                "Passengers by Nationality",
                "Flights by Airline",
                "Bookings by Class",
                "Baggage by Status"
            ],
            command=self.on_report_changed
        )

        self.report_combo.set(
            "Passengers by Nationality"
        )

        self.report_combo.pack(
            side="left",
            padx=10,
            pady=15
        )

        # =====================================================
        # Refresh Button
        # =====================================================

        refresh_button = ctk.CTkButton(
            report_frame,
            text="⟳ Refresh",
            width=150,
            command=self.refresh_reports
        )

        refresh_button.pack(
            side="right",
            padx=15,
            pady=15
        )

        # =====================================================
        # Report Table
        # =====================================================

        table_frame = ctk.CTkFrame(self)

        table_frame.pack(
            padx=30,
            pady=10,
            fill="both",
            expand=True
        )

        self.table = ttk.Treeview(
            table_frame,
            show="headings"
        )

        self.table.pack(
            side="left",
            fill="both",
            expand=True,
            padx=10,
            pady=10
        )

        # Vertical Scrollbar
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

        # Horizontal Scrollbar
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
        # Initial Load
        # =====================================================

        self.refresh_reports()

    # =========================================================
    # Create Statistic Card
    # =========================================================

    def create_stat_card(
        self,
        parent,
        title
    ):

        card = ctk.CTkFrame(
            parent
        )

        title_label = ctk.CTkLabel(
            card,
            text=title,
            font=("Arial", 16, "bold")
        )

        title_label.pack(
            pady=(25, 5)
        )

        value_label = ctk.CTkLabel(
            card,
            text="0",
            font=("Arial", 30, "bold")
        )

        value_label.pack(
            pady=(0, 20)
        )

        card.value_label = value_label

        return card

    # =========================================================
    # Load Statistics
    # =========================================================

    def load_statistics(self):

        connection = create_connection()

        if connection is None:
            messagebox.showerror(
                "Database Error",
                "Could not connect to the database."
            )
            return

        try:

            cursor = connection.cursor()

            # Total Passengers
            cursor.execute(
                "SELECT COUNT(*) FROM Passenger"
            )

            total_passengers = cursor.fetchone()[0]

            # Total Flights
            cursor.execute(
                "SELECT COUNT(*) FROM Flight"
            )

            total_flights = cursor.fetchone()[0]

            # Total Bookings
            cursor.execute(
                "SELECT COUNT(*) FROM Booking"
            )

            total_bookings = cursor.fetchone()[0]

            # Total Baggage
            cursor.execute(
                "SELECT COUNT(*) FROM Baggage"
            )

            total_baggage = cursor.fetchone()[0]

            cursor.close()
            connection.close()

            # Update cards
            self.passenger_card.value_label.configure(
                text=str(total_passengers)
            )

            self.flight_card.value_label.configure(
                text=str(total_flights)
            )

            self.booking_card.value_label.configure(
                text=str(total_bookings)
            )

            self.baggage_card.value_label.configure(
                text=str(total_baggage)
            )

        except Exception as e:

            print(
                f"Error loading statistics: {e}"
            )

            messagebox.showerror(
                "Error",
                f"Could not load statistics.\n\n{e}"
            )

            if connection.is_connected():
                connection.close()

    # =========================================================
    # Refresh Reports
    # =========================================================

    def refresh_reports(self):

        print("Refreshing reports...")

        # Reload summary cards
        self.load_statistics()

        # Reload current report
        selected_report = self.report_combo.get()

        self.load_report(
            selected_report
        )

        print("Reports refreshed successfully.")

    # =========================================================
    # Report Selection Changed
    # =========================================================

    def on_report_changed(
        self,
        selected_report
    ):

        self.load_report(
            selected_report
        )

    # =========================================================
    # Load Selected Report
    # =========================================================

    def load_report(
        self,
        report_name
    ):

        # Clear old table
        for item in self.table.get_children():
            self.table.delete(item)

        # =====================================================
        # Passengers by Nationality
        # =====================================================

        if report_name == "Passengers by Nationality":

            columns = (
                "Nationality",
                "Number of Passengers"
            )

            self.setup_table(
                columns
            )

            connection = create_connection()

            if connection is None:
                return

            try:

                cursor = connection.cursor()

                query = """
                    SELECT
                        nationality,
                        COUNT(*) AS total_passengers
                    FROM Passenger
                    GROUP BY nationality
                    ORDER BY total_passengers DESC
                """

                cursor.execute(query)

                rows = cursor.fetchall()

                for row in rows:

                    self.table.insert(
                        "",
                        "end",
                        values=row
                    )

                cursor.close()
                connection.close()

            except Exception as e:

                messagebox.showerror(
                    "Error",
                    f"Could not load report.\n\n{e}"
                )

                if connection.is_connected():
                    connection.close()

        # =====================================================
        # Flights by Airline
        # =====================================================

        elif report_name == "Flights by Airline":

            columns = (
                "Airline ID",
                "Number of Flights"
            )

            self.setup_table(
                columns
            )

            connection = create_connection()

            if connection is None:
                return

            try:

                cursor = connection.cursor()

                query = """
                    SELECT
                        airline_id,
                        COUNT(*) AS total_flights
                    FROM Flight
                    GROUP BY airline_id
                    ORDER BY total_flights DESC
                """

                cursor.execute(query)

                rows = cursor.fetchall()

                for row in rows:

                    self.table.insert(
                        "",
                        "end",
                        values=row
                    )

                cursor.close()
                connection.close()

            except Exception as e:

                messagebox.showerror(
                    "Error",
                    f"Could not load report.\n\n{e}"
                )

                if connection.is_connected():
                    connection.close()

        # =====================================================
        # Bookings by Class
        # =====================================================

        elif report_name == "Bookings by Class":

            columns = (
                "Class",
                "Number of Bookings"
            )

            self.setup_table(
                columns
            )

            connection = create_connection()

            if connection is None:
                return

            try:

                cursor = connection.cursor()

                query = """
                    SELECT
                        class,
                        COUNT(*) AS total_bookings
                    FROM Booking
                    GROUP BY class
                    ORDER BY total_bookings DESC
                """

                cursor.execute(query)

                rows = cursor.fetchall()

                for row in rows:

                    self.table.insert(
                        "",
                        "end",
                        values=row
                    )

                cursor.close()
                connection.close()

            except Exception as e:

                messagebox.showerror(
                    "Error",
                    f"Could not load report.\n\n{e}"
                )

                if connection.is_connected():
                    connection.close()

        # =====================================================
        # Baggage by Status
        # =====================================================

        elif report_name == "Baggage by Status":

            columns = (
                "Status",
                "Number of Baggage"
            )

            self.setup_table(
                columns
            )

            connection = create_connection()

            if connection is None:
                return

            try:

                cursor = connection.cursor()

                query = """
                    SELECT
                        status,
                        COUNT(*) AS total_baggage
                    FROM Baggage
                    GROUP BY status
                    ORDER BY total_baggage DESC
                """

                cursor.execute(query)

                rows = cursor.fetchall()

                for row in rows:

                    self.table.insert(
                        "",
                        "end",
                        values=row
                    )

                cursor.close()
                connection.close()

            except Exception as e:

                messagebox.showerror(
                    "Error",
                    f"Could not load report.\n\n{e}"
                )

                if connection.is_connected():
                    connection.close()

    # =========================================================
    # Setup Table
    # =========================================================

    def setup_table(
        self,
        columns
    ):

        self.table["columns"] = columns

        for column in columns:

            self.table.heading(
                column,
                text=column
            )

            self.table.column(
                column,
                width=250,
                anchor="center"
            )
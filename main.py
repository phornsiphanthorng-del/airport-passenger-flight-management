import customtkinter as ctk
from tkinter import ttk, messagebox
from datetime import datetime

from database import create_connection
from pages.passengers import PassengerPage
from pages.flights import FlightPage
from pages.booking import BookingPage
from pages.baggage import BaggagePage
from pages.reports import ReportsPage
from pages.settings import SettingsPage


# ============================================================
# APPLICATION THEME
# ============================================================

ctk.set_appearance_mode("light")
ctk.set_default_color_theme("blue")

NAVY = "#0B2D52"
NAVY_2 = "#123E6B"
BLUE = "#1769D2"
BLUE_LIGHT = "#EAF3FF"
TEXT = "#17324D"
MUTED = "#66788A"
WHITE = "#FFFFFF"
BORDER = "#DCE5EE"
GREEN = "#19A974"
ORANGE = "#F59E0B"
PURPLE = "#7C4DDB"
RED = "#E5484D"
BG = "#F5F8FC"


class AirportManagementApp(ctk.CTk):

    def __init__(self):
        super().__init__()

        self.title("Airport Passenger & Flight Data Management System")
        self.geometry("1450x900")
        self.minsize(1150, 700)
        self.configure(fg_color=BG)

        self.current_page = None
        self.search_var = ctk.StringVar()

        self.protocol("WM_DELETE_WINDOW", self.destroy)

        self.build_layout()
        self.show_dashboard()

    # ========================================================
    # MAIN LAYOUT
    # ========================================================

    def build_layout(self):

        self.sidebar = ctk.CTkFrame(
            self,
            width=250,
            corner_radius=0,
            fg_color=NAVY
        )
        self.sidebar.pack(side="left", fill="y")
        self.sidebar.pack_propagate(False)

        self.right_area = ctk.CTkFrame(
            self,
            corner_radius=0,
            fg_color=BG
        )
        self.right_area.pack(
            side="right",
            fill="both",
            expand=True
        )

        self.build_sidebar()
        self.build_topbar()

        self.content = ctk.CTkFrame(
            self.right_area,
            corner_radius=0,
            fg_color=BG
        )
        self.content.pack(
            fill="both",
            expand=True
        )

    # ========================================================
    # SIDEBAR
    # ========================================================

    def build_sidebar(self):

        brand = ctk.CTkFrame(
            self.sidebar,
            fg_color="transparent"
        )
        brand.pack(
            fill="x",
            padx=22,
            pady=(25, 30)
        )

        ctk.CTkLabel(
            brand,
            text="✈",
            font=ctk.CTkFont(
                size=38,
                weight="bold"
            ),
            text_color=WHITE
        ).pack(anchor="w")

        ctk.CTkLabel(
            brand,
            text="Airport Passenger & Flight\nData Management System",
            font=ctk.CTkFont(
                size=16,
                weight="bold"
            ),
            text_color=WHITE,
            justify="left"
        ).pack(
            anchor="w",
            pady=(5, 0)
        )

        self.nav_buttons = {}

        nav_items = [
            ("⌂", "Dashboard", self.show_dashboard),
            ("♟", "Passengers", self.show_passengers),
            ("✈", "Flights", self.show_flights),
            ("▣", "Bookings", self.show_bookings),
            ("▰", "Baggage", self.show_baggage),
            ("▥", "Reports", self.show_reports),
            ("⚙", "Settings", self.show_settings),
        ]

        for icon, text, command in nav_items:

            button = ctk.CTkButton(
                self.sidebar,
                text=f"  {icon}    {text}",
                anchor="w",
                height=48,
                corner_radius=9,
                fg_color="transparent",
                hover_color=NAVY_2,
                text_color="#DCEBFA",
                font=ctk.CTkFont(
                    size=14,
                    weight="bold"
                ),
                command=command
            )

            button.pack(
                fill="x",
                padx=12,
                pady=5
            )

            self.nav_buttons[text] = button

        ctk.CTkFrame(
            self.sidebar,
            height=2,
            fg_color="#28547D"
        ).pack(
            fill="x",
            padx=18,
            pady=(22, 15)
        )

        bottom = ctk.CTkFrame(
            self.sidebar,
            fg_color="transparent"
        )
        bottom.pack(
            side="bottom",
            fill="x",
            padx=20,
            pady=20
        )

        ctk.CTkLabel(
            bottom,
            text="●  MySQL Database",
            text_color="#A9E6C7",
            font=ctk.CTkFont(
                size=12,
                weight="bold"
            )
        ).pack(anchor="w")

        ctk.CTkLabel(
            bottom,
            text="localhost:3306",
            text_color="#91A8BD",
            font=ctk.CTkFont(size=11)
        ).pack(
            anchor="w",
            pady=(4, 0)
        )

    # ========================================================
    # TOP BAR
    # ========================================================

    def build_topbar(self):

        topbar = ctk.CTkFrame(
            self.right_area,
            height=74,
            corner_radius=0,
            fg_color=WHITE,
            border_width=1,
            border_color=BORDER
        )

        topbar.pack(fill="x")
        topbar.pack_propagate(False)

        search_frame = ctk.CTkFrame(
            topbar,
            fg_color=BLUE_LIGHT,
            corner_radius=10
        )

        search_frame.pack(
            side="left",
            fill="x",
            expand=True,
            padx=(24, 15),
            pady=15
        )

        ctk.CTkLabel(
            search_frame,
            text="⌕",
            font=ctk.CTkFont(size=25),
            text_color=BLUE
        ).pack(
            side="left",
            padx=(14, 5)
        )

        self.global_search = ctk.CTkEntry(
            search_frame,
            textvariable=self.search_var,
            placeholder_text="Search passengers, flights, bookings...",
            border_width=0,
            fg_color="transparent",
            text_color=TEXT,
            font=ctk.CTkFont(size=13),
            height=40
        )

        self.global_search.pack(
            side="left",
            fill="x",
            expand=True
        )

        self.global_search.bind(
            "<Return>",
            self.global_search_action
        )

        ctk.CTkButton(
            topbar,
            text="🔔",
            width=42,
            height=42,
            fg_color="transparent",
            hover_color=BLUE_LIGHT,
            text_color=TEXT,
            font=ctk.CTkFont(size=18),
            command=self.show_notifications
        ).pack(
            side="right",
            padx=(0, 3)
        )

        profile = ctk.CTkFrame(
            topbar,
            fg_color="transparent"
        )

        profile.pack(
            side="right",
            padx=(5, 22)
        )

        ctk.CTkLabel(
            profile,
            text="●",
            width=42,
            height=42,
            corner_radius=21,
            fg_color=BLUE_LIGHT,
            text_color=BLUE,
            font=ctk.CTkFont(
                size=20,
                weight="bold"
            )
        ).pack(
            side="left",
            padx=(0, 9)
        )

        ctk.CTkLabel(
            profile,
            text="Admin",
            text_color=TEXT,
            font=ctk.CTkFont(
                size=13,
                weight="bold"
            )
        ).pack(side="left")

        ctk.CTkLabel(
            profile,
            text="⌄",
            text_color=MUTED,
            font=ctk.CTkFont(size=16)
        ).pack(
            side="left",
            padx=(5, 0)
        )

    # ========================================================
    # NAVIGATION
    # ========================================================

    def set_active_nav(self, name):

        for key, button in self.nav_buttons.items():

            if key == name:

                button.configure(
                    fg_color=BLUE,
                    text_color=WHITE
                )

            else:

                button.configure(
                    fg_color="transparent",
                    text_color="#DCEBFA"
                )

    def clear_content(self):

        for widget in self.content.winfo_children():
            widget.destroy()

    def show_dashboard(self):

        self.clear_content()
        self.set_active_nav("Dashboard")
        self.current_page = "Dashboard"

        self.build_dashboard()

    def show_passengers(self):

        self.clear_content()
        self.set_active_nav("Passengers")
        self.current_page = "Passengers"

        PassengerPage(
            self.content
        ).pack(
            fill="both",
            expand=True
        )

    def show_flights(self):

        self.clear_content()
        self.set_active_nav("Flights")
        self.current_page = "Flights"

        FlightPage(
            self.content
        ).pack(
            fill="both",
            expand=True
        )

    def show_bookings(self):

        self.clear_content()
        self.set_active_nav("Bookings")
        self.current_page = "Bookings"

        BookingPage(
            self.content
        ).pack(
            fill="both",
            expand=True
        )

    def show_baggage(self):

        self.clear_content()
        self.set_active_nav("Baggage")
        self.current_page = "Baggage"

        BaggagePage(
            self.content
        ).pack(
            fill="both",
            expand=True
        )

    def show_reports(self):

        self.clear_content()
        self.set_active_nav("Reports")
        self.current_page = "Reports"

        ReportsPage(
            self.content
        ).pack(
            fill="both",
            expand=True
        )

    def show_settings(self):

        self.clear_content()
        self.set_active_nav("Settings")
        self.current_page = "Settings"

        SettingsPage(
            self.content
        ).pack(
            fill="both",
            expand=True
        )

    # ========================================================
    # DATABASE HELPERS
    # ========================================================

    def get_count(self, table_name):

        connection = None
        cursor = None

        try:

            connection = create_connection()

            if not connection:
                return 0

            cursor = connection.cursor()

            cursor.execute(
                f"SELECT COUNT(*) FROM {table_name}"
            )

            result = cursor.fetchone()

            return int(result[0]) if result else 0

        except Exception:

            return 0

        finally:

            try:

                if cursor:
                    cursor.close()

                if connection:
                    connection.close()

            except Exception:
                pass

    def get_dashboard_data(self):

        # None means that the database could not be read.
        data = {
            "passengers": None,
            "flights": None,
            "bookings": None,
            "baggage": None
        }

        airlines = None
        booking_classes = None
        upcoming = None

        connection = None
        cursor = None

        try:
            # Use ONE connection for every dashboard query.
            connection = create_connection()

            if connection is None:
                return data, airlines, booking_classes, upcoming, False

            cursor = connection.cursor(dictionary=True)

            cursor.execute("SELECT COUNT(*) AS total FROM Passenger")
            data["passengers"] = cursor.fetchone()["total"]

            cursor.execute("SELECT COUNT(*) AS total FROM Flight")
            data["flights"] = cursor.fetchone()["total"]

            cursor.execute("SELECT COUNT(*) AS total FROM Booking")
            data["bookings"] = cursor.fetchone()["total"]

            cursor.execute("SELECT COUNT(*) AS total FROM Baggage")
            data["baggage"] = cursor.fetchone()["total"]

            cursor.execute("""
                SELECT
                    a.airline_name,
                    COUNT(f.flight_id) AS total
                FROM Flight f
                JOIN Airline a
                    ON f.airline_id = a.airline_id
                GROUP BY
                    a.airline_id,
                    a.airline_name
                ORDER BY total DESC
            """)
            airlines = cursor.fetchall()

            cursor.execute("""
                SELECT
                    class,
                    COUNT(*) AS total
                FROM Booking
                GROUP BY class
                ORDER BY total DESC
            """)
            booking_classes = cursor.fetchall()

            cursor.execute("""
                SELECT
                    f.flight_number,
                    a.airline_name,
                    f.departure_time,
                    f.arrival_time,
                    f.status
                FROM Flight f
                JOIN Airline a
                    ON f.airline_id = a.airline_id
                WHERE f.departure_time >= NOW()
                ORDER BY f.departure_time ASC
                LIMIT 5
            """)
            upcoming = cursor.fetchall()

            return data, airlines, booking_classes, upcoming, True

        except Exception as e:
            print("Dashboard database error:", e)
            return (
                {"passengers": None, "flights": None,
                 "bookings": None, "baggage": None},
                None,
                None,
                None,
                False
            )

        finally:
            try:
                if cursor is not None:
                    cursor.close()
            except Exception:
                pass

            try:
                if connection is not None and connection.is_connected():
                    connection.close()
            except Exception:
                pass

    def build_dashboard(self):

        outer = ctk.CTkScrollableFrame(
            self.content,
            fg_color=BG,
            corner_radius=0
        )
        outer.pack(fill="both", expand=True)

        # ---------------- HEADER ----------------
        header = ctk.CTkFrame(outer, fg_color="transparent")
        header.pack(fill="x", padx=24, pady=(22, 8))

        left_header = ctk.CTkFrame(header, fg_color="transparent")
        left_header.pack(side="left")

        ctk.CTkLabel(
            left_header,
            text="Welcome, Admin",
            text_color=TEXT,
            font=ctk.CTkFont(size=27, weight="bold")
        ).pack(anchor="w")

        ctk.CTkLabel(
            left_header,
            text="Manage passengers, flights, bookings and more — all in one place.",
            text_color=MUTED,
            font=ctk.CTkFont(size=13)
        ).pack(anchor="w", pady=(4, 0))

        date_text = datetime.now().strftime("%A, %d %B %Y")
        time_text = datetime.now().strftime("%I:%M %p")

        right_header = ctk.CTkFrame(header, fg_color="transparent")
        right_header.pack(side="right", padx=(10, 5))

        ctk.CTkLabel(
            right_header,
            text=date_text,
            text_color=MUTED,
            font=ctk.CTkFont(size=12)
        ).pack(anchor="e")

        ctk.CTkLabel(
            right_header,
            text=time_text,
            text_color=TEXT,
            font=ctk.CTkFont(size=13, weight="bold")
        ).pack(anchor="e", pady=(2, 0))

        # ---------------- DATABASE DATA ----------------
        (
            data,
            airlines,
            booking_classes,
            upcoming,
            database_available
        ) = self.get_dashboard_data()

        # ---------------- STAT CARDS ----------------
        cards = ctk.CTkFrame(outer, fg_color="transparent")
        cards.pack(fill="x", padx=24, pady=(10, 15))

        card_info = [
            ("Total Passengers", data["passengers"], "♟", BLUE),
            ("Total Flights", data["flights"], "✈", BLUE),
            ("Total Bookings", data["bookings"], "▣", GREEN),
            ("Total Baggage", data["baggage"], "▰", ORANGE),
        ]

        for title, value, icon, accent in card_info:
            self.create_stat_card(
                cards, title, value, icon, accent, database_available
            )

        # ---------------- CHARTS ----------------
        charts_row = ctk.CTkFrame(outer, fg_color="transparent")
        charts_row.pack(fill="x", padx=24, pady=(0, 15))

        airline_card = self.create_panel(charts_row, "Flights by Airline")
        airline_card.pack(
            side="left", fill="both", expand=True, padx=(0, 8)
        )

        class_card = self.create_panel(charts_row, "Bookings by Class")
        class_card.pack(
            side="right", fill="both", expand=True, padx=(8, 0)
        )

        self.draw_airline_chart(airline_card, airlines)
        self.draw_class_chart(class_card, booking_classes)

        # ---------------- BOTTOM ----------------
        bottom_row = ctk.CTkFrame(outer, fg_color="transparent")
        bottom_row.pack(fill="x", padx=24, pady=(0, 15))

        flight_card = self.create_panel(bottom_row, "Upcoming Flights")
        flight_card.pack(
            side="left", fill="both", expand=True, padx=(0, 8)
        )

        activity_card = self.create_panel(bottom_row, "Recent Activities")
        activity_card.pack(
            side="right", fill="both", expand=True, padx=(8, 0)
        )

        self.build_upcoming_flights(flight_card, upcoming)
        self.build_recent_activities(activity_card, data)

        # ---------------- QUICK ACTIONS ----------------
        quick = self.create_panel(outer, "Quick Actions")
        quick.pack(fill="x", padx=24, pady=(0, 25))

        action_frame = ctk.CTkFrame(quick, fg_color="transparent")
        action_frame.pack(fill="x", padx=14, pady=(0, 14))

        actions = [
            ("＋  Add Passenger", self.open_add_passenger, BLUE),
            ("✈  Add Flight", self.open_add_flight, BLUE),
            ("▣  Create Booking", self.open_add_booking, GREEN),
            ("⌕  Search Passenger", self.search_passenger, PURPLE),
            ("▥  View Reports", self.show_reports, ORANGE),
        ]

        for text, command, color in actions:
            ctk.CTkButton(
                action_frame,
                text=text,
                command=command,
                height=46,
                corner_radius=9,
                fg_color=color,
                hover_color=self.darken(color),
                text_color=WHITE,
                font=ctk.CTkFont(size=13, weight="bold")
            ).pack(side="left", fill="x", expand=True, padx=5)

    def create_stat_card(
        self,
        parent,
        title,
        value,
        icon,
        accent,
        database_available=True
    ):

        card = ctk.CTkFrame(
            parent,
            fg_color=WHITE,
            border_width=1,
            border_color=BORDER,
            corner_radius=12,
            height=125
        )

        card.pack(
            side="left",
            fill="both",
            expand=True,
            padx=6
        )

        card.pack_propagate(False)

        ctk.CTkLabel(
            card,
            text=icon,
            width=52,
            height=52,
            corner_radius=26,
            fg_color=BLUE_LIGHT,
            text_color=accent,
            font=ctk.CTkFont(size=23, weight="bold")
        ).place(x=16, y=20)

        ctk.CTkLabel(
            card,
            text=title,
            text_color=MUTED,
            font=ctk.CTkFont(size=12)
        ).place(x=82, y=22)

        display_value = str(value) if database_available else "—"

        ctk.CTkLabel(
            card,
            text=display_value,
            text_color=TEXT,
            font=ctk.CTkFont(size=28, weight="bold")
        ).place(x=82, y=48)

        if database_available:
            status_text = "●  Live database"
            status_color = GREEN
        else:
            status_text = "●  Database unavailable"
            status_color = RED

        ctk.CTkLabel(
            card,
            text=status_text,
            text_color=status_color,
            font=ctk.CTkFont(size=10, weight="bold")
        ).place(x=82, y=88)

    def create_panel(self, parent, title):

        panel = ctk.CTkFrame(
            parent,
            fg_color=WHITE,
            border_width=1,
            border_color=BORDER,
            corner_radius=12
        )

        ctk.CTkLabel(
            panel,
            text=title,
            text_color=TEXT,
            font=ctk.CTkFont(
                size=16,
                weight="bold"
            )
        ).pack(
            anchor="w",
            padx=16,
            pady=(14, 8)
        )

        return panel

    # ========================================================
    # AIRLINE CHART
    # ========================================================

    def draw_airline_chart(
        self,
        parent,
        rows
    ):

        canvas = ctk.CTkCanvas(
            parent,
            height=245,
            bg=WHITE,
            highlightthickness=0
        )

        canvas.pack(
            fill="x",
            padx=10,
            pady=(0, 12)
        )

        if rows is None:
            canvas.create_text(
                300,
                115,
                text="Database unavailable",
                fill=RED,
                font=("Arial", 12, "bold")
            )
            return

        if not rows:
            canvas.create_text(
                300,
                115,
                text="No airline data available",
                fill=MUTED
            )
            return

        rows = rows[:6]

        total = sum(
            int(row["total"])
            for row in rows
        ) or 1

        cx = 165
        cy = 112
        radius = 78
        start = -90

        colors = [
            BLUE,
            ORANGE,
            GREEN,
            PURPLE,
            RED,
            "#00A6A6"
        ]

        for i, row in enumerate(rows):

            value = int(row["total"])

            extent = (
                360 * value / total
            )

            canvas.create_arc(
                cx - radius,
                cy - radius,
                cx + radius,
                cy + radius,
                start=start,
                extent=extent,
                fill=colors[i % len(colors)],
                outline=WHITE,
                width=2
            )

            start += extent

        canvas.create_oval(
            cx - 43,
            cy - 43,
            cx + 43,
            cy + 43,
            fill=WHITE,
            outline=WHITE
        )

        canvas.create_text(
            cx,
            cy - 8,
            text=str(total),
            fill=TEXT,
            font=("Arial", 20, "bold")
        )

        canvas.create_text(
            cx,
            cy + 17,
            text="Flights",
            fill=MUTED,
            font=("Arial", 10)
        )

        for i, row in enumerate(rows):

            y = 38 + i * 28

            color = colors[i % len(colors)]

            name = str(
                row["airline_name"]
            )

            value = int(row["total"])

            percent = round(
                value * 100 / total
            )

            canvas.create_oval(
                310,
                y - 5,
                320,
                y + 5,
                fill=color,
                outline=color
            )

            canvas.create_text(
                330,
                y,
                text=name[:20],
                anchor="w",
                fill=TEXT,
                font=("Arial", 10)
            )

            canvas.create_text(
                535,
                y,
                text=f"{value}  ({percent}%)",
                anchor="e",
                fill=MUTED,
                font=("Arial", 9)
            )

    # ========================================================
    # BOOKING CLASS CHART
    # ========================================================

    def draw_class_chart(
        self,
        parent,
        rows
    ):

        canvas = ctk.CTkCanvas(
            parent,
            height=245,
            bg=WHITE,
            highlightthickness=0
        )

        canvas.pack(
            fill="x",
            padx=10,
            pady=(0, 12)
        )

        if rows is None:
            canvas.create_text(
                300,
                115,
                text="Database unavailable",
                fill=RED,
                font=("Arial", 12, "bold")
            )
            return

        if not rows:
            canvas.create_text(
                300,
                115,
                text="No booking data available",
                fill=MUTED
            )
            return

        rows = rows[:5]

        max_value = max(
            int(row["total"])
            for row in rows
        ) or 1

        chart_left = 55
        chart_right = 535
        chart_top = 25
        chart_bottom = 185

        for i in range(5):

            y = (
                chart_bottom
                -
                (
                    i
                    *
                    (
                        chart_bottom
                        -
                        chart_top
                    )
                    /
                    4
                )
            )

            canvas.create_line(
                chart_left,
                y,
                chart_right,
                y,
                fill="#E8EEF5"
            )

        bar_width = min(
            65,
            420 / max(len(rows), 1)
        )

        gap = 35

        colors = [
            BLUE,
            ORANGE,
            GREEN,
            PURPLE,
            RED
        ]

        for i, row in enumerate(rows):

            value = int(row["total"])

            x = (
                chart_left
                +
                40
                +
                i * (bar_width + gap)
            )

            bar_height = (
                130
                *
                value
                /
                max_value
            )

            y1 = chart_bottom - bar_height

            canvas.create_rectangle(
                x,
                y1,
                x + bar_width,
                chart_bottom,
                fill=colors[i % len(colors)],
                outline=""
            )

            canvas.create_text(
                x + bar_width / 2,
                y1 - 12,
                text=str(value),
                fill=TEXT,
                font=("Arial", 10, "bold")
            )

            label = str(row["class"])

            if len(label) > 14:
                label = label[:12] + "…"

            canvas.create_text(
                x + bar_width / 2,
                chart_bottom + 18,
                text=label,
                fill=MUTED,
                font=("Arial", 9)
            )

        canvas.create_text(
            20,
            15,
            text="Bookings",
            fill=MUTED,
            font=("Arial", 9),
            anchor="w"
        )

    # ========================================================
    # UPCOMING FLIGHTS
    # ========================================================

    def build_upcoming_flights(
        self,
        parent,
        rows
    ):

        if rows is None:
            ctk.CTkLabel(
                parent,
                text="Database unavailable",
                text_color=RED,
                font=ctk.CTkFont(size=13, weight="bold")
            ).pack(expand=True, pady=60)
            return

        if not rows:
            ctk.CTkLabel(
                parent,
                text="No upcoming flights scheduled.",
                text_color=MUTED,
                font=ctk.CTkFont(size=12)
            ).pack(expand=True, pady=60)
            return

        table_frame = ctk.CTkFrame(
            parent,
            fg_color="transparent"
        )

        table_frame.pack(
            fill="both",
            expand=True,
            padx=12,
            pady=(0, 14)
        )

        columns = (
            "flight",
            "airline",
            "departure",
            "status"
        )

        tree = ttk.Treeview(
            table_frame,
            columns=columns,
            show="headings",
            height=5
        )

        tree.heading(
            "flight",
            text="Flight No."
        )

        tree.heading(
            "airline",
            text="Airline"
        )

        tree.heading(
            "departure",
            text="Departure"
        )

        tree.heading(
            "status",
            text="Status"
        )

        tree.column(
            "flight",
            width=90,
            anchor="center"
        )

        tree.column(
            "airline",
            width=180
        )

        tree.column(
            "departure",
            width=155
        )

        tree.column(
            "status",
            width=100,
            anchor="center"
        )

        style = ttk.Style()

        style.configure(
            "Treeview",
            rowheight=34,
            font=("Arial", 10),
            background=WHITE,
            fieldbackground=WHITE,
            foreground=TEXT
        )

        style.configure(
            "Treeview.Heading",
            font=("Arial", 10, "bold"),
            background="#EEF4FA",
            foreground=TEXT
        )

        scrollbar = ttk.Scrollbar(
            table_frame,
            orient="vertical",
            command=tree.yview
        )

        tree.configure(
            yscrollcommand=scrollbar.set
        )

        tree.pack(
            side="left",
            fill="both",
            expand=True
        )

        scrollbar.pack(
            side="right",
            fill="y"
        )

        for row in rows:

            departure = row.get(
                "departure_time"
            )

            if hasattr(
                departure,
                "strftime"
            ):

                departure = departure.strftime(
                    "%Y-%m-%d %H:%M"
                )

            else:

                departure = str(
                    departure
                )

            tree.insert(
                "",
                "end",
                values=(
                    row.get(
                        "flight_number",
                        ""
                    ),
                    row.get(
                        "airline_name",
                        ""
                    ),
                    departure,
                    row.get(
                        "status",
                        ""
                    )
                )
            )

    # ========================================================
    # RECENT ACTIVITIES
    # ========================================================

    def build_recent_activities(
        self,
        parent,
        data
    ):

        if any(value is None for value in data.values()):
            ctk.CTkLabel(
                parent,
                text="Database unavailable",
                text_color=RED,
                font=ctk.CTkFont(size=13, weight="bold")
            ).pack(expand=True, pady=60)
            return

        activity_frame = ctk.CTkFrame(
            parent,
            fg_color="transparent"
        )

        activity_frame.pack(
            fill="both",
            expand=True,
            padx=18,
            pady=(0, 10)
        )

        activities = [
            (
                "●",
                "Passenger records available",
                f"{data['passengers']} passengers",
                BLUE
            ),
            (
                "✈",
                "Flight records available",
                f"{data['flights']} flights",
                PURPLE
            ),
            (
                "▣",
                "Booking records available",
                f"{data['bookings']} bookings",
                GREEN
            ),
            (
                "▰",
                "Baggage records available",
                f"{data['baggage']} baggage records",
                ORANGE
            ),
        ]

        for icon, title, detail, color in activities:

            row = ctk.CTkFrame(
                activity_frame,
                fg_color="transparent",
                height=52
            )

            row.pack(
                fill="x",
                pady=2
            )

            row.pack_propagate(False)

            ctk.CTkLabel(
                row,
                text=icon,
                width=38,
                height=38,
                corner_radius=19,
                fg_color=BLUE_LIGHT,
                text_color=color,
                font=ctk.CTkFont(
                    size=16,
                    weight="bold"
                )
            ).pack(
                side="left",
                padx=(0, 10),
                pady=6
            )

            text = ctk.CTkFrame(
                row,
                fg_color="transparent"
            )

            text.pack(
                side="left",
                fill="both",
                expand=True
            )

            ctk.CTkLabel(
                text,
                text=title,
                text_color=TEXT,
                font=ctk.CTkFont(
                    size=11,
                    weight="bold"
                ),
                anchor="w"
            ).pack(
                anchor="w",
                pady=(6, 0)
            )

            ctk.CTkLabel(
                text,
                text=detail,
                text_color=MUTED,
                font=ctk.CTkFont(size=10),
                anchor="w"
            ).pack(anchor="w")

    # ========================================================
    # QUICK ACTIONS
    # ========================================================

    def open_add_passenger(self):

        self.show_passengers()

        self.after(
            250,
            self.call_child_method,
            "open_add_passenger"
        )

    def open_add_flight(self):

        self.show_flights()

        self.after(
            250,
            self.call_child_method,
            "open_add_flight"
        )

    def open_add_booking(self):

        self.show_bookings()

        self.after(
            250,
            self.call_child_method,
            "open_add_booking"
        )

    def call_child_method(
        self,
        method_name
    ):

        children = (
            self.content.winfo_children()
        )

        if not children:
            return

        page = children[0]

        method = getattr(
            page,
            method_name,
            None
        )

        if method:

            try:
                method()
            except Exception:
                pass

    def search_passenger(self):

        self.show_passengers()

        self.after(
            250,
            self.focus_passenger_search
        )

    def focus_passenger_search(self):

        children = (
            self.content.winfo_children()
        )

        if not children:
            return

        page = children[0]

        for child in page.winfo_children():

            self.find_entry_and_focus(
                child
            )

    def find_entry_and_focus(
        self,
        widget
    ):

        try:

            if isinstance(
                widget,
                ctk.CTkEntry
            ):

                placeholder = widget.cget(
                    "placeholder_text"
                )

                if (
                    placeholder
                    and
                    "Passenger"
                    in str(placeholder)
                ):

                    widget.focus()

                    return True

        except Exception:
            pass

        for child in widget.winfo_children():

            if self.find_entry_and_focus(
                child
            ):

                return True

        return False

    # ========================================================
    # TOP SEARCH
    # ========================================================

    def global_search_action(
        self,
        event=None
    ):

        text = self.search_var.get().strip()

        if not text:
            return

        self.show_passengers()

        self.after(
            250,
            lambda: self.insert_into_first_search(
                text
            )
        )

    def insert_into_first_search(
        self,
        text
    ):

        entries = []

        def collect(widget):

            try:

                if isinstance(
                    widget,
                    ctk.CTkEntry
                ):

                    entries.append(widget)

            except Exception:
                pass

            for child in widget.winfo_children():
                collect(child)

        collect(self.content)

        if entries:

            entry = entries[0]

            entry.delete(
                0,
                "end"
            )

            entry.insert(
                0,
                text
            )

    # ========================================================
    # NOTIFICATIONS
    # ========================================================

    def show_notifications(self):

        messagebox.showinfo(
            "Notifications",
            "No new system notifications.\n\n"
            "The airport management system is operating normally."
        )

    # ========================================================
    # COLOR UTILITY
    # ========================================================

    @staticmethod
    def darken(hex_color):

        colors = {
            BLUE: "#1255AA",
            GREEN: "#14845A",
            PURPLE: "#6236B4",
            ORANGE: "#D88708",
            RED: "#B9363B",
        }

        return colors.get(
            hex_color,
            hex_color
        )


# ============================================================
# RUN APPLICATION
# ============================================================

if __name__ == "__main__":

    app = AirportManagementApp()
    app.mainloop()
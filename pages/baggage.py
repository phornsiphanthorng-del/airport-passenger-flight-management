import customtkinter as ctk
from tkinter import ttk, messagebox
from database import create_connection


class BaggagePage(ctk.CTkFrame):

    def __init__(self, parent):

        super().__init__(parent)

        # =====================================================
        # Page Title
        # =====================================================

        title = ctk.CTkLabel(
            self,
            text="Baggage Management",
            font=("Arial", 28, "bold")
        )

        title.pack(
            padx=30,
            pady=(30, 5),
            anchor="w"
        )

        subtitle = ctk.CTkLabel(
            self,
            text="View and manage airport baggage information",
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
            text="Search Baggage:",
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
            placeholder_text="Baggage ID, Booking ID or Tag"
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
            command=self.search_baggage
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
            text="+ Add Baggage",
            width=140,
            command=self.open_add_baggage
        )

        add_button.pack(
            side="right",
            padx=15
        )

        # =====================================================
        # Baggage Table
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
            "Booking ID",
            "Baggage Tag",
            "Weight",
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
                width=150,
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
        # Bottom Buttons
        # =====================================================

        button_frame = ctk.CTkFrame(
            self,
            fg_color="transparent"
        )

        button_frame.pack(
            pady=(0, 20)
        )

        edit_button = ctk.CTkButton(
            button_frame,
            text="Edit Selected",
            width=150,
            command=self.edit_selected
        )

        edit_button.pack(
            side="left",
            padx=10
        )

        delete_button = ctk.CTkButton(
            button_frame,
            text="Delete Selected",
            width=150,
            command=self.delete_selected
        )

        delete_button.pack(
            side="left",
            padx=10
        )

        # =====================================================
        # Load Baggage
        # =====================================================

        self.load_baggage()

    # =====================================================
    # Load Baggage
    # =====================================================

    def load_baggage(self, search_text=""):

        for item in self.table.get_children():
            self.table.delete(item)

        connection = create_connection()

        if connection is None:

            messagebox.showerror(
                "Database Error",
                "Could not connect to the database."
            )

            return

        try:

            cursor = connection.cursor()

            if search_text:

                query = """
                    SELECT
                        baggage_id,
                        booking_id,
                        baggage_tag,
                        weight,
                        status
                    FROM Baggage
                    WHERE
                        CAST(baggage_id AS CHAR) LIKE %s
                        OR CAST(booking_id AS CHAR) LIKE %s
                        OR baggage_tag LIKE %s
                        OR status LIKE %s
                    ORDER BY baggage_id
                """

                search_value = f"%{search_text}%"

                cursor.execute(
                    query,
                    (
                        search_value,
                        search_value,
                        search_value,
                        search_value
                    )
                )

            else:

                query = """
                    SELECT
                        baggage_id,
                        booking_id,
                        baggage_tag,
                        weight,
                        status
                    FROM Baggage
                    ORDER BY baggage_id
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

            print(f"Error loading baggage: {e}")

            messagebox.showerror(
                "Error",
                f"Could not load baggage.\n\n{e}"
            )

            if connection.is_connected():
                connection.close()

    # =====================================================
    # Search Baggage
    # =====================================================

    def search_baggage(self):

        search_text = self.search_entry.get().strip()

        self.load_baggage(search_text)

    # =====================================================
    # Clear Search
    # =====================================================

    def clear_search(self):

        self.search_entry.delete(
            0,
            "end"
        )

        self.load_baggage()

    # =====================================================
    # Add Baggage Window
    # =====================================================

    def open_add_baggage(self):

        add_window = ctk.CTkToplevel(self)

        add_window.title("Add Baggage")
        add_window.geometry("500x650")
        add_window.resizable(False, False)

        # =================================================
        # FIX WINDOW POSITION / FOCUS
        # =================================================

        add_window.transient(
            self.winfo_toplevel()
        )

        add_window.lift()

        add_window.focus_force()

        add_window.grab_set()

        add_window.after(
            100,
            lambda: (
                add_window.lift(),
                add_window.focus_force()
            )
        )

        # =================================================
        # Title
        # =================================================

        title = ctk.CTkLabel(
            add_window,
            text="Add New Baggage",
            font=("Arial", 24, "bold")
        )

        title.pack(
            pady=(25, 20)
        )

        # =================================================
        # Form
        # =================================================

        form_frame = ctk.CTkFrame(
            add_window
        )

        form_frame.pack(
            padx=30,
            pady=10,
            fill="both",
            expand=True
        )

        # Booking ID

        ctk.CTkLabel(
            form_frame,
            text="Booking ID"
        ).pack(
            anchor="w",
            padx=20,
            pady=(20, 5)
        )

        booking_id_entry = ctk.CTkEntry(
            form_frame,
            width=400,
            placeholder_text="Enter booking ID"
        )

        booking_id_entry.pack(
            padx=20
        )

        # Baggage Tag

        ctk.CTkLabel(
            form_frame,
            text="Baggage Tag"
        ).pack(
            anchor="w",
            padx=20,
            pady=(20, 5)
        )

        baggage_tag_entry = ctk.CTkEntry(
            form_frame,
            width=400,
            placeholder_text="Enter unique baggage tag"
        )

        baggage_tag_entry.pack(
            padx=20
        )

        # Weight

        ctk.CTkLabel(
            form_frame,
            text="Weight (kg)"
        ).pack(
            anchor="w",
            padx=20,
            pady=(20, 5)
        )

        weight_entry = ctk.CTkEntry(
            form_frame,
            width=400,
            placeholder_text="Example: 23.50"
        )

        weight_entry.pack(
            padx=20
        )

        # Status

        ctk.CTkLabel(
            form_frame,
            text="Status"
        ).pack(
            anchor="w",
            padx=20,
            pady=(20, 5)
        )

        status_entry = ctk.CTkEntry(
            form_frame,
            width=400,
            placeholder_text="Example: Checked In"
        )

        status_entry.pack(
            padx=20
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
            text="Save Baggage",
            width=150,
            command=lambda: self.save_baggage(
                booking_id_entry.get().strip(),
                baggage_tag_entry.get().strip(),
                weight_entry.get().strip(),
                status_entry.get().strip(),
                add_window
            )
        )

        save_button.pack(
            side="left",
            padx=10
        )

        # Put cursor in Booking ID
        booking_id_entry.focus_set()

    # =====================================================
    # Save Baggage
    # =====================================================

    def save_baggage(
        self,
        booking_id,
        baggage_tag,
        weight,
        status,
        add_window
    ):

        if not booking_id:

            messagebox.showwarning(
                "Missing Information",
                "Please enter a Booking ID.",
                parent=add_window
            )

            return

        if not baggage_tag:

            messagebox.showwarning(
                "Missing Information",
                "Please enter a Baggage Tag.",
                parent=add_window
            )

            return

        if not weight:

            messagebox.showwarning(
                "Missing Information",
                "Please enter the baggage weight.",
                parent=add_window
            )

            return

        if not status:

            messagebox.showwarning(
                "Missing Information",
                "Please enter the baggage status.",
                parent=add_window
            )

            return

        # Validate Booking ID

        try:

            booking_id = int(booking_id)

        except ValueError:

            messagebox.showwarning(
                "Invalid Booking ID",
                "Booking ID must be a number.",
                parent=add_window
            )

            return

        # Validate Weight

        try:

            weight = float(weight)

        except ValueError:

            messagebox.showwarning(
                "Invalid Weight",
                "Weight must be a number.\nExample: 23.50",
                parent=add_window
            )

            return

        connection = create_connection()

        if connection is None:

            messagebox.showerror(
                "Database Error",
                "Could not connect to the database.",
                parent=add_window
            )

            return

        try:

            cursor = connection.cursor()

            query = """
                INSERT INTO Baggage
                (
                    booking_id,
                    baggage_tag,
                    weight,
                    status
                )
                VALUES
                (
                    %s,
                    %s,
                    %s,
                    %s
                )
            """

            values = (
                booking_id,
                baggage_tag,
                weight,
                status
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
                "Baggage added successfully!",
                parent=add_window
            )

            add_window.grab_release()

            add_window.destroy()

            self.load_baggage()

        except Exception as e:

            print(f"Error adding baggage: {e}")

            messagebox.showerror(
                "Error",
                f"Could not add baggage.\n\n{e}",
                parent=add_window
            )

            if connection.is_connected():
                connection.close()

    # =====================================================
    # Edit Selected Baggage
    # =====================================================

    def edit_selected(self):

        selected = self.table.selection()

        if not selected:

            messagebox.showwarning(
                "No Selection",
                "Please select a baggage record to edit."
            )

            return

        item = self.table.item(
            selected[0]
        )

        baggage = item["values"]

        baggage_id = baggage[0]

        edit_window = ctk.CTkToplevel(self)

        edit_window.title("Edit Baggage")
        edit_window.geometry("500x650")
        edit_window.resizable(False, False)

        # =================================================
        # FIX WINDOW POSITION / FOCUS
        # =================================================

        edit_window.transient(
            self.winfo_toplevel()
        )

        edit_window.lift()

        edit_window.focus_force()

        edit_window.grab_set()

        edit_window.after(
            100,
            lambda: (
                edit_window.lift(),
                edit_window.focus_force()
            )
        )

        # =================================================
        # Title
        # =================================================

        title = ctk.CTkLabel(
            edit_window,
            text="Edit Baggage",
            font=("Arial", 24, "bold")
        )

        title.pack(
            pady=(25, 20)
        )

        # =================================================
        # Form
        # =================================================

        form_frame = ctk.CTkFrame(
            edit_window
        )

        form_frame.pack(
            padx=30,
            pady=10,
            fill="both",
            expand=True
        )

        # Booking ID

        ctk.CTkLabel(
            form_frame,
            text="Booking ID"
        ).pack(
            anchor="w",
            padx=20,
            pady=(20, 5)
        )

        booking_id_entry = ctk.CTkEntry(
            form_frame,
            width=400
        )

        booking_id_entry.pack(
            padx=20
        )

        booking_id_entry.insert(
            0,
            baggage[1]
        )

        # Baggage Tag

        ctk.CTkLabel(
            form_frame,
            text="Baggage Tag"
        ).pack(
            anchor="w",
            padx=20,
            pady=(20, 5)
        )

        baggage_tag_entry = ctk.CTkEntry(
            form_frame,
            width=400
        )

        baggage_tag_entry.pack(
            padx=20
        )

        baggage_tag_entry.insert(
            0,
            baggage[2]
        )

        # Weight

        ctk.CTkLabel(
            form_frame,
            text="Weight (kg)"
        ).pack(
            anchor="w",
            padx=20,
            pady=(20, 5)
        )

        weight_entry = ctk.CTkEntry(
            form_frame,
            width=400
        )

        weight_entry.pack(
            padx=20
        )

        weight_entry.insert(
            0,
            baggage[3]
        )

        # Status

        ctk.CTkLabel(
            form_frame,
            text="Status"
        ).pack(
            anchor="w",
            padx=20,
            pady=(20, 5)
        )

        status_entry = ctk.CTkEntry(
            form_frame,
            width=400
        )

        status_entry.pack(
            padx=20
        )

        status_entry.insert(
            0,
            baggage[4]
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
            command=lambda: self.close_edit_window(edit_window)
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
                baggage_id,
                booking_id_entry.get().strip(),
                baggage_tag_entry.get().strip(),
                weight_entry.get().strip(),
                status_entry.get().strip(),
                edit_window
            )
        )

        save_button.pack(
            side="left",
            padx=10
        )

        # Put cursor in Booking ID
        booking_id_entry.focus_set()

    # =====================================================
    # Close Edit Window
    # =====================================================

    def close_edit_window(self, edit_window):

        try:
            edit_window.grab_release()
        except:
            pass

        edit_window.destroy()

    # =====================================================
    # Save Changes
    # =====================================================

    def save_changes(
        self,
        baggage_id,
        booking_id,
        baggage_tag,
        weight,
        status,
        edit_window
    ):

        if not booking_id:

            messagebox.showwarning(
                "Missing Information",
                "Please enter a Booking ID.",
                parent=edit_window
            )

            return

        if not baggage_tag:

            messagebox.showwarning(
                "Missing Information",
                "Please enter a Baggage Tag.",
                parent=edit_window
            )

            return

        if not weight:

            messagebox.showwarning(
                "Missing Information",
                "Please enter the baggage weight.",
                parent=edit_window
            )

            return

        if not status:

            messagebox.showwarning(
                "Missing Information",
                "Please enter the baggage status.",
                parent=edit_window
            )

            return

        # Validate Booking ID

        try:

            booking_id = int(booking_id)

        except ValueError:

            messagebox.showwarning(
                "Invalid Booking ID",
                "Booking ID must be a number.",
                parent=edit_window
            )

            return

        # Validate Weight

        try:

            weight = float(weight)

        except ValueError:

            messagebox.showwarning(
                "Invalid Weight",
                "Weight must be a number.",
                parent=edit_window
            )

            return

        connection = create_connection()

        if connection is None:

            messagebox.showerror(
                "Database Error",
                "Could not connect to the database.",
                parent=edit_window
            )

            return

        try:

            cursor = connection.cursor()

            query = """
                UPDATE Baggage
                SET
                    booking_id = %s,
                    baggage_tag = %s,
                    weight = %s,
                    status = %s
                WHERE baggage_id = %s
            """

            values = (
                booking_id,
                baggage_tag,
                weight,
                status,
                baggage_id
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
                "Baggage updated successfully!",
                parent=edit_window
            )

            edit_window.grab_release()

            edit_window.destroy()

            self.load_baggage()

        except Exception as e:

            print(f"Error updating baggage: {e}")

            messagebox.showerror(
                "Error",
                f"Could not update baggage.\n\n{e}",
                parent=edit_window
            )

            if connection.is_connected():
                connection.close()

    # =====================================================
    # Delete Selected Baggage
    # =====================================================

    def delete_selected(self):

        selected = self.table.selection()

        if not selected:

            messagebox.showwarning(
                "No Selection",
                "Please select a baggage record to delete."
            )

            return

        item = self.table.item(
            selected[0]
        )

        baggage = item["values"]

        baggage_id = baggage[0]

        baggage_tag = baggage[2]

        confirm = messagebox.askyesno(
            "Confirm Delete",
            f"Are you sure you want to delete baggage {baggage_tag}?"
        )

        if not confirm:
            return

        connection = create_connection()

        if connection is None:
            return

        try:

            cursor = connection.cursor()

            query = """
                DELETE FROM Baggage
                WHERE baggage_id = %s
            """

            cursor.execute(
                query,
                (baggage_id,)
            )

            connection.commit()

            cursor.close()
            connection.close()

            messagebox.showinfo(
                "Success",
                "Baggage deleted successfully!"
            )

            self.load_baggage()

        except Exception as e:

            print(f"Error deleting baggage: {e}")

            messagebox.showerror(
                "Error",
                f"Could not delete baggage.\n\n{e}"
            )

            if connection.is_connected():
                connection.close()


                
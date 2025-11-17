import tkinter as tk
from tkinter import ttk, messagebox, filedialog
import re 

# Αρχικοποίηση λιστών για αποθήκευση της δομής του μενού
main_menus = []
sub_menus = []
commands = []
# Θυμόμαστε τον τελευταίο ID για να συνεχίσουμε την αρίθμηση
id_counter = {'m': 0, 'sm': 0, 'c': 0} 

class DCSMenuCreatorApp:
    def __init__(self, master):
        
        # --- 1. Δήλωση Μεταφράσεων και Μεταβλητών Γλώσσας ---
        self.selected_language = tk.StringVar(value='GR')
        self.translations = self.define_translations()
        
        # --- 2. Εκκίνηση GUI ---
        self.master = master
        # ΕΝΗΜΕΡΩΣΗ ΤΙΤΛΟΥ ΠΑΡΑΘΥΡΟΥ
        master.title(self.get_text('app_title')) 
        master.state('zoomed') 

        # 1. Θέμα & Χρώματα (Dark Base)
        self.THEME_COLORS = {
            'm_group_bg': '#FFB366',      # Menu Group: Light Orange
            'sm_group_bg': '#FFFF99',     # Submenu Group: Light Yellow
            'c_group_bg': '#FFFFFF',      # Command Group: White
            
            # Βασικά Χρώματα (Dark Theme)
            'DARK_BG': '#1E1E1E',         # Κύριο Φόντο (Σχεδόν Μαύρο)
            'DARK_FG': '#F0F0F0',         # Κύριο Χρώμα Γραμμάτων (White/Light Gray)
            'WIDGET_BG': '#3C3C3C',       # Φόντο για Entry/Listbox/Text
            'ACCENT_COLOR': '#5A5A5A',    # Button active color
            'LIGHT_FG_CONTRAST': '#1E1E1E', # Σκούρο κείμενο για ανοιχτά φόντα
            
            # Χρώματα για το κείμενο του Lua Preview
            'LUA_FG_BLUE': '#1E90FF',       # Dodger Blue
            'LUA_FG_RED': '#FF6666',        # Light Red
            'LUA_FG_NEUTRAL': '#F0F0F0'     # Default Light Gray
        }
        self.set_dark_theme(master)

        # 3. Επιλογή Συμμαχιών
        self.selected_coalition = tk.StringVar(value='BLUE')
        
        # 4. Δημιουργία της μπάρας στο κάτω μέρος (Footer)
        self.create_footer_bar(master)

        # Χρήση PanedWindow
        self.main_pane = ttk.PanedWindow(master, orient=tk.HORIZONTAL, style='Dark.TPanedwindow')
        self.main_pane.pack(fill=tk.BOTH, expand=True, padx=10, pady=(10, 0)) 

        # 5. Δημιουργία των πλαισίων
        self.create_input_panel()
        self.create_preview_panel()

        self.main_pane.add(self.input_frame, weight=1) 
        self.main_pane.add(self.preview_frame, weight=1) 

        # Αρχική ενημέρωση
        self.update_parent_dropdowns()
        self.update_previews()

    # --- Language and Translation Methods ---

    def define_translations(self):
        """Ορίζει το λεξικό μεταφράσεων."""
        return {
            # ΑΛΛΑΓΗ ΤΙΤΛΟΥ
            'app_title': {'GR': "RADIO MENU CREATOR 2 - DCS", 'ENG': "RADIO MENU CREATOR 2 - DCS"}, 
            'intermediate_header': {'GR': "RADIO MENU CREATOR 2 - DCS", 'ENG': "RADIO MENU CREATOR 2 - DCS"},
            'footer_text': {'GR': "Lock-On Greece     ®Copyright© 2024   by   =GR= Astr0", 'ENG': "Lock-On Greece     ®Copyright© 2024   by   =GR= Astr0"},
            'coalition_title': {'GR': "1. ΕΠΙΛΟΓΗ ΣΥΜΜΑΧΙΑΣ", 'ENG': "1. COALITION SELECTION"},
            'language_label': {'GR': "ΓΛΩΣΣΑ:", 'ENG': "LANGUAGE:"},
            
            'main_menu_title': {'GR': "2. ΚΥΡΙΟ ΜΕΝΟΥ (M)", 'ENG': "2. MAIN MENU (M)"},
            'menu_name_label': {'GR': "ΟΝΟΜΑ ΜΕΝΟΥ:", 'ENG': "MENU NAME:"},
            
            'submenu_title': {'GR': "3. ΥΠΟΜΕΝΟΥ (SM)", 'ENG': "3. SUBMENU (SM)"},
            'parent_menu_label': {'GR': "ΓΟΝΙΚΟ ΜΕΝΟΥ:", 'ENG': "PARENT MENU:"},
            'submenu_name_label': {'GR': "ΟΝΟΜΑ ΥΠΟΜΕΝΟΥ:", 'ENG': "SUBMENU NAME:"},
            
            'command_title': {'GR': "4. ΕΝΤΟΛΕΣ (C)", 'ENG': "4. COMMANDS (C)"},
            'parent_submenu_label': {'GR': "ΓΟΝ. ΥΠΟΜΕΝΟΥ:", 'ENG': "PARENT SUBMENU:"},
            'command_name_label': {'GR': "ΟΝΟΜΑ ΕΝΤΟΛΗΣ:", 'ENG': "COMMAND NAME:"},
            'flag_name_label': {'GR': "ΟΝΟΜΑ FLAG:", 'ENG': "FLAG NAME:"},
            'flag_value_label': {'GR': "ΤΙΜΗ FLAG:", 'ENG': "FLAG VALUE:"},
            
            'add_button': {'GR': "➕ ΠΡΟΣΘΗΚΗ", 'ENG': "➕ ADD"},
            'delete_button': {'GR': "🗑️ ΔΙΑΓΡΑΦΗ ΕΠΙΛΕΓΜΕΝΟΥ", 'ENG': "🗑️ DELETE SELECTED"},
            
            'load_section_title': {'GR': "5. ΦΟΡΤΩΣΗ ΥΠΑΡΧΟΝΤΟΣ LUA ΚΩΔΙΚΑ", 'ENG': "5. LOAD EXISTING LUA CODE"},
            'paste_lua_label': {'GR': "ΕΠΙΚΟΛΛΗΣΤΕ ΤΟΝ ΚΩΔΙΚΑ LUA ΕΔΩ:", 'ENG': "PASTE LUA CODE HERE:"},
            'clear_all_button': {'GR': "🧹 ΚΑΘΑΡΙΣΜΟΣ ΟΛΩΝ", 'ENG': "🧹 CLEAR ALL"},
            'load_file_button': {'GR': "📄 ΦΟΡΤΩΣΗ ΑΠΟ ΑΡΧΕΙΟ", 'ENG': "📄 LOAD FROM FILE"},
            'load_text_button': {'GR': "📋 ΦΟΡΤΩΣΗ ΑΠΟ ΚΕΙΜΕΝΟ", 'ENG': "📋 LOAD FROM TEXT"},
            
            'tree_view_title': {'GR': "🌳 ΔΟΜΗ RADIO MENU", 'ENG': "🌳 RADIO MENU STRUCTURE"},
            'lua_preview_title': {'GR': "📜 ΠΡΟΕΠΙΣΚΟΠΗΣΗ ΚΩΔΙΚΑ LUA:", 'ENG': "📜 LUA CODE PREVIEW:"},
            'export_button': {'GR': "📄 ΑΠΟΘΗΚΕΥΣΗ ΑΡΧΕΙΟΥ LUA", 'ENG': "📄 SAVE LUA FILE"}, 
            
            # Context Menu
            'cut_menu': {'GR': "ΑΠΟΚΟΠΗ", 'ENG': "CUT"},
            'copy_menu': {'GR': "ΑΝΤΙΓΡΑΦΗ", 'ENG': "COPY"},
            'paste_menu': {'GR': "ΕΠΙΚΟΛΛΗΣΗ", 'ENG': "PASTE"},
            'select_all_menu': {'GR': "ΕΠΙΛΟΓΗ ΟΛΩΝ", 'ENG': "SELECT ALL"},
            
            # Listbox components 
            'listbox_parent': {'GR': "ΓΟΝΙΚΟ", 'ENG': "PARENT"},
            'listbox_flag': {'GR': "FLAG", 'ENG': "FLAG"},
            'listbox_menu': {'GR': "ΜΕΝΟΥ", 'ENG': "MENU"},
            'listbox_submenu': {'GR': "ΥΠΟΜΕΝΟΥ", 'ENG': "SUBMENU"},
            'listbox_command': {'GR': "ΕΝΤΟΛΗ", 'ENG': "COMMAND"},
            'listbox_unknown': {'GR': "ΑΓΝΩΣΤΟ", 'ENG': "UNKNOWN"},
            
            # Message Boxes
            'error_title': {'GR': "ΣΦΑΛΜΑ", 'ENG': "ERROR"},
            'warning_title': {'GR': "ΠΡΟΣΟΧΗ", 'ENG': "ATTENTION"},
            'success_title': {'GR': "ΕΠΙΤΥΧΙΑ", 'ENG': "SUCCESS"},
            'delete_confirm_title': {'GR': "ΕΠΙΒΕΒΑΙΩΣΗ ΔΙΑΓΡΑΦΗΣ", 'ENG': "DELETION CONFIRMATION"},
            'clear_confirm_title': {'GR': "ΕΠΙΒΕΒΑΙΩΣΗ ΚΑΘΑΡΙΣΜΟΥ", 'ENG': "CLEARING CONFIRMATION"},
            'load_success_title': {'GR': "ΕΠΙΤΥΧΙΑ ΦΟΡΤΩΣΗΣ", 'ENG': "LOAD SUCCESS"},
            'save_error_title': {'GR': "ΣΦΑΛΜΑ ΑΠΟΘΗΚΕΥΣΗΣ", 'ENG': "SAVE ERROR"},
            'load_error_file_title': {'GR': "ΣΦΑΛΜΑ ΦΟΡΤΩΣΗΣ ΑΡΧΕΙΟΥ", 'ENG': "FILE LOAD ERROR"},
            'load_error_parse_title': {'GR': "ΣΦΑΛΜΑ ΑΝΑΛΥΣΗΣ ΚΩΔΙΚΑ", 'ENG': "CODE PARSING ERROR"},
            
            'err_enter_menu_name': {'GR': "ΠΑΡΑΚΑΛΩ ΕΙΣΑΓΕΤΕ ΤΟ ΟΝΟΜΑ ΜΕΝΟΥ.", 'ENG': "PLEASE ENTER THE MENU NAME."},
            'err_fill_all_fields': {'GR': "ΠΑΡΑΚΑΛΩ ΣΥΜΠΛΗΡΩΣΤΕ ΟΛΑ ΤΑ ΠΕΔΙΑ.", 'ENG': "PLEASE FILL IN ALL FIELDS."},
            'err_select_valid_parent': {'GR': "ΕΠΙΛΕΞΤΕ ΕΝΑ ΕΓΚΥΡΟ ΓΟΝΙΚΟ ΜΕΝΟΥ.", 'ENG': "SELECT A VALID PARENT MENU."},
            'err_parent_id_not_exist': {'GR': "ΤΟ ΓΟΝΙΚΟ ΜΕΝΟΥ ID ΔΕΝ ΥΠΑΡΧΕΙ.", 'ENG': "THE PARENT MENU ID DOES NOT EXIST."},
            'err_select_valid_submenu': {'GR': "ΕΠΙΛΕΞΤΕ ΕΝΑ ΕΓΚΥΡΟ ΓΟΝΙΚΟ ΥΠΟΜΕΝΟΥ.", 'ENG': "SELECT A VALID PARENT SUBMENU."},
            'err_submenu_id_not_exist': {'GR': "ΤΟ ΓΟΝΙΚΟ ΥΠΟΜΕΝΟΥ ID ΔΕΝ ΥΠΑΡΧΕΙ.", 'ENG': "THE PARENT SUBMENU ID DOES NOT EXIST."},
            
            'confirm_delete_menu': {'GR': "ΔΙΑΓΡΑΦΗ ΜΕΝΟΥ {name} ΜΑΖΙ ΜΕ ΟΛΑ ΤΑ ΥΠΟΜΕΝΟΥ ΚΑΙ ΤΙΣ ΕΝΤΟΛΕΣ ΤΟΥ;", 'ENG': "DELETE MENU {name} ALONG WITH ALL ITS SUBMENUS AND COMMANDS?"},
            'confirm_delete_submenu': {'GR': "ΔΙΑΓΡΑΦΗ ΥΠΟΜΕΝΟΥ {name} ΜΑΖΙ ΜΕ ΟΛΕΣ ΤΙΣ ΕΝΤΟΛΕΣ ΤΟΥ;", 'ENG': "DELETE SUBMENU {name} ALONG WITH ALL ITS COMMANDS?"},
            'msg_deleted': {'GR': "ΔΙΑΓΡΑΦΤΗΚΕ:", 'ENG': "DELETED:"},
            'warn_select_to_delete': {'GR': "ΠΑΡΑΚΑΛΩ ΕΠΙΛΕΞΤΕ ΜΙΑ ΕΠΙΛΟΓΗ ΠΡΟΣ ΔΙΑΓΡΑΦΗ.", 'ENG': "PLEASE SELECT AN OPTION TO DELETE."},
            'err_deletion_failed': {'GR': "ΠΡΟΕΚΥΨΕ ΣΦΑΛΜΑ ΚΑΤΑ ΤΗ ΔΙΑΓΡΑΦΗ:", 'ENG': "AN ERROR OCCURRED DURING DELETION:"},
            
            'confirm_clear_all': {'GR': "ΕΙΣΤΕ ΣΙΓΟΥΡΟΙ ΟΤΙ ΘΕΛΕΤΕ ΝΑ ΚΑΘΑΡΙΣΕΤΕ ΟΛΑ ΤΑ ΜΕΝΟΥ, ΥΠΟΜΕΝΟΥ ΚΑΙ ΕΝΤΟΛΕΣ;", 'ENG': "ARE YOU SURE YOU WANT TO CLEAR ALL MENUS, SUBMENUS, AND COMMANDS?"},
            'msg_cleared': {'GR': "ΟΛΑ ΤΑ ΔΕΔΟΜΕΝΑ ΔΙΑΓΡΑΦΗΚΑΝ ΕΠΙΤΥΧΩΣ.", 'ENG': "ALL DATA CLEARED SUCCESSFULLY."},
            
            'warn_no_items_to_export': {'GR': "ΔΕΝ ΕΧΟΥΝ ΠΡΟΣΤΕΘΕΙ ΣΤΟΙΧΕΙΑ ΜΕΝΟΥ. ΔΕΝ ΥΠΑΡΧΕΙ ΚΩΔΙΚΑΣ ΓΙΑ ΕΞΑΓΩΓΗ.", 'ENG': "NO MENU ITEMS HAVE BEEN ADDED. NO CODE TO EXPORT."},
            'export_dialog_title': {'GR': "ΑΠΟΘΗΚΕΥΣΗ DCS MISSION COMMAND LUA FILE", 'ENG': "SAVE DCS MISSION COMMAND LUA FILE"},
            'msg_save_success': {'GR': "ΤΟ ΑΡΧΕΙΟ ΜΕΝΟΥ ΑΠΟΘΗΚΕΥΤΗΚΕ ΕΠΙΤΥΧΩΣ ΣΤΟ:\n{filename}", 'ENG': "MENU FILE SAVED SUCCESSFULLY TO:\n{filename}"},
            'err_save_fail': {'GR': "ΑΔΥΝΑΜΙΑ ΑΠΟΘΗΚΕΥΣΗΣ ΤΟΥ ΑΡΧΕΙΟΥ:", 'ENG': "UNABLE TO SAVE FILE:"},
            
            'load_dialog_title': {'GR': "ΕΠΙΛΟΓΗ LUA FILE ΓΙΑ ΦΟΡΤΩΣΗ", 'ENG': "SELECT LUA FILE TO LOAD"},
            'warn_code_area_empty': {'GR': "ΤΟ ΠΕΔΙΟ ΚΩΔΙΚΑ ΕΙΝΑΙ ΚΕΝΟ.", 'ENG': "THE CODE AREA IS EMPTY."},
            'msg_load_success': {'GR': "ΦΟΡΤΩΘΗΚΑΝ: {m_count} ΜΕΝΟΥ (m{m_max}), {sm_count} ΥΠΟΜΕΝΟΥ (sm{sm_max}), {c_count} ΕΝΤΟΛΕΣ (c{c_max}).", 'ENG': "LOADED: {m_count} MENUS (m{m_max}), {sm_count} SUBMENUS (sm{sm_max}), {c_count} COMMANDS (c{c_max})."},
            
            # Lua Code Comments
            'lua_comment_error': {'GR': "-- ΣΦΑΛΜΑ: ΔΕΝ ΕΧΕΙ ΕΠΙΛΕΓΕΙ ΚΑΜΙΑ ΣΥΜΜΑΧΙΑ.\n", 'ENG': "-- ERROR: NO COALITION SELECTED.\n"},
            'lua_comment_menu': {'GR': "--- 2. ΔΗΛΩΣΗ ΚΥΡΙΩΝ ΜΕΝΟΥ ({side}) ---\n", 'ENG': "--- 2. DECLARATION OF MAIN MENUS ({side}) ---\n"},
            'lua_comment_submenu': {'GR': "\n--- 3. ΔΗΛΩΣΗ ΥΠΟΜΕΝΟΥ ({side}) ---\n", 'ENG': "\n--- 3. DECLARATION OF SUBMENUS ({side}) ---\n"},
            'lua_comment_command': {'GR': "\n--- 4. ΔΗΛΩΣΗ ΕΝΤΟΛΩΝ ({side}) ---\n", 'ENG': "\n--- 4. DECLARATION OF COMMANDS ({side}) ---\n"},

            # Treeview/Listbox texts
            'tree_menu_prefix': {'GR': "ΜΕΝΟΥ:", 'ENG': "MENU:"},
            'tree_submenu_prefix': {'GR': "ΥΠΟΜΕΝΟΥ:", 'ENG': "SUBMENU:"},
            'tree_command_prefix': {'GR': "ΕΝΤΟΛΗ:", 'ENG': "COMMAND:"},
            'listbox_parent_prefix': {'GR': "ΓΟΝΙΚΟ:", 'ENG': "PARENT:"},
        }

    def get_text(self, key, **kwargs):
        """Επιστρέφει το μεταφρασμένο κείμενο για ένα δεδομένο κλειδί."""
        text = self.translations.get(key, {}).get(self.selected_language.get(), f"[{key}_MISSING]")
        return text.format(**kwargs).upper() # Εξασφαλίζουμε ότι όλα τα κείμενα UI είναι κεφαλαία

    def update_language_ui(self):
        """Ενημερώνει όλα τα στοιχεία UI με βάση την επιλεγμένη γλώσσα."""
        
        # Ενημέρωση τίτλου παραθύρου
        self.master.title(self.get_text('app_title'))
        
        # Ενημέρωση Input Panel (αναδημιουργούμε τα frames για να ενημερωθούν οι τίτλοι/labels)
        self.refresh_input_panel() 
        
        # Ενημέρωση Preview Panel (Χρησιμοποιούμε πλέον τις μεταβλητές κλάσης)
        self.tree_label.config(text=self.get_text('tree_view_title')) 
        self.lua_label.config(text=self.get_text('lua_preview_title')) 
        # FIX: Το κουμπί ενημερώνεται απευθείας από την μεταβλητή self.export_button
        self.export_button.config(text=self.get_text('export_button')) 
        
        # Ενημέρωση Listboxes/Previews
        self.update_listboxes()
        self.update_parent_dropdowns()
        self.update_previews() 
    
    def refresh_input_panel(self):
        """Καθαρίζει και ξαναδημιουργεί το input panel για να ενημερώσει τα κείμενα."""
        
        # Αφαίρεση του υπάρχοντος input_frame
        self.main_pane.forget(self.input_frame)
        
        # Δημιουργία νέου input panel
        self.create_input_panel()
        
        # Εισαγωγή του νέου input_frame στην αρχική θέση
        self.main_pane.insert(0, self.input_frame, weight=1) 

    # --- Θέμα και Στυλ ---
    def set_dark_theme(self, master):
        style = ttk.Style()
        style.theme_use('clam') 

        DARK_BG = self.THEME_COLORS['DARK_BG']
        DARK_FG = self.THEME_COLORS['DARK_FG']
        WIDGET_BG = self.THEME_COLORS['WIDGET_BG']
        ACCENT_COLOR = self.THEME_COLORS['ACCENT_COLOR']
        
        # Ρύθμιση φόντου κύριου παραθύρου
        master.configure(bg=DARK_BG)
        
        # TTK Στυλ
        style.configure('Dark.TFrame', background=DARK_BG)
        style.configure('Dark.TPanedwindow', background=DARK_BG)
        style.configure('Dark.TLabel', background=DARK_BG, foreground=DARK_FG)
        style.configure('Dark.TCheckbutton', background=DARK_BG, foreground=DARK_FG, indicatorcolor=DARK_FG) 
        
        # TTK Στυλ για Buttons (ΚΕΦΑΛΑΙΑ)
        style.configure('Dark.TButton', 
                        background=WIDGET_BG, 
                        foreground=DARK_FG, 
                        borderwidth=1, 
                        relief="flat", 
                        font=('Arial', 12, 'bold'), 
                        padding=[10, 5]) 
        style.map('Dark.TButton', background=[('active', ACCENT_COLOR)])

        # Στυλ για Clear Button (Ανοιχτό Κόκκινο - Tomato)
        style.configure('LightRed.TButton', 
                        background='#FF6347', 
                        foreground='white', 
                        borderwidth=1, 
                        relief="flat", 
                        font=('Arial', 12, 'bold'), 
                        padding=[10, 5]) 
        style.map('LightRed.TButton', background=[('active', '#FF8C00')]) 
        
        # TTK Στυλ για Combobox (Default - Light Text)
        style.configure('TCombobox', fieldbackground=WIDGET_BG, foreground=DARK_FG, selectbackground=ACCENT_COLOR, selectforeground=DARK_FG)
        
        # ΕΙΔΙΚΗ ΡΥΘΜΙΣΗ: Μαύρο κείμενο στα Comboboxes των γονικών
        style.configure('BlackFg.TCombobox', fieldbackground=WIDGET_BG, foreground='#000000', selectbackground=ACCENT_COLOR, selectforeground=DARK_FG)

        # TTK Στυλ για Radiobuttons με Χρώματα (για τα coalition buttons)
        style.configure('Blue.TRadiobutton', background='#0000FF', foreground='white', indicatorcolor='white', font=('Arial', 9, 'bold'))
        style.map('Blue.TRadiobutton', 
                  background=[('active', '#0000CC')], 
                  foreground=[('active', 'white')])

        style.configure('Red.TRadiobutton', background='#FF0000', foreground='white', indicatorcolor='white', font=('Arial', 9, 'bold'))
        style.map('Red.TRadiobutton', 
                  background=[('active', '#CC0000')], 
                  foreground=[('active', 'white')])

        style.configure('White.TRadiobutton', background='#FFFFFF', foreground='#1E1E1E', indicatorcolor='#1E1E1E', font=('Arial', 9, 'bold'))
        style.map('White.TRadiobutton', 
                  background=[('active', '#E0E0E0')], 
                  foreground=[('active', '#1E1E1E')])

        # TTK Στυλ για Treeview
        style.configure("Dark.Treeview", background=WIDGET_BG, foreground=DARK_FG, fieldbackground=WIDGET_BG, borderwidth=1, relief="flat")
        style.map('Dark.Treeview', background=[('selected', ACCENT_COLOR)])


    # --- Βοηθητικές Συναρτήσεις για GUI ---

    def create_context_menu(self, widget):
        """Δημιουργεί και συνδέει ένα δεξί κλικ μενού (copy/paste/cut) στο widget."""
        menu = tk.Menu(widget, tearoff=0)
        
        menu.add_command(label=self.get_text('cut_menu'), command=lambda: widget.focus_get().event_generate('<<Cut>>'))
        menu.add_command(label=self.get_text('copy_menu'), command=lambda: widget.focus_get().event_generate('<<Copy>>'))
        menu.add_command(label=self.get_text('paste_menu'), command=lambda: widget.focus_get().event_generate('<<Paste>>'))
        menu.add_separator()
        menu.add_command(label=self.get_text('select_all_menu'), command=lambda: self.select_all(widget))
        
        def show_menu(event):
            current_state = widget.cget('state')
            if current_state == 'disabled':
                menu.entryconfig(self.get_text('cut_menu'), state="disabled")
                menu.entryconfig(self.get_text('paste_menu'), state="disabled")
            else:
                menu.entryconfig(self.get_text('cut_menu'), state="normal")
                menu.entryconfig(self.get_text('paste_menu'), state="normal")
                
            menu.post(event.x_root, event.y_root)

        widget.bind("<Button-3>", show_menu)
        
        # Προσθήκη συντομεύσεων πληκτρολογίου
        widget.bind('<Control-c>', lambda event: widget.focus_get().event_generate('<<Copy>>'))
        widget.bind('<Control-v>', lambda event: widget.focus_get().event_generate('<<Paste>>'))
        widget.bind('<Control-x>', lambda event: widget.focus_get().event_generate('<<Cut>>'))
        widget.bind('<Control-a>', lambda event: self.select_all(widget))

    def select_all(self, widget):
        """Επιλέγει όλο το κείμενο μέσα στο widget."""
        if isinstance(widget, tk.Text):
            widget.tag_add("sel", "1.0", "end")
        return 'break' 
        
    def create_footer_bar(self, master):
        """
        Δημιουργεί τη μαύρη μπάρα στο κάτω μέρος του παραθύρου 
        με κίτρινο κείμενο για το copyright.
        """
        footer_frame = tk.Frame(master, bg='#000000') 
        footer_frame.pack(side=tk.BOTTOM, fill=tk.X)
        
        footer_text = self.get_text('footer_text')
        
        tk.Label(footer_frame, text=footer_text, 
                 bg='#000000', 
                 fg='#FFFF00', # Κίτρινο κείμενο
                 font=('Arial', 9, 'bold')).pack(pady=5, padx=10, anchor=tk.CENTER)


    # --- Δομή Input Panel (Αριστερή Στήλη) ---

    def create_input_panel(self):
        self.input_frame = ttk.Frame(self.master, style='Dark.TFrame')
        
        # 1. Επιλογή Συμμαχιών & Γλώσσας
        self.create_coalition_selection(self.input_frame)

        # 2. Κύριο Μενού (m) - Light Orange
        m_top_frame, m_group = self.create_colored_group(self.input_frame, 'main_menu_title', self.THEME_COLORS['m_group_bg'])
        m_top_frame.pack(fill="x", pady=5) 
        self.create_main_menu_section(m_group) 

        # 3. Υπομενού (sm) - Light Yellow
        sm_top_frame, sm_group = self.create_colored_group(self.input_frame, 'submenu_title', self.THEME_COLORS['sm_group_bg'])
        sm_top_frame.pack(fill="x", pady=5) 
        self.create_sub_menu_section(sm_group) 

        # 4. Εντολές (c) - White
        c_top_frame, c_group = self.create_colored_group(self.input_frame, 'command_title', self.THEME_COLORS['c_group_bg'])
        c_top_frame.pack(fill="x", pady=5) 
        self.create_command_section(c_group) 

        # 5. Φόρτωση
        load_group = ttk.LabelFrame(self.input_frame, text="", style='Dark.TFrame', padding="10")
        load_group.pack(fill="x", pady=5)
        self.create_load_section(load_group)

    def create_colored_group(self, parent, title_key, color):
        """
        Δημιουργεί ένα πλαίσιο (top_frame) που περιέχει τον τίτλο και το χρωματιστό πλαίσιο (inner_frame).
        Επιστρέφει και τα δύο.
        """
        
        top_frame = tk.Frame(parent, bg=self.THEME_COLORS['DARK_BG'], padx=0, pady=0)
        
        # Τίτλος (12pt, bold, αριστερά)
        tk.Label(top_frame, text=self.get_text(title_key), font=('Arial', 12, 'bold'), bg=self.THEME_COLORS['DARK_BG'], fg=self.THEME_COLORS['DARK_FG']).pack(pady=(0, 5), padx=0, anchor='w')
        
        inner_frame = tk.Frame(top_frame, bg=color, padx=10, pady=10, borderwidth=1, relief="solid")
        inner_frame.pack(fill="x")
        
        return top_frame, inner_frame 

    def create_coalition_selection(self, parent_frame):
        """
        Δημιουργεί τα Radiobuttons για την επιλογή συμμαχίας (μονοπληθής),
        την επιλογή γλώσσας, και το ενδιάμεσο κείμενο τίτλου.
        """
        
        coalition_group_frame = ttk.Frame(parent_frame, style='Dark.TFrame', padding="10")
        coalition_group_frame.pack(fill="x", pady=(0, 10))

        # --- ΕΝΔΙΑΜΕΣΟ ΚΕΙΜΕΝΟ ΤΙΤΛΟΥ (ΜΕΤΑΚΙΝΗΘΗΚΕ ΠΑΝΩ-ΠΑΝΩ) ---
        intermediate_label = tk.Label(coalition_group_frame, 
                                      text=self.get_text('intermediate_header'), 
                                      font=('Arial', 16, 'bold'), 
                                      bg=self.THEME_COLORS['DARK_BG'], 
                                      fg=self.THEME_COLORS['DARK_FG'])
        intermediate_label.pack(fill="x", pady=(0, 10))
        # ---------------------------------------------------------


        # Header Frame για τον τίτλο (αριστερά) και τη γλώσσα (δεξιά)
        header_frame = ttk.Frame(coalition_group_frame, style='Dark.TFrame')
        header_frame.pack(fill="x", pady=(0, 5))
        header_frame.columnconfigure(0, weight=1) # Δίνει χώρο στον τίτλο
        
        # 1. Τίτλος Συμμαχίας
        tk.Label(header_frame, 
                 text=self.get_text('coalition_title'), 
                 font=('Arial', 12, 'bold'), 
                 bg=self.THEME_COLORS['DARK_BG'], 
                 fg=self.THEME_COLORS['DARK_FG']).grid(row=0, column=0, sticky='w', padx=0)
        
        # Language Selector (Στοίχιση δεξιά, column 1)
        lang_frame = ttk.Frame(header_frame, style='Dark.TFrame')
        lang_frame.grid(row=0, column=1, sticky='e')
        
        tk.Label(lang_frame, 
                 text=self.get_text('language_label'), 
                 font=('Arial', 9, 'bold'), 
                 bg=self.THEME_COLORS['DARK_BG'], 
                 fg=self.THEME_COLORS['DARK_FG']).pack(side=tk.LEFT, padx=(10, 5))
                 
        # ΑΛΛΑΓΗ ΠΙΣΩ ΣΕ ΚΕΙΜΕΝΟ: GR και ENG
        ttk.Radiobutton(lang_frame, text="GR", variable=self.selected_language, value='GR', 
                        command=self.update_language_ui, style='White.TRadiobutton').pack(side=tk.LEFT, padx=2)

        ttk.Radiobutton(lang_frame, text="ENG", variable=self.selected_language, value='ENG', 
                        command=self.update_language_ui, style='White.TRadiobutton').pack(side=tk.LEFT, padx=2)

        # Περιεχόμενο Συμμαχιών (Coalition Radiobuttons)
        frame = ttk.Frame(coalition_group_frame, style='Dark.TFrame')
        frame.pack(fill="x")

        # 1. BLUE Radiobutton in Blue Frame
        blue_frame = tk.Frame(frame, bg='#0000FF', relief="raised", borderwidth=1) 
        blue_frame.pack(side=tk.LEFT, padx=5, pady=5)
        ttk.Radiobutton(blue_frame, text="BLUE", variable=self.selected_coalition, value='BLUE', 
                        command=self.update_previews, style='Blue.TRadiobutton').pack(padx=10, pady=5)
        
        # 2. RED Radiobutton in Red Frame
        red_frame = tk.Frame(frame, bg='#FF0000', relief="raised", borderwidth=1)
        red_frame.pack(side=tk.LEFT, padx=5, pady=5)
        ttk.Radiobutton(red_frame, text="RED", variable=self.selected_coalition, value='RED', 
                        command=self.update_previews, style='Red.TRadiobutton').pack(padx=10, pady=5)

        # 3. NEUTRAL Radiobutton in White Frame
        white_frame = tk.Frame(frame, bg='#FFFFFF', relief="raised", borderwidth=1) 
        white_frame.pack(side=tk.LEFT, padx=5, pady=5)
        ttk.Radiobutton(white_frame, text="NEUTRAL", variable=self.selected_coalition, value='NEUTRAL', 
                        command=self.update_previews, style='White.TRadiobutton').pack(padx=10, pady=5)
        
    # --- Βοηθητική συνάρτηση για τα πεδία εισαγωγής ---
    def setup_input_widget(self, parent_frame, widget_type, row, col, label_key, height=1, listbox_width=40, custom_style=None): 
        """Ενοποίηση δημιουργίας Label και Widget με dark theme styling & contrast adjustment."""
        
        WIDGET_BG = self.THEME_COLORS['WIDGET_BG']
        DARK_FG = self.THEME_COLORS['DARK_FG']
        PARENT_BG = parent_frame['bg'] 

        if PARENT_BG in [self.THEME_COLORS['m_group_bg'], self.THEME_COLORS['sm_group_bg'], self.THEME_COLORS['c_group_bg']]:
            label_fg_color = self.THEME_COLORS['LIGHT_FG_CONTRAST'] 
        else:
            label_fg_color = DARK_FG 

        # Label Text σε ΚΕΦΑΛΑΙΑ
        tk.Label(parent_frame, text=self.get_text(label_key), bg=PARENT_BG, fg=label_fg_color).grid(row=row, column=0, padx=5, pady=5, sticky="w")
        
        if widget_type == 'Entry':
            widget = tk.Entry(parent_frame, width=40, bg=WIDGET_BG, fg=DARK_FG, insertbackground=DARK_FG, relief="flat")
        elif widget_type == 'Combobox':
            style_name = custom_style if custom_style else 'TCombobox'
            widget = ttk.Combobox(parent_frame, state="readonly", width=37, style=style_name)
        elif widget_type == 'Listbox':
            widget = tk.Listbox(parent_frame, height=height, width=listbox_width, bg=WIDGET_BG, fg=DARK_FG, selectbackground=self.THEME_COLORS['ACCENT_COLOR'], relief="flat")
        else:
            return None

        widget.grid(row=row, column=col, padx=5, pady=5, sticky="ew")
        return widget

    def create_main_menu_section(self, parent_frame):
        parent_frame.columnconfigure(1, weight=1)
        
        self.m_name_entry = self.setup_input_widget(parent_frame, 'Entry', 0, 1, "menu_name_label") 
        self.m_name_entry.bind('<Return>', lambda event: self.add_main_menu())

        ttk.Button(parent_frame, text=self.get_text('add_button'), command=self.add_main_menu, style='Dark.TButton').grid(row=1, column=0, columnspan=2, pady=(5, 5), sticky="ew") 

        self.m_listbox = self.setup_input_widget(parent_frame, 'Listbox', 2, 0, "", height=3, listbox_width=40)
        self.m_listbox.grid(row=2, column=0, columnspan=2, sticky="ew", pady=(0, 5))
        
        ttk.Button(parent_frame, text=self.get_text('delete_button'), command=lambda: self.delete_item(self.m_listbox, main_menus, 'm'), style='Dark.TButton').grid(row=3, column=0, columnspan=2, pady=(0, 5), sticky="ew") 

    def create_sub_menu_section(self, parent_frame):
        parent_frame.columnconfigure(1, weight=1)
        
        self.sm_parent_menu_combobox = self.setup_input_widget(parent_frame, 'Combobox', 0, 1, "parent_menu_label", custom_style='BlackFg.TCombobox') 

        self.sm_name_entry = self.setup_input_widget(parent_frame, 'Entry', 1, 1, "submenu_name_label") 
        self.sm_name_entry.bind('<Return>', lambda event: self.add_sub_menu())

        ttk.Button(parent_frame, text=self.get_text('add_button'), command=self.add_sub_menu, style='Dark.TButton').grid(row=2, column=0, columnspan=2, pady=(5, 5), sticky="ew") 

        self.sm_listbox = self.setup_input_widget(parent_frame, 'Listbox', 3, 0, "", height=3, listbox_width=40)
        self.sm_listbox.grid(row=3, column=0, columnspan=2, sticky="ew", pady=(0, 5))

        ttk.Button(parent_frame, text=self.get_text('delete_button'), command=lambda: self.delete_item(self.sm_listbox, sub_menus, 'sm'), style='Dark.TButton').grid(row=4, column=0, columnspan=2, pady=(0, 5), sticky="ew") 

    def create_command_section(self, parent_frame):
        parent_frame.columnconfigure(1, weight=1)
        
        self.c_parent_submenu_combobox = self.setup_input_widget(parent_frame, 'Combobox', 0, 1, "parent_submenu_label", custom_style='BlackFg.TCombobox') 
        
        self.c_name_entry = self.setup_input_widget(parent_frame, 'Entry', 1, 1, "command_name_label") 
        self.c_flag_entry = self.setup_input_widget(parent_frame, 'Entry', 2, 1, "flag_name_label") 
        self.c_value_entry = self.setup_input_widget(parent_frame, 'Entry', 3, 1, "flag_value_label") 
        
        self.c_name_entry.bind('<Return>', lambda event: self.add_command())
        self.c_flag_entry.bind('<Return>', lambda event: self.add_command())
        self.c_value_entry.bind('<Return>', lambda event: self.add_command())

        ttk.Button(parent_frame, text=self.get_text('add_button'), command=self.add_command, style='Dark.TButton').grid(row=4, column=0, columnspan=2, pady=(5, 5), sticky="ew") 

        self.c_listbox = self.setup_input_widget(parent_frame, 'Listbox', 5, 0, "", height=3, listbox_width=40)
        self.c_listbox.grid(row=5, column=0, columnspan=2, sticky="ew", pady=(0, 5))
        
        ttk.Button(parent_frame, text=self.get_text('delete_button'), command=lambda: self.delete_item(self.c_listbox, commands, 'c'), style='Dark.TButton').grid(row=6, column=0, columnspan=2, pady=(0, 5), sticky="ew") 

    def create_load_section(self, parent_frame):
        DARK_BG = self.THEME_COLORS['DARK_BG']
        DARK_FG = self.THEME_COLORS['DARK_FG']
        
        # 5. Επικεφαλίδα για το Load Section (Μέγεθος 12, Bold, Αριστερά)
        tk.Label(parent_frame, 
                 text=self.get_text('load_section_title'), 
                 font=('Arial', 12, 'bold'), 
                 bg=DARK_BG, 
                 fg=DARK_FG).pack(pady=(0, 5), anchor='w') 

        # Label για το Text Area
        tk.Label(parent_frame, text=self.get_text('paste_lua_label'), bg=DARK_BG, fg=DARK_FG).pack(pady=5) 
        
        # Text Widget για Copy/Paste
        self.lua_import_text = tk.Text(parent_frame, height=6, width=40, wrap=tk.WORD, 
                                       bg=self.THEME_COLORS['WIDGET_BG'], fg=DARK_FG, 
                                       insertbackground=DARK_FG, relief="flat")
        self.lua_import_text.pack(expand=True, fill="both")
        
        # Προσθήκη Context Menu (Copy/Paste)
        self.create_context_menu(self.lua_import_text)

        button_frame = ttk.Frame(parent_frame, style='Dark.TFrame')
        button_frame.pack(fill="x", pady=5)
        
        # Κουμπιά ΦΟΡΤΩΣΗΣ/ΚΑΘΑΡΙΣΜΟΥ
        ttk.Button(button_frame, text=self.get_text('clear_all_button'), command=self.clear_all_data, style='LightRed.TButton').pack(side=tk.LEFT, expand=True, fill="x", padx=2) 
        ttk.Button(button_frame, text=self.get_text('load_file_button'), command=self.load_from_file, style='Dark.TButton').pack(side=tk.LEFT, expand=True, fill="x", padx=2) 
        ttk.Button(button_frame, text=self.get_text('load_text_button'), command=self.load_from_text_area, style='Dark.TButton').pack(side=tk.LEFT, expand=True, fill="x", padx=2) 


    # --- Δομή Preview Panel (Δεξιά Στήλη) ---

    def create_preview_panel(self):
        self.preview_frame = ttk.Frame(self.master, style='Dark.TFrame', padding="10")
        
        # 1. Tree View (Δέντρο)
        # FIX: Αποθηκεύουμε ως self.tree_label για να ενημερώνεται στη γλώσσα
        self.tree_label = tk.Label(self.preview_frame, text=self.get_text('tree_view_title'), font=('Arial', 12, 'bold'), bg=self.THEME_COLORS['DARK_BG'], fg=self.THEME_COLORS['DARK_FG'])
        self.tree_label.pack(pady=(0, 5))
        
        self.tree_view = ttk.Treeview(self.preview_frame, height=12, style='Dark.Treeview')
        self.tree_view.heading('#0', text='') 
        self.tree_view.pack(expand=False, fill="x")
        
        # Ρύθμιση Tags
        self.tree_view.tag_configure('m_tag', foreground=self.THEME_COLORS['m_group_bg'])      
        self.tree_view.tag_configure('sm_tag', foreground=self.THEME_COLORS['sm_group_bg'])    
        self.tree_view.tag_configure('c_tag', foreground=self.THEME_COLORS['DARK_FG'])      
        
        # 2. Lua Code Preview
        # FIX: Αποθηκεύουμε ως self.lua_label για να ενημερώνεται στη γλώσσα
        self.lua_label = tk.Label(self.preview_frame, text=self.get_text('lua_preview_title'), font=('Arial', 12, 'bold'), bg=self.THEME_COLORS['DARK_BG'], fg=self.THEME_COLORS['DARK_FG'])
        self.lua_label.pack(pady=(15, 5))
        
        # Text Widget για Προεπισκόπηση Lua
        self.lua_preview_text = tk.Text(self.preview_frame, height=18, width=70, wrap=tk.WORD, 
                                         bg=self.THEME_COLORS['WIDGET_BG'], fg=self.THEME_COLORS['DARK_FG'], 
                                         insertbackground=self.THEME_COLORS['DARK_FG'], relief="flat")
        self.lua_preview_text.pack(expand=True, fill="both")
        
        # Προσθήκη Context Menu (Copy/Paste)
        self.create_context_menu(self.lua_preview_text)
        
        # 3. Export Button 
        # FIX: Αποθηκεύουμε ως self.export_button για να ενημερώνεται στη γλώσσα
        self.export_button = tk.Button(self.preview_frame, text=self.get_text('export_button'), command=self.export_lua_file, 
                  bg='#006400', fg='white', font=('Arial', 12, 'bold'), relief="flat")
        self.export_button.pack(pady=10, fill="x")

    # --- Add/Delete Logic ---
    
    def get_next_id(self, prefix):
        """Επιστρέφει το επόμενο διαθέσιμο ID (m1, sm1, c1, κ.λπ.)"""
        global id_counter
        id_counter[prefix] += 1
        return f"{prefix}{id_counter[prefix]}"
        
    def add_main_menu(self):
        name = self.m_name_entry.get().strip()
        if not name:
            messagebox.showerror(self.get_text('error_title'), self.get_text('err_enter_menu_name'))
            return

        global main_menus
        new_id = self.get_next_id('m')
        main_menus.append({'id': new_id, 'name': name})
        self.m_name_entry.delete(0, tk.END)
        self.update_listboxes()
        self.update_parent_dropdowns()
        self.update_previews()

    def add_sub_menu(self):
        parent_full_str = self.sm_parent_menu_combobox.get()
        name = self.sm_name_entry.get().strip()
        
        if not all([parent_full_str, name]):
            messagebox.showerror(self.get_text('error_title'), self.get_text('err_fill_all_fields'))
            return
            
        try:
            parent_id = parent_full_str.split(' - ')[0].strip()
        except IndexError:
            messagebox.showerror(self.get_text('error_title'), self.get_text('err_select_valid_parent'))
            return
            
        if parent_id not in [m['id'] for m in main_menus]:
            messagebox.showerror(self.get_text('error_title'), self.get_text('err_parent_id_not_exist'))
            return

        global sub_menus
        new_id = self.get_next_id('sm')
        sub_menus.append({'id': new_id, 'parent_id': parent_id, 'name': name})
        self.sm_name_entry.delete(0, tk.END)
        self.update_listboxes()
        self.update_parent_dropdowns()
        self.update_previews()

    def add_command(self):
        parent_full_str = self.c_parent_submenu_combobox.get()
        name = self.c_name_entry.get().strip()
        flag = self.c_flag_entry.get().strip()
        value = self.c_value_entry.get().strip()
        
        if not all([parent_full_str, name, flag, value]):
            messagebox.showerror(self.get_text('error_title'), self.get_text('err_fill_all_fields'))
            return
            
        try:
            parent_id = parent_full_str.split(' - ')[0].strip()
        except IndexError:
            messagebox.showerror(self.get_text('error_title'), self.get_text('err_select_valid_submenu'))
            return

        if parent_id not in [sm['id'] for sm in sub_menus]:
            messagebox.showerror(self.get_text('error_title'), self.get_text('err_submenu_id_not_exist'))
            return

        global commands
        new_id = self.get_next_id('c')
        commands.append({'id': new_id, 'parent_id': parent_id, 'name': name, 'flag': flag, 'value': value})
        self.c_name_entry.delete(0, tk.END)
        self.c_flag_entry.delete(0, tk.END)
        self.c_value_entry.delete(0, tk.END)
        self.update_listboxes()
        self.update_previews()

    def delete_item(self, listbox, data_list, prefix):
        """Γενική συνάρτηση για διαγραφή από Listbox και λίστα δεδομένων με έλεγχο εξάρτησης."""
        global sub_menus, commands  

        try:
            selected_index = listbox.curselection()[0]
            deleted_id = data_list[selected_index]['id']
            item_name = data_list[selected_index]['name']
            
            # --- Έλεγχος Εξάρτησης και Αναδρομική Διαγραφή ---
            if prefix == 'm':
                dependent_submenus = [sm for sm in sub_menus if sm['parent_id'] == deleted_id]
                if dependent_submenus:
                    confirm = messagebox.askyesno(
                        self.get_text('delete_confirm_title'), 
                        self.get_text('confirm_delete_menu', name=item_name)
                    )
                    if not confirm: return

                    # Εκτέλεση αναδρομικού καθαρισμού
                    sm_to_delete_ids = [sm['id'] for sm in dependent_submenus]
                    commands = [c for c in commands if c['parent_id'] not in sm_to_delete_ids]
                    sub_menus = [sm for sm in sub_menus if sm['parent_id'] != deleted_id]

            elif prefix == 'sm':
                dependent_commands = [c for c in commands if c['parent_id'] == deleted_id]
                if dependent_commands:
                    confirm = messagebox.askyesno(
                        self.get_text('delete_confirm_title'), 
                        self.get_text('confirm_delete_submenu', name=item_name)
                    )
                    if not confirm: return
                    commands = [c for c in commands if c['parent_id'] != deleted_id]
            # --- Τέλος Ελέγχου Εξάρτησης ---
            
            # --- Κανονική Διαγραφή (Διαγράφεται το ίδιο το στοιχείο) ---
            listbox.delete(selected_index)
            del data_list[selected_index] 
            
            # --- Ενημέρωση UI και Μήνυμα Επιτυχίας ---
            self.update_listboxes()
            self.update_parent_dropdowns()
            self.update_previews() 
            messagebox.showinfo(self.get_text('success_title'), f"{self.get_text('msg_deleted')} {deleted_id} - {item_name.upper()}")
            
        except IndexError:
            messagebox.showwarning(self.get_text('warning_title'), self.get_text('warn_select_to_delete'))
        except Exception as e:
            messagebox.showerror(self.get_text('error_title'), f"{self.get_text('err_deletion_failed')} {e}")

    def clear_all_data(self):
        """Καθαρίζει όλα τα δεδομένα (Μενού, Υπομενού, Εντολές) και μηδενίζει τους μετρητές ID."""
        confirm = messagebox.askyesno(
            self.get_text('clear_confirm_title'), 
            self.get_text('confirm_clear_all')
        )
        if not confirm: return
        
        global main_menus, sub_menus, commands, id_counter
        main_menus = []
        sub_menus = []
        commands = []
        id_counter = {'m': 0, 'sm': 0, 'c': 0}
        
        # Clear input fields
        self.m_name_entry.delete(0, tk.END)
        self.sm_name_entry.delete(0, tk.END)
        self.sm_parent_menu_combobox.set("")
        self.c_name_entry.delete(0, tk.END)
        self.c_flag_entry.delete(0, tk.END)
        self.c_value_entry.delete(0, tk.END)
        self.c_parent_submenu_combobox.set("")
        self.lua_import_text.delete(1.0, tk.END) # Clear import text area

        self.update_listboxes()
        self.update_parent_dropdowns()
        self.update_previews() 
        messagebox.showinfo(self.get_text('success_title'), self.get_text('msg_cleared'))
        
    # --- Logic for Previews, Export, Import ---

    def update_listboxes(self):
        """Ανανεώνει το περιεχόμενο όλων των Listbox widgets με βάση τη γλώσσα."""
        
        listbox_parent = self.get_text('listbox_parent')
        listbox_unknown = self.get_text('listbox_unknown')

        self.m_listbox.delete(0, tk.END)
        for m in main_menus:
            self.m_listbox.insert(tk.END, f"{m['id']}: {m['name'].upper()}") 

        self.sm_listbox.delete(0, tk.END)
        for sm in sub_menus:
            parent_name = next((m['name'] for m in main_menus if m['id'] == sm['parent_id']), listbox_unknown)
            self.sm_listbox.insert(tk.END, f"{sm['id']}: {sm['name'].upper()} ({listbox_parent}: {sm['parent_id']} - {parent_name.upper()})") 

        self.c_listbox.delete(0, tk.END)
        listbox_flag = self.get_text('listbox_flag')
        for c in commands:
            self.c_listbox.insert(tk.END, f"{c['id']}: {c['name'].upper()} ({listbox_flag} '{c['flag'].upper()}' = {c['value'].upper()})") 

    def update_parent_dropdowns(self):
        """Ενημερώνει τα dropdowns με τα διαθέσιμα γονικά μενού/υπομενού (ID - Όνομα)."""
        m_options = [f"{m['id']} - {m['name']}" for m in main_menus]
        self.sm_parent_menu_combobox['values'] = m_options
        if m_options and not self.sm_parent_menu_combobox.get() in m_options:
            self.sm_parent_menu_combobox.set(m_options[0])
        elif not m_options:
            self.sm_parent_menu_combobox.set("")

        sm_options = [f"{sm['id']} - {sm['name']}" for sm in sub_menus]
        self.c_parent_submenu_combobox['values'] = sm_options
        if sm_options and not self.c_parent_submenu_combobox.get() in sm_options:
            self.c_parent_submenu_combobox.set(sm_options[0])
        elif not sm_options:
            self.c_parent_submenu_combobox.set("")
            
    def update_previews(self):
        """Ενημερώνει τον κώδικα Lua και τη δομή του δέντρου."""
        self.update_lua_preview()
        self.update_tree_view()
        
    def update_tree_view(self):
        """Ενημερώνει το ttk.Treeview με την ιεραρχική δομή του μενού και εφαρμόζει τα χρώματα."""
        for i in self.tree_view.get_children():
            self.tree_view.delete(i)
            
        tree_menu_prefix = self.get_text('tree_menu_prefix')
        tree_submenu_prefix = self.get_text('tree_submenu_prefix')
        tree_command_prefix = self.get_text('tree_command_prefix')
        listbox_flag = self.get_text('listbox_flag')
            
        for m in main_menus:
            m_parent_id = m['id']
            m_text = f"[{m['id']}] {tree_menu_prefix} {m['name'].upper()}"
            # Εφαρμογή m_tag (Light Orange)
            self.tree_view.insert('', 'end', m_parent_id, text=m_text, open=True, tags=('m_tag',))
            
            for sm in sub_menus:
                if sm['parent_id'] == m_parent_id:
                    sm_parent_id = sm['id']
                    sm_text = f"[{sm['id']}] {tree_submenu_prefix} {sm['name'].upper()}"
                    # Εφαρμογή sm_tag (Light Yellow)
                    self.tree_view.insert(m_parent_id, 'end', sm_parent_id, text=sm_text, open=True, tags=('sm_tag',))
                    
                    for c in commands:
                        if c['parent_id'] == sm_parent_id:
                            c_text = f"[{c['id']}] {tree_command_prefix} {c['name'].upper()} ({listbox_flag}: {c['flag'].upper()}={c['value'].upper()})"
                            # Εφαρμογή c_tag (White)
                            self.tree_view.insert(sm_parent_id, 'end', c['id'], text=c_text, tags=('c_tag',))
                            
    def get_active_coalitions(self):
        """Επιστρέφει μια λίστα με το μόνο ενεργό coalition side."""
        coalition_map = {
            'BLUE': 'coalition.side.BLUE', 
            'RED': 'coalition.side.RED', 
            'NEUTRAL': 'coalition.side.NEUTRAL'
        }
        selected_key = self.selected_coalition.get() 
        return [coalition_map[selected_key]]

    def generate_lua_code(self):
        """Δημιουργεί τον τελικό κώδικα Lua με βάση τις τρεις λίστες και την επιλεγμένη συμμαχία."""
        
        lua_script = "-- DCS Mission Radio Menu Generated Code\n"
        lua_script += "-- Created with Python Tkinter Tool (DARK MODE & COALITION SELECTOR)\n\n" 
        
        active_coalitions = self.get_active_coalitions()
        
        if not active_coalitions:
            lua_script += self.get_text('lua_comment_error')
            return lua_script
            
        coalition_side = active_coalitions[0] 
        side_suffix = coalition_side.split('.')[-1] 
            
        lua_script += f"--- [ {side_suffix} ] -----------------------------------------------\n"
        
        # 1. Δήλωση Κύριων Μενού (m)
        if main_menus:
            lua_script += self.get_text('lua_comment_menu', side=side_suffix)
            for m in main_menus:
                lua_script += f"{m['id']}_{side_suffix} = missionCommands.addSubMenuForCoalition ({coalition_side},'{m['name']}')\n"
        
        # 2. Δήλωση Υπομενού (sm)
        if sub_menus:
            lua_script += self.get_text('lua_comment_submenu', side=side_suffix)
            for sm in sub_menus:
                parent_id_with_suffix = f"{sm['parent_id']}_{side_suffix}"
                lua_script += f"{sm['id']}_{side_suffix} = missionCommands.addSubMenuForCoalition ({coalition_side},'{sm['name']}', {parent_id_with_suffix})\n"

        # 3. Δήλωση Εντολών (c)
        if commands:
            lua_script += self.get_text('lua_comment_command', side=side_suffix)
            for c in commands:
                parent_id_with_suffix = f"{c['parent_id']}_{side_suffix}"
                action_code = f"function() trigger.action.setUserFlag('{c['flag']}',{c['value']}) end"
                lua_script += f"{c['id']}_{side_suffix} = missionCommands.addCommandForCoalition ({coalition_side},'{c['name']}', {parent_id_with_suffix}, {action_code}, nil)\n"

        lua_script += "\n---------------------------------------------------------------\n"
        return lua_script

    def update_lua_preview(self):
        """Ενημερώνει το πεδίο προεπισκόπησης με τον τρέχοντα κώδικα και το ανάλογο χρώμα."""
        lua_code = self.generate_lua_code()
        
        # 1. Καθορισμός χρώματος με βάση την επιλεγμένη συμμαχία
        selected_coalition = self.selected_coalition.get()
        if selected_coalition == 'BLUE':
            fg_color = self.THEME_COLORS['LUA_FG_BLUE']
        elif selected_coalition == 'RED':
            fg_color = self.THEME_COLORS['LUA_FG_RED']
        else: # NEUTRAL
            fg_color = self.THEME_COLORS['LUA_FG_NEUTRAL']
            
        # 2. Εφαρμογή χρώματος και ενημέρωση κειμένου
        self.lua_preview_text.config(state=tk.NORMAL, fg=fg_color) 
        self.lua_preview_text.delete(1.0, tk.END)
        self.lua_preview_text.insert(tk.END, lua_code)
        self.lua_preview_text.config(state=tk.DISABLED) 

    def export_lua_file(self):
        """Αποθηκεύει τον κώδικα Lua σε αρχείο."""
        
        lua_code = self.generate_lua_code()
        
        if not (main_menus or sub_menus or commands):
             messagebox.showwarning(self.get_text('warning_title'), self.get_text('warn_no_items_to_export'))
             return
             
        filename = filedialog.asksaveasfilename(
            defaultextension=".lua",
            filetypes=[("Lua files", "*.lua")],
            title=self.get_text('export_dialog_title')
        )

        if filename:
            try:
                with open(filename, "w", encoding="utf-8") as f:
                    f.write(lua_code)
                messagebox.showinfo(self.get_text('success_title'), self.get_text('msg_save_success', filename=filename))
                self.update_previews()
            except Exception as e:
                messagebox.showerror(self.get_text('save_error_title'), f"{self.get_text('err_save_fail')} {e}")

    def parse_lua_code(self, lua_code):
        """Αναλύει τον Lua κώδικα και γεμίζει τις λίστες δεδομένων, αγνοώντας το coalition suffix."""
        
        global main_menus, sub_menus, commands, id_counter
        main_menus = []
        sub_menus = []
        commands = []
        
        lines = lua_code.split('\n')
        
        # Regex patterns
        id_regex = r"(\w+)(?:_BLUE|_RED|_NEUTRAL)?"
        m_pattern = re.compile(rf"^{id_regex}\s*=\s*missionCommands\.addSubMenuForCoalition\s*\(coalition\.side\.(?:BLUE|RED|NEUTRAL),\s*'([^']+)'\)")
        sm_pattern = re.compile(rf"^{id_regex}\s*=\s*missionCommands\.addSubMenuForCoalition\s*\(coalition\.side\.(?:BLUE|RED|NEUTRAL),\s*'([^']+)',\s*(\w+)(?:_BLUE|_RED|_NEUTRAL)?\)")
        c_pattern = re.compile(rf"^{id_regex}\s*=\s*missionCommands\.addCommandForCoalition\s*\(coalition\.side\.(?:BLUE|RED|NEUTRAL),\s*'([^']+)',\s*(\w+)(?:_BLUE|_RED|_NEUTRAL)?,\s*function\(\)\s*trigger\.action\.setUserFlag\('([^']+)',(\d+)\)\s*end,\s*nil\)")
        
        max_ids = {'m': 0, 'sm': 0, 'c': 0}

        for line in lines:
            line = line.strip()
            if line.startswith('--') or not line:
                # Ελέγχουμε αν η γραμμή είναι σχόλιο ή κενή
                if line.startswith('---'):
                    # Αυτή η γραμμή περιέχει το coalition side
                    side_match = re.search(r'\[\s*(BLUE|RED|NEUTRAL)\s*\]', line)
                    if side_match:
                        # Ενημερώνουμε την επιλεγμένη συμμαχία στο UI
                        self.selected_coalition.set(side_match.group(1))
                continue
            
            # Δοκιμάζουμε για Command
            match_c = c_pattern.match(line)
            if match_c:
                id_str_clean, name, parent_id_full, flag, value = match_c.groups()
                parent_id = re.sub(r"_(BLUE|RED|NEUTRAL)$", "", parent_id_full)
                commands.append({'id': id_str_clean, 'parent_id': parent_id, 'name': name, 'flag': flag, 'value': value})
                try:
                    num = int(id_str_clean[1:]) 
                    max_ids['c'] = max(max_ids['c'], num)
                except (ValueError, TypeError):
                    pass 
                continue
                
            # Δοκιμάζουμε για Sub Menu
            match_sm = sm_pattern.match(line)
            if match_sm:
                id_str_clean, name, parent_id_full = match_sm.groups()
                parent_id = re.sub(r"_(BLUE|RED|NEUTRAL)$", "", parent_id_full)
                sub_menus.append({'id': id_str_clean, 'parent_id': parent_id, 'name': name})
                try:
                    num = int(id_str_clean[1:]) 
                    max_ids['sm'] = max(max_ids['sm'], num)
                except (ValueError, TypeError):
                    pass
                continue
                
            # Δοκιμάζουμε για Main Menu
            match_m = m_pattern.match(line)
            if match_m:
                id_str_clean, name = match_m.groups()
                main_menus.append({'id': id_str_clean, 'name': name})
                try:
                    num = int(id_str_clean[1:]) 
                    max_ids['m'] = max(max_ids['m'], num)
                except (ValueError, TypeError):
                    pass
                continue

        id_counter['m'] = max_ids['m']
        id_counter['sm'] = max_ids['sm']
        id_counter['c'] = max_ids['c']
        
        self.update_listboxes()
        self.update_parent_dropdowns()
        self.update_previews()
        
        messagebox.showinfo(self.get_text('load_success_title'), self.get_text('msg_load_success', m_count=len(main_menus), m_max=max_ids['m'], sm_count=len(sub_menus), sm_max=max_ids['sm'], c_count=len(commands), c_max=max_ids['c']))

    def load_from_file(self):
        filename = filedialog.askopenfilename(
            defaultextension=".lua",
            filetypes=[("Lua files", "*.lua")],
            title=self.get_text('load_dialog_title')
        )
        if filename:
            try:
                with open(filename, "r", encoding="utf-8") as f:
                    lua_code = f.read()
                self.parse_lua_code(lua_code)
            except Exception as e:
                messagebox.showerror(self.get_text('load_error_file_title'), f"{self.get_text('err_save_fail')} {e}")

    def load_from_text_area(self):
        lua_code = self.lua_import_text.get(1.0, tk.END).strip()
        if not lua_code:
            messagebox.showwarning(self.get_text('warning_title'), self.get_text('warn_code_area_empty'))
            return
        try:
            self.parse_lua_code(lua_code)
        except Exception as e:
            messagebox.showerror(self.get_text('load_error_parse_title'), f"{self.get_text('err_deletion_failed')} {e}")


# --- Εκτέλεση της Εφαρμογής ---
if __name__ == "__main__":
    root = tk.Tk()
    app = DCSMenuCreatorApp(root)
    root.mainloop()

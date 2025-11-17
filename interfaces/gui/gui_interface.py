"""
Graphical User Interface for All-in-One System Tools
Tkinter-based GUI implementation
"""

import tkinter as tk
from tkinter import ttk, messagebox
import threading
import time
from typing import Optional
from core.common.config import Config
from core.common.logger import Logger
from core.battery.battery_monitor import create_battery_monitor
from core.diagnostics.hardware_tests import create_diagnostics
from core.monitoring.system_monitor import create_system_monitor
from core.package_mgmt.winget_manager import create_package_manager

try:
    import psutil
    PSUTIL_AVAILABLE = True
except ImportError:
    PSUTIL_AVAILABLE = False

class GUIInterface:
    """Graphical User Interface implementation using Tkinter"""
    
    def __init__(self, config: Config, logger: Logger):
        self.config = config
        self.logger = logger
        self.root = None
        self.notebook = None
        self._running = False
        self._update_thread = None
        
        # Initialize tools
        self.battery_monitor = create_battery_monitor()
        self.diagnostics = create_diagnostics()
        self.system_monitor = create_system_monitor()
        self.package_manager = create_package_manager()
        
        # UI elements
        self.battery_widgets = {}
        self.system_widgets = {}
        self.diagnostics_widgets = {}
    
    def run(self):
        """Run the GUI interface"""
        self.logger.info("Launching Tkinter GUI interface")
        
        # Create main window
        self.root = tk.Tk()
        self.root.title("AIO-SDMS - All-in-One System Diagnostic & Monitoring Suite")
        self.root.geometry("900x600")
        
        # Set window icon (if available)
        try:
            icon_path = "assets/icon.ico"
            self.root.iconbitmap(icon_path)
        except:
            pass
        
        # Create menu bar
        self._create_menu()
        
        # Create main notebook (tabbed interface)
        self.notebook = ttk.Notebook(self.root)
        self.notebook.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)
        
        # Create tabs
        self._create_dashboard_tab()
        self._create_battery_tab()
        self._create_monitoring_tab()
        self._create_diagnostics_tab()
        self._create_packages_tab()
        
        # Start update thread
        self._running = True
        self._update_thread = threading.Thread(target=self._update_loop, daemon=True)
        self._update_thread.start()
        
        # Handle window close
        self.root.protocol("WM_DELETE_WINDOW", self._on_closing)
        
        # Run the main loop
        self.root.mainloop()
    
    def _create_menu(self):
        """Create menu bar"""
        menubar = tk.Menu(self.root)
        self.root.config(menu=menubar)
        
        # File menu
        file_menu = tk.Menu(menubar, tearoff=0)
        menubar.add_cascade(label="File", menu=file_menu)
        file_menu.add_command(label="Refresh", command=self._refresh_all)
        file_menu.add_separator()
        file_menu.add_command(label="Exit", command=self._on_closing)
        
        # Tools menu
        tools_menu = tk.Menu(menubar, tearoff=0)
        menubar.add_cascade(label="Tools", menu=tools_menu)
        tools_menu.add_command(label="Run All Diagnostics", command=self._run_all_diagnostics)
        
        # Help menu
        help_menu = tk.Menu(menubar, tearoff=0)
        menubar.add_cascade(label="Help", menu=help_menu)
        help_menu.add_command(label="About", command=self._show_about)
    
    def _create_dashboard_tab(self):
        """Create dashboard overview tab"""
        frame = ttk.Frame(self.notebook)
        self.notebook.add(frame, text="Dashboard")
        
        # Title
        title = ttk.Label(frame, text="System Overview Dashboard", font=("Arial", 16, "bold"))
        title.pack(pady=10)
        
        # Create grid for overview cards
        overview_frame = ttk.Frame(frame)
        overview_frame.pack(fill=tk.BOTH, expand=True, padx=20, pady=10)
        
        # System info card
        sys_card = ttk.LabelFrame(overview_frame, text="System Information", padding=10)
        sys_card.grid(row=0, column=0, padx=10, pady=10, sticky="nsew")
        
        self.system_widgets['os_label'] = ttk.Label(sys_card, text="OS: Loading...")
        self.system_widgets['os_label'].pack(anchor='w')
        
        self.system_widgets['cpu_label'] = ttk.Label(sys_card, text="CPU: Loading...")
        self.system_widgets['cpu_label'].pack(anchor='w')
        
        self.system_widgets['ram_label'] = ttk.Label(sys_card, text="RAM: Loading...")
        self.system_widgets['ram_label'].pack(anchor='w')
        
        # Quick stats card
        stats_card = ttk.LabelFrame(overview_frame, text="Quick Stats", padding=10)
        stats_card.grid(row=0, column=1, padx=10, pady=10, sticky="nsew")
        
        self.system_widgets['cpu_usage'] = ttk.Label(stats_card, text="CPU Usage: ---%", font=("Arial", 12))
        self.system_widgets['cpu_usage'].pack(anchor='w', pady=5)
        
        self.system_widgets['mem_usage'] = ttk.Label(stats_card, text="Memory Usage: ---%", font=("Arial", 12))
        self.system_widgets['mem_usage'].pack(anchor='w', pady=5)
        
        self.system_widgets['disk_usage'] = ttk.Label(stats_card, text="Disk Usage: ---%", font=("Arial", 12))
        self.system_widgets['disk_usage'].pack(anchor='w', pady=5)
        
        overview_frame.columnconfigure(0, weight=1)
        overview_frame.columnconfigure(1, weight=1)
    
    def _create_battery_tab(self):
        """Create battery monitoring tab"""
        frame = ttk.Frame(self.notebook)
        self.notebook.add(frame, text="Battery")
        
        title = ttk.Label(frame, text="Battery Monitor", font=("Arial", 14, "bold"))
        title.pack(pady=10)
        
        info_frame = ttk.LabelFrame(frame, text="Battery Information", padding=20)
        info_frame.pack(fill=tk.BOTH, expand=True, padx=20, pady=10)
        
        self.battery_widgets['percent'] = ttk.Label(info_frame, text="Battery: ---%", font=("Arial", 24, "bold"))
        self.battery_widgets['percent'].pack(pady=10)
        
        self.battery_widgets['status'] = ttk.Label(info_frame, text="Status: Unknown", font=("Arial", 12))
        self.battery_widgets['status'].pack(pady=5)
        
        self.battery_widgets['time'] = ttk.Label(info_frame, text="Time Remaining: Unknown")
        self.battery_widgets['time'].pack(pady=5)
        
        # Progress bar
        self.battery_widgets['progress'] = ttk.Progressbar(info_frame, length=400, mode='determinate')
        self.battery_widgets['progress'].pack(pady=10)
    
    def _create_monitoring_tab(self):
        """Create system monitoring tab"""
        frame = ttk.Frame(self.notebook)
        self.notebook.add(frame, text="Monitoring")
        
        title = ttk.Label(frame, text="System Performance Monitor", font=("Arial", 14, "bold"))
        title.pack(pady=10)
        
        # CPU section
        cpu_frame = ttk.LabelFrame(frame, text="CPU", padding=10)
        cpu_frame.pack(fill=tk.X, padx=20, pady=5)
        
        self.system_widgets['cpu_percent'] = ttk.Label(cpu_frame, text="Usage: ---%")
        self.system_widgets['cpu_percent'].pack(side=tk.LEFT, padx=10)
        
        self.system_widgets['cpu_cores'] = ttk.Label(cpu_frame, text="Cores: ---")
        self.system_widgets['cpu_cores'].pack(side=tk.LEFT, padx=10)
        
        # Memory section
        mem_frame = ttk.LabelFrame(frame, text="Memory", padding=10)
        mem_frame.pack(fill=tk.X, padx=20, pady=5)
        
        self.system_widgets['mem_percent'] = ttk.Label(mem_frame, text="Usage: ---%")
        self.system_widgets['mem_percent'].pack(side=tk.LEFT, padx=10)
        
        self.system_widgets['mem_total'] = ttk.Label(mem_frame, text="Total: ---")
        self.system_widgets['mem_total'].pack(side=tk.LEFT, padx=10)
        
        # Disk section
        disk_frame = ttk.LabelFrame(frame, text="Disk", padding=10)
        disk_frame.pack(fill=tk.X, padx=20, pady=5)
        
        self.system_widgets['disk_percent'] = ttk.Label(disk_frame, text="Usage: ---%")
        self.system_widgets['disk_percent'].pack(side=tk.LEFT, padx=10)
        
        self.system_widgets['disk_total'] = ttk.Label(disk_frame, text="Total: ---")
        self.system_widgets['disk_total'].pack(side=tk.LEFT, padx=10)
    
    def _create_diagnostics_tab(self):
        """Create hardware diagnostics tab"""
        frame = ttk.Frame(self.notebook)
        self.notebook.add(frame, text="Diagnostics")
        
        title = ttk.Label(frame, text="Hardware Diagnostics", font=("Arial", 14, "bold"))
        title.pack(pady=10)
        
        btn_frame = ttk.Frame(frame)
        btn_frame.pack(pady=10)
        
        ttk.Button(btn_frame, text="Run All Tests", command=self._run_all_diagnostics).pack(side=tk.LEFT, padx=5)
        ttk.Button(btn_frame, text="Clear Results", command=self._clear_diagnostics).pack(side=tk.LEFT, padx=5)
        
        # Results text area
        results_frame = ttk.LabelFrame(frame, text="Test Results", padding=10)
        results_frame.pack(fill=tk.BOTH, expand=True, padx=20, pady=10)
        
        self.diagnostics_widgets['results'] = tk.Text(results_frame, height=15, width=80, wrap=tk.WORD)
        self.diagnostics_widgets['results'].pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
        
        scrollbar = ttk.Scrollbar(results_frame, command=self.diagnostics_widgets['results'].yview)
        scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
        self.diagnostics_widgets['results'].config(yscrollcommand=scrollbar.set)
    
    def _create_packages_tab(self):
        """Create package management tab"""
        frame = ttk.Frame(self.notebook)
        self.notebook.add(frame, text="Packages")
        
        title = ttk.Label(frame, text="Package Manager (Windows Only)", font=("Arial", 14, "bold"))
        title.pack(pady=10)
        
        info = ttk.Label(frame, text="Package management features available through CLI.\nUse: python main.py --cli packages")
        info.pack(pady=20)
    
    def _update_loop(self):
        """Background update loop"""
        while self._running:
            try:
                self._update_system_info()
                self._update_battery_info()
            except Exception as e:
                self.logger.error(f"Update error: {e}")
            
            time.sleep(2)
    
    def _update_system_info(self):
        """Update system information"""
        if not PSUTIL_AVAILABLE:
            return
        
        try:
            import platform
            
            # Dashboard updates
            if 'os_label' in self.system_widgets:
                os_info = f"OS: {platform.system()} {platform.release()}"
                self.system_widgets['os_label'].config(text=os_info)
            
            if 'cpu_label' in self.system_widgets:
                cpu_info = f"CPU: {platform.processor()}"
                self.system_widgets['cpu_label'].config(text=cpu_info)
            
            if 'ram_label' in self.system_widgets:
                total_ram = psutil.virtual_memory().total / (1024**3)
                ram_info = f"RAM: {total_ram:.1f} GB"
                self.system_widgets['ram_label'].config(text=ram_info)
            
            # Quick stats
            cpu_percent = psutil.cpu_percent(interval=0.1)
            mem_percent = psutil.virtual_memory().percent
            disk_percent = psutil.disk_usage('/').percent if platform.system() != 'Windows' else psutil.disk_usage('C:').percent
            
            if 'cpu_usage' in self.system_widgets:
                self.system_widgets['cpu_usage'].config(text=f"CPU Usage: {cpu_percent:.1f}%")
            
            if 'mem_usage' in self.system_widgets:
                self.system_widgets['mem_usage'].config(text=f"Memory Usage: {mem_percent:.1f}%")
            
            if 'disk_usage' in self.system_widgets:
                self.system_widgets['disk_usage'].config(text=f"Disk Usage: {disk_percent:.1f}%")
            
            # Monitoring tab
            if 'cpu_percent' in self.system_widgets:
                self.system_widgets['cpu_percent'].config(text=f"Usage: {cpu_percent:.1f}%")
            
            if 'cpu_cores' in self.system_widgets:
                self.system_widgets['cpu_cores'].config(text=f"Cores: {psutil.cpu_count()}")
            
            if 'mem_percent' in self.system_widgets:
                mem = psutil.virtual_memory()
                self.system_widgets['mem_percent'].config(text=f"Usage: {mem.percent:.1f}%")
                self.system_widgets['mem_total'].config(text=f"Total: {mem.total / (1024**3):.1f} GB")
            
            if 'disk_percent' in self.system_widgets:
                disk = psutil.disk_usage('/') if platform.system() != 'Windows' else psutil.disk_usage('C:')
                self.system_widgets['disk_percent'].config(text=f"Usage: {disk.percent:.1f}%")
                self.system_widgets['disk_total'].config(text=f"Total: {disk.total / (1024**3):.1f} GB")
                
        except Exception as e:
            self.logger.error(f"System info update error: {e}")
    
    def _update_battery_info(self):
        """Update battery information"""
        if not PSUTIL_AVAILABLE:
            return
        
        try:
            battery = psutil.sensors_battery()
            if battery:
                percent = int(battery.percent)
                plugged = battery.power_plugged
                
                self.battery_widgets['percent'].config(text=f"Battery: {percent}%")
                self.battery_widgets['progress']['value'] = percent
                
                status = "Charging" if plugged else "Discharging"
                self.battery_widgets['status'].config(text=f"Status: {status}")
                
                if battery.secsleft != psutil.POWER_TIME_UNLIMITED and battery.secsleft != psutil.POWER_TIME_UNKNOWN:
                    hours = battery.secsleft // 3600
                    minutes = (battery.secsleft % 3600) // 60
                    self.battery_widgets['time'].config(text=f"Time Remaining: {hours}h {minutes}m")
                else:
                    self.battery_widgets['time'].config(text="Time Remaining: Calculating...")
            else:
                self.battery_widgets['percent'].config(text="No Battery Detected")
                self.battery_widgets['status'].config(text="Status: N/A")
                self.battery_widgets['time'].config(text="")
                
        except Exception as e:
            self.logger.error(f"Battery info update error: {e}")
    
    def _refresh_all(self):
        """Refresh all data"""
        self._update_system_info()
        self._update_battery_info()
        messagebox.showinfo("Refresh", "All data refreshed successfully!")
    
    def _run_all_diagnostics(self):
        """Run all diagnostic tests"""
        self.diagnostics_widgets['results'].delete(1.0, tk.END)
        self.diagnostics_widgets['results'].insert(tk.END, "Running diagnostics tests...\n\n")
        
        def run_tests():
            try:
                if hasattr(self.diagnostics, 'run_all_tests'):
                    results = self.diagnostics.run_all_tests()
                    output = "Diagnostic Tests Completed:\n\n"
                    for result in results:
                        output += f"{result}\n"
                else:
                    output = "Diagnostics module not fully implemented.\n"
                    output += "Use CLI for full diagnostics: python main.py --cli diagnostics\n"
                
                self.diagnostics_widgets['results'].insert(tk.END, output)
            except Exception as e:
                self.diagnostics_widgets['results'].insert(tk.END, f"Error: {e}\n")
        
        threading.Thread(target=run_tests, daemon=True).start()
    
    def _clear_diagnostics(self):
        """Clear diagnostics results"""
        self.diagnostics_widgets['results'].delete(1.0, tk.END)
    
    def _show_about(self):
        """Show about dialog"""
        messagebox.showinfo(
            "About AIO-SDMS",
            "All-in-One System Diagnostic & Monitoring Suite\n\n"
            "Version 2.0\n"
            "Author: Srijan-XI\n\n"
            "A comprehensive system monitoring and diagnostic tool."
        )
    
    def _on_closing(self):
        """Handle window close event"""
        self._running = False
        if self._update_thread:
            self._update_thread.join(timeout=1)
        self.root.destroy()
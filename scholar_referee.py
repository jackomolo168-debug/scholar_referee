#!/usr/bin/env python3
"""
ScholarReferee - A lightweight study timer application with retro aesthetic.
"""

import tkinter as tk
from tkinter import messagebox
import time
import sys
import platform


class ScholarReferee:
    """Main application class for the ScholarReferee study timer."""
    
    # Preset intervals in minutes
    PRESETS = {
        "Deep Work": 50,
        "Short Break": 10,
        "Long Break": 20
    }
    
    def __init__(self, root):
        """Initialize the application."""
        self.root = root
        self.root.title("ScholarReferee")
        self.root.resizable(False, False)
        self.root.configure(bg='#2b2b2b')
        
        # Timer state variables
        self.remaining_seconds = 0
        self.is_running = False
        self.is_paused = False
        self.current_preset = "Deep Work"
        self.custom_minutes = tk.IntVar(value=25)

        # Always on top toggle state
        self.always_on_top = tk.BooleanVar(value=False)
        
        # Setup GUI
        self._setup_gui()
        
        # Center window on screen
        self._center_window()
        
        # Bind window close event
        self.root.protocol("WM_DELETE_WINDOW", self._on_closing)

        # Bind keyboard shortcuts
        self.root.bind('<space>', lambda e: self._start_timer() if not self.is_running else self._pause_timer())
        self.root.bind('<Escape>', lambda e: self._reset_timer())
        
    def _center_window(self):
        """Center the window on the screen."""
        self.root.update_idletasks()
        width = 400
        height = 500
        x = (self.root.winfo_screenwidth() // 2) - (width // 2)
        y = (self.root.winfo_screenheight() // 2) - (height // 2)
        self.root.geometry(f'{width}x{height}+{x}+{y}')
        
    def _setup_gui(self):
        """Build the graphical user interface."""
        # Main container with retro color scheme
        main_frame = tk.Frame(self.root, bg='#2b2b2b')
        main_frame.pack(fill=tk.BOTH, expand=True, padx=20, pady=20)
        
        # Title label
        title_label = tk.Label(
            main_frame,
            text="SCHOLARREFEREE",
            font=('Courier', 18, 'bold'),
            fg='#ff6b35',
            bg='#2b2b2b'
        )
        title_label.pack(pady=(0, 20))
        
        # Digital clock display - Using fixed Tkinter font
        self.clock_label = tk.Label(
            main_frame,
            text="00:00",
            font=('Courier', 48, 'bold'),
            fg='#00ff41',
            bg='#1a1a1a',
            relief=tk.SUNKEN,
            bd=3,
            padx=10,
            pady=10
        )
        self.clock_label.pack(pady=20, fill=tk.X)
        
        # Preset buttons frame
        preset_frame = tk.Frame(main_frame, bg='#2b2b2b')
        preset_frame.pack(pady=10)
        
        for preset_name, minutes in self.PRESETS.items():
            btn = tk.Button(
                preset_frame,
                text=f"{preset_name}\n({minutes}m)",
                font=('Courier', 9, 'bold'),
                bg='#3a3a3a',
                fg='#ffffff',
                activebackground='#ff6b35',
                activeforeground='#ffffff',
                relief=tk.RAISED,
                bd=2,
                width=12,
                height=2,
                command=lambda m=minutes, name=preset_name: self._set_preset(m, name)
            )
            btn.pack(side=tk.LEFT, padx=5)
        
        # Custom timer frame
        custom_frame = tk.Frame(main_frame, bg='#2b2b2b')
        custom_frame.pack(pady=15)
        
        tk.Label(
            custom_frame,
            text="Custom:",
            font=('Courier', 10, 'bold'),
            fg='#ffffff',
            bg='#2b2b2b'
        ).pack(side=tk.LEFT, padx=5)
        
        self.custom_entry = tk.Entry(
            custom_frame,
            textvariable=self.custom_minutes,
            font=('Courier', 12),
            width=6,
            bg='#1a1a1a',
            fg='#00ff41',
            insertbackground='#00ff41',
            justify='center'
        )
        self.custom_entry.pack(side=tk.LEFT, padx=5)
        
        tk.Label(
            custom_frame,
            text="minutes",
            font=('Courier', 10),
            fg='#ffffff',
            bg='#2b2b2b'
        ).pack(side=tk.LEFT)
        
        custom_btn = tk.Button(
            custom_frame,
            text="Set Custom",
            font=('Courier', 9),
            bg='#3a3a3a',
            fg='#ffffff',
            activebackground='#ff6b35',
            command=self._set_custom
        )
        custom_btn.pack(side=tk.LEFT, padx=10)
        
        # Control buttons frame
        control_frame = tk.Frame(main_frame, bg='#2b2b2b')
        control_frame.pack(pady=15)
        
        self.start_btn = tk.Button(
            control_frame,
            text="START",
            font=('Courier', 12, 'bold'),
            bg='#00a86b',
            fg='#ffffff',
            activebackground='#008f5a',
            width=8,
            command=self._start_timer
        )
        self.start_btn.pack(side=tk.LEFT, padx=5)
        
        self.pause_btn = tk.Button(
            control_frame,
            text="PAUSE",
            font=('Courier', 12, 'bold'),
            bg='#ff8c00',
            fg='#ffffff',
            activebackground='#e07c00',
            width=8,
            command=self._pause_timer,
            state=tk.DISABLED
        )
        self.pause_btn.pack(side=tk.LEFT, padx=5)
        
        reset_btn = tk.Button(
            control_frame,
            text="RESET",
            font=('Courier', 12, 'bold'),
            bg='#dc143c',
            fg='#ffffff',
            activebackground='#b01030',
            width=8,
            command=self._reset_timer
        )
        reset_btn.pack(side=tk.LEFT, padx=5)
        
        # Always on top toggle
        top_frame = tk.Frame(main_frame, bg='#2b2b2b')
        top_frame.pack(pady=15)
        
        self.top_check = tk.Checkbutton(
            top_frame,
            text="Always on Top",
            variable=self.always_on_top,
            command=self._toggle_always_on_top,
            font=('Courier', 9),
            fg='#ffffff',
            bg='#2b2b2b',
            selectcolor='#2b2b2b',
            activebackground='#2b2b2b'
        )
        self.top_check.pack()
        
        # Status label
        self.status_label = tk.Label(
            main_frame,
            text="Ready • Set a timer",
            font=('Courier', 9, 'italic'),
            fg='#888888',
            bg='#2b2b2b'
        )
        self.status_label.pack(pady=10)
        
    def _set_preset(self, minutes, preset_name):
        """Set a preset timer duration."""
        if self.is_running and not self.is_paused:
            self._reset_timer()
        self.remaining_seconds = minutes * 60
        self.current_preset = preset_name
        self._update_display()
        self.status_label.config(text=f"Preset: {preset_name} ({minutes} min) set")
        
    def _set_custom(self):
        """Set custom timer duration from entry field."""
        try:
            minutes = self.custom_minutes.get()
            if minutes <= 0:
                raise ValueError
            if self.is_running and not self.is_paused:
                self._reset_timer()
            self.remaining_seconds = minutes * 60
            self.current_preset = "Custom"
            self._update_display()
            self.status_label.config(text=f"Custom timer: {minutes} minutes set")
        except (tk.TclError, ValueError):
            messagebox.showwarning("Invalid Input", "Please enter a valid positive integer for minutes.")
            
    def _start_timer(self):
        """Start or resume the countdown timer."""
        if self.remaining_seconds <= 0:
            messagebox.showinfo("Timer", "Please set a timer duration first.")
            return
            
        if self.is_paused:
            self.is_paused = False
            self.is_running = True
            self.status_label.config(text="Timer resumed")
        elif not self.is_running:
            self.is_running = True
            self.status_label.config(text="Timer running")
        
        self.start_btn.config(state=tk.DISABLED)
        self.pause_btn.config(state=tk.NORMAL)
        self._run_timer()
        
    def _pause_timer(self):
        """Pause the countdown timer."""
        if self.is_running and not self.is_paused:
            self.is_paused = True
            self.status_label.config(text="Timer paused")
            self.start_btn.config(state=tk.NORMAL)
            self.pause_btn.config(state=tk.DISABLED)
            
    def _reset_timer(self):
        """Reset the timer to its initial state."""
        self.is_running = False
        self.is_paused = False
        
        # Reset to current preset or custom
        if self.current_preset == "Custom":
            try:
                minutes = self.custom_minutes.get()
                self.remaining_seconds = minutes * 60
            except:
                self.remaining_seconds = 0
        else:
            for name, mins in self.PRESETS.items():
                if name == self.current_preset:
                    self.remaining_seconds = mins * 60
                    break
                    
        self._update_display()
        self.start_btn.config(state=tk.NORMAL)
        self.pause_btn.config(state=tk.DISABLED)
        self.status_label.config(text="Timer reset")
        
    def _run_timer(self):
        """Internal method to handle the countdown logic."""
        if not self.is_running or self.is_paused:
            return
            
        if self.remaining_seconds <= 0:
            self._timer_complete()
            return
            
        # Update display
        self._update_display()
        self.remaining_seconds -= 1
        
        # Schedule next update
        self.root.after(1000, self._run_timer)
        
    def _update_display(self):
        """Update the digital clock display."""
        minutes = self.remaining_seconds // 60
        seconds = self.remaining_seconds % 60
        time_str = f"{minutes:02d}:{seconds:02d}"
        self.clock_label.config(text=time_str)
        
    def _timer_complete(self):
        """Handle timer completion - play alert and reset."""
        self.is_running = False
        self.is_paused = False
        self._update_display()
        self.start_btn.config(state=tk.NORMAL)
        self.pause_btn.config(state=tk.DISABLED)
        
        # Visual alert
        self._flash_window()
        
        # System beep
        self._play_beep()
        
        # Status update
        self.status_label.config(text="Time's up! Great work!")
        
        # Show popup
        messagebox.showinfo("ScholarReferee", f"{self.current_preset} timer completed!\nTime's up!")
        
    def _play_beep(self):
        """Play a system beep or console bell."""
        if platform.system() == "Windows":
            import winsound
            winsound.Beep(880, 500)  # Frequency: 880Hz, Duration: 500ms
        else:
            # For Linux/Mac - print bell character and use system beep
            sys.stdout.write('\a')
            sys.stdout.flush()
            
    def _flash_window(self):
        """Flash the window for visual alert."""
        original_bg = self.root.cget('bg')
        for _ in range(3):
            self.root.configure(bg='#ff6b35')
            self.root.update()
            time.sleep(0.1)
            self.root.configure(bg=original_bg)
            self.root.update()
            time.sleep(0.1)
            
    def _toggle_always_on_top(self):
        """Toggle the always-on-top window property."""
        self.root.attributes('-topmost', self.always_on_top.get())
        status = "enabled" if self.always_on_top.get() else "disabled"
        self.status_label.config(text=f"Always on top {status}")
        
    def _on_closing(self):
        """Handle window closing event."""
        if self.is_running:
            if messagebox.askokcancel("Quit", "Timer is running. Do you really want to quit?"):
                self.root.destroy()
        else:
            self.root.destroy()


def main():
    """Entry point for the application."""
    root = tk.Tk()
    app = ScholarReferee(root)
    root.mainloop()


if __name__ == "__main__":
    main()
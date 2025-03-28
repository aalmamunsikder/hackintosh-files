import os
import sys
import shutil
import zipfile
import threading
import subprocess
import platform
from pathlib import Path
import customtkinter as ctk
from PIL import Image, ImageTk
import tkinter as tk
from tkinter import filedialog, messagebox

# Set appearance mode and default color theme
ctk.set_appearance_mode("dark")
ctk.set_default_color_theme("blue")

# Constants
APP_TITLE = "HackintoshEFI Builder"
APP_VERSION = "1.0.0"
APP_WIDTH = 1200
APP_HEIGHT = 800

# Paths
SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
RESOURCES_DIR = os.path.join(SCRIPT_DIR, "resources")
TEMP_DIR = os.path.join(SCRIPT_DIR, "temp")
OUTPUT_DIR = os.path.join(SCRIPT_DIR, "output")

# Ensure directories exist
os.makedirs(RESOURCES_DIR, exist_ok=True)
os.makedirs(TEMP_DIR, exist_ok=True)
os.makedirs(OUTPUT_DIR, exist_ok=True)

class HackintoshEFIBuilder(ctk.CTk):
    def __init__(self):
        super().__init__()
        
        # Configure window
        self.title(f"{APP_TITLE} v{APP_VERSION}")
        self.geometry(f"{APP_WIDTH}x{APP_HEIGHT}")
        self.minsize(APP_WIDTH, APP_HEIGHT)
        
        # Variables
        self.selected_cpu = ctk.StringVar(value="Intel")
        self.selected_cpu_model = ctk.StringVar(value="")
        self.selected_gpu = ctk.StringVar(value="Intel HD Graphics")
        self.selected_audio = ctk.StringVar(value="Realtek ALC")
        self.selected_ethernet = ctk.StringVar(value="Intel")
        self.selected_wifi = ctk.StringVar(value="None")
        self.selected_opencore_version = ctk.StringVar(value="Latest")
        self.output_path = ctk.StringVar(value=OUTPUT_DIR)
        self.build_progress = ctk.DoubleVar(value=0.0)
        self.status_text = ctk.StringVar(value="Ready")
        
        # Create UI
        self.create_ui()
    
    def create_ui(self):
        # Create main frame with padding
        main_frame = ctk.CTkFrame(self)
        main_frame.pack(fill="both", expand=True, padx=20, pady=20)
        
        # Header
        header_frame = ctk.CTkFrame(main_frame, fg_color="transparent")
        header_frame.pack(fill="x", pady=(0, 20))
        
        title_label = ctk.CTkLabel(
            header_frame, 
            text=APP_TITLE, 
            font=ctk.CTkFont(size=32, weight="bold")
        )
        title_label.pack(side="left")
        
        version_label = ctk.CTkLabel(
            header_frame, 
            text=f"v{APP_VERSION}", 
            font=ctk.CTkFont(size=14),
            text_color="gray"
        )
        version_label.pack(side="left", padx=(10, 0), pady=(10, 0))
        
        # Content area with two columns
        content_frame = ctk.CTkFrame(main_frame)
        content_frame.pack(fill="both", expand=True)
        
        # Left column - Hardware selection
        left_frame = ctk.CTkFrame(content_frame, fg_color="transparent")
        left_frame.pack(side="left", fill="both", expand=True, padx=(0, 10))
        
        hardware_frame = ctk.CTkFrame(left_frame)
        hardware_frame.pack(fill="both", expand=True)
        
        hardware_title = ctk.CTkLabel(
            hardware_frame, 
            text="Hardware Configuration", 
            font=ctk.CTkFont(size=20, weight="bold"),
            anchor="w"
        )
        hardware_title.pack(fill="x", padx=20, pady=(20, 10))
        
        # CPU Selection
        cpu_frame = ctk.CTkFrame(hardware_frame, fg_color="transparent")
        cpu_frame.pack(fill="x", padx=20, pady=10)
        
        cpu_label = ctk.CTkLabel(cpu_frame, text="CPU Type:", width=120, anchor="w")
        cpu_label.pack(side="left")
        
        cpu_intel = ctk.CTkRadioButton(cpu_frame, text="Intel", variable=self.selected_cpu, value="Intel")
        cpu_intel.pack(side="left", padx=(0, 10))
        
        cpu_amd = ctk.CTkRadioButton(cpu_frame, text="AMD", variable=self.selected_cpu, value="AMD")
        cpu_amd.pack(side="left")
        
        # CPU Model
        cpu_model_frame = ctk.CTkFrame(hardware_frame, fg_color="transparent")
        cpu_model_frame.pack(fill="x", padx=20, pady=10)
        
        cpu_model_label = ctk.CTkLabel(cpu_model_frame, text="CPU Model:", width=120, anchor="w")
        cpu_model_label.pack(side="left")
        
        cpu_models = ["Core i3", "Core i5", "Core i7", "Core i9", "Xeon", "Ryzen 3", "Ryzen 5", "Ryzen 7", "Ryzen 9"]
        cpu_model_dropdown = ctk.CTkOptionMenu(cpu_model_frame, variable=self.selected_cpu_model, values=cpu_models)
        cpu_model_dropdown.pack(side="left", fill="x", expand=True)
        
        # GPU Selection
        gpu_frame = ctk.CTkFrame(hardware_frame, fg_color="transparent")
        gpu_frame.pack(fill="x", padx=20, pady=10)
        
        gpu_label = ctk.CTkLabel(gpu_frame, text="Graphics:", width=120, anchor="w")
        gpu_label.pack(side="left")
        
        gpu_options = ["Intel HD Graphics", "AMD Radeon", "NVIDIA (Kepler)", "NVIDIA (disabled)"]
        gpu_dropdown = ctk.CTkOptionMenu(gpu_frame, variable=self.selected_gpu, values=gpu_options)
        gpu_dropdown.pack(side="left", fill="x", expand=True)
        
        # Audio Selection
        audio_frame = ctk.CTkFrame(hardware_frame, fg_color="transparent")
        audio_frame.pack(fill="x", padx=20, pady=10)
        
        audio_label = ctk.CTkLabel(audio_frame, text="Audio:", width=120, anchor="w")
        audio_label.pack(side="left")
        
        audio_options = ["Realtek ALC", "Conexant", "Other"]
        audio_dropdown = ctk.CTkOptionMenu(audio_frame, variable=self.selected_audio, values=audio_options)
        audio_dropdown.pack(side="left", fill="x", expand=True)
        
        # Ethernet Selection
        ethernet_frame = ctk.CTkFrame(hardware_frame, fg_color="transparent")
        ethernet_frame.pack(fill="x", padx=20, pady=10)
        
        ethernet_label = ctk.CTkLabel(ethernet_frame, text="Ethernet:", width=120, anchor="w")
        ethernet_label.pack(side="left")
        
        ethernet_options = ["Intel", "Realtek", "Broadcom", "None"]
        ethernet_dropdown = ctk.CTkOptionMenu(ethernet_frame, variable=self.selected_ethernet, values=ethernet_options)
        ethernet_dropdown.pack(side="left", fill="x", expand=True)
        
        # WiFi Selection
        wifi_frame = ctk.CTkFrame(hardware_frame, fg_color="transparent")
        wifi_frame.pack(fill="x", padx=20, pady=10)
        
        wifi_label = ctk.CTkLabel(wifi_frame, text="WiFi:", width=120, anchor="w")
        wifi_label.pack(side="left")
        
        wifi_options = ["Intel", "Broadcom", "None"]
        wifi_dropdown = ctk.CTkOptionMenu(wifi_frame, variable=self.selected_wifi, values=wifi_options)
        wifi_dropdown.pack(side="left", fill="x", expand=True)
        
        # Right column - Build options and progress
        right_frame = ctk.CTkFrame(content_frame, fg_color="transparent")
        right_frame.pack(side="right", fill="both", expand=True, padx=(10, 0))
        
        build_frame = ctk.CTkFrame(right_frame)
        build_frame.pack(fill="both", expand=True)
        
        build_title = ctk.CTkLabel(
            build_frame, 
            text="Build Configuration", 
            font=ctk.CTkFont(size=20, weight="bold"),
            anchor="w"
        )
        build_title.pack(fill="x", padx=20, pady=(20, 10))
        
        # OpenCore Version
        oc_frame = ctk.CTkFrame(build_frame, fg_color="transparent")
        oc_frame.pack(fill="x", padx=20, pady=10)
        
        oc_label = ctk.CTkLabel(oc_frame, text="OpenCore Version:", width=120, anchor="w")
        oc_label.pack(side="left")
        
        oc_options = ["Latest", "0.9.5", "0.9.4", "0.9.3", "0.9.2", "0.9.1", "0.9.0"]
        oc_dropdown = ctk.CTkOptionMenu(oc_frame, variable=self.selected_opencore_version, values=oc_options)
        oc_dropdown.pack(side="left", fill="x", expand=True)
        
        # Output Path
        output_frame = ctk.CTkFrame(build_frame, fg_color="transparent")
        output_frame.pack(fill="x", padx=20, pady=10)
        
        output_label = ctk.CTkLabel(output_frame, text="Output Path:", width=120, anchor="w")
        output_label.pack(side="left")
        
        output_entry = ctk.CTkEntry(output_frame, textvariable=self.output_path)
        output_entry.pack(side="left", fill="x", expand=True, padx=(0, 10))
        
        output_button = ctk.CTkButton(output_frame, text="Browse", width=80, command=self.browse_output)
        output_button.pack(side="right")
        
        # Kexts selection
        kexts_frame = ctk.CTkFrame(build_frame, fg_color="transparent")
        kexts_frame.pack(fill="x", padx=20, pady=10)
        
        kexts_label = ctk.CTkLabel(
            kexts_frame, 
            text="Kexts Selection", 
            font=ctk.CTkFont(size=16, weight="bold"),
            anchor="w"
        )
        kexts_label.pack(fill="x", pady=(0, 10))
        
        # Kexts checkboxes
        self.kext_vars = {}
        kexts_list = [
            ("Lilu", True),
            ("VirtualSMC", True),
            ("WhateverGreen", True),
            ("AppleALC", True),
            ("IntelMausi", True),
            ("USBInjectAll", True),
            ("CPUFriend", True),
            ("RestrictEvents", True)
        ]
        
        kexts_inner_frame = ctk.CTkFrame(kexts_frame, fg_color="transparent")
        kexts_inner_frame.pack(fill="x")
        
        for i, (kext, default) in enumerate(kexts_list):
            var = ctk.BooleanVar(value=default)
            self.kext_vars[kext] = var
            
            # Create two columns of checkboxes
            col = i % 2
            row = i // 2
            
            checkbox = ctk.CTkCheckBox(kexts_inner_frame, text=kext, variable=var)
            checkbox.grid(row=row, column=col, sticky="w", padx=(10, 20), pady=5)
        
        # Progress section
        progress_frame = ctk.CTkFrame(build_frame, fg_color="transparent")
        progress_frame.pack(fill="x", padx=20, pady=(20, 10))
        
        progress_label = ctk.CTkLabel(
            progress_frame, 
            text="Build Progress", 
            font=ctk.CTkFont(size=16, weight="bold"),
            anchor="w"
        )
        progress_label.pack(fill="x", pady=(0, 10))
        
        self.progress_bar = ctk.CTkProgressBar(progress_frame)
        self.progress_bar.pack(fill="x", pady=5)
        self.progress_bar.set(0)
        
        self.status_label = ctk.CTkLabel(progress_frame, textvariable=self.status_text)
        self.status_label.pack(fill="x", pady=5)
        
        # Action buttons
        button_frame = ctk.CTkFrame(build_frame, fg_color="transparent")
        button_frame.pack(fill="x", padx=20, pady=(20, 20))
        
        build_button = ctk.CTkButton(
            button_frame, 
            text="Build EFI", 
            font=ctk.CTkFont(size=16, weight="bold"),
            height=40,
            command=self.start_build
        )
        build_button.pack(fill="x", pady=5)
        
        # Footer
        footer_frame = ctk.CTkFrame(main_frame, fg_color="transparent")
        footer_frame.pack(fill="x", pady=(20, 0))
        
        footer_text = ctk.CTkLabel(
            footer_frame, 
            text="Hackintosh EFI Builder - A modern tool for creating Hackintosh EFI folders",
            font=ctk.CTkFont(size=12),
            text_color="gray"
        )
        footer_text.pack(side="left")
    
    def browse_output(self):
        """Open file dialog to select output directory"""
        directory = filedialog.askdirectory(initialdir=self.output_path.get())
        if directory:
            self.output_path.set(directory)
    
    def start_build(self):
        """Start the EFI building process in a separate thread"""
        # Disable build button during build
        for widget in self.winfo_children():
            if isinstance(widget, ctk.CTkButton):
                widget.configure(state="disabled")
        
        # Reset progress
        self.build_progress.set(0)
        self.progress_bar.set(0)
        self.status_text.set("Starting build process...")
        
        # Start build in a separate thread
        build_thread = threading.Thread(target=self.build_efi)
        build_thread.daemon = True
        build_thread.start()
    
    def build_efi(self):
        """Build the EFI folder based on selected options"""
        try:
            # Create a unique output directory
            output_dir = os.path.join(self.output_path.get(), "EFI")
            if os.path.exists(output_dir):
                shutil.rmtree(output_dir)
            os.makedirs(output_dir)
            
            # Create EFI structure
            os.makedirs(os.path.join(output_dir, "OC", "ACPI"), exist_ok=True)
            os.makedirs(os.path.join(output_dir, "OC", "Drivers"), exist_ok=True)
            os.makedirs(os.path.join(output_dir, "OC", "Kexts"), exist_ok=True)
            os.makedirs(os.path.join(output_dir, "OC", "Resources"), exist_ok=True)
            os.makedirs(os.path.join(output_dir, "OC", "Tools"), exist_ok=True)
            
            self.update_progress(0.1, "Created EFI folder structure")
            
            # Extract OpenCore
            opencore_zip = os.path.join(SCRIPT_DIR, "opencore.zip")
            if os.path.exists(opencore_zip):
                with zipfile.ZipFile(opencore_zip, 'r') as zip_ref:
                    zip_ref.extractall(TEMP_DIR)
                
                # Copy OpenCore files
                self.copy_opencore_files(TEMP_DIR, output_dir)
                self.update_progress(0.3, "Extracted and copied OpenCore files")
            else:
                self.update_progress(0.3, "OpenCore zip not found, skipping...")
            
            # Process kexts
            self.process_kexts(output_dir)
            self.update_progress(0.7, "Processed and copied kexts")
            
            # Generate config.plist based on hardware selection
            self.generate_config_plist(output_dir)
            self.update_progress(0.9, "Generated config.plist")
            
            # Finalize
            self.update_progress(1.0, f"Build complete! EFI folder created at {output_dir}")
            
            # Re-enable build button
            self.after(0, self.enable_build_button)
            
            # Show success message
            self.after(0, lambda: messagebox.showinfo("Build Complete", 
                                                     f"EFI folder has been successfully created at:\n{output_dir}"))
            
        except Exception as e:
            self.update_progress(0, f"Error: {str(e)}")
            self.after(0, lambda: messagebox.showerror("Build Error", str(e)))
            self.after(0, self.enable_build_button)
    
    def update_progress(self, progress, status):
        """Update the progress bar and status text"""
        self.after(0, lambda: self.build_progress.set(progress))
        self.after(0, lambda: self.progress_bar.set(progress))
        self.after(0, lambda: self.status_text.set(status))
    
    def enable_build_button(self):
        """Re-enable the build button"""
        for widget in self.winfo_children():
            if isinstance(widget, ctk.CTkButton):
                widget.configure(state="normal")
    
    def copy_opencore_files(self, temp_dir, output_dir):
        """Copy OpenCore files to the output directory"""
        # This is a simplified version - in a real app, you'd need to handle
        # finding and copying the correct files from the extracted OpenCore zip
        
        # Copy OpenCore EFI drivers
        drivers_source = os.path.join(temp_dir, "X64", "EFI", "OC", "Drivers")
        drivers_dest = os.path.join(output_dir, "OC", "Drivers")
        
        if os.path.exists(drivers_source):
            for file in os.listdir(drivers_source):
                if file.endswith(".efi"):
                    shutil.copy(
                        os.path.join(drivers_source, file),
                        os.path.join(drivers_dest, file)
                    )
        
        # Copy OpenCore tools
        tools_source = os.path.join(temp_dir, "X64", "EFI", "OC", "Tools")
        tools_dest = os.path.join(output_dir, "OC", "Tools")
        
        if os.path.exists(tools_source):
            for file in os.listdir(tools_source):
                if file.endswith(".efi"):
                    shutil.copy(
                        os.path.join(tools_source, file),
                        os.path.join(tools_dest, file)
                    )
    
    def process_kexts(self, output_dir):
        """Process and copy selected kexts to the output directory"""
        kexts_dest = os.path.join(output_dir, "OC", "Kexts")
        
        # Map of kext names to their zip files
        kext_files = {
            "Lilu": "Lilu-1.7.0-RELEASE.zip",
            "VirtualSMC": "VirtualSMC-1.3.5-RELEASE.zip",
            "WhateverGreen": "WhateverGreen-1.6.9-RELEASE.zip",
            "AppleALC": "AppleALC-1.9.4-RELEASE.zip",
            "IntelMausi": "IntelMausi-1.0.8-RELEASE.zip",
            "USBInjectAll": "RehabMan-USBInjectAll-2018-1108.zip",
            "CPUFriend": "CPUFriend-1.2.9-RELEASE.zip",
            "RestrictEvents": "RestrictEvents-1.1.5-RELEASE.zip"
        }
        
        # Process each selected kext
        for kext_name, var in self.kext_vars.items():
            if var.get() and kext_name in kext_files:
                zip_file = os.path.join(SCRIPT_DIR, kext_files[kext_name])
                
                if os.path.exists(zip_file):
                    # Extract to temp directory
                    kext_temp_dir = os.path.join(TEMP_DIR, kext_name)
                    os.makedirs(kext_temp_dir, exist_ok=True)
                    
                    with zipfile.ZipFile(zip_file, 'r') as zip_ref:
                        zip_ref.extractall(kext_temp_dir)
                    
                    # Find and copy the .kext directory
                    for root, dirs, files in os.walk(kext_temp_dir):
                        for dir in dirs:
                            if dir.endswith(".kext"):
                                kext_path = os.path.join(root, dir)
                                dest_path = os.path.join(kexts_dest, dir)
                                
                                if os.path.exists(dest_path):
                                    shutil.rmtree(dest_path)
                                
                                shutil.copytree(kext_path, dest_path)
    
    def generate_config_plist(self, output_dir):
        """Generate a basic config.plist file based on hardware selection"""
        # In a real app, this would be much more complex and would generate
        # a proper OpenCore config.plist based on the selected hardware
        
        # For this example, we'll just create a placeholder file
        config_path = os.path.join(output_dir, "OC", "config.plist")
        
        with open(config_path, 'w') as f:
            f.write('<?xml version="1.0" encoding="UTF-8"?>\n')
            f.write('<!DOCTYPE plist PUBLIC "-//Apple//DTD PLIST 1.0//EN" "http://www.apple.com/DTDs/PropertyList-1.0.dtd">\n')
            f.write('<plist version="1.0">\n')
            f.write('<dict>\n')
            f.write('    <!-- This is a placeholder config.plist -->\n')
            f.write('    <!-- In a real app, this would be a properly generated config -->\n')
            f.write('    <key>ACPI</key>\n')
            f.write('    <dict/>\n')
            f.write('    <key>Booter</key>\n')
            f.write('    <dict/>\n')
            f.write('    <key>DeviceProperties</key>\n')
            f.write('    <dict/>\n')
            f.write('    <key>Kernel</key>\n')
            f.write('    <dict/>\n')
            f.write('    <key>Misc</key>\n')
            f.write('    <dict/>\n')
            f.write('    <key>NVRAM</key>\n')
            f.write('    <dict/>\n')
            f.write('    <key>PlatformInfo</key>\n')
            f.write('    <dict/>\n')
            f.write('    <key>UEFI</key>\n')
            f.write('    <dict/>\n')
            f.write('</dict>\n')
            f.write('</plist>\n')


if __name__ == "__main__":
    app = HackintoshEFIBuilder()
    app.mainloop()
#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Directory Tree Explorer with Branch Selection
Run by double-clicking - allows you to explore and select any directory
"""

import os
import sys
import platform
from pathlib import Path

class DirectoryExplorer:
    def __init__(self):
        self.current_dir = Path.cwd()
        self.selected_dir = None
        self.history = []
        self.excluded_dirs = {
            '__pycache__', '.git', '.svn', '.hg', '.venv', 'venv', 'env',
            'node_modules', '.idea', '.vscode', '.vs', '.history',
            'dist', 'build', '.pytest_cache', '.mypy_cache'
        }
    
    def clear_screen(self):
        """Clear terminal screen"""
        if platform.system() == 'Windows':
            os.system('cls')
        else:
            os.system('clear')
    
    def print_header(self):
        """Print application header"""
        print("╔══════════════════════════════════════════════════════════╗")
        print("║          DIRECTORY TREE EXPLORER 🌳                      ║")
        print("║          ---------------------------------               ║")
        print("║          Navigate and select any directory               ║")
        print("╚══════════════════════════════════════════════════════════╝")
        print()
    
    def print_current_path(self):
        """Print current directory path"""
        print(f"📁 Current: {self.current_dir}")
        print("-" * 60)
    
    def get_directory_contents(self, directory):
        """Get directories in current path, excluding unwanted ones"""
        try:
            all_items = sorted(os.listdir(directory))
            dirs = []
            files = []
            
            for item in all_items:
                item_path = os.path.join(directory, item)
                if item.startswith('.'):
                    continue
                if item in self.excluded_dirs:
                    continue
                if os.path.isdir(item_path):
                    dirs.append(item)
                else:
                    files.append(item)
            
            return dirs, files
        except PermissionError:
            return [], []
    
    def print_tree(self, start_path=None, level=0, max_depth=3, prefix=""):
        """Print directory tree structure"""
        if start_path is None:
            start_path = self.current_dir
        
        if level > max_depth:
            return
        
        try:
            items = sorted(os.listdir(start_path))
            
            # Filter out excluded directories
            items = [item for item in items 
                    if not item.startswith('.') 
                    and item not in self.excluded_dirs
                    and os.path.isdir(os.path.join(start_path, item))]
            
            for i, item in enumerate(items):
                item_path = os.path.join(start_path, item)
                is_last = (i == len(items) - 1)
                
                # Determine tree symbols
                if level == 0:
                    connector = "📂 "
                elif is_last:
                    connector = "└── "
                else:
                    connector = "├── "
                
                # Print with proper indentation
                print(f"{prefix}{connector}{item}")
                
                # Recursively print subdirectories
                new_prefix = prefix + ("    " if is_last else "│   ")
                self.print_tree(item_path, level + 1, max_depth, new_prefix)
                
        except PermissionError:
            pass
    
    def print_detailed_list(self):
        """Print detailed directory listing with numbers"""
        dirs, files = self.get_directory_contents(self.current_dir)
        
        print("📂 DIRECTORIES:")
        print("-" * 40)
        
        if dirs:
            for i, dir_name in enumerate(dirs, 1):
                dir_path = os.path.join(self.current_dir, dir_name)
                item_count = self.count_items(dir_path)
                print(f"  [{i}] {dir_name}/ ({item_count} items)")
        else:
            print("  (No subdirectories)")
        
        if files:
            print(f"\n📄 FILES ({len(files)} files, not shown)")
        print()
    
    def count_items(self, directory):
        """Count items in a directory"""
        try:
            items = os.listdir(directory)
            # Filter out excluded items
            items = [item for item in items 
                    if not item.startswith('.') 
                    and item not in self.excluded_dirs]
            return len(items)
        except:
            return 0
    
    def navigate_to_parent(self):
        """Navigate to parent directory"""
        parent = self.current_dir.parent
        if parent != self.current_dir:  # Prevent infinite loop at root
            self.history.append(self.current_dir)
            self.current_dir = parent
            return True
        return False
    
    def navigate_to_subdirectory(self, dir_name):
        """Navigate to a subdirectory"""
        new_path = os.path.join(self.current_dir, dir_name)
        if os.path.isdir(new_path):
            self.history.append(self.current_dir)
            self.current_dir = Path(new_path)
            return True
        return False
    
    def go_back(self):
        """Go back in history"""
        if self.history:
            self.current_dir = self.history.pop()
            return True
        return False
    
    def show_help(self):
        """Show help menu"""
        print("\n" + "=" * 60)
        print("📖 HELP MENU")
        print("=" * 60)
        print("  Navigation:")
        print("    [number]  - Enter directory by number")
        print("    p         - Go to parent directory")
        print("    b         - Go back in history")
        print("    h         - Go to home directory")
        print("    r         - Go to project root")
        
        print("\n  Actions:")
        print("    s         - Select current directory")
        print("    t         - Toggle tree view")
        print("    d         - Toggle detailed view")
        print("    +         - Increase tree depth")
        print("    -         - Decrease tree depth")
        
        print("\n  Information:")
        print("    i         - Show directory info")
        print("    ?         - Show this help")
        
        print("\n  System:")
        print("    q         - Quit without selecting")
        print("    x         - Exit and use selected directory")
        print("=" * 60)
        input("\nPress Enter to continue...")
    
    def show_dir_info(self):
        """Show information about current directory"""
        print("\n" + "=" * 60)
        print(f"📊 DIRECTORY INFO: {self.current_dir}")
        print("=" * 60)
        
        try:
            # Count items
            all_items = os.listdir(self.current_dir)
            dirs = [item for item in all_items 
                   if os.path.isdir(os.path.join(self.current_dir, item))]
            files = [item for item in all_items 
                    if os.path.isfile(os.path.join(self.current_dir, item))]
            
            # Calculate size
            total_size = 0
            for item in all_items:
                item_path = os.path.join(self.current_dir, item)
                try:
                    if os.path.isfile(item_path):
                        total_size += os.path.getsize(item_path)
                except:
                    pass
            
            print(f"  Path: {self.current_dir}")
            print(f"  Type: {'Project Root' if len(self.history) == 0 else 'Subdirectory'}")
            print(f"  Directories: {len(dirs)}")
            print(f"  Files: {len(files)}")
            print(f"  Total items: {len(all_items)}")
            print(f"  Approx. size: {self.format_size(total_size)}")
            print(f"  Permission: {'Readable' if os.access(self.current_dir, os.R_OK) else 'Not readable'}")
            
            # Check if it's a Python package
            init_py = os.path.join(self.current_dir, '__init__.py')
            if os.path.exists(init_py):
                print(f"  Python package: ✓ (has __init__.py)")
            elif any(f.endswith('.py') for f in files):
                print(f"  Python package: ⚠ (has .py files but no __init__.py)")
            
        except Exception as e:
            print(f"  Error getting info: {e}")
        
        print("=" * 60)
        input("\nPress Enter to continue...")
    
    def format_size(self, size):
        """Format file size in human-readable format"""
        for unit in ['B', 'KB', 'MB', 'GB']:
            if size < 1024.0:
                return f"{size:.1f} {unit}"
            size /= 1024.0
        return f"{size:.1f} TB"
    
    def get_user_choice(self):
        """Get user input choice"""
        try:
            choice = input("\n👉 Enter choice: ").strip().lower()
            return choice
        except KeyboardInterrupt:
            return 'q'
        except:
            return ''
    
    def main_loop(self):
        """Main interactive loop"""
        tree_view = True
        detailed_view = False
        tree_depth = 3
        
        while True:
            self.clear_screen()
            self.print_header()
            self.print_current_path()
            
            if tree_view:
                print("🌳 DIRECTORY TREE:")
                print("-" * 40)
                self.print_tree(max_depth=tree_depth)
                print()
            
            if detailed_view:
                self.print_detailed_list()
            elif not tree_view:
                dirs, files = self.get_directory_contents(self.current_dir)
                if dirs:
                    print("📂 DIRECTORIES:")
                    print("-" * 40)
                    for i, dir_name in enumerate(dirs, 1):
                        print(f"  [{i}] {dir_name}/")
                    print()
            
            print("🔧 COMMANDS: [1-9] | p=parent | b=back | s=select | ?=help | q=quit")
            
            choice = self.get_user_choice()
            
            # Navigation by number
            if choice.isdigit():
                dirs, _ = self.get_directory_contents(self.current_dir)
                index = int(choice) - 1
                if 0 <= index < len(dirs):
                    self.navigate_to_subdirectory(dirs[index])
                else:
                    print(f"❌ Invalid selection: {choice}")
                    input("Press Enter to continue...")
            
            # Command processing
            elif choice == 'p':  # Parent
                if not self.navigate_to_parent():
                    print("⚠️  Already at root directory")
                    input("Press Enter to continue...")
            
            elif choice == 'b':  # Back
                if not self.go_back():
                    print("⚠️  No history to go back to")
                    input("Press Enter to continue...")
            
            elif choice == 'h':  # Home
                self.history.append(self.current_dir)
                self.current_dir = Path.home()
            
            elif choice == 'r':  # Root (where script started)
                if self.history:
                    self.current_dir = self.history[0]
                    self.history = []
            
            elif choice == 's':  # Select
                self.selected_dir = self.current_dir
                return True
            
            elif choice == 't':  # Toggle tree view
                tree_view = not tree_view
            
            elif choice == 'd':  # Toggle detailed view
                detailed_view = not detailed_view
            
            elif choice == '+':  # Increase tree depth
                tree_depth = min(tree_depth + 1, 10)
                print(f"✅ Tree depth increased to {tree_depth}")
            
            elif choice == '-':  # Decrease tree depth
                tree_depth = max(tree_depth - 1, 1)
                print(f"✅ Tree depth decreased to {tree_depth}")
            
            elif choice == 'i':  # Info
                self.show_dir_info()
            
            elif choice == '?':  # Help
                self.show_help()
            
            elif choice == 'x':  # Exit with selection
                if self.selected_dir:
                    return True
                else:
                    print("⚠️  No directory selected yet. Use 's' to select first.")
                    input("Press Enter to continue...")
            
            elif choice == 'q':  # Quit
                return False
            
            elif choice:  # Invalid command
                print(f"❌ Unknown command: '{choice}'")
                print("Type '?' for help")
                input("Press Enter to continue...")
    
    def run(self):
        """Run the directory explorer"""
        try:
            if self.main_loop():
                if self.selected_dir:
                    print(f"\n✅ Selected directory: {self.selected_dir}")
                    
                    # Ask for action
                    print("\nChoose action:")
                    print("  1. Copy path to clipboard")
                    print("  2. Open in file explorer")
                    print("  3. Print path only")
                    print("  4. Do nothing")
                    
                    action = input("\n👉 Select action (1-4): ").strip()
                    
                    if action == '1':
                        self.copy_to_clipboard(str(self.selected_dir))
                        print("📋 Path copied to clipboard!")
                    elif action == '2':
                        self.open_in_explorer(self.selected_dir)
                        print("📂 Opening in file explorer...")
                    elif action == '3':
                        print(f"\n📁 Path: {self.selected_dir}")
                    
                    input("\nPress Enter to exit...")
                
                return self.selected_dir
            return None
            
        except KeyboardInterrupt:
            print("\n\n👋 Operation cancelled by user.")
            return None
        except Exception as e:
            print(f"\n❌ Error: {e}")
            input("\nPress Enter to exit...")
            return None
    
    def copy_to_clipboard(self, text):
        """Copy text to clipboard"""
        try:
            if platform.system() == 'Windows':
                import pyperclip
                pyperclip.copy(text)
            else:
                import subprocess
                subprocess.run(['pbcopy' if platform.system() == 'Darwin' else 'xclip', '-selection', 'clipboard'], 
                             input=text.encode(), check=True)
        except:
            print("⚠️  Could not copy to clipboard. Install pyperclip: pip install pyperclip")
    
    def open_in_explorer(self, path):
        """Open directory in file explorer"""
        try:
            if platform.system() == 'Windows':
                os.startfile(path)
            elif platform.system() == 'Darwin':
                os.system(f'open "{path}"')
            else:  # Linux
                os.system(f'xdg-open "{path}"')
        except:
            print("⚠️  Could not open file explorer")

def main():
    """Main entry point"""
    explorer = DirectoryExplorer()
    result = explorer.run()
    
    if result:
        print(f"\n🎯 Final selection: {result}")
    else:
        print("\n👋 No directory selected.")

if __name__ == "__main__":
    main()
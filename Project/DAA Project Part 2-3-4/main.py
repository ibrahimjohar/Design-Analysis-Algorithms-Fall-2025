#DAA Project - Divide and Conquer Algorithms Analyzer
#Group Members: Syed Ukkashah (23K-0055), Ibrahim Johar (23K-0074), Amna Asim (23K-0859)
#BAI-5A

from gui import DivideConquerGUI
import tkinter as tk
import os

def main():
    #creating datasets directory if it doesnt exist
    if not os.path.exists("datasets"):
        os.makedirs("datasets")
        print("Created 'datasets' directory")
    
    root = tk.Tk()
    app = DivideConquerGUI(root)
    
    print("=" * 60)
    print("Divide and Conquer Algorithms Application")
    print("=" * 60)
    print("features:")
    print("  • modern dark theme UI")
    print("  • enhanced visualizations")
    print("  • real-time progress indicators")
    print("  • better organization and styling")
    print("=" * 60)
    
    root.mainloop()

if __name__ == "__main__":

    main()

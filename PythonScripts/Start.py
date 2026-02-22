import subprocess
import time
import sys
import os

def launch_symboly():
    # Get the directory where Start.py lives
    base_dir = os.path.dirname(os.path.abspath(__file__))
    
    print("🚀 Symboly System Starting...")

    # 1. Start Recorder (The Brain)
    # This now uses Data.py internally to manage logs
    print("-> Launching Recorder...")
    recorder_path = os.path.join(base_dir, "Recorder.py")
    recorder = subprocess.Popen([sys.executable, recorder_path])

    # 2. Start Graph (The Server)
    print("-> Launching Graph Server...")
    graph_path = os.path.join(base_dir, "Graph.py")
    graph = subprocess.Popen([sys.executable, graph_path])

    # Wait for Dash server to initialize (8050)
    print("-> Waiting for server to stabilize...")
    time.sleep(6) 

    # 3. Start Overlay (The HUD)
    print("-> Launching HUD Overlay...")
    overlay_path = os.path.join(base_dir, "Overlay.py")
    overlay = subprocess.Popen([sys.executable, overlay_path])

    print("\n✅ SYMBOLY ACTIVE")
    print("Graph: http://127.0.0.1:8050")
    print("Data logs saved in /data_logs")

    try:
        overlay.wait()
    except KeyboardInterrupt:
        print("\n🛑 Shutdown signal received...")
    finally:
        # We don't need to do anything extra here because 
        # Overlay.py's closeEvent handles the save!
        
        print("📸 Saving final graph snapshot...")
        # (Optional: If you want to force the save from here, 
        # you'd need to send a signal, but closeEvent is simpler!)
        
        recorder.terminate()
        graph.terminate()
        overlay.terminate()
        print("👋 Symboly session archived. Goodbye!")

if __name__ == "__main__":
    launch_symboly()
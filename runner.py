import subprocess
import time
import os


# Path to your venv Python
VENV_PYTHON = os.path.join(os.getcwd(), ".venv", "Scripts", "python.exe")

def run_producer():
    return subprocess.Popen([VENV_PYTHON, "Producer\\producer.py"])

def run_consumer():
    return subprocess.Popen([VENV_PYTHON, "Consumer\\consumer.py"])

def main():
    print("Starting producer...")
    producer_proc = run_producer()

    # Wait 10 seconds before starting consumer
    time.sleep(10)

    print("Starting consumer...")
    consumer_proc = run_consumer()

    # Keep both running, wait for them to finish
    try:
        producer_proc.wait()
        consumer_proc.wait()
    except KeyboardInterrupt:
        print("Stopping processes...")
        producer_proc.terminate()
        consumer_proc.terminate()

if __name__ == "__main__":
    main()

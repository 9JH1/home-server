import subprocess

def get_ping():
    try:
        # Execute the ping command and capture the output
        result = subprocess.run(['ping', '-c', '1', 'google.com'], capture_output=True, text=True, timeout=10)
        
        # Extracting the ping time from the output
        ping_time = result.stdout.split("time=")[1].split(" ")[0]
        
        return float(ping_time)
    
    except (IndexError, subprocess.TimeoutExpired):
        return None

# Example usage
ping = get_ping()
if ping is not None:
    print("Current ping time:", ping, "ms")
else:
    print("Unable to determine ping time.")
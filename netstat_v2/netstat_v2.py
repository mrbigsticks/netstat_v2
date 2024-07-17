import subprocess

def scan_open_ports():
    try:
        # Execute netstat command to get list of listening ports
        result = subprocess.run(['netstat', '-an'], capture_output=True, text=True, timeout=10)
        
        # Check if the command ran successfully
        if result.returncode == 0:
            output_lines = result.stdout.splitlines()
            open_ports = []
            
            # Parse netstat output to find open ports
            for line in output_lines:
                if 'LISTEN' in line:  # Look for lines indicating a listening port
                    parts = line.split()
                    if len(parts) >= 4:  # Ensure there are enough parts to unpack
                        local_address = parts[3]
                        port = local_address.split(':')[-1]
                        protocol = parts[0]
                        open_ports.append((port, protocol))
            
            # Prepare output in the format suitable for output.txt
            output_data = []
            if open_ports:
                output_data.append("Open ports found:")
                for port, protocol in open_ports:
                    output_data.append(f"    Port: {port}, Protocol: {protocol}")
                output_data.append(f"Total open ports found: {len(open_ports)}")
            else:
                output_data.append("No open ports found")
            
            # Write output to output.txt
            with open('output.txt', 'w') as file:
                for line in output_data:
                    file.write(line + '\n')
            
            print("Scan results written to output.txt")

        else:
            print("Failed to execute netstat command")
    
    except subprocess.TimeoutExpired:
        print("Timeout occurred while executing netstat command")
    except Exception as e:
        print(f"An error occurred: {str(e)}")

if __name__ == "__main__":
    scan_open_ports()

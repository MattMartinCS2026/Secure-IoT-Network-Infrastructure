import socket 
import time  
import argparse

TARGET_IP = "192.168.20.11"     # stores the authorized IoT target machine's IP address
TARGET_PORT = 5000              # stores the TCP port where the target service is listening

MAX_DURATION = 120              # defines the maximum allowed test duration in seconds
MIN_INTERVAL = 0.1              # defines the shortest allowed interval between connection attempts
MAX_PAYLOAD_SIZE = 1024         # defines the largest allowed payload size in bytes


def run_test(interval, duration, payload_size):                             # runs the bounded connectivity test with validated settings
    marker = b"IOT_NETWORK_TEST_DATA"                                       # creates a repeated byte sequence to use as test payload dat
    payload = (marker * (payload_size // len(marker) + 1))[:payload_size]  # builds payload data of the requested size

    successful = 0  # counts connections that succeed
    failed = 0      # counts connections that fail
    attempts = 0    # counts every connection attempt

    print("\nStarting controlled IoT TCP connectivity test...")
    print(f"Target: {TARGET_IP}:{TARGET_PORT}") 
    print(f"Interval: {interval} seconds") 
    print(f"Duration: {duration} seconds") 
    print(f"Payload: {payload_size} bytes")
    print("Press Ctrl+C to stop.\n")  

    start_time = time.monotonic()                        # records a stable start timestamp for elapsed-time calculations

    try:                                                 # handles normal attempts and user interruption
        while time.monotonic() - start_time < duration:  # continues attempts until the requested duration has elapsed
            attempts += 1                                # increments the attempt counter before opening a connection
            try:                                         # handles each individual connection
                with socket.create_connection(           # opens a TCP connection with a one-second timeout
                    (TARGET_IP, TARGET_PORT), timeout=1  # supplies the target address and connection timeout
                ) as connection:                         # keeps the connection open in a context manager and closes it afterward
                    connection.sendall(payload)          # sends the generated test payload to the target
                    successful += 1                         # records the connection and payload send as successful
                print(f"[SUCCESS] Connection #{attempts}")  # reports this successful connection attempt

            except OSError as error:                                # handles network and socket errors without stopping the whole test
                failed += 1                                         # records this failed connection attempt
                print(f"[FAILED] Connection #{attempts}: {error}")  # reports the failed attempt and socket error

            remaining = duration - (time.monotonic() - start_time)  # calculates how much test time remains
            if remaining > 0:                                       # only waits if time remains in the test
                time.sleep(min(interval, remaining))                # sleeps for the interval, capped by the remaining duration

    except KeyboardInterrupt:                # handles the user pressing Ctrl+C while the test is running
        print("\nTest manually stopped.")    # reports that the test ended because of user interruption

    elapsed = time.monotonic() - start_time  # calculates the total elapsed test time

    print("\n========== TEST RESULTS ==========") 
    print(f"Total attempts: {attempts}")  
    print(f"Successful connections: {successful}")  
    print(f"Failed connections: {failed}") 
    print(f"Elapsed time: {elapsed:.2f} seconds")  
    if attempts:                                                                #calculates a success rate only when at least one attempt occurred
        print(f"Connection success rate: {successful / attempts * 100:.2f}%")   # displays successful attempts as a percentage
    print("==================================")  


if __name__ == "__main__":                                                          # runs this entry-point block only when the file is executed directly
    parser = argparse.ArgumentParser(                                               # creates a command-line argument parser
        description="Controlled TCP connectivity test for an authorized IoT lab"    # explains the tool's purpose in help output
    )
    parser.add_argument(                                  # adds an interval command-line option
        "--interval", type=float, default=1.0,            # parses interval as a decimal and defaults to one second
        help="Seconds between connections (minimum 0.1)"  # describes the interval option in help output
    )
    parser.add_argument(                                # adds a duration command-line option
        "--duration", type=int, default=30,             # parses duration as an integer and defaults to 30 seconds
        help="Test duration in seconds (1-120)"         # describes the duration limits in help output
    )
    parser.add_argument(                        # adds a payload command-line option
        "--payload", type=int, default=256,     # parses payload size as an integer and defaults to 256 bytes
        help="Payload size in bytes (1-1024)"   # describes the payload limits in help output
    )
    args = parser.parse_args()                  # parses command-line arguments into the args object

    if args.interval < MIN_INTERVAL:                                    # checks whether the interval is below the allowed minimum
        parser.error("Interval cannot be less than 0.1 seconds.")       # stops with an explanatory interval error
    if not 1 <= args.duration <= MAX_DURATION:                          # checks whether duration is outside the allowed range
        parser.error("Duration must be between 1 and 120 seconds.")     # stops with an explanatory duration error
    if not 1 <= args.payload <= MAX_PAYLOAD_SIZE:                       # checks whether payload size is outside the allowed range
        parser.error("Payload must be between 1 and 1024 bytes.")       # stops with an explanatory payload error

    print("Run against VM in VirtualBox environment.")                          # reminds the user to run the test in the intended environment
    if input("Type RUN to start the bounded connectivity test: ") == "RUN":     # prompts for explicit confirmation to start
        run_test(args.interval, args.duration, args.payload)                    # starts the test using the parsed and validated settings
    else:                                                       # runs when the confirmation text is not exactly "RUN"
        print("Test cancelled.")                                # reports that the test was not started

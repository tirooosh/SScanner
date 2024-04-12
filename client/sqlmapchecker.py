import subprocess


def is_vulnerable_to_sqli(url):
    command = [
        'sqlmap',
        '-u', url,
        '--batch',
        '--level', '1',
        '--risk', '3',
        '--output-dir', '/tmp',
        '--flush-session'
    ]

    try:
        # Running SQLMap with a timeout
        result = subprocess.run(command, stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True, timeout=300)

        # Check if there was any error
        if result.stderr:
            print(f"Error occurred: {result.stderr}")
            return False

        # Check the output for a successful SQL injection indication
        success_indicators = ["Parameter:", "is vulnerable", "Type:", "title:", "payload:"]
        output_lines = result.stdout.split("\n")
        for line in output_lines:
            if any(indicator in line for indicator in success_indicators):
                print("SQL Injection vulnerability detected.")
                return True

    except subprocess.TimeoutExpired:
        print("SQLMap process timed out.")
        return False
    except Exception as e:
        print(f"An exception occurred: {e}")
        return False

    print("No SQL Injection vulnerability detected.")
    return False


if __name__ == '__main__':
    url_to_test = "http://testphp.vulnweb.com/artists.php?artist=1"
    vulnerable = is_vulnerable_to_sqli(url_to_test)
    print("Vulnerable:" if vulnerable else "Not vulnerable.")

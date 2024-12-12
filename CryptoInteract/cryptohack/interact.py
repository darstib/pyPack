# interact.py
from pwn import remote
import json
import re

def challenge(port=80, host="socket.cryptohack.org"):
    """
    Establishes a connection to the specified host and port,and provides methods to send and receive JSON data.

    Args:
        port (int): The port number to connect to (default is 80).
        host (str): The hostname to connect to (default is 'socket.cryptohack.org').

    Returns:
        Interact: An instance of the Interact class for communication.
    """
    return Challenge(port, host)

class Challenge:
    """
    A class to handle interaction with the CryptoHack server.
    """

    def __init__(self, port=80, host="socket.cryptohack.org"):
        """
        Initializes the connection to the server.

        Args:
            port (int): The port number to connect to.
            host (str): The hostname to connect to.
        """
        self.rmt = remote(host, port, level="debug")
        self.rmt.recv(2048)

    def json_recv(self):
        """
        Receives a line from the server and decodes it from JSON.

        Returns:
            dict: The decoded JSON data.
        """
        line = self.rmt.readline().decode()
        return json.loads(line)

    def json_recvs(self):
        """
        Receives all remaining data from the server and extracts JSON objects.

        Returns:
            list: A list of decoded JSON objects.
        """
        lines = self.rmt.recvall(timeout=1).decode()
        return [json.loads(json_) for json_ in re.findall(r'{.*?}', lines)]

    def json_send(self, data):
        """
        Sends JSON-encoded data to the server.

        Args:
            data (dict): The data to send.
        """
        request = json.dumps(data).encode()
        self.rmt.sendline(request)

    def PoW(self, prompt=b'letters or digits):'):
        """Proof of Work for first 4 bytes of sha256"""
        resp = self.rmt.recvuntil(prompt)
        pattern = r"sha256\((.*?)\).hexdigest\(\) == ([a-f0-9]{64})"
        match = re.search(pattern, resp.decode())
        suffix = match.group(1).split("+")[1][2:-1]
        target_hash = match.group(2)
        # search all 4 bytes combinations
        chars = string.ascii_letters + string.digits
        for attempt in itertools.product(chars, repeat=4):
            prefix = "".join(attempt)
            test_str = prefix + suffix
            current_hash = hashlib.sha256(test_str.encode()).hexdigest()

            if current_hash == target_hash:
                print(f"Found match: {prefix}")
                break

        self.rmt.sendline(prefix.encode())
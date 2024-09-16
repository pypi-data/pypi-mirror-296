import argparse
from .core import s
from .encrypt import encrypt
from rgbprint import gradient_print, Color

credit = """
555555555555555555TTTTTTTTTTTTTTTTTTTTTTT
5::::::::::::::::5T:::::::::::::::::::::T
5::::::::::::::::5T:::::::::::::::::::::T
5:::::555555555555T:::::TT:::::::TT:::::T
5:::::5           TTTTTT  T:::::T  TTTTTT
5:::::5                   T:::::T        
5:::::5555555555          T:::::T        
5:::::::::::::::5         T:::::T        
555555555555:::::5        T:::::T        
            5:::::5       T:::::T        
            5:::::5       T:::::T        
5555555     5:::::5       T:::::T        
5::::::55555::::::5     TT:::::::TT      
 55:::::::::::::55      T:::::::::T      
   55:::::::::55        T:::::::::T      
     555555555          TTTTTTTTTTT      
FiveTemp Coded By Abzyms. Socials at
Youtube: @abyzmzs
Github: Abyzms-Amphetamine
"""
def create_webh(encrypted_webhook):
    return f"""
555555555555555555TTTTTTTTTTTTTTTTTTTTTTT
5::::::::::::::::5T:::::::::::::::::::::T
5::::::::::::::::5T:::::::::::::::::::::T
5:::::555555555555T:::::TT:::::::TT:::::T
5:::::5           TTTTTT  T:::::T  TTTTTT
5:::::5                   T:::::T        
5:::::5555555555          T:::::T        
5:::::::::::::::5         T:::::T        
555555555555:::::5        T:::::T        
            5:::::5       T:::::T        
            5:::::5       T:::::T        
5555555     5:::::5       T:::::T        
5::::::55555::::::5     TT:::::::TT      
 55:::::::::::::55      T:::::::::T      
   55:::::::::55        T:::::::::T      
     555555555          TTTTTTTTTTT  
Encrypted Webhook Shown Below This Msg
{encrypted_webhook}
"""

def main():
    parser = argparse.ArgumentParser(description='FiveTemp CLI')
    parser.add_argument('-w', '--webhook', help='Encrypt Your Webhook.', type=str)
    parser.add_argument('-c', '--credits', help='Show Credits.', action='store_true')
    args = parser.parse_args()

    if args.credits:
        gradient_print(credit, start_color=Color.dark_magenta, end_color=Color.blue)
    elif args.webhook:
        encrypted_webhook = encrypt(args.webhook)
        webh = create_webh(encrypted_webhook)
        gradient_print(webh, start_color=Color.dark_magenta, end_color=Color.blue)

if __name__ == "__main__":
    main()

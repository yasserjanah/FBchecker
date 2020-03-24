#!/usr/bin/env python3

__author__ = "Yasser JANAH"
__email__  = "janah.y4ss3r@gmail.com"

try:
    import argparse
    import os
    import requests
    from pwn import log
    from PIL import Image
    from bs4 import BeautifulSoup
except ImportError as err:
    print(err)

try:
    raw_input = input
except NameError:
    pass


class Fore:
    BOLD = "\033[1m"
    UNDE = "\033[4m"
    GREEN = "\033[92m"
    BLUE = "\033[94m"
    YELLOW = "\033[93m"
    RED = "\033[91m"
    WHITE = "\033[0m"
    CYAN = "\033[0;36m"


def show_img(img):
    im = Image.open(img)
    im.show()


def is_valid(email_or_num, p):
    URL = "https://mbasic.facebook.com/login/identify/?ctx=recover"  # URL
    payload = {'lsd': 'AVpNLmOr', 'charset_test': '€,´,€,´,水,Д,Є',
               'email': email_or_num, 'did_submit': 'Search'}  # Post Data
    found = False
    img_link = False
    req = requests.post(URL, data=payload)  # send post request
    if req.status_code == 200:
        whitelist = ['Reset Your Password', 'Not my account','votre mot de passe', 'Envoyer le code par e-mail']
        for w in whitelist:
            if w in req.content.decode('utf-8'):
                found = True
        if found:
            soup = BeautifulSoup(req.content.decode(
                'utf-8'), 'html.parser')  # parse html result
            #print(soup.findAll('div', {'class': 'p v w'}), soup.findAll('strong'), ' | found : ', w)
            #open('index.html', 'w').write(req.content.decode('utf-8'))
            try:
                name = soup.findAll('strong')[0].text  # get name of account
            except IndexError:
                name = soup.findAll('div', {'class': 'p v w'})[0].text
            # default value of img is 50x50 , but for best practice i download image 500x500
            img_links = soup.findAll('img')  # [1]['src'][:-2]+"300"
            for i in img_links:
                if "profile" in i['src']:
                    img_link = i['src'][:-2]+"500"
            img_path = "recent_search/" + \
                name.replace(' ', '-')+"__"+email_or_num+"_.jpg"
            img_data = requests.get(img_link).content if (
                img_link != False) else 0
            if img_data != 0:
                img = open(img_path, mode="wb")
                img.write(img_data)
                img.close()
            p.success(Fore.GREEN+'done.'+Fore.WHITE)
            log.success("Found Name : "+Fore.BOLD+Fore.GREEN+name+Fore.WHITE)
            try:
                emails = soup.findAll('div', {'class':'bi bj'})
                if len(emails) != 0:
                    log.success("Found user emails or numbers :")
                    for i in emails:
                        print('\t\t'+Fore.YELLOW+i.text+Fore.WHITE)
            except Exception as err:
                print(err)
            if img_data != 0:
                log.success("Profile image Saved in : "+Fore.YELLOW+"'"+Fore.CYAN + \
                            Fore.BOLD+img_path+Fore.YELLOW+"'"+Fore.WHITE)
                ask = raw_input(Fore.GREEN+'['+Fore.WHITE+'+'+Fore.GREEN+']'+Fore.WHITE+' do you want to display profile image ? [Y/n] ')
                if ((ask.lower() == 'y') or (ask.lower() == '')):
                    show_img(img_path)
        else:
            p.failure(Fore.RED+'done.'+Fore.WHITE)
            log.failure(Fore.RED+"no user is associated with " +
                        Fore.BOLD+Fore.YELLOW+email_or_num+Fore.WHITE+".")
    else:
        log.failure("something is wrong , check your internet connection !")

def _print_help():
    print(Fore.BOLD+Fore.YELLOW+"\nUsage: "+Fore.WHITE+f"python -id/--id {Fore.BOLD}<{Fore.WHITE}{Fore.CYAN}Email{Fore.WHITE}{Fore.BOLD}>{Fore.RED}/{Fore.WHITE}<{Fore.CYAN}Number{Fore.WHITE}{Fore.BOLD}>{Fore.WHITE}")
    print(Fore.WHITE+'\n\t\033[1m\033[4mOptions\033[0m:')
    print(Fore.WHITE+'\t\t-id\t--id\t\tEmail '+Fore.RED+Fore.BOLD+'OR'+Fore.WHITE+' Number.\n')

def main():
    if not os.path.isdir('recent_search'):
        os.mkdir('recent_search')
    parser = argparse.ArgumentParser()
    parser.print_help = _print_help
    parser.add_argument(
        '-id', '--id', help='', type=str, required=True)
    args = parser.parse_args()
    p = log.progress("Searching using "+Fore.YELLOW+args.id+Fore.WHITE+" ")
    is_valid(args.id, p)


if __name__ == '__main__':
    try:
        main()
    except IndexError:
    	main()
    except KeyboardInterrupt:
        exit()
    except Exception as mainerr:
        raise(mainerr)

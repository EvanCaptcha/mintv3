import requests
import time
import cfscrape
import threading
import names
import random
from random import randint
import string
from discord_webhook import DiscordWebhook, DiscordEmbed

#USmint bot V3 lets gooooo


def atc(ses, pid):
    completeAtc = False
    while not completeAtc:
        print("Adding to cart...")
        headers = {
            'User-Agent': 'Mozilla/5.0 (X11; Linux x86_64; rv:68.0) Gecko/20100101 Firefox/68.0',
            'Accept': '*/*',
            'Accept-Language': 'en-US,en;q=0.5',
            'Referer': 'https://catalog.usmint.gov/proof-set-2020-20RG.html?cgid=bestsellers',
            'Content-Type': 'application/x-www-form-urlencoded; charset=UTF-8',
            'X-Requested-With': 'XMLHttpRequest',
            'Connection': 'keep-alive',
            'TE': 'Trailers',
        }

        params = (
            ('format', 'ajax'),
        )

        data = {
            'cartAction': 'add',
            'pid': f'{pid}',
            'cgid': 'bestsellers',
            'egc': 'null',
            'navid': '',
            'personalizationSelected': '',
            'personalizationColor': '',
            'personalizationMessage': '',
            'personalizationFont': '',
            'Quantity': '1'
        }
        response = ses.post('https://catalog.usmint.gov/on/demandware.store/Sites-USM-Site/default/Cart-AddProduct', headers=headers, params=params, data=data)
        try:
            if response.text.split('"productid_cart","')[1].split('"]);')[0] == pid:
                completeAtc = True
        except:
            print("ATC error... Retrying")
            time.sleep(1)
            pass

def validate(ses):
    print("Validating cart limit... ")
    headers = {
        'User-Agent': 'Mozilla/5.0 (X11; Linux x86_64; rv:68.0) Gecko/20100101 Firefox/68.0',
        'Accept': 'application/json, text/javascript, */*; q=0.01',
        'Accept-Language': 'en-US,en;q=0.5',
        'Referer': 'https://catalog.usmint.gov/on/demandware.store/Sites-USM-Site/default/Cart-Show',
        'X-Requested-With': 'XMLHttpRequest',
        'Connection': 'keep-alive',
        'TE': 'Trailers',
    }

    response = ses.get('https://catalog.usmint.gov/on/demandware.store/Sites-USM-Site/default/Cart-ValidateBulkLimit', headers=headers)
    return response.text

def getValues(ses):
    print('Scraping values...')
    res = ses.get('https://catalog.usmint.gov/on/demandware.store/Sites-USM-Site/default/Cart-Show')
    billSecure = res.text.split('<input type="hidden" name="dwfrm_billing_securekey" value="')[1].split('"/>')[0]
    shipSecure = res.text.split('<input type="hidden" name="dwfrm_singleshipping_securekey" value="')[1].split('"/>')[0]
    cartId = res.text.split('<form action="https://catalog.usmint.gov/on/demandware.store/Sites-USM-Site/default/Cart-Show/')[1].split('"')[0]
    return [billSecure, shipSecure, cartId]
def setInfo1(ses, billSecure, shipSecure, cartId, fName, lName, addy, phone, email):

    print("Setting address..")
    headers = {
        'User-Agent': 'Mozilla/5.0 (X11; Linux x86_64; rv:68.0) Gecko/20100101 Firefox/68.0',
        'Accept': 'application/json, text/javascript, */*; q=0.01',
        'Accept-Language': 'en-US,en;q=0.5',
        'Referer': 'https://catalog.usmint.gov/on/demandware.store/Sites-USM-Site/default/Cart-Show',
        'X-Requested-With': 'XMLHttpRequest',
        'Connection': 'keep-alive',
        'TE': 'Trailers',
    }

    params = (
        ('avsdata',
         '{"firstname":"' + fName + '","lastname":"' + lName + '","address1":"' + addy + '","address2":"","city":"Chappaqua","postalCode":"10514","state":"NY","country":"US"}'),
    )

    response = ses.get('https://catalog.usmint.gov/on/demandware.store/Sites-USM-Site/default/AVS-ajax', headers=headers, params=params)
    data = {
        'dwfrm_singleshipping_shippingAddress_addressFields_selectedAddressID': 'newaddress',
        'dwfrm_singleshipping_shippingAddress_addressFields_firstName': f'{fName}',
        'dwfrm_singleshipping_shippingAddress_addressFields_lastName': f'{lName}',
        'dwfrm_singleshipping_shippingAddress_addressFields_phone': f'{phone}',
        'dwfrm_singleshipping_shippingAddress_email': f'{email}',
        'dwfrm_billing_billingAddress_emailsource': 'Website - Checkout',
        'dwfrm_singleshipping_shippingAddress_addressFields_address1': f'{addy}',
        'dwfrm_singleshipping_shippingAddress_addressFields_address2': '',
        'dwfrm_singleshipping_shippingAddress_addressFields_city': 'CHAPPAQUA',
        'dwfrm_singleshipping_shippingAddress_addressFields_states_state': 'NY',
        'dwfrm_singleshipping_shippingAddress_addressFields_zip': '10514-1409',
        'dwfrm_singleshipping_shippingAddress_addressFields_country': 'US',
        'dwfrm_singleshipping_shippingAddress_isCreateAccountSelected': 'false',
        'dwfrm_singleshipping_createAccount_password': '',
        'dwfrm_singleshipping_createAccount_passwordconfirm': '',
        'dwfrm_singleshipping_createAccount_question': '1',
        'dwfrm_singleshipping_createAccount_answer': '',
        'dwfrm_singleshipping_securekey': f'{shipSecure}',
        'dwfrm_billing_securekey': f'{billSecure}',
        'format': 'ajax',
        'refresh': 'shipping',
        'dwfrm_singleshipping_shippingAddress_applyShippingAddress': ''
    }

    response = ses.post(f'https://catalog.usmint.gov/on/demandware.store/Sites-USM-Site/default/COSummary-Submit/{cartId}',headers=headers, data=data)


def setCardBill(ses, billSecure, shipSecure, cartId, fName, lName, addy, phone, email):
    print("Setting card and billing...")
    headers = {
        'User-Agent': 'Mozilla/5.0 (X11; Linux x86_64; rv:68.0) Gecko/20100101 Firefox/68.0',
        'Accept': 'text/html, */*; q=0.01',
        'Accept-Language': 'en-US,en;q=0.5',
        'Referer': 'https://catalog.usmint.gov/on/demandware.store/Sites-USM-Site/default/Cart-Show',
        'Content-Type': 'application/x-www-form-urlencoded; charset=UTF-8',
        'X-Requested-With': 'XMLHttpRequest',
        'Connection': 'keep-alive',
        'TE': 'Trailers',
    }

    data = [
        ('dwfrm_singleshipping_shippingAddress_useAsBillingAddress', 'true'),
        ('dwfrm_billing_billingAddress_addressFields_selectedAddressID', ''),
        ('dwfrm_billing_billingAddress_addressFields_firstName', f'{fName}'),
        ('dwfrm_billing_billingAddress_addressFields_lastName', f'{lName}'),
        ('dwfrm_billing_billingAddress_addressFields_address1', f'{addy}'),
        ('dwfrm_billing_billingAddress_addressFields_address2', ''),
        ('dwfrm_billing_billingAddress_addressFields_city', 'CHAPPAQUA'),
        ('dwfrm_billing_billingAddress_addressFields_states_state', 'NY'),
        ('dwfrm_billing_billingAddress_addressFields_zip', '10514-1409'),
        ('dwfrm_billing_billingAddress_addressFields_country', 'US'),
        ('dwfrm_billing_billingAddress_addressFields_phone', f'{phone}'),
        ('dwfrm_billing_billingAddress_email_emailAddress', f'{email}'),
        ('dwfrm_billing_securekey', f'{billSecure}'),
        ('dwfrm_billing_securekey', f'{billSecure}'),
        ('dwfrm_singleshipping_securekey', f'{shipSecure}'),
        ('refresh', 'payment'),
        ('format', 'ajax'),
        ('dwfrm_billing_applyBillingAndPayment', ''),
        ('dwfrm_billing_paymentMethods_selectedPaymentMethodID', 'CREDIT_CARD'),
        ('dwfrm_billing_paymentMethods_creditCard_type', 'Amex'),
        ('dwfrm_billing_paymentMethods_creditCard_owner', 'Evan Wohl'),
        ('dwfrm_billing_paymentMethods_creditCard_number', '373868251595525'),
        ('dwfrm_billing_paymentMethods_creditCard_month', '10'),
        ('dwfrm_billing_paymentMethods_creditCard_year', '2026'),
        ('dwfrm_billing_paymentMethods_creditCard_cvn', '9417'),
        ('dwfrm_emailsignup_phone', ''),
    ]

    response = ses.post(f'https://catalog.usmint.gov/on/demandware.store/Sites-USM-Site/default/Cart-Show/{cartId}', headers=headers, data=data)
    headers = {
        'User-Agent': 'Mozilla/5.0 (X11; Linux x86_64; rv:68.0) Gecko/20100101 Firefox/68.0',
        'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8',
        'Accept-Language': 'en-US,en;q=0.5',
        'Referer': 'https://catalog.usmint.gov/on/demandware.store/Sites-USM-Site/default/Cart-Show',
        'Content-Type': 'application/x-www-form-urlencoded',
        'Connection': 'keep-alive',
        'Upgrade-Insecure-Requests': '1',
        'TE': 'Trailers',
    }

    data = {
        'dwfrm_billing_paymentMethods_selectedPaymentMethodID': 'CREDIT_CARD',
        'dwfrm_billing_paymentMethods_creditCard_type': 'Amex',
        'dwfrm_billing_paymentMethods_creditCard_owner': 'Evan Wohl',
        'dwfrm_billing_paymentMethods_creditCard_number': '*'*11 + '5525',
        'dwfrm_billing_paymentMethods_creditCard_month': '10',
        'dwfrm_billing_paymentMethods_creditCard_year': '2026',
        'dwfrm_billing_paymentMethods_creditCard_cvn': '****',
        'dwfrm_billing_securekey': f'{billSecure}',
        'dwfrm_emailsignup_phone': ''
    }
    print("Attempting checking out...")
    checkedOut = False
    while not checkedOut:
        response = ses.post('https://catalog.usmint.gov/on/demandware.store/Sites-USM-Site/default/COSummary-Submit', headers=headers, data=data)
        if 'We are sorry, but we are unable to process your payment and submit your order this time' in response.text:
            print("Error checking out... trying again.")
            time.sleep(2.5)
        elif 'Thank you for your order' in response.text:
            print("Possible successful checkout!")
            file = open('checkouts.txt', 'a')
            webhook = DiscordWebhook(url='https://discord.com/api/webhooks/772848524437487667/xj3K-_QD3iaOaDAUCnEbpv4zraPJkckjMf71FArHEYcNqc4aLEi-5xEW_uMub8nI5RmZ')
            # create embed object for webhook
            orderNum = 'USM' + response.text.split('<span class="value">USM')[1].split('</span>')[0]
            file.write(email + ':' + orderNum + '\n')
            embed = DiscordEmbed(title='evxn.net | USMint V3', description=f'Succesful checkout logged. \nOrder Number: ' + orderNum + '\nEmail used: ' + email, color=242424)
            embed.set_footer(text='Programmed in Python by Evan')
            # add embed object to webhook
            webhook.add_embed(embed)
            webhook.execute()
            checkedOut = True
        else:
            line = random.choice(open('proxies.txt').readlines()).replace('\n', "")
            IP = line.split(":")[0]
            port = line.split(":")[1]
            proxies = {'https': f'https://{IP}:{port}'}
            ses.proxies.update(proxies)

def monitor(pid):
    webhook = DiscordWebhook(url='https://discord.com/api/webhooks/772848524437487667/xj3K-_QD3iaOaDAUCnEbpv4zraPJkckjMf71FArHEYcNqc4aLEi-5xEW_uMub8nI5RmZ')
    print("Monitoring " + pid + "...")
    response = requests.get(f"https://catalog.usmint.gov/on/demandware.store/Sites-USM-Site/default/Product-GetAvailability?pid={pid}")
    json = response.json()
    while json['status'] == 'NOT_AVAILABLE':
        print("Monitoring...")
        json = requests.get(f"https://catalog.usmint.gov/on/demandware.store/Sites-USM-Site/default/Product-GetAvailability?pid={pid}").json()
    else:
        print("Stock detected on product " + pid + " is " + json['ats'])
        # create embed object for webhook
        embed = DiscordEmbed(title='evxn.net | USMint V3', description=f'Stock detected on product ' + pid + ": " + json['ats'], color=242424)
        embed.set_footer(text='Programmed in Python by Evan')
        # add embed object to webhook
        webhook.add_embed(embed)
        webhook.execute()
def task(pid):
    while True:
        try:
            ses = requests.session()
            addyNum = '21'
            addyStreet = 'Quaker Lane'

            def random_string_generator(str_size, allowed_chars):
                return ''.join(random.choice(allowed_chars) for x in range(str_size))
            chars = string.ascii_letters
            jig = random_string_generator(3, chars)
            addy = addyNum + ' ' + jig.upper() + ' ' + addyStreet
            def random_with_N_digits(n):
                range_start = 10 ** (n - 1)
                range_end = (10 ** n) - 1
                return randint(range_start, range_end)
            fName = names.get_first_name(gender='male')
            phone = random_with_N_digits(10)
            lName = names.get_last_name()
            s = cfscrape.create_scraper(ses)
            line = random.choice(open('proxies.txt').readlines()).replace('\n', "")
            IP = line.split(":")[0]
            port = line.split(":")[1]
            proxies = {'https': f'https://{IP}:{port}'}
            s.proxies.update(proxies)
            atc(s, pid)
            values = getValues(s)
            billSecure = values[0]
            shipSecure = values[1]
            cartID = values[2]
            domains = ['@1secmail.com', '@1secmail.net', '@esiix.com', '@wwjmp.com']
            email = random_string_generator(7, chars).lower() + domains[randint(0, 3)]
            setInfo1(s, billSecure, shipSecure, cartID, fName, lName, addy, phone, email)
            setCardBill(s, billSecure, shipSecure, cartID, fName, lName, addy, phone, email)
        except:
            print("An error was encountered during the checkout process. It has been restarted and will be bruteforced until success.")
            pass

def main():
    pid = input("What is the PID of the product?\n")
    threads = input("How many threads do you want to run?\n")
    monitor(pid)
    jobs = []
    for i in range(0, int(threads)):
        t = jobs.append(threading.Thread(target=task, args=(pid,)))

    # start  threads
    for j in jobs:
        j.start()

if __name__ == '__main__':
    main()

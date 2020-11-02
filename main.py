import requests
import time
import cfscrape
import threading
from multiprocessing import Process
import os

#USmint bot V3 lets gooooo
def atc(ses, pid):
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

def validate(ses):
    print("Validating cart limit...")
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
def setInfo1(ses):
    global cartId
    global billSecure
    global shipSecure
    print('Scraping values...')
    res = ses.get('https://catalog.usmint.gov/on/demandware.store/Sites-USM-Site/default/Cart-Show')
    billSecure = res.text.split('<input type="hidden" name="dwfrm_billing_securekey" value="')[1].split('"/>')[0]
    shipSecure = res.text.split('<input type="hidden" name="dwfrm_singleshipping_securekey" value="')[1].split('"/>')[0]
    cartId = res.text.split('<form action="https://catalog.usmint.gov/on/demandware.store/Sites-USM-Site/default/Cart-Show/')[1].split('"')[0]
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
         '{"firstname":"Evan","lastname":"Wohl","address1":"21 QUAKER LANE","address2":"","city":"Chappaqua","postalCode":"10514","state":"NY","country":"US"}'),
    )

    response = ses.get('https://catalog.usmint.gov/on/demandware.store/Sites-USM-Site/default/AVS-ajax', headers=headers, params=params)
    data = {
        'dwfrm_singleshipping_shippingAddress_addressFields_selectedAddressID': 'newaddress',
        'dwfrm_singleshipping_shippingAddress_addressFields_firstName': 'Evan',
        'dwfrm_singleshipping_shippingAddress_addressFields_lastName': 'Wohl',
        'dwfrm_singleshipping_shippingAddress_addressFields_phone': '6465816354',
        'dwfrm_singleshipping_shippingAddress_email': 'evstwo@gmail.com',
        'dwfrm_billing_billingAddress_emailsource': 'Website - Checkout',
        'dwfrm_singleshipping_shippingAddress_addressFields_address1': '21 QUAKER LN',
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


def setCardBill(ses):
    global checkedOut
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
        ('dwfrm_billing_billingAddress_addressFields_firstName', 'Evan'),
        ('dwfrm_billing_billingAddress_addressFields_lastName', 'Wohl'),
        ('dwfrm_billing_billingAddress_addressFields_address1', '21 QUAKER LN'),
        ('dwfrm_billing_billingAddress_addressFields_address2', ''),
        ('dwfrm_billing_billingAddress_addressFields_city', 'CHAPPAQUA'),
        ('dwfrm_billing_billingAddress_addressFields_states_state', 'NY'),
        ('dwfrm_billing_billingAddress_addressFields_zip', '10514-1409'),
        ('dwfrm_billing_billingAddress_addressFields_country', 'US'),
        ('dwfrm_billing_billingAddress_addressFields_phone', '6465816354'),
        ('dwfrm_billing_billingAddress_email_emailAddress', 'evstwo@gmail.com'),
        ('dwfrm_billing_securekey', f'{billSecure}'),
        ('dwfrm_billing_securekey', f'{billSecure}'),
        ('dwfrm_singleshipping_securekey', f'{shipSecure}'),
        ('refresh', 'payment'),
        ('format', 'ajax'),
        ('dwfrm_billing_applyBillingAndPayment', ''),
        ('dwfrm_billing_paymentMethods_selectedPaymentMethodID', 'CREDIT_CARD'),
        ('dwfrm_billing_paymentMethods_creditCard_type', 'Visa'),
        ('dwfrm_billing_paymentMethods_creditCard_owner', 'Evan Wohl'),
        ('dwfrm_billing_paymentMethods_creditCard_number', '4767718396533285'),
        ('dwfrm_billing_paymentMethods_creditCard_month', '10'),
        ('dwfrm_billing_paymentMethods_creditCard_year', '2026'),
        ('dwfrm_billing_paymentMethods_creditCard_cvn', '941'),
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
        'dwfrm_billing_paymentMethods_creditCard_type': 'Visa',
        'dwfrm_billing_paymentMethods_creditCard_owner': 'Evan Wohl',
        'dwfrm_billing_paymentMethods_creditCard_number': '************3285',
        'dwfrm_billing_paymentMethods_creditCard_month': '10',
        'dwfrm_billing_paymentMethods_creditCard_year': '2026',
        'dwfrm_billing_paymentMethods_creditCard_cvn': '***',
        'dwfrm_billing_securekey': f'{billSecure}',
        'dwfrm_emailsignup_phone': ''
    }
    print("Attempting checking out...")
    while not checkedOut:
        response = ses.post('https://catalog.usmint.gov/on/demandware.store/Sites-USM-Site/default/COSummary-Submit', headers=headers, data=data)
        if not 'Thank you for your order.' in response.text:
            print("Error checking out... trying again.")
        else:
            print("Possible successful checkout!")
            checkedOut = True

def monitor(pid):
    print("Monitoring " + pid + "...")
    response = requests.get(f"https://catalog.usmint.gov/on/demandware.store/Sites-USM-Site/default/Product-GetAvailability?pid={pid}")
    json = response.json()
    while json['status'] == 'NOT_AVAILABLE':
        print("Monitoring...")
        json = requests.get(f"https://catalog.usmint.gov/on/demandware.store/Sites-USM-Site/default/Product-GetAvailability?pid={pid}").json()
    else:
        print("Stock detected on product " + pid + " is " + json['ats'])
def task(pid):
    global checkedOut
    checkedOut = False
    while not checkedOut:
        try:
            start = time.time()
            ses = requests.session()
            s = cfscrape.create_scraper(ses)
            atc(s, pid)
            print(validate(s))
            setInfo1(s)
            setCardBill(s)
            end = time.time()
            print("Task completed in " + str(end - start))
        except:
            print("An error was encountered during the checkout process. It has been restarted and will be bruteforced until success.")
            pass
if __name__ == '__main__':
    pid = '20RG'
    monitor(pid)
    jobs = []
    threads = 5
    for i in range(0, int(threads)):
        jobs.append(threading.Thread(target=task(pid)))

    # start  threads
    for j in jobs:
        j.start()

    # ensure all threads have been finished
    for j in jobs:
        j.join()

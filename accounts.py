import requests
import cfscrape

def getValues(ses):
    global emailSecure
    global profileSecure
    global cartId
    headers = {
        'User-Agent': 'Mozilla/5.0 (X11; Linux x86_64; rv:68.0) Gecko/20100101 Firefox/68.0',
        'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8',
        'Accept-Language': 'en-US,en;q=0.5',
        'Referer': 'https://catalog.usmint.gov/account-login',
        'Connection': 'keep-alive',
        'Upgrade-Insecure-Requests': '1',
        'Cache-Control': 'max-age=0',
    }
    response = ses.get('https://catalog.usmint.gov/account-register', headers=headers)
    profileSecure = response.text.split('<input type="hidden" name="dwfrm_profile_securekey" value="')[1].split('"/>')[0]
    emailSecure = response.text.split('<input type="hidden" name="dwfrm_emailsignup_securekey" value="')[1].split('"/>')[0]
    cartId = response.text.split('<form action="https://catalog.usmint.gov/account-register?dwcont=')[1].split('"')[0]

def submitSignup(email, ses):
    global paymentSecure
    headers = {
        'User-Agent': 'Mozilla/5.0 (X11; Linux x86_64; rv:68.0) Gecko/20100101 Firefox/68.0',
        'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8',
        'Accept-Language': 'en-US,en;q=0.5',
        'Referer': 'https://catalog.usmint.gov/account-login?dwcont=C751452587',
        'Content-Type': 'application/x-www-form-urlencoded',
        'Connection': 'keep-alive',
        'Upgrade-Insecure-Requests': '1',
        'TE': 'Trailers',
    }

    params = (
        ('dwcont', f'{cartId}'),
    )

    data = {
        'emailsource': 'Website - Registration',
        'dwfrm_profile_customer_firstname': 'Evan',
        'dwfrm_profile_customer_lastname': '',
        'dwfrm_profile_customer_email': f'{email}',
        'dwfrm_profile_customer_emailconfirm': f'{email}',
        'dwfrm_profile_login_password': '',
        'dwfrm_profile_login_passwordconfirm': '',
        'dwfrm_profile_login_question': '5',
        'dwfrm_profile_login_answer': 'Superman',
        'formAgreement': 'on',
        'dwfrm_profile_confirm': 'Create Your Account',
        'dwfrm_profile_securekey': f'{profileSecure}',
        'dwfrm_emailsignup_securekey': f'{emailSecure}'
    }

    response = ses.post('https://catalog.usmint.gov/account-login', headers=headers, params=params, data=data)
    response = ses.get('https://catalog.usmint.gov/on/demandware.store/Sites-USM-Site/default/PaymentInstruments-Add?format=ajax', headers=headers)
    paymentSecure = response.text.split('<input type="hidden" name="dwfrm_paymentinstruments_securekey" value="')[1].split('"/>')[0]
def setCard(ses):
    headers = {
        'User-Agent': 'Mozilla/5.0 (X11; Linux x86_64; rv:68.0) Gecko/20100101 Firefox/68.0',
        'Accept': 'application/json, text/javascript, */*; q=0.01',
        'Accept-Language': 'en-US,en;q=0.5',
        'Referer': 'https://catalog.usmint.gov/on/demandware.store/Sites-USM-Site/default/PaymentInstruments-List',
        'Content-Type': 'application/x-www-form-urlencoded; charset=UTF-8',
        'X-Requested-With': 'XMLHttpRequest',
        'Connection': 'keep-alive',
        'TE': 'Trailers',
    }


    data = {
        'dwfrm_paymentinstruments_creditcards_newcreditcard_owner': 'Evan',
        'dwfrm_paymentinstruments_creditcards_newcreditcard_type': 'Visa',
        'dwfrm_paymentinstruments_creditcards_newcreditcard_number': '',
        'dwfrm_paymentinstruments_creditcards_newcreditcard_month': '1',
        'dwfrm_paymentinstruments_creditcards_newcreditcard_year': '2025',
        'dwfrm_paymentinstruments_securekey': f'{paymentSecure}'
    }

    response = ses.post('https://catalog.usmint.gov/on/demandware.store/Sites-USM-Site/default/PaymentInstruments-AddContinue', headers=headers, data=data).json()
    if response['success']:
        print("Card succesfully set. ")

def setAddress(ses):
    headers = {
        'User-Agent': 'Mozilla/5.0 (X11; Linux x86_64; rv:68.0) Gecko/20100101 Firefox/68.0',
        'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8',
        'Accept-Language': 'en-US,en;q=0.5',
        'Referer': 'https://catalog.usmint.gov/account-login',
        'Connection': 'keep-alive',
        'Upgrade-Insecure-Requests': '1',
        'Cache-Control': 'max-age=0',
    }
    response = ses.get('https://catalog.usmint.gov/on/demandware.store/Sites-USM-Site/default/Address-Add?format=ajax', headers=headers)
    prof2Secure = response.text.split('<input type="hidden" name="dwfrm_profile_securekey" value="')[1].split('"/>')[0]

    headers = {
        'User-Agent': 'Mozilla/5.0 (X11; Linux x86_64; rv:68.0) Gecko/20100101 Firefox/68.0',
        'Accept': 'application/json, text/javascript, */*; q=0.01',
        'Accept-Language': 'en-US,en;q=0.5',
        'Referer': 'https://catalog.usmint.gov/on/demandware.store/Sites-USM-Site/default/Address-List',
        'Content-Type': 'application/x-www-form-urlencoded; charset=UTF-8',
        'X-Requested-With': 'XMLHttpRequest',
        'Connection': 'keep-alive',
        'TE': 'Trailers',
    }

    data = {
        'dwfrm_profile_address_addressid': '10 Pond Lane',
        'dwfrm_profile_address_firstname': 'John',
        'dwfrm_profile_address_lastname': 'Smith',
        'dwfrm_profile_address_address1': '10 ABQ Pond Lane',
        'dwfrm_profile_address_address2': 'Suite 103',
        'dwfrm_profile_address_country': 'US',
        'dwfrm_profile_address_states_state': 'NY',
        'dwfrm_profile_address_city': 'New York',
        'dwfrm_profile_address_zip': '10001',
        'dwfrm_profile_address_phone': '',
        'dwfrm_profile_address_isDefaultShipping': 'true',
        'dwfrm_profile_address_isDefaultBilling': 'true',
        'dwfrm_profile_securekey': f'{prof2Secure}'
    }

    response = ses.post('https://catalog.usmint.gov/on/demandware.store/Sites-USM-Site/default/Address-AddContinue', headers=headers, data=data)
    print(response.text)

if __name__ == '__main__':
    ses = requests.session()
    s = cfscrape.create_scraper(ses)
    getValues(s)
    submitSignup('abghk@fw025.com', ses=s)
    setCard(s)
    setAddress(s)

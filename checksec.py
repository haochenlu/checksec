import sys
import socket
import ssl
import threading

from cryptography import x509
from cryptography.hazmat.primitives.serialization import Encoding, PublicFormat


def get_info_cipher_suites(ssock: ssl.SSLSocket):
    """" This function receives a secure socket and returns a dictionary.
    The dictionary contains the key 'using', associated to the cipher
    being used (as a string), and also the key 'ciphers', linked to a
    list of ciphers that the server supports, in the form of a list of
    strings.
    """

    # TODO

    return {
        'using': 'TODO',
        'ciphers': ['TODO'],
    }

def get_info_certificate(ssock: ssl.SSLSocket):
    """" This function receives a secure socket and returns a dictionary.
    The dictionary includes elements 'version', 'notBefore' and
    'notAfter', linked to the version, starting date/time and ending
    date/time (respectively) of the certificate associated to the
    socket.
    """

    # TODO

    return {
        'version': 'TODO',
        'notBefore': 'TODO',
        'notAfter': 'TODO',
    }

def get_info_names_subject(ssock: ssl.SSLSocket):
    """" This function receives a secure socket and returns a dictionary.
    The dictionary contains elements 'names' and 'altNames', with
    lists of tuples in the format ('nameType', 'name').

    Example output:
    {
        'names': [('countryName', 'CA')],
        'altNames': [('DNS', 'www.ubc.ca'), ('DNS', 'ubc.ca')]
    }
    """

    # TODO

    return {
        'names': 'TODO',
        'altNames': 'TODO',
    }

def get_info_names_issuer(ssock: ssl.SSLSocket):
    """" This function receives a secure socket and returns a lists of
    tuples.  The tuples should have the format ('nameType', 'name').

    Example output:
    [('countryName', 'US'), ('organizationName', 'Entrust, Inc.')]
    """

    # TODO

    return None

def get_info_public_key(ssock: ssl.SSLSocket):
    """This function receives a secure socket and returns the public key
    as a string (not a bytestring).  You will probably need to use the
    cryptography library for this.
    """

    # TODO

    return None

def print_cert_info(ssock: ssl.SSLSocket):
    """Prints the certificate info. Do not change this function.
    """
    # get and print cipher suites
    ciphers = get_info_cipher_suites(ssock)

    print('Supported cipher suites:')
    for cipher in ciphers.get('ciphers'):
        print(f'\t{cipher}')

    using = ciphers.get('using')
    print(f'Using cipher suite: {using}')
    print()

    # get and print certificate information
    cert_info = get_info_certificate(ssock)
    cert_version = cert_info.get('version')
    cert_not_before = cert_info.get('notBefore')
    cert_not_after = cert_info.get('notAfter')

    print(f'Certificate version     : {cert_version}')
    print(f'Certificate start time  : {cert_not_before}')
    print(f'Certificate end time    : {cert_not_after}')
    print()

    # get and print subject information
    subject_names = get_info_names_subject(ssock)

    print(f'Certificate Subject:')
    for name in subject_names.get('names'):
        print('%32s: %s' % name)
    print()

    # get and print alt names
    print(f'Certificate Subject Alt Names:')
    for name in subject_names.get('altNames'):
        print('%32s: %s' % name)
    print()

    # get and print issuer information
    issuer_names = get_info_names_issuer(ssock)

    print(f'Certificate Issuer:')
    for name in issuer_names:
        print('%32s: %s' % name)
    print()

    public_key = get_info_public_key(ssock)

    print('Server public key:')
    print(public_key)


def main():
    if len(sys.argv) < 2:
        print('ERROR: Hostname not provided.')
        return

    hostname = sys.argv[1]
    port = 443
    if len(sys.argv) >= 3:
        port = sys.argv[2]

    # print host information
    print(f'Host: {hostname}')
    print(f'Port: {port}')
    print()

    # open connection
    # TODO


if __name__ == '__main__':
    main()

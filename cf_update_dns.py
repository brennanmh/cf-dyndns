import json
import argparse

import requests
#import pprint as pp

cf_api_root = "https://api.cloudflare.com/client/v4"

def get_wan_ip():
    ip = requests.get('https://api.ipify.org').content.decode('utf8')
    return ip


def get_account_id(account_email, api_key):
    api = "/accounts"
    api_url = cf_api_root + api
    headers = {
        "X-Auth-Email": account_email,
        "X-Auth-Key": api_key,
        "Content-Type": "application/json"
    }
    resp = requests.get(api_url, headers=headers)
    if resp.status_code != 200:
        print("Failed to list accounts with code {}".format(resp.status_code))
        return 0

    accounts = resp.json()
    return accounts['result'][0]['id']


def get_zone_id(account_email, api_key, account_id, domain_name):
    api_url = cf_api_root + f"/zones?name={domain_name}&account.id={account_id}"
    headers = {
        "X-Auth-Email": account_email,
        "X-Auth-Key": api_key,
        "Content-Type": "application/json"
    }
    resp = requests.get(api_url, headers=headers)
    if resp.status_code != 200:
        print(f"Failed to get zone {domain_name} with code {resp.status_code}")
        return 0

    zones = resp.json()
    return zones['result'][0]['id']


def get_record_id(account_email, api_key, zone_id, record_name):
    api_url = cf_api_root + f"/zones/{zone_id}/dns_records?type=A&name={record_name}"
    headers = {
        "X-Auth-Email": account_email,
        "X-Auth-Key": api_key,
        "Content-Type": "application/json"
    }
    resp = requests.get(api_url, headers=headers)
    if resp.status_code != 200:
        print(f"Failed to get record for {record_name} with code {resp.status_code}")
        return None

    record = resp.json()
    return record['result'][0]


def update_host(account_email, api_key, zone_id, record_id, hostname, new_ip):
    print(f"Updating host {hostname} to {new_ip}")
    api_url = cf_api_root + f"/zones/{zone_id}/dns_records/{record_id}"
    args = {
        "type": "A",
        "name": hostname,
        "content": new_ip,
        "proxied": True
    }
    data = json.dumps(args)
    headers = {
        "X-Auth-Email": account_email,
        "X-Auth-Key": api_key,
        "Content-Type": "application/json"
    }
    resp = requests.patch(api_url, headers=headers, data=data)
    if resp.status_code != 200:
        print(f"Failed to update record for {hostname} with code {resp.status_code}")

    print(f"Updated {hostname} to {new_ip}")


if __name__ == '__main__':
    parser = argparse.ArgumentParser()

    parser.add_argument("domains", help="the domains to update", nargs='+')
    parser.add_argument('-k', '--api-key', help='cloudflare api key', required=True)
    parser.add_argument('-a', '--account_email', help='cloudflare account email', required=True)

    args = parser.parse_args()
    account_email = args.account_email
    api_key = args.api_key
    domains = args.domains

    wan_ip = get_wan_ip()
    print(f'My public IP address is: {wan_ip}')

    account_id = get_account_id(account_email, api_key)
    if account_id == 0:
        sys.exit(1)

    for domain in domains:
        zone_id = get_zone_id(account_email, api_key, account_id, domain)
        if zone_id == 0:
            continue

        record = get_record_id(account_email, api_key, zone_id, domain)
        if record == None:
            continue

        if record['content'] == wan_ip:
            print(f"{domain} already set to {wan_ip}")
            continue

        record_id = record['id']

        update_host(account_email, api_key, zone_id, record_id, domain, wan_ip)

#!/usr/bin/env bash

cf_api_token="1XRDNCKM4gJaE6hUQE4oBBlqNveDUYyzwl1oyEne"
cf_api_key="cc7aec72e4aacf3551a25b468dc1e4c8c85c7"

curl -X GET "https://api.cloudflare.com/client/v4/accounts" \
     -H "X-Auth-Email: brennanmh@gmail.com" \
     -H "X-Auth-Key: ${cf_api_key}" \
     -H "Content-Type: application/json"

echo
echo
echo "+===== nthroot.org zone id ===========================+"
echo
echo


curl -X GET "https://api.cloudflare.com/client/v4/zones?name=nthroot.org&account.id=032af6b11dd722a1ef04e475f1274686" \
     -H "X-Auth-Email: brennanmh@gmail.com" \
     -H "X-Auth-Key: ${cf_api_key}" \
     -H "Content-Type: application/json"

nthroot_zone_id="7f573f0ae0c6f9cd01b3a82f18d0d877"

echo
echo
echo "+===== nthroot.org A record =========================+"
echo
echo


curl -X GET "https://api.cloudflare.com/client/v4/zones/${nthroot_zone_id}/dns_records?name=nthroot.org&type=A" \
     -H "X-Auth-Email: brennanmh@gmail.com" \
     -H "X-Auth-Key: ${cf_api_key}" \
     -H "Content-Type: application/json"

#!/usr/bin/env bash
set -e

ENV="$HOME/shmry_cloud_hyperscale/namecheap.env"

if [ ! -f "$ENV" ]; then
  echo "❌ Missing $ENV"
  exit 1
fi

source "$ENV"

TARGET=$(echo "$SHMRY_TARGET_URL" | sed 's#https://##' | sed 's#http://##')

echo "📡 Configuring nifdu.com DNS → SHMRY"

curl -s "https://api.namecheap.com/xml.response" \
  --get \
  --data-urlencode "ApiUser=$NAMECHEAP_USER" \
  --data-urlencode "ApiKey=$NAMECHEAP_API_KEY" \
  --data-urlencode "UserName=$NAMECHEAP_USER" \
  --data-urlencode "ClientIp=$NAMECHEAP_CLIENT_IP" \
  --data-urlencode "Command=namecheap.domains.dns.setHosts" \
  --data-urlencode "SLD=$DOMAIN_SLD" \
  --data-urlencode "TLD=$DOMAIN_TLD" \
  --data-urlencode "HostName1=www" \
  --data-urlencode "RecordType1=CNAME" \
  --data-urlencode "Address1=$TARGET" \
  --data-urlencode "TTL1=300" \
  --data-urlencode "HostName2=@" \
  --data-urlencode "RecordType2=URL" \
  --data-urlencode "Address2=https://www.${DOMAIN_SLD}.${DOMAIN_TLD}" \
  --data-urlencode "TTL2=300" \
| tee ~/shmry_cloud_hyperscale/namecheap_dns_response.xml

echo
echo "✅ DNS sync request submitted"
echo
echo "🌐 Expected endpoints after propagation:"
echo "https://www.${DOMAIN_SLD}.${DOMAIN_TLD}"
echo "https://www.${DOMAIN_SLD}.${DOMAIN_TLD}/api/health"
echo "https://www.${DOMAIN_SLD}.${DOMAIN_TLD}/api/customers"
echo "https://www.${DOMAIN_SLD}.${DOMAIN_TLD}/api/instances"
echo "https://www.${DOMAIN_SLD}.${DOMAIN_TLD}/api/dashboard"
echo
echo "⏳ DNS propagation may take several minutes"


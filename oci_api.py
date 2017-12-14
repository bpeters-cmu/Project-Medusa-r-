import requests
import oci
config = {
    "user": 'ocid1.user.oc1..aaaaaaaaqwuvrt5r6ilprmbpq5stynbohmc6m6h3cw4ongvuohtg7adenusa',
    "key_file": 'C:/Users/benpeter/.oci/oci_api_key.pem',
    "fingerprint": 'f9:80:ae:7b:87:41:7e:b9:eb:78:08:29:63:1b:8f:2b',
    "tenancy": 'ocid1.tenancy.oc1..aaaaaaaa2ga2wc6bkwwayxq3vmjhjfieamxaxjudiciobpfk7zwcdoykus4q',
    "region": 'us-phoenix-1'
}

compute = oci.core.ComputeClient(config)
response = compute.list_instances("ocid1.compartment.oc1..aaaaaaaapjubpc2gi5b3o7gxqbyyfww6bnuzsnyrjp6scns2zrw3b2kz2qbq")

print(str(response.data))

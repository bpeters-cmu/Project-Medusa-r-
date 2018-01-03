import oci



class OCIApi:

    def __init__(self, user, key_file, fingerprint, tenancy, region):
        self.config = {
            "user": user,
            "key_file": key_file,
            "fingerprint": fingerprint,
            "tenancy": tenancy,
            "region": region
        }

    def get_instances(self, compartment_ocid=None):

        self.config = {
            "user": 'ocid1.user.oc1..aaaaaaaawnwprfxu7rx2osz3zwpwlk5pg3ip4ua6igbtc4qle3pjhna3e2ja',
            "key_file": 'C:/Users/benpeter/.oci/oci_api_key.pem',
            "fingerprint": 'f9:80:ae:7b:87:41:7e:b9:eb:78:08:29:63:1b:8f:2b',
            "tenancy": 'ocid1.tenancy.oc1..aaaaaaaa2ga2wc6bkwwayxq3vmjhjfieamxaxjudiciobpfk7zwcdoykus4q',
            "region": 'us-phoenix-1'
        }

        compute = oci.core.ComputeClient(self.config)
        compartment_ocid = "ocid1.compartment.oc1..aaaaaaaapjubpc2gi5b3o7gxqbyyfww6bnuzsnyrjp6scns2zrw3b2kz2qbq"
        response = compute.list_instances(compartment_ocid)
        data = response.data
        instance_ocid = ''
        for item in data:
            if item.display_name == 'iaas_project_medusa_ad':
                instance_ocid = item.id
        ip = self.get_public_ip(compartment_ocid, instance_ocid)
        print(ip)

    def get_public_ip(self, compartment_ocid, instance_ocid):
        vnics = self.get_instance_vnic(compartment_ocid, instance_ocid)
        return vnics[0].public_ip

    def get_instance_vnic(self, compartment,instance_id):
        compute = oci.core.ComputeClient(self.config)
        network = oci.core.VirtualNetworkClient(self.config)
        vnic = []
        vnic_attachments = compute.list_vnic_attachments(compartment,instance_id=instance_id).data
        for attachment in vnic_attachments:
            if attachment.lifecycle_state == "ATTACHED":
                vnic_attachment = network.get_vnic(attachment.vnic_id).data
                vnic.append(vnic_attachment)
        return vnic

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

        print('get_instances')
        compute = oci.core.ComputeClient(self.config)
        response = compute.list_instances(compartment_ocid)
        data = response.data
        print(data)
        instance_map = {}
        result = {}
        for item in data:
            if 'medusa' in item.display_name:
                instance_map[item.display_name] = item.id

        for key, value in instance_map.items():
            result[key] = self.get_public_ip(compartment_ocid, value)

        return result

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

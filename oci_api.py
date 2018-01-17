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
            print('item display: ' + item.display_name)
            if 'medusa' in item.display_name:
                instance_map[item.display_name] = item.id

        for key, value in instance_map.items():
            print('key'+ key)
            print('value: ' + value)
            result[key] = self.get_public_ip(compartment_ocid, value)
        print('result: ' + result)
        return result

    def get_public_ip(self, compartment_ocid, instance_ocid):
        print('get pub ip')
        vnic = self.get_instance_vnic(compartment_ocid, instance_ocid)
        return vnic.public_ip

    def get_instance_vnic(self, compartment,instance_id):
        print('get instance vnic')
        compute = oci.core.ComputeClient(self.config)
        network = oci.core.VirtualNetworkClient(self.config)
        vnic = []
        vnic_attachments = compute.list_vnic_attachments(compartment,instance_id=instance_id).data
        print(vnic_attachments)
        for attachment in vnic_attachments:
            if attachment.lifecycle_state == "ATTACHED":
                print('test')
                vnic_attachment = network.get_vnic(attachment.vnic_id).data
                print(vnic_attachment)
                return vnic_attachment
        return None

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

    def get_instances(self, compartment_ocid):
        print('get_instances')
        compute = oci.core.ComputeClient(self.config)
        response = compute.list_instances(compartment_ocid)
        instance_info = {}
        instance_info['linux'] = []
        instance_info['windows'] = []
        for i in response.data:
            if 'type' in i.freeform_tags:
                if i.freeform_tags['type'] == 'linux':
                    instance = {}
                    instance['name'] = i.display_name
                    instance['ip'] = self.get_public_ip(compartment_ocid, i.id)
                    instance_info['linux'].append(instance)
                elif i.freeform_tags['type'] == 'windows':
                    instance = {}
                    instance['name'] = i.display_name
                    instance['ip'] = self.get_public_ip(compartment_ocid, i.id)
                    instance_info['windows'].append(instance)
        return instance_info

    def get_public_ip(self, compartment_ocid, instance_ocid):
        print('get pub ip')
        vnic = self.get_instance_vnic(compartment_ocid, instance_ocid)
        print('pub ip: ' + vnic.public_ip)
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

    def get_compartments(self):
        identity = oci.identity.IdentityClient(self.config)
        result = oci.pagination.list_call_get_all_results(identity.list_compartments, self.config['tenancy'])
        comps = {}
        compartments = []
        for c in result.data:
            comp = {}
            comp['name'] = c.description
            comp['ocid'] = c.id
            compartments.append(comp)
        comps['compartments'] = compartments
        return comps

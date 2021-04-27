#!/usr/bin/env python
"""
################################################################################
#
# Demo - Sample Script to obtain and print out Tenants and VRFs from an ACI Fabric
#
# NOT FOR PRODUCTION USE. ONLY TESTED IN LAB ENVIRONMENT
#
# Michael Petrinovic 2021
#
# Requirements: requests
# pip install requests
#
################################################################################

###
#
# USAGE
#
# python check-aci-solution.py
#
"""

import requests

# Enter your APIC hostname/IP and user credentials below.
apic = "10.66.110.115"
username = "admin"
password = "admincisco"

# Create AAA Login
base_url = "https://" + str(apic) + "/api/"
auth_bit = "aaaLogin.json"
auth_url = base_url + auth_bit
auth_data = {
  "aaaUser":{
    "attributes":{
      "name":username,
      "pwd":password
    }
  }
}

# Create the Request using above AAA Login
requests.packages.urllib3.disable_warnings()
aci_session = requests.session()
aci_session.post(auth_url, json=auth_data, verify=False)

# Obtain and utilize the correct Tenant Class
tenant_class="node/class/fvTenant.json" # FIX Incorrect Class for Tenant
#tenant_class="node/class/fvtenants.json"
tenant_url = base_url + tenant_class

# Generate and request Tenant information
tenants = aci_session.get(tenant_url, verify=False)
tenants_output_json = tenants.json()
#print (tenants_output_json) # FIX OPTION

# Let's get all our tenants
# Start with an empty list
tenant_list = []
count = 0

# Extract relevant data from Tenant List
tn_out_list = tenants_output_json['imdata']

# Loop over data set
for tenant in tn_out_list:
    dn = tenant['fvTenant']['attributes']['dn']
    split_dn = dn.split("/")
    count = count + 1
    tenant_list.append(split_dn[1])

# Print out results
CCIE_DC_Tenants = 0
print("\nTenants: ")
print('==========')
for tenant_name in tenant_list:
    print(tenant_name[3:])
    if "CCIE_DC_T" in tenant_name:
        CCIE_DC_Tenants = CCIE_DC_Tenants + 1
print('==========')
print('\nThere are', count, 'Tenants')
print('==========')

if CCIE_DC_Tenants == 26:
    print("Congratulations, you have the correct amount of CCIE_DC Tenants")
else:
    print("You do NOT have the correct amount of CCIE_DC Tenants: ", CCIE_DC_Tenants)

# Obtain and utilize the correct VRF Class
vrf_class="node/class/fvCtx.json" # FIX Incorrect Class for VRF
#vrf_class="node/class/fvVrf.json"
vrf_url = base_url + vrf_class

# Generate and request VRF information
vrfs = aci_session.get(vrf_url, verify=False)
vrf_output_json = vrfs.json()
#print (vrf_output_json) # FIX OPTION

# Let's get all our VRFs
# Start with an empty list
vrf_list = []
count = 0

# Extract relevant data from VRF List
vrf_out_list = vrf_output_json['imdata']

# Loop over data set
for vrf in vrf_out_list:
    #print(vrf)
    # FIX Ensure using the correct KEY = fvCtx instead of fvVrf
    dn = vrf['fvCtx']['attributes']['dn']
    split_dn = dn.split("/")
    vrf_list.append(dn)
    count = count + 1

# Print out results
CCIE_DC_VRFS = 0
print("\nVRFs in the Fabric: ")
print('====================')
for vrf_name in vrf_list:
    print(vrf_name)
    if "CCIE_DC_VRF" in vrf_name:
        CCIE_DC_VRFS = CCIE_DC_VRFS + 1
print('====================')
print('\nThere are', count, 'VRFs')
print('==========')
if CCIE_DC_VRFS == 26:
    print("Congratulations, you have the correct amount of CCIE_DC VRFs")
else:
    print("You do NOT have the correct amount of CCIE_DC VRFs: ", CCIE_DC_VRFS)

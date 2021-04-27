#!/usr/bin/env python
"""
################################################################################
#
# Demo - Create Tenant/VRF however does NOT create a complete working scenario
#
# NOT FOR PRODUCTION USE. ONLY TESTED IN LAB ENVIRONMENT
#
# Michael Petrinovic 2021
#
# Requirements: acitoolkit
# https://github.com/datacenter/acitoolkit
# pip install acitoolkit
#
#
# NOTE: Currently does no validation if the tenant name already exists when providing the name_prefix
# and iterations to auto-create
#
################################################################################

###
#
# USAGE
#
# Deploy Configuration
# python aci-deploy.py --url https://10.66.110.115 --login admin --password admincisco --prefix CCIE_DC --amount 26
#
"""

import acitoolkit.acitoolkit as aci
import time

def main():

    # Take login credentials from the command line if provided
    # Otherwise, take them from your environment variables file ~/.profile
    description = ('Simple application to build a Tenant/AP/EPG/BD/VRF')
    creds = aci.Credentials('apic', description)
    creds.add_argument('--delete', action='store_true', help='Delete the configuration from the APIC')
    creds.add_argument('--prefix', help='Prefix to use for all objects', default="mipetrin_acitoolkit")
    creds.add_argument('--amount', nargs='?', const=1, type=int, default=3, help='The total amount of iterations to complete')
    creds.add_argument('--test', action='store_true', help='Don\'t write to APIC. Print JSON output only')
    creds.add_argument('--debug', action='store_true', help='Verbose output')
    creds.add_argument('--force', action='store_true', help='Force delete')

    args = creds.get()

    name_prefix = args.prefix
    total_amount = args.amount
    debug_enabled = args.debug

    # Validate number is not above 26 for letters in alphabet
    if total_amount < 1 or total_amount > 26:
        print ("Please select a number between 1 - 26")
        return

    # Login to APIC
    session = aci.Session(args.url, args.login, args.password)
    resp = session.login()
    if not resp.ok:
        print('%% Could not login to APIC')
        return

    # Start time count at this point, otherwise takes into consideration the amount of time taken to input the password
    start_time = time.time()

    count = 1

    while (count < total_amount):
        if debug_enabled:
            print 'The count is:', count

        # FIX THIS CODE
        tenant = aci.Tenant(name_prefix + str(count) + str(chr(ord('@')+count)))
        context = aci.Context(name_prefix + str(count) + str(chr(ord('@')+count)), tenant)

        # Delete the configuration if desired
        # WARNING - NO VALIDATION TAKES PLACE CURRENTLY. SIMPLY DELETES CONFIG
        #
        # WARNING - READ THAT AGAIN
        #
        # WARNING - NO VALIDATION TAKES PLACE CURRENTLY. SIMPLY DELETES CONFIG
        aborted = False
        abort_count = 0

        if args.delete:
            #selection = None # First pass, ensure selection exists but no choice yet
            if debug_enabled:
                print "Checkpoint: args.delete"

            while 1:
                # raw_input returns an empty string for "enter"
                yes = {'yes','y', 'ye'}
                no = {'no','n', ''}

                # Force delete without my typical warnings
                if args.force:
                    tenant.mark_as_deleted()
                    break

                selection = raw_input("Are you absolutely sure you want to DELETE the entire tenant: ["
                                      + tenant.name + "]???  [y|N]  ").lower()

                if selection in yes:
                    # Uncomment the below line with caution. Wipes all tenants that match the criteria
                    tenant.mark_as_deleted()
                    print ("Delete action is being performed...")
                    print ("-" * 30)
                    break
                elif selection in no:
                    # everything else to default to NO
                    print "Aborting delete..."
                    aborted = True
                    print ("-" * 30)
                    break
                else:
                    print "error state"

        if aborted:
            count = count + 1 # Ensure that we do loop to the next iteration from name perspective in an aborted scenario
            abort_count += 1 # Keep track of how many we abort/skip over deleting, per user selection
            continue # to the next iteration of the loop as no config push is required
        elif args.test:
            print(tenant.get_json())
        else:
            # Push our json configuration to the APIC (either to be created or deleted) unless aborted
            resp = session.push_to_apic(tenant.get_url(),
                                        tenant.get_json())
            if resp.ok:
                # print 'Success:', count
                # Print what was sent
                if debug_enabled:
                    print 'Success:', count
                    print 'Pushed the following JSON to the APIC'
                    print 'URL:', tenant.get_url()
                    print 'JSON:', tenant.get_json()

            if not resp.ok:
                print('%% Error: Could not push configuration to APIC')
                print(resp.text)
                exit(0)

        count = count + 1 # Loop to the next iteration from name perspective for Test/Update

    print "=" * 80

    if args.delete:
        print 'Attempted to delete the following object count:', total_amount - abort_count
    elif args.test:
        print 'Printed test output for a total object count:', total_amount
    else:
        print 'Successfully pushed total object count to the APIC:', total_amount

    print "=" * 80

    print ("#" * 80)
    finish_time = time.time()
    print ("Started @ {}".format(time.asctime(time.localtime(start_time))))
    print ("Ended @ {}".format(time.asctime(time.localtime(finish_time))))
    print("--- Total Execution Time: %s seconds ---" % (finish_time - start_time))
    print ("#" * 80)

if __name__ == '__main__':
    main()

import time
import oci
import os
import json
import sys
from pandas.io.json import json_normalize
import pandas as pd
from oci import config



#import config as cfg
tenancy_id = 'ocid1.tenancy.oc1..aaaaaaaauwf5vnl7szsfxaq44yv6lml7dahxf72e677rty3zxjkh3qrsyl6q' # Tenancy & Root compartment OCID
compartment_id = 'ocid1.compartment.oc1..aaaaaaaaec7xg2meskc544ra3mfj5c3e3hxsfw4dtjinxinebsgs47gsy77a' #  compartment OCID
userocid = 'ocid1.user.oc1..aaaaaaaaker3tujdz6qvpbi3fpdpbcmelzu74dw7er5i7ukxxa57pj43usna' # User OCID
home_region = 'us-ashburn-1' # Home Region
key_file = '~/.oci/oci_api_key.pem' # Prvate file for User Authentication
fingerprint = '09:fd:0f:58:f5:d3:d0:c4:7d:f8:6a:a6:de:19:c2:fd' # Finger print of the public key added in user tokens
# Config for Home Region Connection
config = {
    "user": userocid,
    "key_file": key_file,
    "fingerprint": fingerprint,
    "tenancy": tenancy_id,
    "region": home_region,
    "compartment_id": compartment_id }

print("\n")
print(".........................................................................................................")
print("................................. The Program Starts Here................................................")
print(".........................................................................................................")
print("\n")


dataframe = pd.read_excel('emails.xlsx',engine ='openpyxl')  #here,we are baically creating a dataframe from the list sent that is present in the excel file 
print("\n\nSo, there are about ",len(dataframe.index)," people whose account needs to be deleted\n\n")    #Total number of people in the list
list_of_people=dataframe.values.tolist()
identity_client = oci.identity.IdentityClient(config)   #connection made to the tenancy to get the list of regions subscribed to this tenancy
list_of_people1=[]
lst = []
for a in list_of_people:
  list_of_people1.append(str(a).strip("[]"))

identity_client = oci.identity.IdentityClient(config)   #connection made to the tenancy to get the list of regions subscribed to this tenancy
list_region_subscriptions_response = identity_client.list_region_subscriptions(tenancy_id)

for list_user in list_of_people1:
   print("\n\nDeleting the resources of user ",list_user,"\n\n")
   for regions in list_region_subscriptions_response.data: # For each person we will translate through all the regions that are present-
       config["region"]=regions.region_name                  # -and display the respective query for all these regions
    
       resource_search_client = oci.resource_search.ResourceSearchClient(config)  # Making object for querying for all the regions
       core_client = oci.core.ComputeClient(config)
       database_client = oci.database.DatabaseClient(config)
       core_client_net = oci.core.VirtualNetworkClient(config)
       core_client_bvolume = oci.core.BlockstorageClient(config)
       object_storage_client = oci.object_storage.ObjectStorageClient(config)
       core_client_insc = oci.core.ComputeManagementClient(config)
       analytics_client = oci.analytics.AnalyticsClient(config)    
       print("\n\nIn the region ",regions.region_name," the resources of the user are\n\n") # Printing the resources of the user for that particular-
    
       search_resources_response = resource_search_client.search_resources(                          # -region
           search_details=oci.resource_search.models.StructuredSearchDetails(                        # Now we are querying the required resources 
               type="Structured",
               query="query instance resources where (definedTags.namespace = 'Owner' && definedTags.key = 'createtBy' && definedTags.value ="+str(list_user)+")",
               matching_context_type="HIGHLIGHTS"),limit=500)
    

       search_resources_response_analytics = resource_search_client.search_resources(                          # -region
           search_details=oci.resource_search.models.StructuredSearchDetails(                        # Now we are querying the required resources 
               type="Structured",
               query="query analyticsinstance resources where (definedTags.namespace = 'Owner' && definedTags.key = 'createtBy' && definedTags.value ="+str(list_user)+")",
               matching_context_type="HIGHLIGHTS"),limit=500) 


       search_resources_response_db = resource_search_client.search_resources(                          # -region
           search_details=oci.resource_search.models.StructuredSearchDetails(                        # Now we are querying the required resources 
               type="Structured",
               query="query database resources where (definedTags.namespace = 'Owner' && definedTags.key = 'createtBy' && definedTags.value ="+str(list_user)+")",
               matching_context_type="HIGHLIGHTS"),limit=500)
    
       search_resources_response_subnet = resource_search_client.search_resources(                          # -region
           search_details=oci.resource_search.models.StructuredSearchDetails(                        # Now we are querying the required resources 
               type="Structured",
               query="query subnet resources where (definedTags.namespace = 'Owner' && definedTags.key = 'createtBy' && definedTags.value ="+str(list_user)+")",
               matching_context_type="HIGHLIGHTS"),limit=500)

       search_resources_response_volume = resource_search_client.search_resources(                          # -region
           search_details=oci.resource_search.models.StructuredSearchDetails(                        # Now we are querying the required resources 
               type="Structured",
               query="query volume resources where (definedTags.namespace = 'Owner' && definedTags.key = 'createtBy' && definedTags.value ="+str(list_user)+")",
               matching_context_type="HIGHLIGHTS"),limit=500)


       search_resources_response_boot = resource_search_client.search_resources(                          # -region
           search_details=oci.resource_search.models.StructuredSearchDetails(                        # Now we are querying the required resources 
               type="Structured",
               query="query bootvolume resources where (definedTags.namespace = 'Owner' && definedTags.key = 'createtBy' && definedTags.value ="+str(list_user)+")",
               matching_context_type="HIGHLIGHTS"),limit=500)


       search_resources_response_lb = resource_search_client.search_resources(                          # -region
           search_details=oci.resource_search.models.StructuredSearchDetails(                        # Now we are querying the required resources 
               type="Structured",
               query="query loadbalancer resources where (definedTags.namespace = 'Owner' && definedTags.key = 'createtBy' && definedTags.value ="+str(list_user)+")",
               matching_context_type="HIGHLIGHTS"),limit=500) 


       search_resources_response_nat = resource_search_client.search_resources(                          # -region
           search_details=oci.resource_search.models.StructuredSearchDetails(                        # Now we are querying the required resources 
               type="Structured",
               query="query natgateway resources where (definedTags.namespace = 'Owner' && definedTags.key = 'createtBy' && definedTags.value ="+str(list_user)+")",
               matching_context_type="HIGHLIGHTS"),limit=500)


      
       search_resources_response_route = resource_search_client.search_resources(                          # -region
           search_details=oci.resource_search.models.StructuredSearchDetails(                        # Now we are querying the required resources 
               type="Structured",
               query="query routetable resources where (definedTags.namespace = 'Owner' && definedTags.key = 'createtBy' && definedTags.value ="+str(list_user)+")",
               matching_context_type="HIGHLIGHTS"),limit=500)


     
       search_resources_response_vcn = resource_search_client.search_resources(                          # -region
           search_details=oci.resource_search.models.StructuredSearchDetails(                        # Now we are querying the required resources 
               type="Structured",
               query="query vcn resources where (definedTags.namespace = 'Owner' && definedTags.key = 'createtBy' && definedTags.value ="+str(list_user)+")",
               matching_context_type="HIGHLIGHTS"),limit=500)


       search_resources_response_sgway = resource_search_client.search_resources(                          # -region
           search_details=oci.resource_search.models.StructuredSearchDetails(                        # Now we are querying the required resources 
               type="Structured",
               query="query servicegateway resources where (definedTags.namespace = 'Owner' && definedTags.key = 'createtBy' && definedTags.value ="+str(list_user)+")",
               matching_context_type="HIGHLIGHTS"),limit=500)


       search_resources_response_igway = resource_search_client.search_resources(                          # -region
           search_details=oci.resource_search.models.StructuredSearchDetails(                        # Now we are querying the required resources 
               type="Structured",
               query="query internetgateway resources where (definedTags.namespace = 'Owner' && definedTags.key = 'createtBy' && definedTags.value ="+str(list_user)+")",
               matching_context_type="HIGHLIGHTS"),limit=500)
  
     


       search_resources_response_lpgway = resource_search_client.search_resources(                          # -region
           search_details=oci.resource_search.models.StructuredSearchDetails(                        # Now we are querying the required resources 
               type="Structured",
               query="query localpeeringgateway resources where (definedTags.namespace = 'Owner' && definedTags.key = 'createtBy' && definedTags.value ="+str(list_user)+")",
               matching_context_type="HIGHLIGHTS"),limit=500)


       search_resources_response_bucket = resource_search_client.search_resources(                          # -region
           search_details=oci.resource_search.models.StructuredSearchDetails(                        # Now we are querying the required resources 
               type="Structured",
               query="query bucket resources where (definedTags.namespace = 'Owner' && definedTags.key = 'createtBy' && definedTags.value ="+str(list_user)+")",
               matching_context_type="HIGHLIGHTS"),limit=500)


       search_resources_response_adb = resource_search_client.search_resources(                          # -region
           search_details=oci.resource_search.models.StructuredSearchDetails(                        # Now we are querying the required resources 
               type="Structured",
               query="query autonomousdatabase resources where (definedTags.namespace = 'Owner' && definedTags.key = 'createtBy' && definedTags.value ="+str(list_user)+")",
               matching_context_type="HIGHLIGHTS"),limit=500)


       search_resources_response_insc = resource_search_client.search_resources(                          # -region
           search_details=oci.resource_search.models.StructuredSearchDetails(                        # Now we are querying the required resources 
               type="Structured",
               query="query instanceconfiguration resources where (definedTags.namespace = 'Owner' && definedTags.key = 'createtBy' && definedTags.value ="+str(list_user)+")",
               matching_context_type="HIGHLIGHTS"),limit=500)


                                                                                    #Get the data from response

#print("Do you want to proceed with the Destroy action?  Please enter 'y' for Yes and 'n' for No.")
#if
       i=1
       for a in search_resources_response.data.items:                                  # Here, we are displaying all the resources we have queried
          print(i,"    ",a.display_name,"   ",a.identifier,"    ",a.resource_type)

          terminate_instance_response = core_client.terminate_instance(
          instance_id=a.identifier,
          preserve_boot_volume=False,
          preserve_data_volumes=False)
          print(terminate_instance_response.headers)
          lst.append([a.display_name,a.identifier,a.resource_type,a.lifecycle_state,regions.region_name])
       i=i+1


       i=1
       for a in search_resources_response_insc.data.items:                                  # Here, we are displaying all the resources we have queried
          print(i,"    ",a.display_name,"   ",a.identifier,"    ",a.resource_type)
          try:
             delete_instance_configuration_response = core_client_insc.delete_instance_configuration(
             instance_configuration_id=a.identifier)
             print(delete_instance_configuration_response.headers)
             lst.append([a.display_name,a.identifier,a.resource_type,a.lifecycle_state,regions.region_name])
          except:
             pass
          i=i+1

       i=1
       print(search_resources_response.data.items)
       for a in search_resources_response_analytics.data.items:                                  # Here, we are displaying all the resources we have queried
          print(i,"    ",a.display_name,"   ",a.identifier,"    ",a.resource_type)
          terminate_analytics_instance_response = analytics_client.delete_analytics_instance(analytics_instance_id=a.identifier)
          print(terminate_analytics_instance_response.headers)
          lst.append([a.display_name,a.identifier,a.resource_type,a.lifecycle_state,regions.region_name])
       i=i+1


       i=1
       for a in search_resources_response_adb.data.items:                                  # Here, we are displaying all the resources we have queried
          print(i,"    ",a.display_name,"   ",a.identifier,"    ",a.resource_type)
          try:
             delete_autonomous_database_response = database_client.delete_autonomous_database(
             autonomous_database_id=a.identifier)
             print(delete_autonomous_database_response.headers)
             lst.append([a.display_name,a.identifier,a.resource_type,a.lifecycle_state,regions.region_name])
          except:
             pass
       i=i+1

       i=1
       for a in search_resources_response_db.data.items:                                  # Here, we are displaying all the resources we have queried
          print(i,"    ",a.display_name,"   ",a.identifier,"    ",a.resource_type)
          try:
             delete_db_system_response = database_client.delete_db_system(
             db_sytem_id=a.identifier)
             print(delete_db_system_response.headers)
             lst.append([a.display_name,a.identifier,a.resource_type,a.lifecycle_state,regions.region_name])
          except:
             pass
       i=i+1


       i=1
       for a in search_resources_response_volume.data.items:                                  # Here, we are displaying all the resources we have queried
          print(i,"    ",a.display_name,"   ",a.identifier,"    ",a.resource_type)
          try:
             delete_volume_response = core_client_bvolume.delete_volume(             
             volume_id=a.identifier)
             print(delete_volume_response.headers)
             lst.append([a.display_name,a.identifier,a.resource_type,a.lifecycle_state,regions.region_name])
          except:
             pass      
       i=i+1

       i=1
       for a in search_resources_response_boot.data.items:                                  # Here, we are displaying all the resources we have queried
          print(i,"    ",a.display_name,"   ",a.identifier,"    ",a.resource_type)
          try:
             delete_boot_volume_response = core_client_bvolume.delete_boot_volume(
             boot_volume_id=a.identifier)
             print(delete_boot_volume_response.headers)
             lst.append([a.display_name,a.identifier,a.resource_type,a.lifecycle_state,regions.region_name])
          except:
             pass      
       i=i+1

       i=1
       for a in search_resources_response_bucket.data.items:                                  # Here, we are displaying all the resources we have queried
          print(i,"    ",a.display_name,"   ",a.identifier,"    ",a.resource_type)
          try:
             list_objects_response = object_storage_client.list_objects(
             namespace_name="axdvjzox0ixb",
             bucket_name=a.display_name)
             for objects in list_objects_response.data.objects:
                delete_object_response = object_storage_client.delete_object(
                namespace_name="axdvjzox0ixb",
                bucket_name=a.display_name,
                object_name=objects.name)
                print(delete_object_response.headers)
          except:
             pass
       i=i+1

       i=1
       for a in search_resources_response_bucket.data.items:                                  # Here, we are displaying all the resources we have queried
          print(i,"    ",a.display_name,"   ",a.identifier,"    ",a.resource_type)
          try:
             delete_bucket_response = object_storage_client.delete_bucket(
             namespace_name="axdvjzox0ixb",
             bucket_name=a.display_name)
             print(delete_bucket_response.headers)
             lst.append([a.display_name,a.identifier,a.resource_type,a.lifecycle_state,regions.region_name])
          except:
             pass
       i=i+1



       i=1
       for a in search_resources_response_db.data.items:                                  # Here, we are displaying all the resources we have queried
          print(i,"    ",a.display_name,"   ",a.identifier,"    ",a.resource_type)
          try:
             delete_database_response = database_client.delete_database(
             database_id=a.identifier)
             print(delete_database_response.headers)
             lst.append([a.display_name,a.identifier,a.resource_type,a.lifecycle_state,regions.region_name])
          except:
             pass       
          i=i+1


       i=1
       for a in search_resources_response_lb.data.items:                                  # Here, we are displaying all the resources we have queried
          print(i,"    ",a.display_name,"   ",a.identifier,"    ",a.resource_type)
          try:
             delete_loadbalancer_response = load_balancer_client.delete_load_balancer(
             load_balancer_id=a.identifier)
             print(delete_loadbalancer_response.headers)
             lst.append([a.display_name,a.identifier,a.resource_type,a.lifecycle_state,regions.region_name])
          except:
             pass
          i=i+1


       i=1
       for a in search_resources_response_route.data.items:                                  # Here, we are displaying all the resources we have queried
          print(i,"    ",a.display_name,"   ",a.identifier,"    ",a.resource_type)
          try:
             delete_route_table_response = core_client_net.delete_route_table(
             rt_id=a.identifier)
             print(delete_route_table_response.headers)
             lst.append([a.display_name,a.identifier,a.resource_type,a.lifecycle_state,regions.region_name])
          except:
             pass      
          i=i+1


       i=1
       for a in search_resources_response_nat.data.items:                                  # Here, we are displaying all the resources we have queried
          print(i,"    ",a.display_name,"   ",a.identifier,"    ",a.resource_type)
          try:
             delete_nat_gateway_response = core_client_net.delete_nat_gateway(            
             nat_gateway_id=a.identifier)
             print(delete_nat_gateway_response.headers)
             lst.append([a.display_name,a.identifier,a.resource_type,a.lifecycle_state,regions.region_name])
          except:
             pass      
          i=i+1

       i=1
       for a in search_resources_response_subnet.data.items:                                  # Here, we are displaying all the resources we have queried
          print(i,"    ",a.display_name,"   ",a.identifier,"    ",a.resource_type)
          try:
            delete_subnet_response = core_client_net.delete_subnet(
            subnet_id=a.identifier)
            print(delete_subnet_response.headers)
            lst.append([a.display_name,a.identifier,a.resource_type,a.lifecycle_state,regions.region_name])
          except:
            pass       
          i=i+1


       i=1
       for a in search_resources_response_sgway.data.items:                                  # Here, we are displaying all the resources we have queried
          print(i,"    ",a.display_name,"   ",a.identifier,"    ",a.resource_type)
          try:
            delete_service_gateway_response = core_client_net.delete_service_gateway(
            service_gateway_id=a.identifier)
            print(delete_service_gateway_response.headers)
            lst.append([a.display_name,a.identifier,a.resource_type,a.lifecycle_state,regions.region_name])
          except:
            pass       
          i=i+1


       i=1
       for a in search_resources_response_igway.data.items:                                  # Here, we are displaying all the resources we have queried
          print(i,"    ",a.display_name,"   ",a.identifier,"    ",a.resource_type)
          try:
            delete_internet_gateway_response = core_client_net.delete_internet_gateway(
            ig_id=a.identifier)
            print(delete_internet_gateway_response.headers)
            lst.append([a.display_name,a.identifier,a.resource_type,a.lifecycle_state,regions.region_name])
          except:
            pass       
          i=i+1


       i=1
       for a in search_resources_response_lpgway.data.items:                                  # Here, we are displaying all the resources we have queried
          print(i,"    ",a.display_name,"   ",a.identifier,"    ",a.resource_type)
          try:
            delete_local_peering_gateway_response = core_client_net.delete_local_peering_gateway(
            local_peering_gateway_id=a.identifier)
            print(delete_local_peering_gateway_response.headers)
            lst.append([a.display_name,a.identifier,a.resource_type,a.lifecycle_state,regions.region_name])
          except:
            pass       
          i=i+1



       i=1
       for a in search_resources_response_vcn.data.items:                                  # Here, we are displaying all the resources we have queried
          print(i,"    ",a.display_name,"   ",a.identifier,"    ",a.resource_type)
          try:
            delete_vcn_response = core_client_net.delete_vcn(
            vcn_id=a.identifier)
            print(delete_vcn_response.headers)
            lst.append([a.display_name,a.identifier,a.resource_type,a.lifecycle_state,regions.region_name])
          except:
            pass       
          i=i+1
df=pd.DataFrame(lst)   #Python is case sensitive
print(df)
filename=pd.ExcelWriter('Excel_lists_destroy.xlsx')
df.to_excel(filename,sheet_name=regions.region_name)
filename.save()

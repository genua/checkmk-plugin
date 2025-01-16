# checkmk-plugin
Extended Checkmk Check plugin for genua physical and virtual appliances.

## Description
Extends the existing genua checks for more genua products and with extended capabilities

## Products covered
genuscreen, genubox (as rendezvous or service box), genucenter, genugate

### General features:
* genua specific labels are detected and added automatically
* The inventory now includes a genua section with product type, SW & HW version, type, licence key, serial number
* SNMP Info service provides product details

### genugate features
* genugate monitoring added
* New PFL Status service
* New NTP Synchronization service

### genucenter features
* genucenter monitoring added with appliance and operation system information
  
### genubox features
* New Swap service
* New fbzs service lists all existing and open connections
* New Sessions service 
* New ServiceBox Info
* New ServiceBox CPU
* New ServiceBox Memory
* The last 3 services show the information published by this Service Box. On a Rendezvous Box, all connected Service Boxes are listed. This allows you to monitor them via the Rendezvous Box in case they are unreachable.

## Change log:
v1.0.0 First release of the extended genua checks

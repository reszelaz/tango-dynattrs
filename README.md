# Project to reproduce Sardana issue with highly dynamic attributes

Code is authored by Henrik Enquist from MAXIV

To repduce the issue:

1. Create the necessary elements in the Tango DB:
```
tango_admin --add-server BuggyDS/test BuggyDS test/buggyds/1    
tango_admin --add-server BuggyDS/test BuggyDS test/buggyds/2
tango_admin --add-property test/buggyds/1 AorB A
tango_admin --add-property test/buggyds/1 AorB B
```
2. Start the server:
```
python3 buggyds.py test
```
3. You will get the following exception:
```
zreszela@pc255:~/workspace/tango-dynattrs (main)> python3 buggyds.py zreszela
Create dynamic attribute: SecondValue                                                                                                      
Create dynamic attribute: ThirdValue                                                                                                       
Create dynamic attribute: FirstValue                                                                                                       
Create dynamic attribute: FirstValue                                                                                                       
DevFailed[                                                                                                                                 
DevError[                                                                                                                                  
    desc = Device test/zreszela/buggyds-02 -> Attribute FirstValue already exists for your device class but with other definition          
           (data type, data format or data write type)                                                                                     
  origin = DeviceImpl::add_attribute                                                                                                       
  reason = API_AttrNotFound                                                                                                                
severity = ERR]                                                                                                                            
]
```

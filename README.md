# Configuration As Code
***Companion Repository to [Kill the CLI](https://gratuitous-arp.net/kill-the-cli/) - Example of Configuration Templates***

There is nothing new about configuration templates. One way or another we all have them.   

They may live on the last device we configured, in a Notepad file (groan), in Excel (not sure which is worse), 
in a Word document (OK this is worse..at least Notepad is text), or in a code repository similar to what I am showing here.

This GitHub repository is the companion repository to the [Kill the CLI](https://gratuitous-arp.net/kill-the-cli/) post on The Gratuitous Arp.  It is intended to showcase an example of what can be done with "configuation as code" to get you one step closer to infrastructure as code.

This example represents a small step towards getting your configuration templates ready for Automation.  Even if you are not interested in Network Automation (in which case Im afraid you've stumbled into the wrong neighborhood), using a revision control system to track the changes to your templates overtime is in and of itself powerful and saves you some heavy lifting. 

Who changed the port channel mode  to LACP? to LACP active? When was that change made?  Who has the latest template?  All questions easily answered when your configuration templates are under revision control and in a revision control system.  GitHub and GitLab are some of the more recognizable and odds are a revision control system is already deployed in your Enterprise.

![Commit History](/Users/claudiadeluna/Indigo Wire Networks Dropbox/Claudia de Luna/scripts/articles/2023/Kill_The_CLI/images/commit_history.png)

This repository takes a very basic configuration activity, configuring vPCs on Cisco Nexus switches,  and shows you the template under revision control AND with logic to easily generate configuations for one or more vPCs with varying numbers of interfaces in the port-channel.  In addition, it leverages a YAML file to store the "design" or "configuration details" needed to generate this configuration.  Further, it attempts to take away some of the personal variation you can see with this type of configuration.  

In the Python script which generates the configlet you can see the implementation of the guidelines in a consistent and reproducable manner.

Once you have this, its a simple matter to save the actual commands in a format which can then be pushed to the device.  More is needed to do that step with confidence but this is a start.  At least this is how I got started.  Production versions of this have more error checking PRE and POST.   The update and rollback commands are saved to JSON files which can then be loaded into a framework to push the commands.  But this little text file still comes in very handy for change control  as it has most of the information needed for change control. 

- Devices (CIs)
- Change Summary and Actual Commands
- Verification
- Rollback

```

! ==================================================================
! Cisco Nexus VPC Design Details
! core01_02_devs_ports45-48
! cisco_nexus_vpc_intf_template.j2
! 
! Configlet Generated: 20-12-2023  060837
! ==================================================================


! ++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++
! Primary Device: core01 Secondary Device: core02
! Connecting To: Access1
no int port-channel1045
interface port-channel1045
  description TO Access1
  switchport
  switchport mode trunk
  switchport trunk allowed vlan add 10
  switchport trunk allowed vlan add 20
  switchport trunk allowed vlan add 30
  spanning-tree port type network
  vpc 1045
  shutdown
  

default int Ethernet1/45
interface Ethernet1/45
  description TO Access1
  switchport
  switchport mode trunk
  switchport trunk allowed vlan add 10
  switchport trunk allowed vlan add 20
  switchport trunk allowed vlan add 30
  channel-group 1045 mode active
  shutdown
  

!
! ------------------------------------------------------------------
! VERIFICATION COMMANDS

show vpc 1045
show port-channel summary interface port-channel1045
show int status | i 1045

show spanning-tree vlan 10
show spanning-tree vlan 20
show spanning-tree vlan 30
!
! ------------------------------------------------------------------
! ROLLBACK COMMANDS

no int port-channel1045
default int Ethernet1/45


! ++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++
! Primary Device: core01 Secondary Device: core02
! Connecting To: Access2
no int port-channel1046
interface port-channel1046
  description TO Access2
  switchport
  switchport mode trunk
  switchport trunk allowed vlan add 10
  switchport trunk allowed vlan add 20
  switchport trunk allowed vlan add 30
  spanning-tree port type network
  vpc 1046
  shutdown
  

default int Ethernet1/46, Ethernet1/47
interface Ethernet1/46, Ethernet1/47
  description TO Access2
  switchport
  switchport mode trunk
  switchport trunk allowed vlan add 10
  switchport trunk allowed vlan add 20
  switchport trunk allowed vlan add 30
  channel-group 1046 mode active
  shutdown
  

!
! ------------------------------------------------------------------
! VERIFICATION COMMANDS

show vpc 1046
show port-channel summary interface port-channel1046
show int status | i 1046

show spanning-tree vlan 10
show spanning-tree vlan 20
show spanning-tree vlan 30
!
! ------------------------------------------------------------------
! ROLLBACK COMMANDS

no int port-channel1046
default int Ethernet1/46, Ethernet1/47


! ++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++
! Primary Device: core01 Secondary Device: core02
! Connecting To: Access3
no int port-channel1048
interface port-channel1048
  description TO Access3
  switchport
  switchport mode trunk
  switchport trunk allowed vlan add 100
  switchport trunk allowed vlan add 200
  switchport trunk allowed vlan add 300
  spanning-tree port type network
  vpc 1048
  no shutdown
  

default int Ethernet1/48
interface Ethernet1/48
  description TO Access3
  switchport
  switchport mode trunk
  switchport trunk allowed vlan add 100
  switchport trunk allowed vlan add 200
  switchport trunk allowed vlan add 300
  channel-group 1048 mode active
  no shutdown
  

!
! ------------------------------------------------------------------
! VERIFICATION COMMANDS

show vpc 1048
show port-channel summary interface port-channel1048
show int status | i 1048

show spanning-tree vlan 100
show spanning-tree vlan 200
show spanning-tree vlan 300
!
! ------------------------------------------------------------------
! ROLLBACK COMMANDS

no int port-channel1048
default int Ethernet1/48




! ==================================================================
! CONFIGLET END

```

If you are considering putting your templates in a revision control system I hope this helps get you started!


<a title="MIchael Schmid, CC BY-SA 3.0 &lt;https://creativecommons.org/licenses/by-sa/3.0&gt;, via Wikimedia Commons" href="https://commons.wikimedia.org/wiki/File:Meridional%2BSaggittalEbene_1.svg" style="display:block;" align="right"><img width="256" alt="Meridional+SaggittalEbene 1" src="https://upload.wikimedia.org/wikipedia/commons/thumb/3/3e/Meridional%2BSaggittalEbene_1.svg/512px-Meridional%2BSaggittalEbene_1.svg.png?20220226121202" align="right" style="display:block;"></a>

# Python-based Automation for Fast Modeling of Production Arista Switches in GNS3


I wrote this specifically to assist in *fast* modeling of a production EVPN Layer-3 Leaf & Spine physical network of Arista switches in a pre-existing GNS3 server, using Arista cEOS docker images.  It needs to be executed on the same Linux host that the GNS3 server is running on.

## Requirements

- Python 3.6 or...
  - ...or you take your chances
- GNS3 server
  - version 2.2 (or you takes your chances)
  - With Docker installed
    - With Arista cEOS images installed
  - With the cEOS images defined as GNS templates that have been named 'ceos:' + *[version-number]*
    - Where *[version-number]* is the EOS version number returned in "show version" output on an EOS device
  - ...or you take your chances
  - "ceos:" followed-by the version-number 
  - sudo permissions on the Linux host running GNS3 server
    - Maybe(?) - I worked this up with a RHEL8 instance that GNS3 had been "less than gently" installed on, and couldn't get around GNS3 assigning ownership of every project folder to root.  I doubt that's a typical problem, but I had to work around it.

## Instructions

### Prep

- Get your GNS3 server up and running on a Linux host.
- Have your login credentials for your production switches handy
- Make sure that your production switches can receive eAPI connections from your GNS3 server
- Copy gns3-dcod.py and gns3-dcod-config-mover.py onto a convenient directory on your GNS3 server
  - Make them both executable ('chmod +x ./gns3-dcod.py' and 'chmod +x ./gns3-dcod-config-mover.py' from the directory that you copied them into )
- Create a file named "input-switch-list" in the same directory that you installed the .py files
  - Populate 'input-switch-list' with the names of the switches that you want to model in gns3

### Go time!

- Enter: './gns3-dcod.py' from the directory you created the files in
- Follow the prompts
  - You'll be prompted for username/password credentials to authenticate to the switches for eAPI calls
  - You'll be prompted to provide a project name for GNS3
- Wait for the completion message at the shell-session that you executed gns3-dcod.py from
- Open your new GNS3 project, turn the virtual-switches on, and have fun.
  - You'll have to access the switches using the "auxiliary console" created in the GNS3 client

## The files

## Executables

### gns3-dcod.py

- Grabs startup configuration, version info, and lldp neighbor information from the list of Arista switches in 'input-switch-list'
- Prompts for username/password and a name to use for the GNS3 project file
- Uses Arista eAPI to retrieve all data
- Sanitizes the switch configs for use in a cEOS environment
- Removes all AAA and username configuration
- Reformats interface names to match the cEOS interface naming convention  (Ethernet_n_ , not Ethernt_n_/1)
- Comments out incompatible commands ("queue..." not supported on cEOS)
- Configures a matching system mac-address to
  - Increase verisimilitude with prod device that is being modeled
  - Avoid mLAG incompatibility with cEOS
    - Docker container default mac address has U/L bit set to L instead of U
- Builds a table of interconnections between the switches
  - From the lldp neighbor and startup config data
- Creates a GNS3 project
  - Creates models of all of the switches from 'input-switch-list' in the new GNS3 project
  - Modeled devices matches cEOS versioning, interface count, and system-mac-address
- Creates the interconnects between all of the cEOS switches in the previous step
- Invokes 'gns3-dcod-config-mover.py' to copy the converted device configurations into the GNS3 project folder and into the modeled devices.

### gns3-dcod-config-mover.py

- Copies the converted device configurations into the GNS3 project folder and into the modeled devices.
- Separate file so that it can be invoked with sudo, due to GNS3 creating every single project folder as root.

## Inputs

### input-switch-list

- You must populate this file manually
- A list of switches that you want included in the model.
- Enter one FQDN per line.
  - The logic that scrapes LLDP neighbor information depends on the names in the input-switch-list file matching the names reported in the LLDP neighbor information

## Outputs

### outfiles/

- New directory created in the path you executed gns3.dcod.py from
- Temporarily hosts (the sanitized copies of) the configuration files of the switches to be emulated
- Temporarily hosts a file with a list of required details for each switch (most importantly the docker overlay file-system path to copy the config file of each switch into)

### GNS Project

- A GNS3 project containing the switches that you're emulating
  - Including any physical links between them that were discovered in LLDP tables

### Docker containers

- GNS3 creates a docker container for switch being emulated (in response to API calls from gns3-dcod.py)

To ensure reproducibility , we have used make.

While installing make in workspaces , there might be issues related to it's installation.

Follow the below steps to install it properly.

This approach has two steps :

* Installing Chocolatey package installer.
* Installing make using chocolatey package manager. 

# Installing Chocolatey package installer.

To install make , we will be using chocolatey package installer. Chocolatey is a software management automation tool for Windows that wraps installers, executables, zips, and scripts into compiled packages.

* Navigate to [Official page of chocolatey package installer.](https://chocolatey.org/install)

* Execute the below command in Windows Powershell (Administrator mode).

<img src= "figs/markdown_images/script.png">

This will install chocolatey package installer in the amazon workspaces.

To verify if it is properly installed or not , run the below command in the powershell.
```
choco
```
The output must be :

```
Chocolatey v2.4.0
Please run 'choco -?' or 'choco <command> -?' for help menu.
```

Although the version can change , but if you get a similar output , they Chocolatey package installer is successfully installed.

# 

# Installing make using chocolatey package manager

Now since we have the package installer installed , we can use it to install make.

To do this execute the below command in Windows Powershell (Admin Mode) :

```
choco install make
```

This will install make successfully.

To verify this , open a terminal or Git Bash or Powershell and type the below command :

```
make 
```

You will get the following command that will ensure that make files can be executed properly.

```
make: *** No targets specified and no makefile found.  Stop.
```

Sometimes the changes might not reflect , to do this , restart the terminal or Git Bash or Powershell for the changes to take effect.
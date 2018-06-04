**************************
SSH Keys
**************************

This is a basic introduction to SSH keys, and how to set them up.

Included in here is a sample SSH `config` file that astronomers at Swinburne 
might use to access g2 or ozstar.

To use copy the `config` file to the `.ssh` directory.
`cp config ~/.ssh/`

Replace `USERNAME` in the files to your username.

Since to get to sstar001, you have to first SSH to g2,
we can set up a `ProxyCommand` which allows us to automatically SSH into 
g2 then into sstar001. 


Author
--------------------------------------------------------
Adam Batten `email <mailto:abatten@swin.edu.au>`_


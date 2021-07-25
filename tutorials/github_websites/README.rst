===============================
Creating a website using Github
===============================

Author: Adam Batten
Year: 2018

Step 0: Create a Github Account
"""""""""""""""""""""""""""""""
This one is pretty obvious.

Step 1: Create Github Repository
""""""""""""""""""""""""""""""""
Create an empty repository on Github with the name ``<USERNAME>.github.io``.

i.e if your username is jsmith, then you create a repository called ``jsmith.github.io``

Make sure that this repository is public. The name of this repository will also be the url to the website. i.e. https://jsmith.github.io

Step 2: Find a website template
"""""""""""""""""""""""""""""""
You could write your own html and css if you like. But there are plenty of templates out there so you don't have to. My favourites are from: https://html5up.net/.

Check out: Prologue, Editorial, Strata, Phantom, Strongly Typed, Escape Velocity. They might be some good starting point, but really anyone of them are good.

HTML5up websites also have the benefit of being designed to adapt to the type of device that you are using, so you don't have to think about it.

Download any template to start with.

In the future there are tools like Jekyll, which could make your website life easier.

Step 3: Make local repository
"""""""""""""""""""""""""""""
Create a folder on your computer with the same name as the one you created on github. i.e ``jsmith.github.io``. This will be the location of file for the website.

Step 4: Put template in local repository
""""""""""""""""""""""""""""""""""""""""
Extract the selected template into the repository you created onto your local machine. There should be a file called ``index.html``.

Step 5: Git add/commit/push to remote
"""""""""""""""""""""""""""""""""""""
Now to push the website template to github. You will need to add the remote repository as the origin.:

.. code:: bash

  git init
  git remote add origin https://github.com/<USERNAME>/<USERNAME>.github.io

Then commit and push to the origin.:

.. code:: bash 

  git add -A
  git commit -m "Initial commit of my website"
  git push origin master


You should now be able to go to the url ``<USERNAME>.github.io`` and view your website.

Note: Sometimes that doesn't work and you see a blank page. 

To fix this go to settings > options. Click "Choose a Theme" in the Github Pages section. Then click "Select Theme" (It doesn't matter what you select). Then it should work when you go to ``<USERNAME>.github.io``.

Step 6: Modifying the template
""""""""""""""""""""""""""""""
Obviously you are going to modify the template. This can be done by editing the index.html file. index.html is the home page of the website. Some themes come with additional pages such as generic.html or elements.html. 

generic.html: This is a generic additional page for your website, you can duplicate this to make many pages.

elements.html: This page lists a bunch of different icons, buttions and objects you can add to your website. By looking at the htlm you can work out how to use them.



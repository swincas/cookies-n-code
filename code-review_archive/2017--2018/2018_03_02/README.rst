*************************************
Getting Started with Version Control
*************************************

How to track changes to one or multiple files over time -- version control.

The current presentation talking about git and Github is `here (pdf) <VersionControlWithGitAndUsingGithub.pdf>`_

(The previous presentation with mercurial is `here (pdf) <VersionControlWithGitAndMercurial.pdf>`_


********************
Sample .gitconfig
********************

::

	[user]
	  name = Your Name
	  email = your_email_address

	[credential]
	  helper = osxkeychain

	[core]
	  excludesfile = ~/.gitignore
	  filemode = true

	[branch]
	  autosetupmerge = true

	[url "https://"]
	  insteadOf = git://

	[alias]
	  dfw = diff --ignore-space-change
	  st  = status
	  lgp = "log -p"
	  lg = "log --format='%Cred%h%Creset %s %Cgreen(%cr) %C(blue)<%an>%Creset%C(yellow)%d%Creset' --no-merges"
	  unstage = reset -q HEAD --
	  discard = checkout --
	  uncommit = reset --mixed HEAD~
	  amend = commit --amend
	  nevermind = !git reset --hard HEAD && git clean -d -f
	  graph = log --graph -10 --branches --remotes --tags  --format=format:'%Cgreen%h %Creset# %<(75,trunc)%s (%cN, %cr) %Cred%d' --date-order
	  precommit = diff --cached --diff-algorithm=minimal -w
	  branches = branch -a
	  tags = tag
	  stashes = stash list

	[color]
	  diff = auto
	  status = auto
	  branch = auto
	  interactive = auto
	  ui = true

	[color "branch"]
	  current = yellow reverse
	  local = yellow
	  remote = green

	[color "diff"]
	  meta = blue bold
	  frag = magenta bold
	  old = red bold
	  new = green bold

	[color "status"]
	  added = green
	  changed = yellow
	  untracked = cyan

	[push]
	  default = matching

.. 

Author
--------------------------------------------------------
Manodeep Sinha `email <mailto:manodeep@gmail.com>`_

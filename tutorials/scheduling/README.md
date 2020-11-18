# Cron Syntax

Specify the schedule using the following syntax. Cron will run the command at the start of the minute whenever the datetime matches with the specified schedule.

minute hour day_of_month month_of_year day_of_week command

[Crontab.guru - The cron schedule expression editor](https://crontab.guru/)

Make sure to check the *timezone* of the machine if you're using a remote server.

## Time shortcuts

You can use shortcuts instead of the 5 tokens.

@yearly, @monthly, @weekly, @daily, @hourly

@reboot - when system starts up

## Staggering events

When there are many scheduled tasks, it's common to pick a time that's not on the hour so that they do not all start at the same time and slow the system down. For example, schedule your backup at 03:47 instead of 00:00.

This isn't possible with the time shortcuts, as they start at minute 0 (although you could always add a sleep to the start of the command).

## Editing crontab

Each user has their own crontab.

Don't edit the cron file directly, instead use the crontab command

```bash
crontab -l # show your crontab
crontab -e # edit your crontab
crontab -ri # delete your crontab
```

## Commands

Commands are run with the priveleges of the user account that the crontab file corresponds to.

It does not have the full `PATH` and does not source your .bashrc or anything so use the FULL PATH to all executables/scripts.

It just uses sh not bash

You can add `SHELL=/bin/bash` at the top of the crontab to use bash

It's quite useful to string multiple commands together for simple things such as `cd` before running the command that do not warrent making a dedicated script for. Keep in mind that `&&` will stop if the first part fails whereas `;` will keep running regardless.

### Python environments for conda/virtualenv

Because `source` is a **bash** build-in and cron uses sh by default, use `.` instead for activating the environment. Remember to use the full path and probably cd to the project path.

### Output and mail

If you are getting "you have mail" when logging in or opening a shell, you can suppress output from commands by sending stdout to a file or  `> /dev/null`

# When not to use cron

- when your computer is not on all the time - use anacron
- when it needs to run more than every minute - use a daemon. see celery beat
- When it's not related to a specific machine - use cloud eg. github actions
- when it needs retry logic
- to start services that need to run all the time. Use an actual service manager such as systemd that can restart it if it fails

# Monitoring if you need to be notified of failure

crontab.guru links to a service that can notify you if a command doesn't run when expected or fails.

[Cron Monitoring & Uptime Monitoring for Busy Developers - Cronitor](https://cronitor.io/)
### Handy script to enable autocomplete when typing ssh commands (with hostnames in .ssh/config files)
### Copy this script to your $HOME directory to use
# SSH
function _ssh_completion() {
egrep -o '^Host [-a-zA-Z]+' $HOME/.ssh/config | awk '{print $2}'
}
complete -W "$(_ssh_completion)" ssh

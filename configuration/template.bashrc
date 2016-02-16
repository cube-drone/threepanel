# ~/.bashrc: executed by bash(1) for non-login shells.
# see /usr/share/doc/bash/examples/startup-files (in the package bash-doc)
# for examples

# don't put duplicate lines or lines starting with space in the history.
# See bash(1) for more options
HISTCONTROL=ignoreboth

# append to the history file, don't overwrite it
shopt -s histappend

# for setting history length see HISTSIZE and HISTFILESIZE in bash(1)
HISTSIZE=3000
HISTFILESIZE=5000

# check the window size after each command and, if necessary,
# update the values of LINES and COLUMNS.
shopt -s checkwinsize

# If set, the pattern "**" used in a pathname expansion context will
# match all files and zero or more directories and subdirectories.
#shopt -s globstar

alias ls='ls --color=auto'
alias grep='grep --color=auto'
alias fgrep='fgrep --color=auto'
alias egrep='egrep --color=auto'
alias ll='ls -alF'
alias la='ls -A'
alias l='ls -CF'

export PYTHONPATH=${DJANGO_PATH}
source ${VIRTUALENV_PATH}/bin/activate
alias dj='python3 ${DJANGO_PATH}/manage.py'
alias in='cd ${DJANGO_PATH} && invoke'

export DJANGO_PROJECT_SLUG="${DJANGO_PROJECT_SLUG}"
export DJANGO_DEBUG="${DJANGO_DEBUG}"
export DJANGO_DOMAIN="${DJANGO_DOMAIN}"
export DJANGO_ADMIN_NAME="${DJANGO_ADMIN_NAME}"
export DJANGO_ADMIN_EMAIL="${DJANGO_ADMIN_EMAIL}"
export MANDRILL_KEY="${MANDRILL_KEY}"
export DJANGO_SECRET_KEY="${DJANGO_SECRET_KEY}"
export POSTGRES_DB_PASSWORD="${POSTGRES_DB_PASSWORD}"
export PAPERTRAIL_SERVER="${PAPERTRAIL_SERVER}"

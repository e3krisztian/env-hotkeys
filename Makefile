REQUIRED_PACKAGES=wmctrl ratmenu python-daemon xbindkeys xbindkeys-config

LN=ln --symbolic --force --verbose

.PHONY: check install

check:
	dpkg --status $(REQUIRED_PACKAGES) 2>&1 | \
	  egrep '^(Package|Status)' | \
	  sed -e 's/^P/\nP/' -e 's/^S/  S/'; echo

install:
	sudo apt-get install $(REQUIRED_PACKAGES)
	$(LN) --backup=existing $(PWD)/dot.xbindkeysrc ~/.xbindkeysrc
	$(LN) $(PWD)/focus-* ~/bin
	$(LN) $(PWD)/raise-or-exec.py ~/bin/raise-or-exec

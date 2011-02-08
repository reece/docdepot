.SUFFIXES:
.PHONY: FORCE
.DELETE_ON_ERROR:


default:
	@echo "There ain't no stinkin' $@ rule, cowboy" 1>&2; exit 1


.PHONY: clean cleaner cleanest
clean:
	find . -name '*~' -print0 | xargs -0 rm -fv
cleaner: clean
	find . -name '*Case Conflict*' -print0 | xargs -0 rm -fv
cleanest: cleaner
	find . -name '*pyc' -print0 | xargs -0 rm -fv

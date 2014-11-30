PYBLUE_PAGES=../pyblue-pages
all:
	#
	# Edit the documentation
	#
	pyblue serve -r docs -v

pages:
	#
	# Generates documentation into a GitHub Page repository
	#
	pyblue make -r docs -o ${PYBLUE_PAGES}
	cd ${PYBLUE_PAGES} && git commit -am "updated the docs" && git push
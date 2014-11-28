
all:
	#
	# Edit the documentation
	#
	pyblue serve -r docs

doc:
	#
	# Generates documentation into a GitHub Page repository
	#
	pyblue make -r docs -o ../pyblue-pages
	cd ../pyblue-pages
	git commit -am "updated the docs"
	git push
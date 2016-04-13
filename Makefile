# The repository that contains the GITHUB pages checkout
GITHUB_PAGES=../pyblue-ghpages

all: docs

README.rst: README.md
	# PyPi accepts only rst files in long description.
	echo pandoc README.md -o README.rst

rst: README.rst

docs:
	# View the documentation.
	pyblue serve -r docs -v

pypi: rst
	#python setup.py sdist upload
	echo done

pages: rst
	# Generate/commit/push documentation into the GitHub Page repository.
	echo cd ${GITHUB_PAGES} && git pull
	echo pyblue -r docs -o ${GITHUB_PAGES}
	echo cd ${GITHUB_PAGES} && git commit -am "updated the docs" && git push
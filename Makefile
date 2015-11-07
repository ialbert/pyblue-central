# The repository that contains the GITHUB pages checkout
GITHUB_PAGES=../pyblue-pages

all: docs

README.rst: README.md
	# PyPi accepts only rst files in long description.
	pandoc --from=markdown --to=rst README.md -o README.rst

rst: README.rst

docs:
	# View the documentation.
	pyblue serve -r docs -v

pypi:
	# Push out to PyPI.
	#pandoc --from=markdown --to=rst README.md -o README.rst
	python setup.py sdist upload

pages: rst
	# Generate/commit/push documentation into the GitHub Page repository.
	cd ${GITHUB_PAGES} && git pull
	pyblue make -r docs -o ${GITHUB_PAGES}
	cd ${GITHUB_PAGES} && git commit -am "updated the docs" && git push
# The repository that contains the GITHUB pages checkout
GITHUB_PAGES=../pyblue-ghpages

all:
	pyblue -r docs

README.rst: README.md
	# Generate .rst from .md
	# PyPi accepts only rst files in long description.
	pandoc README.md -o README.rst

rst: README.rst

docs:
	# View the documentation.
	pyblue serve -r docs -v

pypi: rst
#	python setup.py sdist bdist_wheel
	twine upload dist/*

pages: rst
	# Generate/commit/push documentation into the GitHub Page repository.
	cd ${GITHUB_PAGES} && git pull
	pyblue -v -r docs --no-time -o ${GITHUB_PAGES}
	cd ${GITHUB_PAGES} && git commit -am "updated the docs" && git push

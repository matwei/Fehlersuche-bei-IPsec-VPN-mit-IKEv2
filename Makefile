# Minimal makefile for Sphinx documentation
#

# You can set these variables from the command line.
SPHINXOPTS    =
SPHINXBUILD   = sphinx-build
SPHINXPROJ    = FehlersuchebeiIKEv2IPsecVPN
SOURCEDIR     = source
BUILDDIR      = build

SOURCE = source/einfuehrung.rst \
	 source/grundlagen/index.rst \
	 source/grundlagen/paketmitschnitt.rst \
	 source/grundlagen/theoretisch.rst \
	 source/ikev2/ueberblick.rst \
	 source/ikev2/betriebsarten.rst \
	 source/ikev2/nachrichten.rst \
	 source/vorgehen/fragen.rst \
	 source/vorgehen/antworten.rst \
	 source/fehler/index.rst \
#
DRAFTS = build/draft/einfuehrung-draft.pdf \
	 build/draft/grundlagen/index-draft.pdf \
	 build/draft/grundlagen/paketmitschnitt-draft.pdf \
	 build/draft/grundlagen/theoretisch-draft.pdf \
	 build/draft/ikev2/ueberblick-draft.pdf \
	 build/draft/ikev2/betriebsarten-draft.pdf \
	 build/draft/ikev2/nachrichten-draft.pdf \
	 build/draft/vorgehen/fragen-draft.pdf \
	 build/draft/vorgehen/antworten-draft.pdf \
	 build/draft/fehler/index-draft.pdf \
#

build/draft/%-draft.pdf: source/%.rst; pandoc -o $@ --variable subparagraph -H pandoc/draft.tex $<

# Put it first so that "make" without argument is like "make help".
help:
	@$(SPHINXBUILD) -M help "$(SOURCEDIR)" "$(BUILDDIR)" $(SPHINXOPTS) $(O)

.PHONY: help Makefile $(SOURCE)

epub: Makefile
	$(SPHINXBUILD) -M epub "$(SOURCEDIR)" "$(BUILDDIR)" $(SPHINXOPTS) $(O)

latexpdf: Makefile
	$(SPHINXBUILD) -M latexpdf "$(SOURCEDIR)" "$(BUILDDIR)" $(SPHINXOPTS) $(O)

draftpaths:
	[ -d build/draft/grundlagen ] || mkdir -p build/draft/grundlagen
	[ -d build/draft/ikev2 ] || mkdir -p build/draft/ikev2
	[ -d build/draft/vorgehen ] || mkdir -p build/draft/vorgehen
	[ -d build/draft/fehler ] || mkdir -p build/draft/fehler

draft: draftpaths $(DRAFTS)
	
# Catch-all target: route all unknown targets to Sphinx using the new
# "make mode" option.  $(O) is meant as a shortcut for $(SPHINXOPTS).
%: Makefile
	@$(SPHINXBUILD) -M $@ "$(SOURCEDIR)" "$(BUILDDIR)" $(SPHINXOPTS) $(O)


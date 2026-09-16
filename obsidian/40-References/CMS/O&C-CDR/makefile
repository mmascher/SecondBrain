TEX = pdflatex
main = main
src = *.tex $(wildcard tex/*tex)
FLAGS = -interaction=nonstopmode

main.pdf : $(src)
	$(TEX) $(main).tex $(FLAGS)
	bibtex $(main)
	makeglossaries $(main)
	$(TEX) $(main).tex $(FLAGS)
	$(TEX) $(main).tex $(FLAGS)

.PHONY: clean texclean
texclean :
	rm -rf *.aux *.log *.out *.toc *.acr *.alg *.acn *.glo *.ist *.glg *.gls *.bbl *.blg
clean : texclean
	rm -f $(main).pdf

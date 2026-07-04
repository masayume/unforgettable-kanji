#!/bin/bash

### how to install xelatex with chinese characters support
### sudo apt-get install texlive-xetex latex-cjk-all


pandoc  chapters/00-cover.md   \
		chapters/00-title.md   \
		chapters/01-introduction.md   \
		chapters/02-school.md   \
		chapters/03-feelings.md   \
		chapters/04-space.md   \
		chapters/05-hard.md   \
		chapters/20-counters.md   \
-o book.pdf 	\
--pdf-engine=xelatex \
-V CJKmainfont="Noto Sans CJK SC" \
-V geometry:margin=2cm
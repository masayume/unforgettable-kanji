#!/bin/bash

### How to install xelatex with chinese characters support
### sudo apt-get install texlive-xetex latex-cjk-all

# firefox: https://gemini.google.com/app/c9605be629883976 		

### Useful links
# 	https://gemini.google.com/app/c9605be629883976 	pandoc/latex format
# 	https://gemini.google.com/app/ab20670ca488c210 	kanji info
# 	https://jisho.org/search/季%20%23kanji 			
# 	https://livellosegreto.it/@kanjioftheday@c.im/116839652208594928

### Quick page formatting:
#	On\'yomi: ジュ (JU)
#	Kun\'yomi: _KUNYOMI_
#	\vspace{2cm}
#	\newpage

#		chapters/00-title.md   \
#		chapters/02-school.md   \
#		chapters/03-feelings.md   \
#		chapters/04-space.md   \
#		chapters/05-hard.md   \
#		chapters/06-body.md   \
#		chapters/07-time.md   \
#		chapters/20-counters.md   \


pandoc  chapters/00-cover.md   \
		chapters/01-introduction.md   \
		chapters/02-school.md   \
		chapters/03-feelings.md   \
		chapters/04-space.md   \
		chapters/05-hard.md   \
		chapters/06-body.md   \
		chapters/07-time.md   \
-o book.pdf 	\
--pdf-engine=xelatex \
-V CJKmainfont="Noto Sans CJK SC" \
-V geometry:margin=2cm
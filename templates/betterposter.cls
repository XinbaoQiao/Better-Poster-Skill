%%%% Better Poster Skill class
%%%% Clean-room Better Poster implementation inspired by Rafael Bailo's betterposter-latex-template.
%%%% Original poster concept: Mike Morrison's #betterposter.
\NeedsTeXFormat{LaTeX2e}
\ProvidesClass{betterposter}[2026/06/03 Better Poster Skill class]

\LoadClass{article}
\RequirePackage{geometry}
\geometry{a0paper,landscape,margin=0in}
\RequirePackage[T1]{fontenc}
\RequirePackage[utf8]{inputenc}
\RequirePackage{graphicx}
\RequirePackage{xcolor}
\RequirePackage{enumitem}
\RequirePackage{ragged2e}
\RequirePackage{amsmath,amssymb}
\RequirePackage{ifthen}
\RequirePackage[hidelinks]{hyperref}
\IfFileExists{lato.sty}{\RequirePackage[default]{lato}}{\RequirePackage{lmodern}}

\renewcommand{\familydefault}{\sfdefault}
\pagestyle{empty}
\setlength{\parindent}{0pt}
\setlist[itemize]{nosep,leftmargin=1.1em}
\setlist[enumerate]{nosep,leftmargin=1.15em}
\setlength{\fboxsep}{0pt}
\setlength{\fboxrule}{0pt}

\definecolor{imperialblue}{RGB}{0,62,116}
\definecolor{empirical}{RGB}{0,77,64}
\definecolor{theory}{RGB}{26,35,126}
\definecolor{methods}{RGB}{140,22,22}
\definecolor{intervention}{RGB}{255,213,79}
\definecolor{plum}{RGB}{88,28,135}
\definecolor{aurora}{RGB}{4,78,99}
\definecolor{sidebarcool}{RGB}{247,249,252}
\definecolor{mutedgray}{RGB}{105,111,119}

\newcommand{\columnbackgroundcolor}{white}
\newcommand{\columnfontcolor}{black}
\newcommand{\maincolumnbackgroundcolor}{imperialblue}
\newcommand{\maincolumnfontcolor}{white}
\newcommand{\posteraccentcolor}{imperialblue}

\newlength{\leftbarwidth}
\newlength{\rightbarwidth}
\newlength{\columnmarginvertical}
\newlength{\columnmarginhorizontal}
\newlength{\maincolumnmarginvertical}
\newlength{\maincolumnmarginhorizontal}
\newlength{\postercontentheight}
\newlength{\postercenterwidth}
\newlength{\postertempwidth}

\setlength{\leftbarwidth}{0.20\paperwidth}
\setlength{\rightbarwidth}{0.20\paperwidth}
\setlength{\columnmarginvertical}{0.025\paperheight}
\setlength{\columnmarginhorizontal}{0.025\paperheight}
\setlength{\maincolumnmarginvertical}{0.070\paperheight}
\setlength{\maincolumnmarginhorizontal}{0.070\paperheight}
\setlength{\postercontentheight}{\textheight}

\newcommand{\fontsizestandard}{\fontsize{32.00}{50.50}\selectfont}
\newcommand{\fontsizemain}{\fontsize{116.00}{220.00}\selectfont}
\newcommand{\fontsizetitle}{\fontsize{80.00}{120.00}\selectfont}
\newcommand{\fontsizeauthor}{\fontsize{48.00}{68.00}\selectfont}
\newcommand{\fontsizesection}{\fontsize{48.00}{68.00}\selectfont}
\newcommand{\fontsizecaption}{\fontsize{24.00}{31.00}\selectfont}
\newcommand{\fontsizesmall}{\fontsize{22.00}{30.00}\selectfont}

\DeclareOption{a2paper}{%
  \geometry{a2paper,landscape,margin=0in}%
  \renewcommand{\fontsizestandard}{\fontsize{16.00}{25.00}\selectfont}%
  \renewcommand{\fontsizemain}{\fontsize{58.00}{110.00}\selectfont}%
  \renewcommand{\fontsizetitle}{\fontsize{40.00}{50.00}\selectfont}%
  \renewcommand{\fontsizeauthor}{\fontsize{24.00}{34.00}\selectfont}%
  \renewcommand{\fontsizesection}{\fontsize{24.00}{34.00}\selectfont}%
  \renewcommand{\fontsizecaption}{\fontsize{12.00}{16.00}\selectfont}%
  \renewcommand{\fontsizesmall}{\fontsize{11.00}{15.00}\selectfont}%
}
\DeclareOption{a1paper}{%
  \geometry{a1paper,landscape,margin=0in}%
  \renewcommand{\fontsizestandard}{\fontsize{22.63}{35.36}\selectfont}%
  \renewcommand{\fontsizemain}{\fontsize{82.02}{155.56}\selectfont}%
  \renewcommand{\fontsizetitle}{\fontsize{56.57}{70.71}\selectfont}%
  \renewcommand{\fontsizeauthor}{\fontsize{33.94}{48.08}\selectfont}%
  \renewcommand{\fontsizesection}{\fontsize{33.94}{48.08}\selectfont}%
  \renewcommand{\fontsizecaption}{\fontsize{16.97}{24.04}\selectfont}%
  \renewcommand{\fontsizesmall}{\fontsize{15.56}{21.21}\selectfont}%
}
\DeclareOption{a0paper}{\geometry{a0paper,landscape,margin=0in}}
\DeclareOption*{\PassOptionsToClass{\CurrentOption}{article}}
\ProcessOptions\relax

\newcommand{\posterpanel}[6]{%
  \begingroup
  \setlength{\postertempwidth}{#1}%
  \colorbox{#2}{%
    \begin{minipage}[t][#1][t]{\postertempwidth}%
      \colorbox{#2}{%
        \begin{minipage}[t][\postercontentheight][t]{\postertempwidth}%
          \vspace*{#4}%
          \hspace*{#5}%
          \begin{minipage}[t][\dimexpr\postercontentheight-2#4\relax][t]{\dimexpr\postertempwidth-2#5\relax}%
            \color{#3}\raggedright\fontsizestandard #6%
          \end{minipage}%
        \end{minipage}%
      }%
    \end{minipage}%
  }%
  \endgroup
}

\newcommand{\betterposter}[3]{%
  \noindent%
  \posterpanel{\textheight}{\leftbarwidth}{\columnbackgroundcolor}{\columnfontcolor}{\columnmarginvertical}{\columnmarginhorizontal}{#2}%
  \setlength{\postercenterwidth}{\dimexpr\textwidth-\leftbarwidth-\rightbarwidth\relax}%
  \posterpanel{\textheight}{\postercenterwidth}{\maincolumnbackgroundcolor}{\maincolumnfontcolor}{\maincolumnmarginvertical}{\maincolumnmarginhorizontal}{#1}%
  \posterpanel{\textheight}{\rightbarwidth}{\columnbackgroundcolor}{\columnfontcolor}{\columnmarginvertical}{\columnmarginhorizontal}{#3}%
}

\newcommand{\maincolumn}[2]{%
  \vfill{%
    \RaggedRight\fontsizemain\bfseries #1\vspace{1em}%
  }%
  \vfill%
  \begin{minipage}[t][0.25\textheight][b]{\textwidth}%
    #2%
  \end{minipage}%
}

\newcommand{\qrplaceholder}{%
  \begingroup\setlength{\fboxsep}{0.5em}\fcolorbox{black}{white}{%
  \begin{minipage}[c][0.88\linewidth][c]{0.88\linewidth}\centering\color{black}\bfseries QR\end{minipage}}\endgroup
}
\newcommand{\includeqr}[2]{\IfFileExists{#1}{\includegraphics[width=#2]{#1}}{\qrplaceholder}}
\newcommand{\phoneiconline}{%
  \begingroup
  \setlength{\unitlength}{1pt}%
  \begin{picture}(34,56)
    \linethickness{2pt}%
    \put(7,3){\line(1,0){20}}\put(7,53){\line(1,0){20}}%
    \put(7,3){\line(0,1){50}}\put(27,3){\line(0,1){50}}%
    \put(14,10){\line(1,0){6}}%
  \end{picture}%
  \endgroup
}
\newcommand{\phoneicon}[1]{\IfFileExists{#1}{\includegraphics[height=0.85\linewidth]{#1}}{\phoneiconline}}
\newcommand{\qrcode}[3]{%
  \begin{minipage}[c]{0.30\textwidth}%
    \includeqr{#1}{\textwidth}%
  \end{minipage}%
  \begin{minipage}[c]{0.12\textwidth}%
    \hfill\phoneicon{#2}%
  \end{minipage}%
  \begin{minipage}[c]{0.50\textwidth}%
    #3%
  \end{minipage}%
}
\newcommand{\compactqrcode}[2]{%
  \begin{minipage}[t]{0.30\textwidth}%
    \includeqr{#1}{\textwidth}\par #2%
  \end{minipage}%
}
\newcommand{\inlineqrcode}[2]{%
  \begin{minipage}[c]{0.20\linewidth}\centering\includeqr{#1}{\linewidth}\end{minipage}\hfill
  \begin{minipage}[c]{0.66\linewidth}#2\end{minipage}%
}
\newcommand{\postergraphic}[3][]{%
  \IfFileExists{#2}{\includegraphics[#1]{#2}}{%
    \fcolorbox{mutedgray}{white}{%
      \begin{minipage}[c][0.22\paperheight][c]{0.92\linewidth}
        \centering\color{mutedgray}{\fontsize{24}{30}\selectfont #3}
      \end{minipage}}}%
}
\newcommand{\institutionbrand}[3]{%
  \IfFileExists{#1}{%
    \begin{center}
      \includegraphics[width=#3,height=0.085\paperheight,keepaspectratio]{#1}%
      \par\vspace{0.35em}{\fontsizesmall\bfseries #2\par}%
    \end{center}%
  }{}%
}
\newcommand{\metric}[2]{%
  \begin{minipage}[t]{0.46\linewidth}
    {\fontsize{46}{54}\selectfont\bfseries\color{\posteraccentcolor}#1\par}
    {\fontsizesmall #2\par}
  \end{minipage}
}
\newcommand{\evidencecard}[2]{%
  \begingroup\setlength{\fboxsep}{0.45em}
  \colorbox{sidebarcool}{\begin{minipage}[t]{0.42\linewidth}
    {\fontsize{34}{42}\selectfont\bfseries\color{black}#1\par}
    {\fontsizesmall\color{black}#2\par}
  \end{minipage}}\endgroup
}
\newcommand{\heroimage}[2]{%
  \begin{center}
  \IfFileExists{#1}{\includegraphics[width=0.96\linewidth,height=0.34\paperheight,keepaspectratio]{#1}}{\postergraphic[width=0.96\linewidth]{#1}{Hero figure placeholder}}
  \par\vspace{0.025\paperheight}{\fontsize{26}{34}\selectfont\bfseries #2\par}
  \end{center}
}
\renewcommand{\section}[1]{\vspace{2em}{\fontsizesection\bfseries\leavevmode #1}\par\vspace{0.5em}}
\renewcommand{\title}[1]{{\fontsizetitle\bfseries\leavevmode #1}\par}
\renewcommand{\author}[1]{{\color{gray}\fontsizeauthor #1}\par\vspace{-1.0em}}
\newcommand{\institution}[1]{\vspace{-1.0em}{\color{gray}#1}\par\vspace{-1.0em}}
\newcommand{\posterfootnote}[1]{{\color{mutedgray}\fontsizecaption #1}}

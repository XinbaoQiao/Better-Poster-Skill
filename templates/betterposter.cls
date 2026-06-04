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
\definecolor{methods}{RGB}{127,29,29}
\definecolor{intervention}{RGB}{244,180,0}
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
\setlength{\columnmarginvertical}{0.032\paperheight}
\setlength{\columnmarginhorizontal}{0.026\paperheight}
\setlength{\maincolumnmarginvertical}{0.070\paperheight}
\setlength{\maincolumnmarginhorizontal}{0.060\paperheight}
\setlength{\postercontentheight}{\dimexpr\paperheight-24pt\relax}

\newcommand{\fontsizestandard}{\fontsize{32}{45}\selectfont}
\newcommand{\fontsizemain}{\fontsize{112}{132}\selectfont}
\newcommand{\fontsizetitle}{\fontsize{72}{86}\selectfont}
\newcommand{\fontsizeauthor}{\fontsize{40}{50}\selectfont}
\newcommand{\fontsizesection}{\fontsize{46}{58}\selectfont}
\newcommand{\fontsizecaption}{\fontsize{24}{31}\selectfont}
\newcommand{\fontsizesmall}{\fontsize{22}{30}\selectfont}

\DeclareOption{a0paper}{}
\DeclareOption{a1paper}{%
  \geometry{a1paper,landscape,margin=0in}%
  \renewcommand{\fontsizestandard}{\fontsize{22}{31}\selectfont}%
  \renewcommand{\fontsizemain}{\fontsize{78}{94}\selectfont}%
  \renewcommand{\fontsizetitle}{\fontsize{52}{62}\selectfont}%
  \renewcommand{\fontsizeauthor}{\fontsize{30}{38}\selectfont}%
  \renewcommand{\fontsizesection}{\fontsize{34}{43}\selectfont}%
  \renewcommand{\fontsizecaption}{\fontsize{18}{24}\selectfont}%
  \renewcommand{\fontsizesmall}{\fontsize{16}{22}\selectfont}%
}
\DeclareOption{a2paper}{%
  \geometry{a2paper,landscape,margin=0in}%
  \renewcommand{\fontsizestandard}{\fontsize{16}{23}\selectfont}%
  \renewcommand{\fontsizemain}{\fontsize{54}{66}\selectfont}%
  \renewcommand{\fontsizetitle}{\fontsize{38}{47}\selectfont}%
  \renewcommand{\fontsizeauthor}{\fontsize{22}{29}\selectfont}%
  \renewcommand{\fontsizesection}{\fontsize{24}{32}\selectfont}%
  \renewcommand{\fontsizecaption}{\fontsize{13}{18}\selectfont}%
  \renewcommand{\fontsizesmall}{\fontsize{12}{17}\selectfont}%
}
\DeclareOption*{\PassOptionsToClass{\CurrentOption}{article}}
\ProcessOptions\relax

\newcommand{\posterpanel}[6]{%
  \begingroup
  \setlength{\postertempwidth}{#1}%
  \colorbox{#2}{%
    \begin{minipage}[t][\postercontentheight][t]{\postertempwidth}%
      \vspace*{#4}%
      \hspace*{#5}%
      \begin{minipage}[t][\dimexpr\postercontentheight-2#4\relax][t]{\dimexpr\postertempwidth-2#5\relax}%
        \color{#3}\raggedright\fontsizestandard #6%
      \end{minipage}%
    \end{minipage}%
  }%
  \endgroup
}

\newcommand{\betterposter}[3]{%
  \noindent\makebox[\paperwidth][l]{%
    \posterpanel{\leftbarwidth}{\columnbackgroundcolor}{\columnfontcolor}{\columnmarginvertical}{\columnmarginhorizontal}{#2}%
    \setlength{\postercenterwidth}{\dimexpr\paperwidth-\leftbarwidth-\rightbarwidth\relax}%
    \posterpanel{\postercenterwidth}{\maincolumnbackgroundcolor}{\maincolumnfontcolor}{\maincolumnmarginvertical}{\maincolumnmarginhorizontal}{#1}%
    \posterpanel{\rightbarwidth}{\columnbackgroundcolor}{\columnfontcolor}{\columnmarginvertical}{\columnmarginhorizontal}{#3}%
  }%
}

\newcommand{\maincolumn}[2]{%
  \begin{minipage}[t][\dimexpr\postercontentheight-2\maincolumnmarginvertical\relax][t]{\linewidth}%
    \vfill
    {\RaggedRight\fontsizemain\bfseries #1\par}%
    \vfill
    \vspace{0.025\paperheight}%
    \begin{minipage}[b][0.17\paperheight][b]{\linewidth}#2\end{minipage}%
  \end{minipage}%
}

\newcommand{\qrplaceholder}{%
  \begingroup\setlength{\fboxsep}{0.5em}\fcolorbox{black}{white}{%
  \begin{minipage}[c][0.88\linewidth][c]{0.88\linewidth}\centering\color{black}\bfseries QR\end{minipage}}\endgroup
}
\newcommand{\includeqr}[2]{\IfFileExists{#1}{\includegraphics[width=#2]{#1}}{\qrplaceholder}}
\newcommand{\qrcode}[3]{%
  \begin{minipage}[c]{0.30\linewidth}\centering\includeqr{#1}{\linewidth}\end{minipage}\hfill
  \begin{minipage}[c]{0.12\linewidth}\centering\IfFileExists{#2}{\includegraphics[width=0.82\linewidth]{#2}}{}\end{minipage}\hfill
  \begin{minipage}[c]{0.50\linewidth}#3\end{minipage}%
}
\newcommand{\compactqrcode}[2]{%
  \begin{minipage}[t]{0.34\linewidth}\centering\includeqr{#1}{\linewidth}\par\vspace{0.25em}#2\end{minipage}%
}
\newcommand{\inlineqrcode}[2]{%
  \begin{minipage}[c]{0.16\linewidth}\centering\includeqr{#1}{\linewidth}\end{minipage}\hfill
  \begin{minipage}[c]{0.78\linewidth}#2\end{minipage}%
}
\newcommand{\postergraphic}[3][]{%
  \IfFileExists{#2}{\includegraphics[#1]{#2}}{%
    \fcolorbox{mutedgray}{white}{%
      \begin{minipage}[c][0.22\paperheight][c]{0.92\linewidth}
        \centering\color{mutedgray}{\fontsize{24}{30}\selectfont #3}
      \end{minipage}}}%
}
\newcommand{\institutionbrand}[3]{%
  \begin{center}
    \IfFileExists{#1}{%
      \includegraphics[width=#3,height=0.085\paperheight,keepaspectratio]{#1}%
    }{%
      \begingroup\setlength{\fboxsep}{0.5em}\fcolorbox{mutedgray}{white}{%
        \begin{minipage}[c][0.060\paperheight][c]{0.50\linewidth}%
          \centering\color{mutedgray}{\fontsizesmall Institution\\Logo}%
        \end{minipage}}\endgroup%
    }%
    \par\vspace{0.35em}{\fontsizesmall\bfseries #2\par}%
  \end{center}%
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
\renewcommand{\section}[1]{\par\vspace{1.05em}{\fontsizesection\bfseries\color{\posteraccentcolor}#1\par}\vspace{0.25em}}
\renewcommand{\title}[1]{{\fontsizetitle\bfseries #1\par}\vspace{0.35em}}
\renewcommand{\author}[1]{{\fontsizeauthor\color{mutedgray}#1\par}\vspace{-0.2em}}
\newcommand{\institution}[1]{{\fontsizesmall\color{mutedgray}#1\par}\vspace{0.4em}}
\newcommand{\posterfootnote}[1]{{\color{mutedgray}\fontsizecaption #1}}

%%%% Better Poster Skill class
%%%% Clean-room, API-compatible Better Poster implementation inspired by:
%%%% Rafael Bailo, betterposter-latex-template
%%%% https://github.com/rafaelbailo/betterposter-latex-template
%%%% Original poster concept: Mike Morrison's #betterposter.
\NeedsTeXFormat{LaTeX2e}
\ProvidesClass{betterposter}[2026/06/03 Better Poster Skill class]

\LoadClass{article}
\pagestyle{empty}
\setlength{\parindent}{0pt}

% --- Core packages ----------------------------------------------------------
\RequirePackage{geometry}
\geometry{a0paper,landscape,margin=0in}
\RequirePackage[T1]{fontenc}
\RequirePackage[utf8]{inputenc}
\RequirePackage{graphicx}
\RequirePackage{xcolor}
\RequirePackage{enumitem}
\RequirePackage{ragged2e}
\RequirePackage{ifthen}
\RequirePackage{amsmath,amssymb,amsfonts}
\RequirePackage[hidelinks]{hyperref}

% Use Lato when available, otherwise fall back cleanly.
\IfFileExists{lato.sty}{\RequirePackage[default]{lato}}{\RequirePackage{lmodern}}

\setlist[itemize]{nosep,leftmargin=1.15em}
\setlist[enumerate]{nosep,leftmargin=1.25em}
\setlength{\fboxsep}{0pt}
\setlength{\fboxrule}{0pt}

% --- Colour palettes --------------------------------------------------------
\definecolor{imperialblue}{RGB}{0,62,116}
\definecolor{empirical}{RGB}{0,77,64}
\definecolor{theory}{RGB}{26,35,126}
\definecolor{methods}{RGB}{127,29,29}
\definecolor{intervention}{RGB}{244,180,0}
\definecolor{aurora}{RGB}{4,78,99}
\definecolor{plum}{RGB}{88,28,135}
\definecolor{forest}{RGB}{20,83,45}
\definecolor{graphite}{RGB}{31,41,55}
\definecolor{signalred}{RGB}{185,28,28}
\definecolor{sidebarwarm}{RGB}{250,248,242}
\definecolor{sidebarcool}{RGB}{247,249,252}
\definecolor{mutedgray}{RGB}{105,111,119}

\newcommand{\columnbackgroundcolor}{white}
\newcommand{\columnfontcolor}{black}
\newcommand{\maincolumnbackgroundcolor}{imperialblue}
\newcommand{\maincolumnfontcolor}{white}
\newcommand{\posteraccentcolor}{imperialblue}

% --- Sizing -----------------------------------------------------------------
\newlength{\leftbarwidth}
\newlength{\rightbarwidth}
\newlength{\columnmarginvertical}
\newlength{\columnmarginhorizontal}
\newlength{\maincolumnmarginvertical}
\newlength{\maincolumnmarginhorizontal}
\newlength{\bpcolumnwidth}

\newcommand{\fontsizestandard}{\fontsize{32}{45}\selectfont}
\newcommand{\fontsizemain}{\fontsize{112}{132}\selectfont}
\newcommand{\fontsizetitle}{\fontsize{72}{86}\selectfont}
\newcommand{\fontsizeauthor}{\fontsize{40}{50}\selectfont}
\newcommand{\fontsizesection}{\fontsize{46}{58}\selectfont}
\newcommand{\fontsizecaption}{\fontsize{24}{31}\selectfont}

\DeclareOption{a0paper}{\geometry{a0paper}}
\DeclareOption{a1paper}{%
  \geometry{a1paper}%
  \renewcommand{\fontsizestandard}{\fontsize{22}{31}\selectfont}%
  \renewcommand{\fontsizemain}{\fontsize{78}{94}\selectfont}%
  \renewcommand{\fontsizetitle}{\fontsize{52}{62}\selectfont}%
  \renewcommand{\fontsizeauthor}{\fontsize{30}{38}\selectfont}%
  \renewcommand{\fontsizesection}{\fontsize{34}{43}\selectfont}%
  \renewcommand{\fontsizecaption}{\fontsize{18}{24}\selectfont}%
}
\DeclareOption{a2paper}{%
  \geometry{a2paper}%
  \renewcommand{\fontsizestandard}{\fontsize{16}{23}\selectfont}%
  \renewcommand{\fontsizemain}{\fontsize{54}{66}\selectfont}%
  \renewcommand{\fontsizetitle}{\fontsize{38}{47}\selectfont}%
  \renewcommand{\fontsizeauthor}{\fontsize{22}{29}\selectfont}%
  \renewcommand{\fontsizesection}{\fontsize{24}{32}\selectfont}%
  \renewcommand{\fontsizecaption}{\fontsize{13}{18}\selectfont}%
}
\DeclareOption*{\PassOptionsToClass{\CurrentOption}{article}}
\ProcessOptions\relax

\setlength{\leftbarwidth}{0.20\paperwidth}
\setlength{\rightbarwidth}{0.20\paperwidth}
\setlength{\columnmarginvertical}{0.032\paperheight}
\setlength{\columnmarginhorizontal}{0.026\paperheight}
\setlength{\maincolumnmarginvertical}{0.070\paperheight}
\setlength{\maincolumnmarginhorizontal}{0.060\paperheight}

% --- Internal layout helpers ------------------------------------------------
\newcommand{\bp@centeredpage}[3]{%
  \begin{minipage}[c][\textheight][c]{\textwidth}%
    \begin{center}%
      \begin{minipage}[t][\dimexpr\textheight-2#1\relax][t]{\dimexpr\textwidth-2#2\relax}%
        #3%
      \end{minipage}%
    \end{center}%
  \end{minipage}%
}

\newcommand{\bp@column}[7]{%
  \begingroup%
  \setlength{\bpcolumnwidth}{#2}%
  \begin{minipage}[t][#1][t]{\bpcolumnwidth}%
    \noindent\colorbox{#3}{%
      \begin{minipage}[t][#1][t]{\bpcolumnwidth}%
        {\leavevmode\color{#4}\bp@centeredpage{#5}{#6}{#7}}%
      \end{minipage}%
    }%
  \end{minipage}%
  \endgroup%
}

% --- Public API -------------------------------------------------------------
% Mirrors the Rafael Bailo template call shape: main, left, right.
\newcommand{\betterposter}[3]{%
  \noindent%
  \bp@column{\textheight}{\leftbarwidth}{\columnbackgroundcolor}{\columnfontcolor}{\columnmarginvertical}{\columnmarginhorizontal}{#2}%
  \bp@column{\textheight}{\dimexpr\textwidth-\leftbarwidth-\rightbarwidth\relax}{\maincolumnbackgroundcolor}{\maincolumnfontcolor}{\maincolumnmarginvertical}{\maincolumnmarginhorizontal}{#1}%
  \bp@column{\textheight}{\rightbarwidth}{\columnbackgroundcolor}{\columnfontcolor}{\columnmarginvertical}{\columnmarginhorizontal}{#3}%
}

\newcommand{\maincolumn}[2]{%
  \vfill%
  {\RaggedRight\fontsizemain\bfseries #1\par}%
  \vspace{0.045\textheight}%
  \vfill%
  \begin{minipage}[t][0.24\textheight][b]{\textwidth}%
    #2%
  \end{minipage}%
}

\newcommand{\bpqrplaceholder}{%
  \fcolorbox{black}{white}{%
    \begin{minipage}[c][0.88\linewidth][c]{0.88\linewidth}%
      \centering\color{black}{\fontsize{22}{26}\selectfont QR}\par
      {\fontsize{13}{16}\selectfont generate or replace}%
    \end{minipage}%
  }%
}

\newcommand{\bpincludeqr}[2]{%
  \IfFileExists{#1}{\includegraphics[width=#2]{#1}}{\bpqrplaceholder}%
}

\newcommand{\bpincludeicon}[2]{%
  \IfFileExists{#1}{\includegraphics[height=#2]{#1}}{}%
}

\newcommand{\qrcode}[3]{%
  \begin{minipage}[c]{0.30\textwidth}%
    \centering\bpincludeqr{#1}{\textwidth}%
  \end{minipage}%
  \hfill%
  \begin{minipage}[c]{0.12\textwidth}%
    \centering\bpincludeicon{#2}{0.85\textwidth}%
  \end{minipage}%
  \hfill%
  \begin{minipage}[c]{0.50\textwidth}%
    {#3}%
  \end{minipage}%
}

\newcommand{\compactqrcode}[2]{%
  \begin{minipage}[t]{0.35\textwidth}%
    \centering\bpincludeqr{#1}{\textwidth}\par\vspace{0.3em}#2%
  \end{minipage}%
}

\newcommand{\inlineqrcode}[2]{%
  \begin{minipage}[c]{0.16\textwidth}%
    \centering\bpincludeqr{#1}{\textwidth}%
  \end{minipage}%
  \hfill%
  \begin{minipage}[c]{0.78\textwidth}%
    #2%
  \end{minipage}%
}

\newcommand{\postergraphic}[3][]{%
  \IfFileExists{#2}{\includegraphics[#1]{#2}}{%
    \fcolorbox{mutedgray}{white}{%
      \begin{minipage}[c][0.22\paperheight][c]{0.92\linewidth}%
        \centering\color{mutedgray}{\fontsize{24}{30}\selectfont #3}%
      \end{minipage}%
    }%
  }%
}

\renewcommand{\section}[1]{%
  \vspace{1.15em}{\fontsizesection\bfseries\leavevmode #1}\par\vspace{0.35em}%
}
\renewcommand{\title}[1]{{\fontsizetitle\bfseries\leavevmode #1}\par\vspace{0.22em}}
\renewcommand{\author}[1]{{\color{mutedgray}\fontsizeauthor #1}\par\vspace{0.08em}}
\newcommand{\institution}[1]{{\color{mutedgray}\fontsizestandard #1}\par\vspace{0.1em}}
\newcommand{\posterfootnote}[1]{{\color{mutedgray}\fontsizecaption #1}}

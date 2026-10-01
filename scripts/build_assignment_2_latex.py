"""Generate standalone, editable Vietnamese LaTeX reports and compile final PDFs."""
from pathlib import Path
import subprocess

ROOT=Path(__file__).resolve().parents[1]
SRC=ROOT/'src'
OUT=ROOT/'output/pdf'
TMP=ROOT/'tmp/assignment2'
TMP.mkdir(parents=True,exist_ok=True)
students=[('Nguyen Thai Thanh Binh','2570175'),('Vu Tien Giang','2570188'),('Pham Huy Thanh','2570317')]
PRE=r'''\documentclass[11pt,a4paper]{article}
\usepackage[margin=22mm,headheight=15pt]{geometry}
\usepackage{fontspec}
\setmainfont{Times New Roman}
\setsansfont{Arial}
\usepackage{amsmath,amssymb,graphicx,booktabs,tikz,fancyhdr,xcolor,hyperref}
\usetikzlibrary{arrows.meta,calc}
\definecolor{navy}{HTML}{16354B}
\definecolor{teal}{HTML}{007F7B}
\definecolor{rust}{HTML}{B64D32}
\hypersetup{colorlinks=true,linkcolor=navy,urlcolor=teal,pdfauthor={STUDENT},pdftitle={EE5430 - Standing waves}}
\pagestyle{fancy}\fancyhf{}\lhead{\small EE5430 -- Đường truyền và sóng đứng}
\rhead{\small STUDENT}\cfoot{\thepage}
\setlength{\parindent}{0pt}\setlength{\parskip}{5pt}
\newcommand{\jj}{\mathrm{j}}
\newcommand{\ohm}{\,\Omega}
\newcommand{\step}[1]{\par\vspace{3pt}{\color{navy}\bfseries #1}\par}
\newcommand{\result}[1]{\par\smallskip\noindent\fcolorbox{teal}{teal!5}{\parbox{0.94\linewidth}{#1}}\par\smallskip}
\newcommand{\problem}[2]{\clearpage\section*{#1}\textbf{Dữ kiện và yêu cầu.} #2\par}
\begin{document}
\begin{titlepage}\centering
{\sffamily\large ĐẠI HỌC BÁCH KHOA -- ĐHQG TP. HỒ CHÍ MINH\par}
\vspace{5mm}{\sffamily Khoa Điện -- Điện tử\par}
\vspace{16mm}\includegraphics[width=32mm]{LOGO}\par
\vspace{15mm}{\color{navy}\rule{\linewidth}{1pt}}\par
\vspace{8mm}{\sffamily\bfseries\LARGE EE5430\par}
\vspace{5mm}{\sffamily\bfseries\LARGE ĐƯỜNG TRUYỀN VÀ SÓNG ĐỨNG\par}
\vspace{5mm}{\Large Bài tập 2 -- Lời giải sáu bài toán\par}
\vspace{8mm}{\color{navy}\rule{\linewidth}{1pt}}\par
\vspace{14mm}\begin{tabular}{rl}\textbf{Sinh viên:}&STUDENT\\[3mm]\textbf{Mã số sinh viên:}&SID\end{tabular}
\vspace{16mm}\begin{minipage}{0.83\linewidth}
\textbf{Nội dung báo cáo}\par
Hệ số phản xạ và hệ số sóng đứng; xác định vị trí cực trị và trở kháng dọc đường truyền;
suy ra tải từ phép đo dịch chuyển nút sóng; đo bằng đường dây có khe đo.
\par\smallskip Báo cáo sử dụng một quy ước tọa độ thống nhất, công thức pha có kiểm tra dấu,
đồ thị Smith chuẩn hóa và đồ thị điện áp có trục, đơn vị, chú thích.
\end{minipage}\vfill Tháng 10 năm 2026
\end{titlepage}
\section*{Cơ sở lý thuyết và quy ước}
\step{1. Tọa độ, giả thiết và hệ số phản xạ}
Xét đường truyền không tổn hao, trở kháng đặc tính thực $Z_0>0$.
Chọn $d=0$ tại tải; $d$ tăng từ tải về phía nguồn. Quy ước thời gian là $e^{\jj\omega t}$.
Với đường truyền điện môi không khí, dùng $v_p\simeq3\times10^8\,\mathrm{m/s}$.
\begin{align}
\Gamma_L&=\frac{Z_L-Z_0}{Z_L+Z_0}=\rho e^{\jj\theta},&
\beta&=\frac{2\pi}{\lambda},& \lambda&=\frac{v_p}{f},\\
\Gamma(d)&=\Gamma_L e^{-\jj2\beta d},&
Z(d)&=Z_0\frac{1+\Gamma(d)}{1-\Gamma(d)}.
\end{align}
\step{2. Biên độ điện áp, VSWR và vị trí cực trị}
\begin{align}
\frac{|V(d)|}{|V^+|}&=\sqrt{1+\rho^2+2\rho\cos(\theta-2\beta d)},\\
S\equiv\mathrm{VSWR}&=\frac{1+\rho}{1-\rho},& \rho&=\frac{S-1}{S+1}.
\end{align}
Điện áp lớn nhất khi $\Gamma(d)=+\rho$ và nhỏ nhất khi $\Gamma(d)=-\rho$.
Lấy nghiệm đầu tiên $0\le d<\lambda/2$:
\begin{align}
d_{\max}&=\frac{[\theta]_{2\pi}}{2\beta},&
d_{\min}&=\frac{[\theta-\pi]_{2\pi}}{2\beta},\\
Z(d_{\max})&=Z_0S,&Z(d_{\min})&=\frac{Z_0}{S}.
\end{align}
Ký hiệu $[a]_{2\pi}$ là phần dư của $a$ trong $[0,2\pi)$; không dùng trực tiếp
một góc âm để tính khoảng cách. Hai cực trị cùng loại cách nhau $\lambda/2$;
hai cực trị kề nhau khác loại cách nhau $\lambda/4$.
\step{3. Suy ra tải từ dịch chuyển nút khi nối tắt}
Nối tắt tại đúng mặt phẳng tải cho $\Gamma_{\mathrm{SC}}=-1$.
Gọi $d_L$ và $d_{\mathrm{SC}}$ là vị trí nút của tải và nối tắt,
đo trên cùng một thang, tăng về nguồn. Điều kiện pha tại hai nút là
\[
\theta-2\beta d_L=\pi+2k\pi,\qquad
\pi-2\beta d_{\mathrm{SC}}=\pi+2m\pi.
\]
Trừ hai phương trình và đặt $\Delta d=d_L-d_{\mathrm{SC}}$:
\begin{equation}
\boxed{\Gamma_L=-\rho\,e^{\jj4\pi\Delta d/\lambda}},\qquad
\boxed{Z_L=Z_0\frac{1+\Gamma_L}{1-\Gamma_L}}.
\end{equation}
Nếu \emph{thay tải bằng nối tắt} làm nút dịch về nguồn một đoạn $a$, thì
$\Delta d=-a$. Nếu nút dịch về tải thì $\Delta d=+a$.
Ghép nút khác nhau một chu kỳ $\lambda/2$ không đổi kết quả vì pha lệch $2\pi$.
\step{4. Đọc đồ thị Smith}
Chuẩn hóa $z=Z/Z_0=r+\jj x$, rồi ánh xạ $\Gamma=(z-1)/(z+1)$.
Vòng tròn tâm gốc bán kính $\rho$ là vòng VSWR. Đi về nguồn quay theo chiều
kim đồng hồ; một vòng ứng với $\lambda/2$. Hai giao điểm trục thực cho
$z_{\min}=1/S$ và $z_{\max}=S$. Kết quả đại số được dùng để kiểm tra số đọc đồ thị.
'''

BODY=r'''
\problem{Bài 1. Phản xạ, cực trị và đồ thị Smith}
{$Z_0=50\ohm$, $Z_L=25-\jj50\ohm$, $\lambda=10\,\mathrm{cm}$.
Tìm $\Gamma_L$, VSWR, cực trị điện áp đầu tiên từ tải và trở kháng tại đó.}
\step{Bước 1. Chuẩn hóa tải và tính hệ số phản xạ}
\[
z_L=\frac{25-\jj50}{50}=0.5-\jj1,\qquad
\Gamma_L=\frac{-25-\jj50}{75-\jj50}
=\frac{625-\jj5000}{8125}=0.076923-\jj0.615385.
\]
Do đó $\rho=0.620174$, $\theta=-82.8750^\circ\equiv277.1250^\circ$ và
\[S=\frac{1+0.620174}{1-0.620174}=4.265564.\]
\step{Bước 2. Quay vòng VSWR về nguồn và xác định vị trí}
Với $2\beta=720^\circ/\lambda=72^\circ/\mathrm{cm}$, từ tải quay theo chiều
kim đồng hồ đến phía trục thực âm trước ($97.1250^\circ$), rồi phía dương:
\[
d_{\min}=\frac{277.1250^\circ-180^\circ}{72^\circ/\mathrm{cm}}
=1.348959\,\mathrm{cm},\qquad
d_{\max}=\frac{277.1250^\circ}{72^\circ/\mathrm{cm}}=3.848959\,\mathrm{cm}.
\]
\begin{center}
\begin{tikzpicture}[scale=3.0,>=Stealth]
\draw[gray!60] (0,0) circle (1);
\begin{scope}\clip (0,0) circle(1);
\foreach \r in {0.2,0.5,1,2,5}{\pgfmathsetmacro{\cx}{\r/(1+\r)}\pgfmathsetmacro{\rr}{1/(1+\r)}\draw[gray!35,line width=.3pt](\cx,0)circle(\rr);}
\foreach \x in {-5,-2,-1,-0.5,-0.2,0.2,0.5,1,2,5}{\pgfmathsetmacro{\cy}{1/\x}\pgfmathsetmacro{\rr}{abs(1/\x)}\draw[gray!35,line width=.3pt](1,\cy)circle(\rr);}
\end{scope}
\draw[gray!60](-1,0)--(1,0);
\foreach \r in {0.2,0.5,1,2,5}{\pgfmathsetmacro{\gx}{(\r-1)/(\r+1)}\node[above,font=\tiny,fill=white,inner sep=.6pt]at(\gx,0){\r};}
\node[font=\tiny]at(.92,.09){$r$};
\node[font=\tiny,fill=white]at(0,0.98){$x=+1$};
\node[font=\tiny,fill=white]at(0,-0.98){$x=-1$};
\draw[teal,thick](0,0)circle(.620174);
\draw[rust,->,thick](-82.875:.70)arc[start angle=-82.875,end angle=-180,radius=.70];
\draw[teal,->,thick](-183:.74)arc[start angle=-183,end angle=-360,radius=.74];
\draw[dashed,gray](0,0)--(.076923,-.615385);
\fill[rust](.076923,-.615385)circle(.018);
\node[font=\small,below right,fill=white,inner sep=1pt]at(.076923,-.615385){$z_L=0.5-\jj1$};
\fill[teal](-.620174,0)circle(.018);\fill[teal](.620174,0)circle(.018);
\node[below left,font=\scriptsize,fill=white]at(-.620174,0){$z_{\min}=0.23444$};
\node[below right,font=\scriptsize,fill=white]at(.620174,0){$z_{\max}=4.26556$};
\node[font=\scriptsize,align=center]at(-1.28,-.55){Tới $V_{\min}$\\$97.125^\circ$};
\node[font=\scriptsize,align=center]at(.6,.90){Tới $V_{\max}$\\tổng $277.125^\circ$};
\end{tikzpicture}\par
\small Hình 1. Đồ thị Smith trở kháng: lưới $r,x$ chuẩn hóa và vòng VSWR.
\end{center}
\step{Bước 3. Trở kháng tại hai vị trí và kiểm tra}
\result{$Z(d_{\min})=50/S=11.7218\ohm$; $Z(d_{\max})=50S=213.2782\ohm$.
Hai giá trị đều thuần thực. $d_{\max}-d_{\min}=2.5\,\mathrm{cm}=\lambda/4$.}
Trên đồ thị, $\Gamma=-\rho$ và $+\rho$ lần lượt cho các giá trị trên;
thay các khoảng cách vào $\Gamma(d)$ thu được phần ảo bằng không.

\problem{Bài 2. Đường truyền điện môi không khí}
{$Z_0=75\ohm$, $f=1.5\,\mathrm{GHz}$, $Z_L=150+\jj75\ohm$.
Tìm VSWR, cực trị đầu tiên và $Z_{\mathrm{in}}$ tại $d=3\,\mathrm{cm}$.}
\step{Bước 1. Bước sóng và hệ số phản xạ}
\begin{align*}
\lambda&=\frac{3\times10^8}{1.5\times10^9}=0.20\,\mathrm{m}=20\,\mathrm{cm},&
\beta&=\frac{2\pi}{0.20}=10\pi\,\mathrm{rad/m},\\
\Gamma_L&=\frac{75+\jj75}{225+\jj75}=0.4+\jj0.2,&
\rho&=\sqrt{0.4^2+0.2^2}=0.447214,\\
\theta&=\tan^{-1}\left(\frac{0.2}{0.4}\right)=26.5651^\circ,&
S&=\frac{1+0.447214}{1-0.447214}=2.618034.
\end{align*}
\step{Bước 2. Cực trị đầu tiên đo từ tải về nguồn}
Vì $2\beta=36^\circ/\mathrm{cm}$, điện áp cực đại xuất hiện trước:
\begin{align*}
d_{\max}&=\frac{26.5651^\circ}{36^\circ/\mathrm{cm}}=0.737918\,\mathrm{cm},\\
d_{\min}&=\frac{26.5651^\circ+180^\circ}{36^\circ/\mathrm{cm}}=5.737918\,\mathrm{cm}.
\end{align*}
Ở cực tiểu, dùng góc $206.5651^\circ$ tương đương $\theta-180^\circ$ modulo $360^\circ$.
\step{Bước 3. Trở kháng nhìn vào đường truyền tại 3 cm}
\[
Z_{\mathrm{in}}(d)=Z_0\frac{Z_L+\jj Z_0\tan(\beta d)}{Z_0+\jj Z_L\tan(\beta d)},\qquad
\beta d=10\pi(0.03)=0.3\pi=54^\circ.
\]
Với $t=\tan54^\circ=1.376382$, thay số:
\begin{align*}
Z_{\mathrm{in}}&=75\frac{150+\jj(75+75t)}{75-75t+\jj150t}\\
&=75\frac{150+\jj178.2286}{-28.2286+\jj206.4573}
=56.2434-\jj62.1808\ohm.
\end{align*}
\step{Bước 4. Kiểm tra độc lập bằng phép quay hệ số phản xạ}
\[
\Gamma(3\,\mathrm{cm})=(0.4+\jj0.2)e^{-\jj108^\circ}
\simeq0.066604-\jj0.442226.
\]
Thay vào $75(1+\Gamma)/(1-\Gamma)$ thu lại cùng $Z_{\mathrm{in}}$.
Độ lớn $|\Gamma(d)|=0.447214$ không đổi vì đường truyền không tổn hao.
\result{$S=2.6180$; $d_{\max}=0.7379\,\mathrm{cm}$;
$d_{\min}=5.7379\,\mathrm{cm}$; $Z_{\mathrm{in}}(3\,\mathrm{cm})=56.2434-\jj62.1808\ohm$.}
Để đối chiếu: $Z_{\min}=28.6475\ohm$, $Z_{\max}=196.3525\ohm$ và
$d_{\min}-d_{\max}=5\,\mathrm{cm}=\lambda/4$.

\problem{Bài 3. Suy ra tải khi nút nối tắt dịch về nguồn}
{$Z_0=50\ohm$, $S=3$, khoảng cách hai nút liên tiếp $20\,\mathrm{cm}$.
Thay tải bằng ngắn mạch làm nút dịch $8\,\mathrm{cm}$ về nguồn. Tìm $Z_L$.}
\step{Bước 1. Tìm bước sóng và độ lớn phản xạ}
\[
\frac{\lambda}{2}=20\,\mathrm{cm}\Rightarrow\lambda=40\,\mathrm{cm},\qquad
\rho=\frac{S-1}{S+1}=\frac{3-1}{3+1}=0.5.
\]
\step{Bước 2. Xác định đúng dấu dịch chuyển}
Gọi nút ban đầu là $d_L$. Sau khi thay tải bằng nối tắt, nút ở
$d_{\mathrm{SC}}=d_L+8\,\mathrm{cm}$. Vì vậy
\[
\Delta d=d_L-d_{\mathrm{SC}}=-8\,\mathrm{cm}.
\]
Đây là hiệu vị trí \emph{tải trừ nối tắt}, trái dấu với dịch chuyển khi thay tải.
\step{Bước 3. Pha hệ số phản xạ và trở kháng tải}
\begin{align*}
\Gamma_L&=-0.5\exp\left(\jj\frac{4\pi(-8)}{40}\right)
=0.5e^{\jj36^\circ}=0.404508+\jj0.293893,\\
Z_L&=50\frac{1.404508+\jj0.293893}{0.595492-\jj0.293893}
=85.0373+\jj66.6449\ohm.
\end{align*}
\result{$Z_L=85.04+\jj66.64\ohm$. Phần phản kháng dương, nên tải có tính cảm.}
\step{Bước 4. Kiểm tra bằng vị trí nút}
Với $\theta=36^\circ$ và $2\beta=18^\circ/\mathrm{cm}$:
\[
d_{\min,L}=\frac{[36^\circ-180^\circ]_{360^\circ}}{18^\circ/\mathrm{cm}}
=12\,\mathrm{cm}.
\]
Nối tắt có nút ở $d=0,20,40,\ldots\,\mathrm{cm}$. Nút tương ứng với nút tại
$12\,\mathrm{cm}$ là nút ở $20\,\mathrm{cm}$: dịch $+8\,\mathrm{cm}$ về nguồn.
\begin{center}\begin{tikzpicture}[x=.26cm,y=1cm,>=Stealth]
\draw[->](0,0)--(42,0)node[right]{\small $d$ (cm), về nguồn};
\foreach \v in {0,12,20,32,40}{\draw(\v,.07)--(\v,-.07)node[below]{\small\v};}
\foreach \v in {12,32}{\fill[teal](\v,.55)circle(2pt);}
\foreach \v in {0,20,40}{\fill[rust](\v,1.05)circle(2pt);}
\node[left,font=\small]at(0,.55){Tải};\node[left,font=\small]at(0,1.05){Nối tắt};
\draw[->,thick](12,.68)--(20,.68)node[midway,above,font=\small]{$8$ cm};
\end{tikzpicture}\par\small Hình 2. Vị trí nút trước và sau khi thay tải.
\end{center}
Cuối cùng, tính lại $(Z_L-50)/(Z_L+50)$ cho $|\Gamma_L|=0.5$,
suy ra $(1+0.5)/(1-0.5)=3$, đúng VSWR đề bài.

\problem{Bài 4. Suy ra tải khi nút nối tắt dịch về tải}
{$Z_0=100\ohm$, $S=1.5$, khoảng cách hai nút liên tiếp $30\,\mathrm{cm}$.
Thay tải bằng ngắn mạch làm nút dịch $6\,\mathrm{cm}$ về tải.
Tìm $\lambda$, $Z_L$ và xác định tính cảm hay dung.}
\step{Bước 1. Bước sóng và độ lớn phản xạ}
\[
\lambda=2(30)=60\,\mathrm{cm},\qquad
\rho=\frac{1.5-1}{1.5+1}=0.2.
\]
\step{Bước 2. Đổi chiều dịch chuyển thành hiệu tọa độ}
Vì nút nối tắt dịch về tải, $d_{\mathrm{SC}}=d_L-6\,\mathrm{cm}$.
Do đó $\Delta d=d_L-d_{\mathrm{SC}}=+6\,\mathrm{cm}$.
\step{Bước 3. Tính pha và tải}
\begin{align*}
\Gamma_L&=-0.2\exp\left(\jj\frac{4\pi(6)}{60}\right)
=0.2e^{-\jj108^\circ}=-0.061803-\jj0.190211,\\
Z_L&=100\frac{0.938197-\jj0.190211}{1.061803+\jj0.190211}
=82.5021-\jj32.6934\ohm.
\end{align*}
\result{$\lambda=60\,\mathrm{cm}$; $Z_L=82.50-\jj32.69\ohm$.
Vì $\operatorname{Im}(Z_L)<0$, tải có tính dung.}
\step{Bước 4. Kiểm tra dấu qua vị trí cực tiểu}
Với $\theta=-108^\circ\equiv252^\circ$ và $2\beta=12^\circ/\mathrm{cm}$,
\[
d_{\min,L}=\frac{252^\circ-180^\circ}{12^\circ/\mathrm{cm}}=6\,\mathrm{cm}.
\]
Nút nối tắt tại $0\,\mathrm{cm}$; vì thế nút tải ở $6\,\mathrm{cm}$ dịch về
$0\,\mathrm{cm}$ sau khi nối tắt, đúng $6\,\mathrm{cm}$ về phía tải.
\begin{center}\begin{tikzpicture}[x=.30cm,y=1cm,>=Stealth]
\draw[->](0,0)--(38,0)node[right]{\small $d$ (cm), về nguồn};
\foreach \v in {0,6,30,36}{\draw(\v,.07)--(\v,-.07)node[below]{\small\v};}
\foreach \v in {6,36}{\fill[teal](\v,.55)circle(2pt);}
\foreach \v in {0,30}{\fill[rust](\v,1.05)circle(2pt);}
\node[left,font=\small]at(0,.55){Tải};\node[left,font=\small]at(0,1.05){Nối tắt};
\draw[->,thick](6,.72)--(0,.72)node[midway,above,font=\small]{$6$ cm};
\end{tikzpicture}\par\small Hình 3. Nút dịch theo chiều giảm của tọa độ $d$.
\end{center}
Kiểm tra đại số: $|\Gamma_L|=0.2$ cho $S=(1+0.2)/(1-0.2)=1.5$.
Không thể suy ra tần số chỉ từ bài này nếu chưa biết vận tốc pha của đường truyền.

\problem{Bài 5. Khe đo: nút nối tắt dịch về phía tải}
{$Z_0=50\ohm$, điện môi không khí, $S=1.8$. Hai nút của tải ở
$32.0$ và $44.0\,\mathrm{cm}$; khi nối tắt, nút tương ứng ở $26.6\,\mathrm{cm}$.
Tìm bước sóng, tần số và tải.}
\step{Bước 1. Đọc khoảng cách nút và tìm tần số}
\[
\lambda=2(44.0-32.0)=24.0\,\mathrm{cm}=0.24\,\mathrm m,\qquad
f=\frac{3\times10^8}{0.24}=1.25\,\mathrm{GHz}.
\]
\step{Bước 2. Suy ra pha từ cùng một thang đo}
Số chỉ tăng về nguồn theo mũi tên. Không cần biết vị trí tuyệt đối của mặt phẳng tải:
\[
\Delta d=32.0-26.6=+5.4\,\mathrm{cm},\qquad
\rho=\frac{1.8-1}{1.8+1}=\frac27.
\]
\begin{align*}
\Gamma_L&=-\frac27\exp\left(\jj\frac{4\pi(5.4)}{24}\right)
=\frac27e^{-\jj18^\circ}=0.271730-\jj0.088291,\\
Z_L&=50\frac{1.271730-\jj0.088291}{0.728270+\jj0.088291}
=85.3229-\jj16.4056\ohm.
\end{align*}
\result{$\lambda=24\,\mathrm{cm}$; $f\simeq1.25\,\mathrm{GHz}$;
$Z_L=85.32-\jj16.41\ohm$ (tải có tính dung).}
WAVE5
\step{Kiểm tra và cách hiểu đồ thị}
Ở nút tải, biên độ chuẩn hóa nhỏ nhất là $1-\rho=5/7$, không bằng không;
ở bụng là $1+\rho=9/7$, nên tỉ số bằng $9/5=1.8$.
Nối tắt có $\rho=1$ nên nút điện áp bằng không. Các nút nối tắt ở
$26.6,38.6\,\mathrm{cm}$ và các nút tải ở $32.0,44.0\,\mathrm{cm}$,
đúng độ dịch $5.4\,\mathrm{cm}$ và khoảng lặp $12\,\mathrm{cm}$.
Hai đường trên hình được chuẩn hóa riêng theo biên độ sóng tới của từng phép đo;
không dùng độ cao tuyệt đối của chúng để suy ra công suất.

\problem{Bài 6. Khe đo: thang tăng về phía nguồn}
{$Z_0=75\ohm$, điện môi không khí, $S=2.5$.
Nút tải ở $18.2$ và $28.2\,\mathrm{cm}$; nút nối tắt ở $21.2$ và
$31.2\,\mathrm{cm}$. Tìm tần số và tải.}
\step{Bước 1. Tính bước sóng và tần số}
\[
\lambda=2(28.2-18.2)=20\,\mathrm{cm}=0.20\,\mathrm m,\qquad
f=\frac{3\times10^8}{0.20}=1.50\,\mathrm{GHz}.
\]
\step{Bước 2. Hiệu tọa độ và hệ số phản xạ}
Vì thang tăng về nguồn, ghép $18.2$ với $21.2\,\mathrm{cm}$:
\[
\Delta d=18.2-21.2=-3.0\,\mathrm{cm},\qquad
\rho=\frac{2.5-1}{2.5+1}=\frac37.
\]
\begin{align*}
\Gamma_L&=-\frac37\exp\left(\jj\frac{4\pi(-3)}{20}\right)
=\frac37e^{\jj72^\circ}=0.132436+\jj0.407596,\\
Z_L&=75\frac{1.132436+\jj0.407596}{0.867564-\jj0.407596}
=66.6351+\jj66.5425\ohm.
\end{align*}
\result{$f\simeq1.50\,\mathrm{GHz}$; $Z_L=66.64+\jj66.54\ohm$ (tải có tính cảm).}
WAVE6
\step{Kiểm tra tính tuần hoàn và VSWR}
Nút nối tắt trước đó ở $11.2\,\mathrm{cm}$. Nếu ghép với nút này,
$\Delta d=18.2-11.2=7.0\,\mathrm{cm}$; pha tính ra tăng $360^\circ$,
nên vẫn cho cùng $\Gamma_L$ và $Z_L$. Đồ thị có cực tiểu tải $4/7$,
cực đại $10/7$, tỉ số $(10/7)/(4/7)=2.5$. Khoảng cách nút là $10\,\mathrm{cm}$.
Với vận tốc ánh sáng chính xác $299\,792\,458\,\mathrm{m/s}$,
tần số bài 5 và 6 lần lượt là $1.24914$ và $1.49896\,\mathrm{GHz}$;
sai khác nhỏ này do quy ước làm tròn $v_p$, không ảnh hưởng các trở kháng đã tính.
\end{document}
'''

def wave(n,x0,x1,lam,nodeL,nodeSC,rho,ticks):
    # Exact envelopes referred to measured voltage minima; PGF trig uses degrees.
    return rf'''\begin{{center}}
\begin{{tikzpicture}}[x=.42cm,y=1.35cm,>=Stealth]
\draw[->](0,0)--({x1-x0+.5},0)node[right,font=\small]{{$x$ (cm)}};
\draw[->](0,0)--(0,2.25)node[above,font=\small]{{$|V|/|V^+|$}};
\foreach \v in {{0,1,2}}{{\draw(-.12,\v)--(.12,\v)node[left=4pt,font=\scriptsize]{{\v}};}}
\draw[teal,thick,domain={x0}:{x1},samples=241,variable=\t]
plot ({{\t-{x0}}},{{sqrt(1+{rho}*{rho}-2*{rho}*cos(720*(\t-{nodeL})/{lam}))}});
\draw[rust,dashed,thick,domain={x0}:{x1},samples=241,variable=\t]
plot ({{\t-{x0}}},{{2*abs(sin(360*(\t-{nodeSC})/{lam}))}});
''' + '\n'.join(rf'\draw[gray!50,dotted]({v-x0},0)--({v-x0},2);\draw({v-x0},.05)--({v-x0},-.05)node[below,font=\scriptsize]{{{v:.1f}}};' for v in ticks)+rf'''
\draw[teal,thick](1,2.72)--(2,2.72)node[right,font=\small]{{Có tải $Z_L$}};
\draw[rust,dashed,thick](8,2.72)--(9,2.72)node[right,font=\small]{{Nối tắt}};
\draw[->](3,-.6)--(11,-.6)node[midway,below,font=\small]{{Về phía nguồn}};
\end{{tikzpicture}}\par
\small Hình {n}. Biên độ điện áp theo vạch thang đo; đường cong tính từ vị trí nút.
\end{{center}}'''

BODY=BODY.replace('WAVE5',wave(4,24,48,24,32,26.6,2/7,[26.6,32,38.6,44]))
BODY=BODY.replace('WAVE6',wave(5,9,34,20,18.2,21.2,3/7,[11.2,18.2,21.2,28.2,31.2]))
for name,sid in students:
    stem=f'EE5430_Assignment_2_{name.replace(" ","_")}_{sid}'
    tex=SRC/(stem+'.tex')
    content=(PRE+BODY).replace('STUDENT',name).replace('SID',sid).replace('LOGO',(ROOT/'assets/hcmut_logo.png').as_posix())
    tex.write_text(content,encoding='utf-8')
    for _ in range(2):
        proc=subprocess.run(['xelatex','-interaction=nonstopmode','-halt-on-error',f'-output-directory={TMP}',str(tex)],cwd=ROOT,capture_output=True,text=True,encoding='utf-8',errors='replace')
        (TMP/(stem+'.console.txt')).write_text(proc.stdout,encoding='utf-8')
        if proc.returncode: raise RuntimeError(proc.stdout[-5000:])
    (OUT/(stem+'.pdf')).write_bytes((TMP/(stem+'.pdf')).read_bytes())
    print(OUT/(stem+'.pdf'))


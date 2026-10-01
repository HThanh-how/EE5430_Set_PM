from pathlib import Path
import cmath, math, json
from reportlab.pdfgen import canvas
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.ttfonts import TTFont
from reportlab.lib.colors import HexColor
from pypdf import PdfReader

ROOT = Path(__file__).resolve().parents[1]
OUT = ROOT / 'output/pdf'
OUT.mkdir(parents=True, exist_ok=True)
pdfmetrics.registerFont(TTFont('Arial', 'C:/Windows/Fonts/arial.ttf'))
pdfmetrics.registerFont(TTFont('ArialBold', 'C:/Windows/Fonts/arialbd.ttf'))
students = [('Nguyen Thai Thanh Binh','2570175'),('Vu Tien Giang','2570188'),('Pham Huy Thanh','2570317')]

def direct(z,z0,lam):
    g=(z-z0)/(z+z0); r=abs(g); a=cmath.phase(g); s=(1+r)/(1-r)
    return dict(g=g,r=r,a=a,s=s,dmax=(a%(2*math.pi))*lam/(4*math.pi),dmin=((a-math.pi)%(2*math.pi))*lam/(4*math.pi),zmin=z0/s,zmax=z0*s)

def inverse(s,z0,lam,delta):
    r=(s-1)/(s+1); g=-r*cmath.exp(1j*4*math.pi*delta/lam)
    return g,z0*(1+g)/(1-g)

a=direct(25-50j,50,10); b=direct(150+75j,75,20)
zin=75*((150+75j)+1j*75*math.tan(2*math.pi*3/20))/(75+1j*(150+75j)*math.tan(2*math.pi*3/20))
inv=[inverse(*v) for v in [(3,50,40,-8),(1.5,100,60,6),(1.8,50,24,5.4),(2.5,75,20,-3)]]
for (s,z0,lam,delta),(g,z) in zip([(3,50,40,-8),(1.5,100,60,6),(1.8,50,24,5.4),(2.5,75,20,-3)], inv):
    recovered=(z-z0)/(z+z0)
    assert abs(recovered-g)<1e-12
    assert abs((1+abs(recovered))/(1-abs(recovered))-s)<1e-12
    assert abs(g*cmath.exp(-1j*4*math.pi*delta/lam)+abs(g))<1e-12
def comp(z): return f'{z.real:.4f} '+('+' if z.imag>=0 else '-')+f' j{abs(z.imag):.4f}'

class Report:
    def __init__(self,name,sid):
        self.name=name; self.sid=sid; self.page=0
        self.path=OUT/f'EE5430_Assignment_2_{name.replace(" ","_")}_{sid}.pdf'
        self.c=canvas.Canvas(str(self.path),pagesize=(595.28,841.89))
        self.c.setTitle(f'EE5430 - Bài tập 2 - {name}')
    def start(self,title):
        if self.page: self.c.showPage()
        self.page+=1; self.y=752
        self.c.setFillColor(HexColor('#18324b')); self.c.setFont('ArialBold',18)
        self.c.drawString(44,790,'EE5430 | ĐƯỜNG TRUYỀN & SÓNG ĐỨNG')
        self.c.setFont('Arial',10); self.c.drawString(44,772,f'{self.name}  •  MSSV {self.sid}')
        self.c.setFont('Arial',9); self.c.drawString(44,30,'Lời giải theo đề ảnh gồm 6 bài • Quy ước e^(jωt)')
        self.c.drawRightString(551,30,str(self.page)); self.heading(title)
    def heading(self,t):
        self.y-=8; self.c.setFont('ArialBold',13); self.c.setFillColor(HexColor('#18324b')); self.c.drawString(44,self.y,t); self.y-=24
    def line(self,t,bold=False):
        self.c.setFont('ArialBold' if bold else 'Arial',10.5); self.c.setFillColor(HexColor('#202b34'))
        assert pdfmetrics.stringWidth(t,'ArialBold' if bold else 'Arial',10.5)<509,t
        self.c.drawString(44,self.y,t); self.y-=18
    def lines(self,items):
        for t in items:self.line(t)
        self.y-=8
    def smith(self):
        c=self.c; cx=295; cy=267; R=157
        def curve(points,col):
            p=c.beginPath(); p.moveTo(cx+R*points[0].real,cy+R*points[0].imag)
            for q in points[1:]:p.lineTo(cx+R*q.real,cy+R*q.imag)
            c.setStrokeColor(HexColor(col)); c.setLineWidth(.45); c.drawPath(p)
        c.setStrokeColor(HexColor('#73899a')); c.circle(cx,cy,R)
        for r in [0,.2,.5,1,2,5]:
            pts=[]
            for k in range(801):
                x=math.tan(-math.pi/2+.001+k*(math.pi-.002)/800)
                z=complex(r,x);pts.append((z-1)/(z+1))
            curve(pts,'#c0cbd2')
        for x in [-5,-2,-1,-.5,-.2,.2,.5,1,2,5]:
            pts=[]
            for k in range(501):
                r=(k/500)*100;z=complex(r,x);pts.append((z-1)/(z+1))
            curve(pts,'#c0cbd2')
        c.setStrokeColor(HexColor('#16817a'));c.setLineWidth(1.2);c.circle(cx,cy,R*a['r'])
        c.setStrokeColor(HexColor('#73899a')); c.line(cx-R,cy,cx+R,cy)
        for g,label,dx,dy in [(a['g'],'zL = 0.5 - j1',-20,-18),(complex(a['r'],0),'Vmax',6,8),(complex(-a['r'],0),'Vmin',-35,8)]:
            x=cx+R*g.real;y=cy+R*g.imag;c.setFillColor(HexColor('#c14b37'));c.circle(x,y,3,fill=1,stroke=0)
            c.setFont('Arial',10);c.drawString(x+dx,y+dy,label)
        c.setFillColor(HexColor('#202b34'));c.setFont('Arial',10)
        c.drawString(95,84,'Đi về nguồn: quay theo chiều kim đồng hồ trên vòng |Γ| không đổi.')

for name,sid in students:
    q=Report(name,sid)
    q.start('Cơ sở tính toán và đồ thị Smith (bài 1)')
    q.lines(['Giả thiết đường truyền không tổn hao; d ≥ 0 đo từ tải về phía nguồn.',
        'ΓL = (ZL - Z0)/(ZL + Z0) = ρe^(jθ);  S = VSWR = (1 + ρ)/(1 - ρ).',
        'β = 2π/λ;  Γ(d) = ΓL e^(-j2βd);  Z(d) = Z0[1 + Γ(d)]/[1 - Γ(d)].',
        'Vmax khi θ - 2βd = 0 (mod 2π); Vmin khi θ - 2βd = π (mod 2π).',
        'Zmax = Z0 S; Zmin = Z0/S. Các cực trị cùng loại cách nhau λ/2.',
        'Với phép nối tắt: ΓSC = -1. Gọi Δd = dmin,tải - dmin,nối tắt.',
        'Suy ra ΓL = -ρ e^(j4πΔd/λ). Δd > 0 nghĩa là tải có nút xa tải hơn.',
        'Trên Smith: chuẩn hóa zL = ZL/Z0, đọc ΓL và quay về nguồn tới trục thực.',
        'Các số dưới đây tính bằng công thức để kiểm tra độ chính xác khi đọc đồ thị.'])
    q.smith()
    q.start('Dạng 1 | Hệ số phản xạ, VSWR và cực trị')
    q.heading('Bài 1 - Z0 = 50 Ω; ZL = 25 - j50 Ω; λ = 10 cm')
    q.lines(['Chuẩn hóa: zL = 0.5 - j1 (điểm đã đánh dấu trên đồ thị Smith).',
        f'ΓL = (-25 - j50)/(75 - j50) = {comp(a["g"])}.',
        f'ρ = {a["r"]:.6f}; θ = {math.degrees(a["a"]):.4f}° = {math.degrees(a["a"])%360:.4f}° (mod 360°).',
        f'VSWR = (1 + {a["r"]:.6f})/(1 - {a["r"]:.6f}) = {a["s"]:.4f}.',
        '2β = 4π/λ = 72°/cm. Chọn nghiệm không âm nhỏ nhất:',
        f'dmin = [(θ - 180°) mod 360°]/72 = {a["dmin"]:.4f} cm.',
        f'dmax = [θ mod 360°]/72 = {a["dmax"]:.4f} cm.',
        f'Z(dmin) = Z0/S = {a["zmin"]:.4f} Ω (thuần thực).',
        f'Z(dmax) = Z0S = {a["zmax"]:.4f} Ω (thuần thực).'])
    q.heading('Bài 2 - Z0 = 75 Ω; ZL = 150 + j75 Ω; f = 1.5 GHz')
    q.lines(['Điện môi không khí: vp ≈ 3×10⁸ m/s, λ = vp/f = 0.20 m = 20 cm.',
        f'ΓL = (75 + j75)/(225 + j75) = {comp(b["g"])}.',
        f'ρ = {b["r"]:.6f}; θ = {math.degrees(b["a"]):.4f}°; VSWR = {b["s"]:.4f}.',
        '2β = 36°/cm; áp dụng các điều kiện pha như bài 1:',
        f'dmax = θ/36 = {b["dmax"]:.4f} cm.',
        f'dmin = [(θ - 180°) mod 360°]/36 = {b["dmin"]:.4f} cm.',
        'Tại d = 3 cm: βd = 54°; tan(βd) = 1.376382.',
        'Zin = Z0[ZL + jZ0 tan(βd)]/[Z0 + jZL tan(βd)].',
        f'Zin(3 cm) = {comp(zin)} Ω.',
        f'Kiểm tra: Zmin = {b["zmin"]:.4f} Ω; Zmax = {b["zmax"]:.4f} Ω.'])
    q.start('Dạng 2 | Xác định tải từ phép đo sóng đứng')
    q.heading('Bài 3 - Z0 = 50 Ω; S = 3; Δxmin = 20 cm')
    g,z=inv[0]
    q.lines(['Hai nút liên tiếp cách nhau λ/2, nên λ = 2×20 = 40 cm.',
        'ρ = (S - 1)/(S + 1) = (3 - 1)/(3 + 1) = 0.5.',
        'Khi thay tải bằng ngắn mạch, nút dịch 8 cm về nguồn:',
        'dmin,nối tắt = dmin,tải + 8 cm => Δd = -8 cm.',
        'Vì vậy ΓL = -0.5 exp[-j4π(8)/40] = 0.5 góc 36°.',
        f'ΓL = {comp(g)}.',
        'ZL = Z0(1 + ΓL)/(1 - ΓL).',
        f'ZL = {comp(z)} Ω.',
        'Tải có phần phản kháng dương: tính cảm.',
        'Kiểm tra: nút tải đầu tiên tại 12 cm; nối tắt có nút tại 20 cm.',
        'Dịch từ 12 đến 20 cm đúng 8 cm về nguồn.'])
    q.heading('Bài 4 - Z0 = 100 Ω; S = 1.5; Δxmin = 30 cm')
    g,z=inv[1]
    q.lines(['λ = 2Δxmin = 60 cm; ρ = (1.5 - 1)/(1.5 + 1) = 0.2.',
        'Thay bằng ngắn mạch làm nút dịch 6 cm về tải:',
        'dmin,nối tắt = dmin,tải - 6 cm => Δd = +6 cm.',
        'ΓL = -0.2 exp[j4π(6)/60] = 0.2 góc (-108°).',
        f'ΓL = {comp(g)}.',
        f'ZL = 100(1 + ΓL)/(1 - ΓL) = {comp(z)} Ω.',
        'Im(ZL) < 0 nên tải có tính dung.',
        'Kiểm tra: nút tải đầu tiên tại 6 cm; nối tắt có nút tại 0 cm.',
        'Dịch từ 6 đến 0 cm đúng 6 cm về tải.',
        'Lưu ý: dịch chuyển mô tả sự thay tải bằng ngắn mạch;',
        'không được dùng trực tiếp dấu đó cho Δd = dmin,tải - dmin,nối tắt.'])
    q.start('Dạng 3 | Đo bằng đường dây có khe đo')
    q.heading('Bài 5 - Z0 = 50 Ω; S = 1.8; nút tại 32.0 và 44.0 cm')
    g,z=inv[2]
    q.lines(['λ/2 = 44.0 - 32.0 = 12.0 cm => λ = 24.0 cm = 0.24 m.',
        'f = vp/λ ≈ (3×10⁸)/0.24 = 1.25 GHz.',
        'Nối tắt làm nút từ 32.0 cm dịch về tải tới 26.6 cm.',
        'Số chỉ tăng về nguồn (theo mũi tên): Δd = 32.0 - 26.6 = +5.4 cm.',
        'ρ = (1.8 - 1)/(1.8 + 1) = 2/7 = 0.285714.',
        '4πΔd/λ = 162°; ΓL = -(2/7)e^(j162°) = (2/7) góc (-18°).',
        f'ΓL = {comp(g)}.',
        f'ZL = 50(1 + ΓL)/(1 - ΓL) = {comp(z)} Ω.',
        'Kết quả: λ = 24 cm; f ≈ 1.25 GHz; tải có tính dung.',
        'Kiểm tra pha: nút tải xa nút nối tắt 5.4 cm, đúng Δd = 0.225λ.'])
    q.heading('Bài 6 - Z0 = 75 Ω; S = 2.5; thang tăng về nguồn')
    g,z=inv[3]
    q.lines(['λ/2 = 28.2 - 18.2 = 10.0 cm => λ = 20.0 cm = 0.20 m.',
        'f = vp/λ ≈ (3×10⁸)/0.20 = 1.50 GHz.',
        'Nút tải tại 18.2 cm; nút nối tắt tương ứng tại 21.2 cm.',
        'Δd = 18.2 - 21.2 = -3.0 cm (nút tải gần tải hơn).',
        'ρ = (2.5 - 1)/(2.5 + 1) = 3/7 = 0.428571.',
        '4πΔd/λ = -108°; ΓL = -(3/7)e^(-j108°) = (3/7) góc 72°.',
        f'ΓL = {comp(g)}.',
        f'ZL = 75(1 + ΓL)/(1 - ΓL) = {comp(z)} Ω.',
        'Kết quả: f ≈ 1.50 GHz; tải có tính cảm.',
        'Có thể dùng nút nối tắt 11.2 cm: Δd = +7.0 cm.',
        'Hai cách ghép lệch λ/2, làm pha lệch 2π nên cho cùng ΓL và ZL.'])
    q.heading('Kiểm tra chung')
    q.lines(['Thay các ZL tìm được vào ΓL = (ZL - Z0)/(ZL + Z0) thu lại đúng ρ.',
        'VSWR tính ngược lần lượt là 3; 1.5; 1.8; 2.5 cho bài 3-6.',
        'Dùng vp = 299 792 458 m/s: f5 = 1.24914 GHz; f6 = 1.49896 GHz.',
        'Các kết quả chính dùng vp ≈ 3×10⁸ m/s theo quy ước bài tập.'])
    q.c.save()
    reader=PdfReader(q.path)
    assert len(reader.pages)==4
    assert all(len(p.extract_text())>400 for p in reader.pages)
    print(q.path)

print('Numerical results:',a,b,'Zin3=',zin,'inverse=',[(comp(g),comp(z)) for g,z in inv])



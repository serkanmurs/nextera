filepath = 'src/app/page.tsx'
content = open(filepath, 'r').read()

print("PDF pasta grafik + logo fix...")

# Mevcut PDF butonundaki conic-gradient'i SVG pie chart ile degistir
# Ve logo ekle

# Mevcut pie chart satiri
old_pie = 'h+="<div style=\\"display:flex;justify-content:center;margin:20px 0\\"><div style=\\"width:180px;height:180px;border-radius:50%;background:conic-gradient(#D97706 0% "+pP2+"%, #DC2626 "+pP2+"% "+(pP2+pK2)+"%, #1E40AF "+(pP2+pK2)+"% "+(pP2+pK2+pM2)+"%, #059669 "+(pP2+pK2+pM2)+"% 100%)\\"></div></div>"'

new_pie = '''var svgPie=(function(){
            var r=80,cx=90,cy=90;
            var data2=[{v:pP2,c:"#D97706"},{v:pK2,c:"#DC2626"},{v:pM2,c:"#1E40AF"},{v:pB2,c:"#059669"}];
            var paths="";var cumul=0;
            data2.forEach(function(d){
              if(d.v<=0)return;
              var startAngle=cumul/100*2*Math.PI-Math.PI/2;
              var endAngle=(cumul+d.v)/100*2*Math.PI-Math.PI/2;
              var largeArc=d.v>50?1:0;
              var x1=cx+r*Math.cos(startAngle);
              var y1=cy+r*Math.sin(startAngle);
              var x2=cx+r*Math.cos(endAngle);
              var y2=cy+r*Math.sin(endAngle);
              if(d.v>=100){
                paths+="<circle cx=\\""+cx+"\\" cy=\\""+cy+"\\" r=\\""+r+"\\" fill=\\""+d.c+"\\"/>";
              }else{
                paths+="<path d=\\"M "+cx+" "+cy+" L "+x1+" "+y1+" A "+r+" "+r+" 0 "+largeArc+" 1 "+x2+" "+y2+" Z\\" fill=\\""+d.c+"\\"/>";
              }
              cumul+=d.v;
            });
            return "<svg width=\\"180\\" height=\\"180\\" viewBox=\\"0 0 180 180\\">"+paths+"</svg>";
          })();
          h+="<div style=\\"display:flex;justify-content:center;margin:20px 0\\">"+svgPie+"</div>"'''

if old_pie in content:
    content = content.replace(old_pie, new_pie)
    print("  OK 1. SVG pasta grafik eklendi")
else:
    print("  SKIP 1. Pie chart satiri bulunamadi")

# 2. Logo ekle - NextERA text yerine logo img
old_logo = 'h+="<div><div style=\\"font-size:28px;font-weight:800;color:#0E7490\\">Next<span style=\\"color:#F97316\\">ERA</span></div><div style=\\"font-size:12px;color:#64748B\\">Ki\\u015filik Analiz Raporu</div></div>"'

new_logo = 'h+="<div style=\\"display:flex;align-items:center;gap:12px\\"><img src=\\""+window.location.origin+"/logo.png\\" style=\\"width:48px;height:48px;border-radius:10px\\" onerror=\\"this.style.display=\'none\'\\"/><div><div style=\\"font-size:28px;font-weight:800;color:#0E7490\\">Next<span style=\\"color:#F97316\\">ERA</span></div><div style=\\"font-size:12px;color:#64748B\\">Ki\\u015filik Analiz Raporu</div></div></div>"'

if old_logo in content:
    content = content.replace(old_logo, new_logo)
    print("  OK 2. Logo eklendi")
else:
    print("  SKIP 2. Logo satiri bulunamadi")

open(filepath, 'w').write(content)
print("")
print("Kaydedildi. Simdi: npm run build")

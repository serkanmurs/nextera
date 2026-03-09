filepath = 'src/app/page.tsx'
content = open(filepath, 'r').read()

# Satir 309'daki conic-gradient'i SVG ile degistir
old_line = 'h+="<div style=\\"width:180px;height:180px;border-radius:50%;background:conic-gradient(#D97706 0% "+pP2+"%, #DC2626 "+pP2+"% "+(pP2+pK2)+"%, #1E40AF "+(pP2+pK2)+"% "+(pP2+pK2+pM2)+"%, #059669 "+(pP2+pK2+pM2)+"% 100%);box-shadow:0 2px 8px rgba(0,0,0,0.1)\\"></div></div>";'

new_line = '''var svgParts="";var cum=0;
          [{v:pP2,c:"#D97706"},{v:pK2,c:"#DC2626"},{v:pM2,c:"#1E40AF"},{v:pB2,c:"#059669"}].forEach(function(sl){
            if(sl.v<=0)return;
            var sA=cum/100*2*Math.PI-Math.PI/2;
            var eA=(cum+sl.v)/100*2*Math.PI-Math.PI/2;
            var la=sl.v>50?1:0;
            var x1=90+80*Math.cos(sA);
            var y1=90+80*Math.sin(sA);
            var x2=90+80*Math.cos(eA);
            var y2=90+80*Math.sin(eA);
            if(sl.v>=100){svgParts+="<circle cx=\\"90\\" cy=\\"90\\" r=\\"80\\" fill=\\""+sl.c+"\\"/>";}
            else{svgParts+="<path d=\\"M 90 90 L "+x1+" "+y1+" A 80 80 0 "+la+" 1 "+x2+" "+y2+" Z\\" fill=\\""+sl.c+"\\"/>";}
            cum+=sl.v;
          });
          h+="<svg width=\\"180\\" height=\\"180\\" viewBox=\\"0 0 180 180\\">"+svgParts+"</svg></div>";'''

if old_line in content:
    content = content.replace(old_line, new_line)
    print("OK - Print PDF pasta grafigi SVG ile degistirildi")
else:
    print("BULUNAMADI - farkli format")

open(filepath, 'w').write(content)
print("Kaydedildi. Simdi: npm run build")

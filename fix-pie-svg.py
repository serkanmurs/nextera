filepath = 'src/app/page.tsx'
content = open(filepath, 'r').read()

print("Ekran pasta grafigini SVG ile degistirme...")

# Uygulama ekranindaki conic-gradient pie chart'i bul
# Bu PersonalityTestScreen sonuc ekraninda
old_conic = '''<div style={{display:"flex",justifyContent:"center",marginBottom:24}}>
          <div style={{width:180,height:180,borderRadius:"50%",background:`conic-gradient(#D97706 0% ${pP}%, #DC2626 ${pP}% ${pP+pK}%, #1E40AF ${pP+pK}% ${pP+pK+pM}%, #059669 ${pP+pK+pM}% 100%)`,boxShadow:"0 2px 8px rgba(0,0,0,0.1)"}}/>
        </div>'''

new_svg_pie = '''<div style={{display:"flex",justifyContent:"center",marginBottom:24}}>
          <svg width="180" height="180" viewBox="0 0 180 180">
            {(()=>{
              const r=80,cx=90,cy=90;
              const slices=[{v:pP,c:"#D97706"},{v:pK,c:"#DC2626"},{v:pM,c:"#1E40AF"},{v:100-pP-pK-pM,c:"#059669"}];
              let cumul=0;
              return slices.map((s,i)=>{
                if(s.v<=0)return null;
                const startA=cumul/100*2*Math.PI-Math.PI/2;
                const endA=(cumul+s.v)/100*2*Math.PI-Math.PI/2;
                const large=s.v>50?1:0;
                const x1=cx+r*Math.cos(startA);
                const y1=cy+r*Math.sin(startA);
                const x2=cx+r*Math.cos(endA);
                const y2=cy+r*Math.sin(endA);
                cumul+=s.v;
                if(s.v>=100)return <circle key={i} cx={cx} cy={cy} r={r} fill={s.c}/>;
                return <path key={i} d={`M ${cx} ${cy} L ${x1} ${y1} A ${r} ${r} 0 ${large} 1 ${x2} ${y2} Z`} fill={s.c}/>;
              });
            })()}
          </svg>
        </div>'''

if old_conic in content:
    content = content.replace(old_conic, new_svg_pie)
    print("  OK - Ekran pasta grafigi SVG ile degistirildi")
else:
    # Alternatif arama - farkli format olabilir
    alt = 'conic-gradient(#D97706 0%'
    if alt in content:
        # Tum conic-gradient div'ini bul
        idx = content.find(alt)
        div_start = content.rfind('<div style={{display:"flex",justifyContent:"center"', idx - 200, idx)
        if div_start > -1:
            # Kapanisini bul
            depth = 0
            j = div_start
            div_end = -1
            in_jsx = True
            while j < len(content):
                if content[j:j+5] == '<div ' or content[j:j+4] == '<div>':
                    depth += 1
                elif content[j:j+6] == '</div>':
                    depth -= 1
                    if depth == 0:
                        div_end = j + 6
                        break
                elif content[j:j+2] == '/>':
                    if depth == 1 and 'borderRadius' in content[j-100:j]:
                        div_end = j + 2
                        # Sonraki </div> i de bul
                        next_close = content.find('</div>', div_end)
                        if next_close > -1:
                            div_end = next_close + 6
                        break
                j += 1
            
            if div_end > -1:
                content = content[:div_start] + new_svg_pie + content[div_end:]
                print("  OK - Alternatif: Ekran pasta grafigi SVG ile degistirildi")
            else:
                print("  SKIP - Div sonu bulunamadi")
        else:
            print("  SKIP - Div basi bulunamadi")
    else:
        print("  SKIP - conic-gradient bulunamadi")

# Ana sayfadaki mini kart'taki da conic-gradient varsa degistir
# (Bu sadece sonuc ekraninda, kart'ta yok)

open(filepath, 'w').write(content)
print("Kaydedildi. Simdi: npm run build")

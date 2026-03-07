filepath = 'src/app/page.tsx'
content = open(filepath, 'r').read()

print("Yorum sistemi guncelleniyor...")

# 1. Mevcut QCOMMENTS dizisini ve kisisel yorumlar bolumunu kaldir
# QCOMMENTS dizisini bul ve kaldir
qc_start = content.find('// Soru bazli yorumlar')
if qc_start > -1:
    qc_end = content.find('];\n', content.find('const QCOMMENTS', qc_start))
    if qc_end > -1:
        qc_end += 3  # ];\n
        content = content[:qc_start] + content[qc_end:]
        print("  OK 1. QCOMMENTS kaldirildi")

# 2. PD icindeki kisa s/w yerine detayli ozet paragraflar ekle
# Mevcut PD'yi tamamen degistir
old_PD_start = "const PD: Record<string,{t:string;c:string;bg:string;e:string;s:string[];w:string[]}> = {"
old_PD_end = "};\n"

pd_start = content.find(old_PD_start)
if pd_start > -1:
    # PD'nin sonunu bul - }; ile biter
    # Icice {} oldugundan dikkatli olmali
    depth = 0
    i = content.find('{', pd_start)
    pd_end = -1
    while i < len(content):
        if content[i] == '{':
            depth += 1
        elif content[i] == '}':
            depth -= 1
            if depth == 0:
                pd_end = i + 1
                break
        i += 1
    
    if pd_end > -1:
        # Sonraki ; ve newline'i da al
        if pd_end < len(content) and content[pd_end] == ';':
            pd_end += 1
        
        new_PD = '''const PD: Record<string,{t:string;c:string;bg:string;e:string;s:string[];w:string[];summary:string}> = {
  P:{t:"Popüler Optimist",c:"#D97706",bg:"#FEF3C7",e:"🌟",
    s:["Eğlenceli ve enerjik","Kolay arkadaşlık kurar","İyimser ve coşkulu","İlham verici","Yaratıcı fikirler üretir"],
    w:["Odaklanma süresi kısa olabilir","Dağınık olabilir","Detayları atlayabilir","Abartıya kaçabilir"],
    summary:"Canlı bir kişiliğe sahipsin. Enerji seviyen yüksek ve insanlarla bir arada olmak senin için büyük bir motivasyon kaynağı. Esprili ve eğlenceli yapınla ortamlara renk katıyor, doğal karizmanla insanları kendine çekiyorsun. Yaratıcı fikirlerin ve iyimser bakış açın sayesinde çevrene ilham veriyorsun. Kolay arkadaşlık kuruyor, sıcakkanlı tavırlarınla insanları rahatlatıyorsun.\\n\\nAncak dikkat etmen gereken bazı noktalar var. Odaklanma süren kısa olabiliyor ve detayları atlama eğiliminde olabiliyorsun. Dağınıklık ve abartıya kaçma gibi konularda kendini geliştirmen faydalı olacaktır. Her ortamda aynı dozda espri yaparsan kantarın topuzunu kaçırabilirsin. Unutma ki enerjini doğru yönettiğinde etrafındaki herkes için gerçek bir ilham kaynağı olabilirsin."},
  K:{t:"Güçlü Kolerik",c:"#DC2626",bg:"#FEE2E2",e:"🔥",
    s:["Doğal lider","Kararlı ve hedef odaklı","Hızlı karar verir","Organize ve üretken","Cesur ve risk alır"],
    w:["Sabırsız olabilir","Otoriter davranabilir","Başkalarının duygularını göz ardı edebilir","İnatçı olabilir"],
    summary:"Oldukça etkili ve etkileyici bir duruşun var. Başkalarının karşı gelmekte tereddüt edeceği kadar güçlü ve hakim bir karaktere sahipsin. Doğal bir lidersin; kararlı, hedef odaklı ve organize çalışırsın. Cesursun, risk almaktan korkmuyorsun. Hızlı karar verir ve sonuç odaklı hareket edersin.\\n\\nGelişim alanlarına baktığımızda, sabırsızlık ve otoriter davranma eğilimin öne çıkıyor. Başkalarına neyi nasıl yapması gerektiğini söylemekten kaçınmıyorsun. Standartların o kadar yüksek ki seni tatmin etmek hayli güç olabiliyor. Başkalarının duygularını göz ardı etmemeye özen göster. İnatçılığını azaltıp empatiyi artırdığında, liderlik kapasiten çok daha etkili hale gelecektir."},
  M:{t:"Mükemmeliyetçi Melankolik",c:"#1E40AF",bg:"#DBEAFE",e:"💎",
    s:["Detaycı ve analitik","Planlı ve düzenli","Derin düşünür","Yaratıcı ve yetenekli","Sadık ve özverili"],
    w:["Aşırı eleştirici olabilir","Karamsarlığa yatkın","Karar vermekte zorlanabilir","Aşırı hassas olabilir"],
    summary:"Planlama senin için çok önemli. Her şeyin bir program dahilinde ilerlemesini istersin ve belirsizlikler seni rahatsız eder. Sistemli, düzenli ve detaycı bir yapın var. Derin düşünür, analitik yaklaşırsın. Yaratıcılığın ve yeteneklerin sayesinde elinden çıkan işler kaliteli olur. Sadık ve özverili birisin.\\n\\nAncak mükemmel için sürekli iyiden fedakarlık ediyorsun. Karar vermekten çekinebiliyor, pek çok fırsatı kaçırabiliyorsun. Duygularını ve coşkunu ifade etmekte kendini sınırlıyorsun. Aşırı duyarlılık ve eleştirici bakış açın bazen seni ve çevreni yorabiliyor. Yerli yersiz endişeler yaşayıp huzursuz olabiliyorsun. İhtiyatı elden bırakma ama çok da elinde sıkma. Kendine biraz daha güven ve mükemmeli beklemek yerine harekete geç."},
  B:{t:"Barışçıl Soğukkanlı",c:"#059669",bg:"#D1FAE5",e:"🌿",
    s:["Sakin ve dengeli","İyi dinleyici","Uyumlu ve barışçıl","Sabırlı ve hoşgörülü","Güvenilir ve tutarlı"],
    w:["Kararsız olabilir","Motivasyon eksikliği","Değişime dirençli","Pasif kalabilir"],
    summary:"Karşındaki insan için kolay kolay bulunmayan hazine gibi bir özelliğin var: Dinlemek. İyi bir dinleyicisin ve bu insanları çok rahatlatıyor. Duygu durumun genellikle tutarlı; olaylar karşısında beklenmedik tepkiler vermiyorsun. Sakin, dengeli ve uyumlu yapınla insanlar arasındaki sorunlarda farklılıkları uzlaştırmaya çalışıyorsun.\\n\\nGelişim alanlarına baktığımızda, dikkatleri üzerine toplamamak için geride durma eğiliminde olabiliyorsun. Kararsızlık ve motivasyon eksikliği yaşayabiliyor, değişime direnç gösterebiliyorsun. Bir çare düşünüyorsun ama sonra bunun iyi sonuç vermeyeceğini düşünüyorsun. Hep bir isteksizlik hali olabiliyor. Çocuktan büyüğe herkesin istediği gibi davranmasına göz yumabiliyorsun. Kendi sesini daha fazla duyur ve harekete geçmekten çekinme."},
};'''

        content = content[:pd_start] + new_PD + content[pd_end:]
        print("  OK 2. PD ozet paragraflarla guncellendi")

# 3. Sonuc ekranindaki kisisel yorumlar bolumunu ozet ile degistir
old_personal = '{/* Kisisel Yorumlar */}'
if old_personal in content:
    # Kisisel Yorumlar div'ini bul ve degistir
    ps = content.find(old_personal)
    # Bu bolumun sonunu bul - Kaynak satirina kadar
    pe = content.find("Kaynak: Florence Littauer", ps)
    if pe > -1:
        # Geriye git, <div bulana kadar
        pe2 = content.rfind("'<div style={{fontSize:11", 0, pe)
        # Daha basit: tum personal comments bolumunu degistir
        # ps'den Kaynak div'ine kadar olan kismi degistir
        
        new_personal = '''{/* Genel Yorum */}
        <div style={{marginTop:20}}>
          <h3 style={{margin:"0 0 14px",fontSize:18,fontWeight:800,color:"#0F172A"}}>Kişilik Profilin Hakkında</h3>
          <div style={{padding:"16px",borderRadius:12,background:PD[dom].bg,border:"1px solid "+PD[dom].c+"20"}}>
            {PD[dom].summary.split("\\n\\n").map((p: string,i: number)=>(
              <p key={i} style={{margin:i===0?"0 0 12px 0":"12px 0 0 0",fontSize:14,color:"#0F172A",lineHeight:1.7}}>{p}</p>
            ))}
          </div>
        </div>

        '''
        
        # ps'den kaynak div'inin basina kadar degistir
        kaynak_div_start = content.rfind('<div style={{fontSize:11,color:"#94A3B8"', ps, pe + 50)
        if kaynak_div_start > -1:
            content = content[:ps] + new_personal + content[kaynak_div_start:]
            print("  OK 3. Kisisel yorumlar genel ozetle degistirildi")
        else:
            print("  SKIP 3. Kaynak div basi bulunamadi")
else:
    print("  SKIP 3. Kisisel Yorumlar blogu bulunamadi")

# 4. PDF icindeki yorumlari da ozet ile degistir
old_pdf_comments = '// Kisisel yorumlar'
if old_pdf_comments in content:
    pc_start = content.find(old_pdf_comments)
    pc_end = content.find('pdf.save("NextERA_Kisilik_Raporu.pdf");', pc_start)
    if pc_end > -1:
        new_pdf_comments = '''// Genel yorum
            y+=10;
            if(y>250){pdf.addPage();y=20;}
            pdf.setFontSize(14);pdf.setTextColor(14,116,144);pdf.text("Kisilik Profilin Hakkinda",margin,y);y+=8;
            pdf.setFontSize(10);pdf.setTextColor(15,23,42);
            const summaryText=PD[dom].summary.replace(/\\\\n\\\\n/g," ");
            const sLines=pdf.splitTextToSize(summaryText,w-2*margin);
            sLines.forEach((line: string)=>{
              if(y>275){pdf.addPage();y=20;}
              pdf.text(line,margin,y);y+=5;
            });
            y+=8;
            
            '''
        content = content[:pc_start] + new_pdf_comments + content[pc_end:]
        print("  OK 4. PDF yorumlar ozetle guncellendi")

# 5. QCOMMENTS referanslarini temizle (artik kullanilmiyor)
content = content.replace('QCOMMENTS', 'QCOMMENTS_UNUSED')
# Aslinda tamamen kaldiralim - kullanilmayan referanslar
if 'QCOMMENTS_UNUSED' in content:
    # Sadece tanimi kaldirmistik, referanslari da kaldiralim
    content = content.replace('QCOMMENTS_UNUSED', 'null')
    print("  OK 5. QCOMMENTS referanslari temizlendi")

# SAVE
open(filepath, 'w').write(content)
print("")
print("YORUM SISTEMI GUNCELLENDI!")
print("  - 40 tekil yorum yerine genel ozet paragraflar")
print("  - Her kisilik tipi icin detayli 2 paragraf yorum")
print("  - PDF'de de ozet gorunuyor")
print("")
print("Simdi: npm run build")

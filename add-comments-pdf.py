filepath = 'src/app/page.tsx'
content = open(filepath, 'r').read()

print("Detayli yorum + PDF fix basliyor...")

# ============================================================
# 1. YORUM VERİSİ - Her sorunun her seçeneği için yorum
# House of Human formatında - seçime özel paragraflar
# ============================================================

# Yorumları PQ dizisinin yanına COMMENTS olarak ekleyeceğiz
# Her sorunun 4 seçeneği için 4 yorum

old_PD = 'const PD: Record<string,{t:string;c:string;bg:string;e:string;s:string[];w:string[]}>'

COMMENTS_DATA = '''
// Soru bazli yorumlar - her sorunun 4 secenegi icin yorum
const QCOMMENTS: string[][] = [
  // 1: Maceraperest/Uyumlu/Canli/Analitik
  ["Cesursun. Yeni bir girişimde bulunmaktan ve bir konuda ustalaşmaktan çekinmiyorsun. Sakin hayat sürmek isteyen arkadaşlarını bazen yorabilirsin.",
   "Başkalarının da ihtiyaçları olabileceği konusunda empati gösteriyorsun ve başkalarının ihtiyaçlarına saygı duyuyorsun.",
   "Canlı bir kişiliğe sahipsin. Enerji seviyen yüksek. İnsanlarla bir arada olmak senin için bir fırsat.",
   "Planlama senin için çok önemli. Sana göre her şey bir program dahilinde ilerlemeli. Belirsizlikler seni rahatsız eder."],
  // 2: Israrci/Sakaci/Ikna edici/Bariscil
  ["Oldukça etkili bir duruşun var. Başkalarının karşı gelmekte tereddüt edeceği kadar etkili ve hakim bir karaktere sahipsin.",
   "Esprilisin. Eğlenceli bir insansın. Her ortamda aynı dozda espri yaparsan kantarın topuzunu kaçırabilirsin.",
   "Karizmatik bir kişiliğe sahipsin. Başkalarını harekete geçirmeyi ve konuya katmayı başarabiliyorsun.",
   "Duygu durumunun genellikle tutarlı olduğunu söyleyebiliriz. Olaylar karşısında beklenmedik tepkiler vermiyorsun."],
  // 3: Uysal/Ozverili/Sosyal/Azimli
  ["Öyle bir duruşun var ki insanlar senden bir zarar gelmeyeceğini hissedebiliyorlar.",
   "Sistemli bir şekilde işlerini düzenlemeyi ve bunun için metodlar kullanmayı seviyorsun.",
   "İnsanlarla bir arada olmak senin için fırsat. Şirinliğini, esprilerini göstermek için bir fırsat.",
   "Pek korkmuyorsun. Risk almaya hazırsın. Şans cesurlardan yanadır."],
  // 4: Dusunceli/Kontrollu/Rekabetci/Inandirici
  ["Duygularını ve coşkunu ifade etmekte kendini sınırlıyorsun. İhtiyatı elden bırakma ama çok da elinde sıkma.",
   "Sensörlerin hep açık. Başkalarının düşüncelerine oldukça önem veriyorsun. Aşırı duyarlılık bazen yorar.",
   "Tartışmalar senin beslenme kaynakların. En büyük zevkin neden haklı olduğunu anlatmak.",
   "Espri zekan sayesinde ince espriler yapabiliyorsun. Bazıları bunu alaycılık olarak algılayabilir."],
  // 5: Hayat veren/Saygili/Ihtiyatli/Becerili
  ["İnsanlara ilham veriyorsun. Enerjin bulaşıcı ve çevreni motive ediyorsun.",
   "İnsanlar arasındaki sorunlarda farklılıkları uzlaştırmaya çalışıyorsun.",
   "Detaycı ve dikkatlisin. Her adımını düşünerek atıyorsun.",
   "Organize ve üretkensin. Elinden çıkan işler kaliteli olur."],
  // 6: Memnun/Duyarli/Guvenen/Hayat Dolu
  ["Karşındaki insan için kolay bulunmayan bir özelliğin var: Dinlemek. İyi bir dinleyicisin.",
   "Farklı düşünen insanlara karşı oldukça hoşgörülüsün. Başkalarının düşüncelerine saygılısın.",
   "Hep çalış hep başar. Ama ara sıra dinlenmek lazım. Baltayı bilemek için durmak gerekir.",
   "Mutfaktaki bir şef gibisin. Herkes seni izlesin, dinlesin ve yaptıklarına değer versin."],
  // 7-20 Guclu yonler devam
  ["Detaycı ve planlısın. Her şeyin bir düzeni olmasını istersin.","Sabırlısın ve insanlara zaman tanırsın.","Olumlu bakış açın insanları etkiler ve motive eder.","Doğal bir yönlendiricisin. İnsanlar seni takip eder."],
  ["Kararlısın ve kararlarının arkasında durursun.","Anı yaşamayı bilirsin. Hayattan keyif alırsın.","Her şeyin bir programı vardır senin için. Düzen ve disiplin önemlidir.","Mütevazısın ve dikkatleri üzerine çekmekten kaçınırsın."],
  ["Düzenli ve sistematiksin. Çevren her zaman derli topludur.","Nazik ve kibar yaklaşımın insanları rahatlatır.","Açık sözlüsün. Düşündüğünü söylemekten çekinmezsin.","İyimsersin. Her durumda olumlu tarafı görürsün."],
  ["Dostça davranışların insanları kendine çeker.","Sadık ve vefalısın. Verdiğin sözü tutarsın.","Eğlenceli kişiliğin ortamlara renk katar.","Etkili bir iletişim tarzın var. Sözlerin ağırlık taşır."],
  ["Cesaret senin en belirgin özelliklerinden. Korkmadan adım atarsın.","Hoş ve sevimli tavırlarınla insanları etkilersin.","Diplomatik yaklaşımın çatışmaları çözmeye yardımcı olur.","Ayrıntılara önem verirsin. Hiçbir detayı kaçırmazsın."],
  ["Neşeli kişiliğin çevrene pozitif enerji yayar.","Tutarlısın. Söylediklerin ve yaptıkların uyumludur.","Kültürlü ve bilgilisin. Entelektüel bir bakış açın var.","Güvenilir birisin. İnsanlar sana güvenebilir."],
  ["İdealistsin. Yüksek standartların ve hayallerin var.","Bağımsızsın. Kendi başına karar verir ve uygularsın.","Kendi halinde sakin bir yapın var. Huzuru seversin.","Başkalarına ilham verirsin. Esin kaynağısın."],
  ["Sıcakkanlısın. İnsanlarla kolayca bağ kurarsın.","Kararlısın. Bir kez karar verdiğinde geri adım atmazsın.","İnce esprilerinle ortamı neşelendirirsin.","Derin düşünürsün. Yüzeysel kalmayı sevmezsin."],
  ["Arabulucu rolü senin için doğaldır. Barışı sağlarsın.","Sanatsal ve estetik yönün güçlüdür.","Harekete geçiren enerjin var. İnsanları motive edersin.","Kolay kaynaşır, herkesle iletişim kurarsın."],
  ["İnce düşüncelisin. Başkalarının duygularını önemsersin.","Azimlisin. Başladığın işi bitirirsin.","Konuşkan ve sosyalsin. İletişim kurman kolaydır.","Hoşgörülüsün. İnsanların hatalarını affedersin."],
  ["İyi bir dinleyicisin. İnsanlar sana açılır.","Vefalısın. Dostluklarına değer verirsin.","Liderlik vasfın doğuştan gelir.","Enerjik ve hareketlisin. Durağanlıktan hoşlanmazsın."],
  ["Kanaatkar ve mütevazısın.","Yönetici ruhlusun. Kontrolü elde tutmayı seversin.","Organizasyon yeteneğin güçlüdür.","Şirin ve sempatik tavırlarınla sevilen birisin."],
  ["Mükemmeliyetçisin. En iyisini istersin.","Tatlı ve uyumlu birisin. İnsanlarla iyi geçinirsin.","Üretken ve verimlisin. Sonuç odaklı çalışırsın.","Popülersin. İnsanlar seninle olmaktan hoşlanır."],
  ["Hareketli ve dinamiksin. Yerinde duramayan bir yapın var.","Gözü peksin. Risklerden korkmazsın.","Terbiyeli ve saygılı davranışlarınla takdir edilirsin.","Dengeli ve ölçülüsün. Aşırılıklardan kaçınırsın."],
  // 21-40 Zayif yonler
  ["Dikkatleri üzerine toplamamak için geride duruyorsun. Arkadaşların yeterince destek almadıklarını hissedebilirler.","Bir çare düşünüyorsun; sonra bunun iyi sonuç vermeyeceğini düşünüyorsun. Heyecanın eksik.","Yaşamın derinliklerine inmiyorsun. Basit ve çocukça bir bakış açın var.","Başkalarına neyi nasıl yapması gerektiğini söylemekten kaçınmıyorsun. Otoritersin."],
  ["Sebat etmiyorsun. Bir işi sonuna kadar götüremiyorsun. Çabuk vazgeçiyorsun.","Standartların o kadar yüksek ki seni tatmin etmek hayli güç.","Duygularını ifade etmekte zorlanıyorsun. Coşkusuz görünebilirsin.","Diyelim ki karşındaki kusurluydu ve kin besledin. Hiç hak etmediği halde bazı insanlara da kin besliyorsun."],
  ["Hep bir ayak direme hali. Hep bir isteksizlik hali var.","Yerli yersiz pek çok konuda derin kaygılar ve endişeler yaşayıp huzursuz oluyorsun.","Tartışmalar senin beslenme kaynakların. Haklı olduğunu anlatmak en büyük zevkin.","Kendini tekrarlıyorsun. Aynı şeyleri söyleyip duruyorsun."],
  ["Mükemmel için sürekli iyiden fedakarlık ediyorsun. Karar vermekten çekiniyorsun.","Çocuktan büyüğe herkesin istediği gibi davranmasına göz yumuyorsun.","Unutkansın. Önemli detayları gözden kaçırabiliyorsun.","Patavatsızlık yapabiliyorsun. Düşüncelerini kırıcı biçimde ifade edebiliyorsun."],
  ["Geveze olabiliyorsun. Konuşmayı uzatıyorsun.","Sabırsızsın. Her şeyin hemen olmasını istiyorsun.","Güvensizsin. Kendine yeterince inanmıyorsun.","Kararsızsın. Seçim yapmakta zorlanıyorsun."],
  ["Belki içinde bir şefkat kırıntısı var ama dışarı vuramıyorsun.","Bulaşmayan, mesafeli bir yapın var.","Ne yapacağın belirsiz. Tutarsız davranışlar sergileyebiliyorsun.","Şevkatsizsin. İnsanlara karşı soğuk durabiliyorsun."],
  ["İnatçısın. Fikrini değiştirmek zordur.","Gelişigüzel davranıyorsun. Detaylara önem vermiyorsun.","Zor beğenirsin. Mükemmel olmayan hiçbir şey seni tatmin etmez.","Tereddütlüsün. Adım atmakta gecikiyorsun."],
  ["Renksiz ve sönük durabiliyorsun. Enerji seviyen düşük görünüyor.","Kötümsersin. Olayların hep kötü tarafını görüyorsun.","Kibirli olabiliyorsun. Kendini başkalarından üstün görebiliyorsun.","Her şeye göz yumuyorsun. Senden hoşlanmayacaklarından endişe ediyorsun."],
  ["Kolay sinirleniyorsun. Duygu kontrolün zayıf olabiliyor.","Amaçsızsın. Net bir hedefin yok gibi görünüyor.","İddiacısın. Haklı olduğundan bir an bile tereddüt etmiyorsun.","Yabancılaşmışsın. İnsanlardan uzaklaşma eğiliminde olabiliyorsun."],
  ["Ahmakça davranabiliyorsun. Düşünmeden hareket ediyorsun.","Negatif davranan birisin. Olumsuz tepkilere odaklanıyorsun.","Küstahsın. İnsanlara emir vererek kontrolü sağlamaya çalışıyorsun.","Kayıtsızsın. Olan bitene aldırmıyorsun."],
  ["Endişelisin. Sürekli kaygılanıyorsun.","Yalnızlığa sığınıyorsun. İnsanlardan uzaklaşıyorsun.","İş delisisin. Kendini sürekli çalışmak ve üretmek zorunda hissediyorsun.","Tanınmak istiyorsun. İlgi ve onay arayışındasın."],
  ["Aşırı hassassın. Her şeyi kişisel algılayabiliyorsun.","Patavatsızlık yapabiliyorsun. Düşüncelerini kırıcı biçimde ifade edebiliyorsun.","Ürkeksin. Risk almaktan kaçınıyorsun.","Gevezesin. Konuşmayı bırakmak zor geliyor."],
  ["Şüphecisin. İnsandan, olaylardan, her şeyden şüphe duyuyorsun.","Düzensizsin. İşlerini organize etmekte zorlanıyorsun.","Otoritersin. İnsanlara ne yapmaları gerektiğini söylemekten geri durmuyorsun.","Bunalımlısın. Zorlandığın zaman mırıldanmaktan kendini alıkoyamıyorsun."],
  ["Tutarsızsın. Aykırı ve mantıksız davranışlar sergileyebiliyorsun.","İçe dönüksün. Duygularını paylaşmakta zorlanıyorsun.","Hoşgörüsüzsün. Başkalarının hatalarını affetmekte zorlanıyorsun.","Umursamazsın. Olan bitene kayıtsız kalabiliyorsun."],
  ["Dağınıksın. Eşyaların ve düşüncelerin karmakarışık olabiliyor.","Karamsarsın. Yargılayıcı ve olumsuz tepkilere odaklanan bir yapın var.","Zorlandığın zaman mırıldanmaktan kendini alıkoyamıyorsun.","İnsanları kullanabiliyorsun. Kendi çıkarın için başkalarından faydalanabiliyorsun."],
  ["Çabuk düşünmüyor ve çabuk davranmıyorsun. Ağırkanlı olabiliyorsun.","Dik kafasın. Fikrini kolay kolay değiştirmezsin.","Hava atabiliyorsun. Kendini göstermek istiyorsun.","Şüphecisin. Her şeyi sorgulamadan kabul etmezsin."],
  ["Yalnızlığı seviyorsun. İnsanlardan uzak kalmayı tercih ediyorsun.","Güdmeye çalışıyorsun. İnsanları kontrol etmek istiyorsun.","Tembelsin. Harekete geçmekte zorlanıyorsun.","Gürültücüsün. Dikkat çekmekten hoşlanıyorsun."],
  ["Ağırkanlısın. Tepki vermekte yavaş kalabiliyorsun.","Şüphecisin. İnsanlara güvenmekte zorlanıyorsun.","Çabuk sinirleniyorsun. Sabrın kısa sürede tükenebiliyor.","Kafası dağınıksın. Odaklanmakta zorlanabiliyorsun."],
  ["Huzursuzluğun dinmiyor. İç huzuru bulmakta zorlanıyorsun.","Acelecisin. Sabırsızlığın hatalara yol açabiliyor.","İntikamcısın. Kötülükleri unutmaz ve karşılık vermek istersin.","Gönülsüzsün. İsteksiz bir halde işlere yaklaşıyorsun."],
  ["Her şeyde ödün verebiliyorsun. Kendi değerlerinden kolayca vazgeçebiliyorsun.","Tenkitçisin. Sürekli eleştiren ve olumsuz gören bir yapın var.","Kurnazlık yapabiliyorsun. Durumu kendi lehine çevirmeye çalışıyorsun.","Değişkensin. Ruh halin ve kararların sık sık değişebiliyor."],
];

''' + 'const PD: Record<string,{t:string;c:string;bg:string;e:string;s:string[];w:string[]}>'

if old_PD in content:
    content = content.replace(old_PD, COMMENTS_DATA)
    print("  OK 1. 40 soru yorumlari eklendi")

# ============================================================
# 2. SONUC EKRANINA YORUMLARI EKLE
# Guclu Yonlerin/Gelisim Alanlarin'dan sonra kisisel yorumlar
# ============================================================

old_kaynak = '''<div style={{fontSize:11,color:"#94A3B8",textAlign:"center",marginTop:16}}>Kaynak: Florence Littauer'''

# Yorumlar bolumu - kaynak'tan once ekle
personal_comments = '''
        {/* Kisisel Yorumlar */}
        <div style={{marginTop:20}}>
          <h3 style={{margin:"0 0 14px",fontSize:18,fontWeight:800,color:"#0F172A"}}>Kişisel Yorumların</h3>
          <div style={{fontSize:13,color:"#64748B",marginBottom:12}}>Seçimlerine göre sana özel değerlendirme:</div>
          {Object.entries(ans).sort((a,b)=>Number(a[0])-Number(b[0])).map(([qi,oi])=>{
            const qIdx=Number(qi);
            const comment=QCOMMENTS[qIdx]?.[oi];
            if(!comment)return null;
            return(
              <div key={qi} style={{padding:"12px 14px",marginBottom:8,borderRadius:10,background:qIdx<20?"#F8FAFC":"#FFF7ED",borderLeft:qIdx<20?"3px solid #0E7490":"3px solid #F97316"}}>
                <div style={{fontSize:11,color:"#94A3B8",marginBottom:4}}>Soru {qIdx+1} - {PQ[qIdx].o[oi]}</div>
                <div style={{fontSize:13,color:"#0F172A",lineHeight:1.6}}>{comment}</div>
              </div>
            );
          })}
        </div>

        ''' + '<div style={{fontSize:11,color:"#94A3B8",textAlign:"center",marginTop:16}}>Kaynak: Florence Littauer'

if old_kaynak in content:
    content = content.replace(old_kaynak, personal_comments)
    print("  OK 2. Kisisel yorumlar sonuc ekranina eklendi")

# ============================================================
# 3. PDF FIX - jsPDF'i client-side dynamic import ile kullan
# Server-side import sorunu cozumu
# ============================================================

# Mevcut import'u kaldir (server-side sorun yaratir)
content = content.replace('import jsPDF from "jspdf";\n', '')
content = content.replace('import html2canvas from "html2canvas";\n', '')

# PDF butonundaki kodu dynamic import ile degistir
old_pdf_btn = 'const pdf=new jsPDF("p","mm","a4");'
new_pdf_btn = 'const {default:jsPDF}=await import("jspdf");const pdf=new jsPDF("p","mm","a4");'

if old_pdf_btn in content:
    content = content.replace(old_pdf_btn, new_pdf_btn, 1)
    print("  OK 3. PDF dynamic import fix")

# ============================================================
# 4. PDF icerigine yorumlari da ekle
# ============================================================
old_pdf_save = "pdf.save(\"NextERA_Kisilik_Raporu.pdf\");"

new_pdf_save = """// Kisisel yorumlar
            y+=10;
            if(y>250){pdf.addPage();y=20;}
            pdf.setFontSize(14);pdf.setTextColor(14,116,144);pdf.text("Kisisel Yorumlariniz",margin,y);y+=8;
            pdf.setFontSize(10);
            Object.entries(ans).sort((a,b)=>Number(a[0])-Number(b[0])).forEach(([qi,oi])=>{
              const qIdx=Number(qi);
              const cm=QCOMMENTS[qIdx]?.[Number(oi)];
              if(!cm)return;
              if(y>260){pdf.addPage();y=20;}
              pdf.setTextColor(148,163,184);pdf.text("Soru "+(qIdx+1)+" - "+PQ[qIdx].o[Number(oi)],margin,y);y+=5;
              pdf.setTextColor(15,23,42);
              const lines=pdf.splitTextToSize(cm,w-2*margin);
              pdf.text(lines,margin,y);y+=lines.length*5+4;
            });
            
            pdf.save("NextERA_Kisilik_Raporu.pdf");"""

if old_pdf_save in content:
    content = content.replace(old_pdf_save, new_pdf_save)
    print("  OK 4. PDF yorumlar eklendi")

# ============================================================
# 5. PersonalityTestScreen'e ans'i sonuc ekraninda da erisebilir yap
# initialResults varsa answers'i da al
# ============================================================
old_init_done = 'const [done,setDone]=useState(!!initialResults);'
new_init_done = 'const [done,setDone]=useState(!!initialResults);\n  const initAns=initialResults?.answers||{};'

if old_init_done in content:
    content = content.replace(old_init_done, new_init_done)

# ans yerine (initialResults varsa initAns kullan)
# Sonuc ekranindaki ans referanslarini guncelle
# calc fonksiyonunda ans zaten dogru doluyor
# Ama initialResults ile acildiginda ans bos oluyor
# initAns'i ans'e merge edelim
old_ans_init = 'const [ans,setAns]=useState<Record<number,number>>({});'
new_ans_init = 'const [ans,setAns]=useState<Record<number,number>>(initialResults?.answers ? Object.fromEntries(Object.entries(initialResults.answers).map(([k,v])=>[Number(k),Number(v)])) : {});'

if old_ans_init in content:
    content = content.replace(old_ans_init, new_ans_init)
    print("  OK 5. Initial answers yukleniyor")

# SAVE
open(filepath, 'w').write(content)
print("")
print("DETAYLI YORUM + PDF FIX TAMAMLANDI!")
print("  - 40 soru x 4 secenek = 160 yorum paragrafi")
print("  - Sonuc ekraninda kisisel yorumlar")
print("  - PDF dynamic import fix")
print("  - PDF icinde yorumlar")
print("")
print("Simdi: npm run build")

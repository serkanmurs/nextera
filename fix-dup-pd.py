filepath = 'src/app/page.tsx'
content = open(filepath, 'r').read()

# Sorun: "};\n> = {" seklinde iki PD ust uste binmis
# "};> = {" veya "};\n> = {" kismini bul
bad = '};> = {'
if bad not in content:
    bad = '};\n> = {'

if bad in content:
    # Yeni PD'nin sonu "};" ile bitiyor
    # Sonra eski PD "> = {" ile basliyor
    # Eski PD'nin sonunu bul - "};" ile biter
    bad_start = content.find(bad)
    # "};" yeni PD'nin sonu, "> = {" eski PD'nin basi
    # "};" kalsin, "> = {" ve sonrasi silinsin
    
    # Eski PD "> = {" ile basliyor, sonundaki "};" i bul
    old_pd_start = bad_start + 2  # "};" den sonra
    
    # Eski PD icinde kac tane { ve } var sayalim
    depth = 0
    i = old_pd_start
    # ">" karakterini atla
    while i < len(content) and content[i] in '> \n\r':
        i += 1
    # Simdi "= {" ile baslamali
    if content[i] == '=':
        i += 1
        while i < len(content) and content[i] in ' ':
            i += 1
    
    # { ile baslamali
    if i < len(content) and content[i] == '{':
        start_brace = i
        depth = 0
        j = start_brace
        end_pos = -1
        while j < len(content):
            if content[j] == '{':
                depth += 1
            elif content[j] == '}':
                depth -= 1
                if depth == 0:
                    end_pos = j + 1
                    break
            j += 1
        
        if end_pos > -1:
            # Sonraki ; ve newline'i da al
            if end_pos < len(content) and content[end_pos] == ';':
                end_pos += 1
            while end_pos < len(content) and content[end_pos] in '\n\r':
                end_pos += 1
            
            # "};" kalsin, gerisi silinsin
            content = content[:bad_start + 2] + '\n' + content[end_pos:]
            print("OK - Eski PD blogu kaldirildi")
        else:
            print("HATA - Eski PD sonu bulunamadi")
    else:
        print(f"HATA - Beklenen karakter bulunamadi: '{content[i:i+5]}'")
else:
    print("Duplikat PD bulunamadi - belki zaten temiz")

open(filepath, 'w').write(content)
print("Kaydedildi. Simdi: npm run build")

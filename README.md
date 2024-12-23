# URL və Təhlükəsizlik Analiz Aləti

Bu skript server log faylını analiz edərək URL-ləri və onların status kodlarını yoxlayır, 404 səhvlərini aşkar edir və URL-ləri qara siyahı domenləri ilə müqayisə edir. Nəticələr müxtəlif fayllarda saxlanılır, o cümlədən JSON, CSV və mətn fayllarında.

## Xüsusiyyətlər
1. **Log Analizi**:
   - URL-lərin və onların status kodlarının log faylından çıxarılması.
   - 404 status kodlu URL-lərin sayılması.

2. **Qara Siyahı Domenlərinin Analizi**:
   - HTML faylından qara siyahı domenlərini oxuyur.
   - Qara siyahıya düşən URL-ləri müəyyən edir.

3. **Nəticələrin Yadda Saxlanması**:
   - URL-lərin status kodları mətn faylında saxlanılır.
   - 404 səhv sayına malik URL-lər CSV formatında saxlanılır.
   - Qara siyahıya düşən URL-lər JSON faylında qeyd olunur.
   - Ümumi statistikalar JSON formatında saxlanılır.

## Fayl Strukturu
- **Giriş Faylları**:
  - `access_log.txt`: Log faylı (server giriş məlumatları).
  - `threat_feed.html`: Qara siyahı domenlərini əks etdirən HTML faylı.
- **Çıxış Faylları**:
  - `url_status_report.txt`: URL-lərin və status kodlarının siyahısı.
  - `malware_candidates.csv`: 404 səhv sayına malik URL-lərin siyahısı.
  - `alert.json`: Qara siyahıya düşən URL-lər haqqında məlumat.
  - `summary_report.json`: Analizin ümumi statistikası.

## Necə İşləyir?
1. **Log Faylı Təhlili**:
   - `access_log.txt` faylından URL-lər və onların status kodları çıxarılır.
   - 404 status kodlu URL-lərin sayı hesablanır.

2. **Qara Siyahı Analizi**:
   - `threat_feed.html` faylından qara siyahı domenləri oxunur.
   - URL-lər qara siyahı domenləri ilə müqayisə edilir.

3. **Nəticələrin Yadda Saxlanması**:
   - Bütün URL-lərin və status kodlarının siyahısı `url_status_report.txt` faylına yazılır.
   - 404 səhv sayına malik URL-lər `malware_candidates.csv` faylına yazılır.
   - Qara siyahıya düşən URL-lər `alert.json` faylına saxlanılır.
   - Ümumi statistika `summary_report.json` faylına qeyd olunur.

## Giriş və Çıxış Nümunələri
### Giriş Log Faylı (access_log.txt)
127.0.0.1 - - [23/Dec/2024:10:15:32 +0000] "GET http://example.com/page HTTP/1.1" 200 192.168.1.1 - - [23/Dec/2024:10:16:45 +0000] "GET http://malicious.com/login HTTP/1.1" 404

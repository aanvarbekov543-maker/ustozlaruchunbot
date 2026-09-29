# -*- coding: utf-8 -*-
"""
1-Oktabr — O'qituvchi va murabbiylar kuni uchun Telegram bot
=================================================

Ishlash tartibi:
1) Ustoz /start bosadi -> ismlar ro'yxatidan o'zinikini tanlaydi (xabar ichidagi tugmalar orqali)
2) Bot undan maxfiy kodni so'raydi -> to'g'ri kiritsa
3) Ustozga maxsus tayyorlangan tabrik matni chiqadi

O'RNATISH:
    pip install python-telegram-bot --upgrade

ISHGA TUSHIRISH:
    python ustozlar_bot.py
"""

import logging
from telegram import (
    Update,
    InlineKeyboardMarkup,
    InlineKeyboardButton,
)
from telegram.ext import (
    ApplicationBuilder,
    CommandHandler,
    MessageHandler,
    CallbackQueryHandler,
    ConversationHandler,
    ContextTypes,
    filters,
)

logging.basicConfig(
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
    level=logging.INFO,
)

# ============================================================
# 1) BOT TOKENI
# ============================================================
BOT_TOKEN = "8892774160:AAHArDkKpTbVfl2w7ChZIqdiTzjDr-Ac6v0"

# ============================================================
# 2) USTOZLAR MA'LUMOTLARI
#    Har bir ustoz uchun: shaxsiy kod (6 xonali, tasodifiy) va tabrik matni
# ============================================================
TEACHERS = {
    "Xojiboyev Baxtiyorjon Kozimovich": {
        "code": "224906",
        "congrats": "1-OKTABR — O'QITUVCHI VA MURABBIYLAR KUNI\n\nAziz va qadrli Ustoz!\n\nSizni 1-oktabr – O‘qituvchi va murabbiylar kuni bilan chin qalbimdan muborakbod etamiz! Sizga avvalo mustahkam sog‘lik, oilaviy xotirjamlik, cheksiz baxt va ish faoliyatingizda ulkan muvaffaqiyatlar tilaymiz.\n\nUstozlik – inson hayotidagi eng sharafli va mas’uliyatli kasblardan biridir. Chunki ustoz nafaqat bilim beradi, balki o‘z shogirdining kelajagiga yo‘l ko‘rsatadi, uning qalbiga ezgulik, mehnatsevarlik va insoniylik tuyg‘ularini singdiradi. Sizning har bir darsingiz, har bir nasihatingiz va bizga bildirgan ishonchingiz hayotimizda alohida o‘rin egallaydi.\n\nBiz erishayotgan har bir yutuq ortida Sizning mehnatingiz, sabringiz va mehringiz borligini doimo qadrlaymiz. Siz bergan bilim va tarbiya biz bilan birga butun hayotimiz davomida hamroh bo‘lishiga ishonamiz.\n\nXonadoningizdan fayz-u baraka, qalbingizdan xotirjamlik, yuzingizdan tabassum hech qachon arimasin. Shogirdlaringizning yutuqlari Sizga doimo faxr va quvonch olib kelsin. Bayramingiz muborak bo‘lsin, aziz Ustoz!",
    },
    "Xurboyev Dilshodbek Fazlidinovich": {
        "code": "435003",
        "congrats": "1-OKTABR — O'QITUVCHI VA MURABBIYLAR KUNI\n\nHurmatli Ustoz!\n\nSizni O‘qituvchi va murabbiylar kuni bilan samimiy muborakbod etamiz! Ushbu go‘zal bayramda Sizga qalbimdagi eng ezgu tilaklarni izhor etishni istaymiz.\n\nSiz bizga oddiygina dars bermaysiz. Siz bizga hayotni anglashni, bilim olishni, o‘z maqsadimiz sari intilishni va har qanday qiyinchilik oldida taslim bo‘lmaslikni o‘rgatasiz. Har bir aytgan so‘zingiz, bergan maslahatingiz va bildirgan ishonchingiz biz uchun katta ahamiyatga ega.\n\nUstozning mehnati ko‘pincha ko‘zga ko‘rinmasligi mumkin, ammo uning natijasi shogirdlarining kelajagida namoyon bo‘ladi. Siz tarbiyalagan shogirdlarning har bir yutug‘i, har bir yaxshi natijasi Sizning mehnatingizning eng go‘zal mevasi bo‘lib qoladi.\n\nSizga uzoq umr, mustahkam sog‘lik, oilangizga tinchlik-xotirjamlik, ishlaringizga rivoj va hayotingizga ko‘plab quvonchli kunlar tilaymiz. Har doim shogirdlaringiz ardog‘ida bo‘ling. Bayramingiz muborak bo‘lsin!",
    },
    "Kashkabayev Shairbek Baxtibekovich": {
        "code": "626925",
        "congrats": "1-OKTABR — O'QITUVCHI VA MURABBIYLAR KUNI\n\nAziz Ustoz!\n\nSizni kasb bayramingiz – O‘qituvchi va murabbiylar kuni bilan chin yurakdan tabriklaymiz! Sizga hayotdagi eng go‘zal ne’matlar – mustahkam sog‘lik, oilaviy baxt, qalb xotirjamligi va uzoq umr tilaymiz.\n\nInson hayotida ota-onadan keyin uning dunyoqarashiga eng katta ta’sir ko‘rsatadigan insonlardan biri, albatta, ustozdir. Sizning bergan bilimlaringiz, hayotiy maslahatlaringiz va tarbiyangiz biz uchun bebaho boylikdir.\n\nBa’zan birgina ustozning aytgan so‘zi insonning butun hayot yo‘lini o‘zgartirishi mumkin. Sizning har bir nasihatingiz bizni yaxshilikka, izlanishga va o‘z ustimizda ishlashga undaydi.\n\nSizga mehnatingizning rohatini ko‘rishingizni, shogirdlaringizning yutuqlaridan doimo faxrlanib yurishingizni tilaymiz. Qalbingizdagi mehr, ko‘zingizdagi quvonch va yuzingizdagi tabassum hech qachon so‘nmasin. Bayramingiz qutlug‘ bo‘lsin!",
    },
    "Djumaboyev Abdushukur xxx": {
        "code": "636685",
        "congrats": "1-OKTABR — O'QITUVCHI VA MURABBIYLAR KUNI\n\nQadrli Ustoz!\n\nSizni 1-oktabr – O‘qituvchi va murabbiylar kuni bilan muborakbod etamiz! Ushbu ulug‘ bayram munosabati bilan Sizga eng ezgu va samimiy tilaklarimni yo‘llaymiz.\n\nSizning har bir darsingiz biz uchun yangi bilim va yangi imkoniyatlar eshigini ochadi. Bizga o‘rgatayotgan faningiz bilan bir qatorda tartib-intizom, mas’uliyat, sabr, halollik va insoniylik kabi muhim fazilatlarni ham singdirib kelasiz.\n\nUstozlik – katta sabr va fidoyilikni talab qiladigan sharafli yo‘l. Siz bu yo‘lda o‘z bilimingiz va mehringizni biz bilan ayamasdan baham ko‘rib kelmoqdasiz. Buning uchun Sizga chin dildan rahmat aytamiz.\n\nHayotingiz doimo yorug‘ va mazmunli bo‘lsin. Oilangizga tinchlik, dasturxoningizga baraka, qalbingizga xotirjamlik, faoliyatingizga ulkan zafarlar tilaymiz. Barcha ezgu niyatlaringiz amalga oshsin. Bayramingiz muborak bo‘lsin!",
    },
    "Usmonov Baxtiyorjon Ibragimovich": {
        "code": "778636",
        "congrats": "1-OKTABR — O'QITUVCHI VA MURABBIYLAR KUNI\n\nHurmatli va mehribon Ustoz!\n\nSizni O‘qituvchi va murabbiylar kuni bilan chin qalbimdan tabriklaymiz! Sizga avvalo sihat-salomatlik, uzoq umr, oilaviy baxt va barcha ishlaringizda omad tilaymiz.\n\nSizning kasbingiz oddiy kasb emas. Siz yosh avlodning kelajagini shakllantirayotgan, ularning qalbiga bilim va ezgulik urug‘larini ekayotgan buyuk insonlardan birisiz. Har kuni biz uchun sarflayotgan vaqtingiz, sabringiz va mehnatingiz albatta o‘z samarasini beradi.\n\nBizning har bir yaxshi natijamiz Sizga quvonch bag‘ishlashini bilamiz. Shuning uchun kelajakda Siz bergan bilimlarni munosib ravishda qo‘llab, yaxshi inson bo‘lishga harakat qilamiz.\n\nSizga hech qachon charchoq va tashvish hamroh bo‘lmasin. Har bir kuningiz quvonchli xabarlar bilan boshlangan, yaxshi kayfiyat bilan davom etgan va xotirjamlik bilan yakunlangan kunlardan iborat bo‘lsin. Bayramingiz muborak, aziz Ustoz!",
    },
    "Abduraximova Zulxumor Toxirovna": {
        "code": "207622",
        "congrats": "1-OKTABR — O'QITUVCHI VA MURABBIYLAR KUNI\n\nAziz Ustoz!\n\nSizni O‘qituvchi va murabbiylar kuni bilan muborakbod etamiz! Bu kun Siz kabi fidoyi, mehribon va bilimdon insonlarga bo‘lgan hurmatimizni yanada chuqurroq ifoda etish uchun ajoyib imkoniyatdir.\n\nSiz bizga bilim berish bilan birga, hayotda qanday inson bo‘lish kerakligini ham o‘rgatyapsiz. Har bir nasihatingiz, har bir talabingiz va har bir qo‘llab-quvvatlashingiz bizning kelajagimiz uchun xizmat qiladi.\n\nSizning sabringiz, mehnatingiz va o‘quvchilaringizga bo‘lgan mehringiz tahsinga loyiq. Shogirdlaringizning yutuqlari, yaxshi natijalari va kelajakdagi muvaffaqiyatlari Siz uchun eng katta mukofot bo‘lsin.\n\nUmringiz uzoq, sog‘lig‘ingiz mustahkam bo‘lsin. Oilangizda doimo tinchlik va totuvlik hukm sursin. Hayotingiz baxtli onlar, yaxshi insonlar va unutilmas quvonchli voqealarga boy bo‘lsin. Bayramingiz muborak bo‘lsin!",
    },
    "Ahmardinova Muxarramxon Baxodirjon qizi": {
        "code": "334130",
        "congrats": "1-OKTABR — O'QITUVCHI VA MURABBIYLAR KUNI\n\nQadrli Ustoz!\n\nSizni O‘qituvchi va murabbiylar kuni bilan chin yurakdan tabriklaymiz!\n\nHayotimizda bizga yo‘l ko‘rsatadigan, xatolarimizni to‘g‘rilaydigan va kelajakka ishonch bilan qarashimizga yordam beradigan insonlar juda ko‘p emas. Siz ana shunday insonlardan birisiz.\n\nSizning mehnatingiz, sabringiz va bizga ajratayotgan vaqtingiz uchun cheksiz minnatdormiz. Sizdan olgan bilimlarimiz maktab yoki darsxona bilan cheklanib qolmay, butun hayotimiz davomida bizga xizmat qiladi.\n\nTilagim – doimo sog‘-salomat bo‘ling, oilangiz bag‘rida baxtli hayot kechiring. Mehnatlaringiz samarasi yanada ko‘paysin, shogirdlaringizning yutuqlari Sizni har kuni quvontirsin. Qalbingiz doimo xotirjam, ko‘nglingiz doimo bahoriy bo‘lsin. Bayramingiz muborak!",
    },
    "Amirov Javlonbek Alijon o‘g‘li": {
        "code": "730226",
        "congrats": "1-OKTABR — O'QITUVCHI VA MURABBIYLAR KUNI\n\nHurmatli Ustoz!\n\nSizni eng ulug‘ va sharafli kasb egalarining bayrami bilan muborakbod etamiz! O‘qituvchilik – kelajak avlodga yo‘l ko‘rsatish, ularning qalbiga ilm va tarbiya nurini olib kirish demakdir.\n\nSizning har bir darsingiz ortida katta mehnat, tayyorgarlik va mas’uliyat bor. Biz buni qadrlaymiz. Bizga o‘rgatayotgan bilimlaringiz, bildirayotgan ishonchingiz va doimo yaxshi natijaga undayotganingiz uchun Sizga katta rahmat.\n\nSizga avvalo sog‘lik, uzoq umr, oilangizga fayz-u baraka va xotirjamlik tilaymiz. Ish faoliyatingizda yangi marralarni zabt eting, shogirdlaringizning muvaffaqiyatlari Siz uchun eng katta faxr bo‘lsin.\n\nHar bir kuningiz quvonchli xabarlar, samimiy insonlar va go‘zal lahzalarga boy bo‘lsin. Bayramingiz muborak bo‘lsin, aziz Ustoz!",
    },
    "Artikov Zaxidjon Ergashovich": {
        "code": "751673",
        "congrats": "1-OKTABR — O'QITUVCHI VA MURABBIYLAR KUNI\n\nAziz Ustoz!\n\nSizni kasb bayramingiz bilan samimiy tabriklaymiz! Sizga aytadigan tilaklarimiz juda ko‘p, ammo ularning eng muhimi – doimo sog‘-salomat va baxtli bo‘lishingizdir.\n\nBizga bergan har bir bilimingiz, aytgan har bir nasihatingiz va ko‘rsatgan har bir yo‘l-yo‘rig‘ingiz uchun Sizdan minnatdormiz. Sizning darslaringiz bizga faqatgina fan o‘rganish emas, balki hayotga tayyorlanish imkonini ham beradi.\n\nShogirdlaringizning har bir muvaffaqiyati, yaxshi natijalari va yutuqlari Sizning qalbingizga quvonch olib kirsin. Mehnatlaringiz doimo qadrlansin, obro‘-e’tiboringiz yanada oshsin.\n\nXonadoningizdan tinchlik, dasturxoningizdan baraka, qalbingizdan mehr va yuzingizdan tabassum arimasin. Barcha orzu-niyatlaringiz ro‘yobga chiqsin. O‘qituvchi va murabbiylar kuni muborak bo‘lsin!",
    },
    "Axmedova Roxatoy Urmonovna": {
        "code": "683594",
        "congrats": "1-OKTABR — O'QITUVCHI VA MURABBIYLAR KUNI\n\nQadrli va hurmatli Ustoz!\n\nSizni O‘qituvchi va murabbiylar kuni bilan chin qalbimdan muborakbod etamiz! Siz kabi ustozlarning mehnatini oddiy so‘zlar bilan ta’riflash juda qiyin.\n\nSiz bizga bilim berasiz, savollarimizga javob berasiz, xatolarimizni tushuntirasiz va eng muhimi, kelajagimizga ishonch bilan qarashga o‘rgatasiz. Sizning sabringiz va fidoyiligingiz har qanday maqtovga loyiq.\n\nTilaymanki, hayotingizning har bir kuni quvonch va baxt bilan o‘tsin. Sog‘lig‘ingiz mustahkam, umringiz uzoq, oilangiz tinch va farovon bo‘lsin. Kasbiy faoliyatingizda doimo yuqori natijalarga erishing.\n\nSiz tarbiyalagan shogirdlar kelajakda katta yutuqlarga erishib, Sizni faxr bilan eslab yurishsin. Bayramingiz muborak bo‘lsin, aziz Ustoz!",
    },
    "Dadaboyeva Malikaxon Farxodjon qizi": {
        "code": "541046",
        "congrats": "1-OKTABR — O'QITUVCHI VA MURABBIYLAR KUNI\n\nMuhtaram Ustoz!\n\nSizni O‘qituvchi va murabbiylar kuni bilan chin dildan muborakbod etamiz! Sizga ushbu bayramda eng ezgu va samimiy tilaklarimni yo‘llaymiz.\n\nUstoz – inson hayotida iz qoldiradigan buyuk kasb egasidir. Sizning bizga bergan bilimlaringiz, tarbiyangiz va maslahatlaringiz kelajakda ham bizga yo‘l ko‘rsatib turadi.\n\nSizga o‘z kasbingizdan doimo zavq olib, shogirdlaringizning yutuqlaridan faxrlanib yurishingizni tilaymiz. Har bir mehnatingiz munosib e’tirof etilsin.\n\nSiz va oilangizga sog‘lik-salomatlik, xotirjamlik, baxt va farovonlik tilaymiz. Hayotingizda faqat yaxshi kunlar, quvonchli yangiliklar va unutilmas lahzalar ko‘p bo‘lsin. Bayramingiz muborak!",
    },
    "Egamberdiyeva Feruzaxon Yusupjonovna": {
        "code": "921426",
        "congrats": "1-OKTABR — O'QITUVCHI VA MURABBIYLAR KUNI\n\nAziz va hurmatli Ustoz!\n\nSizni go‘zal va sharafli bayram – O‘qituvchi va murabbiylar kuni bilan chin dildan tabriklaymiz!\n\nSizning mehnatingiz tufayli biz bilim olamiz, dunyoqarashimiz kengayadi va kelajakdagi maqsadlarimiz sari dadil qadam tashlashni o‘rganamiz. Har bir darsingiz bizga yangi bilim, yangi fikr va yangi imkoniyat beradi.\n\nSizning sabr-toqatingiz, mehringiz va fidoyiligingiz biz uchun juda qadrlidir. Bizga bergan bilimlaringiz va qilayotgan mehnatingiz uchun chin qalbimdan rahmat aytamiz.\n\nDoimo sog‘lom va bardam bo‘ling. Oilangizda tinchlik va farovonlik hukm sursin. Kasbiy faoliyatingizda omad va zafarlar Sizga doim hamroh bo‘lsin. Shogirdlaringizning yutuqlari Sizni hech qachon tark etmaydigan faxr va quvonchga aylansin. Bayramingiz muborak bo‘lsin!",
    },
    "G‘anijonova Nozimaxon Shoyatbek qizi": {
        "code": "700381",
        "congrats": "1-OKTABR — O'QITUVCHI VA MURABBIYLAR KUNI\n\nHurmatli Ustoz!\n\nSizni O‘qituvchi va murabbiylar kuni bilan chin qalbimdan tabriklaymiz! Sizga hayotdagi eng yaxshi va ezgu tilaklarni tilaymiz.\n\nSizning bizga bergan bilimlaringizni hech qanday boylik bilan o‘lchab bo‘lmaydi. Chunki bilim inson bilan birga butun umr qoladigan eng katta boylikdir. Siz esa ana shu bebaho boylikni biz bilan baham ko‘ryapsiz.\n\nSizga qilayotgan mehnatingizda kuch-g‘ayrat, qalbingizda xotirjamlik va hayotingizda baxt tilaymiz. Har bir yangi kun Sizga yangi quvonchlar olib kelsin.\n\nOilangiz doimo sog‘-omon, xonadoningiz fayzli va barakali bo‘lsin. Siz tarbiyalayotgan shogirdlar kelajakda yurtimizga foydasi tegadigan, bilimli va yaxshi insonlar bo‘lib yetishsin. Bayramingiz muborak bo‘lsin!",
    },
    "G‘ofurova Gulmiraxon Qodirjon qizi": {
        "code": "674421",
        "congrats": "1-OKTABR — O'QITUVCHI VA MURABBIYLAR KUNI\n\nQadrli Ustoz!\n\nSizni kasb bayramingiz – O‘qituvchi va murabbiylar kuni bilan muborakbod etamiz!\n\nHar bir insonning hayotida uni ilhomlantirgan, bilim bergan va to‘g‘ri yo‘l ko‘rsatgan ustoz bo‘ladi. Siz ham biz uchun ana shunday qadrli insonlardan birisiz.\n\nSizning mehnatingiz, sabringiz va mehringiz tufayli ko‘plab o‘quvchilar o‘z kelajagiga ishonch bilan qarashni o‘rganmoqda. Sizning har bir darsingiz va har bir nasihatingiz biz uchun qimmatli.\n\nSizga mustahkam sog‘lik, uzoq umr, oilaviy baxt va kasbiy faoliyatingizda ulkan muvaffaqiyatlar tilaymiz. Har doim shogirdlaringizning hurmati va ehtiromida bo‘ling. Bayramingiz muborak bo‘lsin!",
    },
    "Jabborov Baxodirjon Ashurvoy o‘g‘li": {
        "code": "983322",
        "congrats": "1-OKTABR — O'QITUVCHI VA MURABBIYLAR KUNI\n\nAziz Ustoz!\n\nBugungi bayramingiz bilan Sizni chin yurakdan tabriklaymiz! Sizga eng avvalo sihat-salomatlik, uzoq umr va oilaviy baxt tilaymiz.\n\nUstozning mehnati inson hayotida juda katta iz qoldiradi. Sizning bugun bergan bilimingiz ertaga bizning kelajagimizga aylanadi. Sizning bir og‘iz yaxshi so‘zingiz bizga kuch, birgina maslahatingiz esa to‘g‘ri yo‘l topishimizga yordam beradi.\n\nSizning shogirdlaringiz doimo yaxshi natijalarga erishib, Sizning nomingizni faxr bilan tilga olishsin. Har bir qilgan mehnatingizning rohatini ko‘rib yashang.\n\nXonadoningizdan fayz-u baraka arimasin, qalbingiz doimo quvonchga to‘lsin. Bayramingiz muborak bo‘lsin, hurmatli Ustoz!",
    },
    "Karimov Ixtiyorjon Baxtiyorovich": {
        "code": "866025",
        "congrats": "1-OKTABR — O'QITUVCHI VA MURABBIYLAR KUNI\n\nMuhtaram Ustoz!\n\nSizni O‘qituvchi va murabbiylar kuni bilan samimiy tabriklaymiz! Ushbu go‘zal kun Sizga bo‘lgan hurmatimiz va minnatdorligimizni ifodalash uchun eng yaxshi kunlardan biridir.\n\nSiz bizga bilim berish bilan birga, har kuni o‘z ustimizda ishlashni, maqsadlarimizga intilishni va insoniy fazilatlarni qadrlashni o‘rgatasiz. Buning uchun Sizga katta rahmat.\n\nSizga kelgusi faoliyatingizda ulkan zafarlar, yangi marralar va katta yutuqlar tilaymiz. Har bir boshlagan ishingiz omadli yakun topsin.\n\nSog‘lig‘ingiz mustahkam, oilangiz farovon, hayotingiz mazmunli va baxtli bo‘lsin. Doimo biz kabi shogirdlaringizning hurmati va mehrini his qilib yuring. Bayramingiz muborak!",
    },
    "Madumarova Lobaroy Odiljon qizi": {
        "code": "914295",
        "congrats": "1-OKTABR — O'QITUVCHI VA MURABBIYLAR KUNI\n\nAziz va mehribon Ustoz!\n\nSizni O‘qituvchi va murabbiylar kuni bilan chin dildan tabriklaymiz! Sizga ushbu bayramda eng go‘zal tilaklarimni yo‘llaymiz.\n\nSizning har bir darsingiz, har bir tushuntirishingiz va har bir nasihatingiz bizning bilimimiz va dunyoqarashimizni boyitib boradi. Siz bizga faqat kitobdagi bilimlarni emas, hayotda kerak bo‘ladigan sabr, mehnat, halollik va mas’uliyatni ham o‘rgatyapsiz.\n\nMehnatingizning eng katta mukofoti shogirdlaringizning yutuqlari bo‘lsin. Siz tarbiyalagan yoshlar kelajakda katta marralarni zabt etib, Sizni doimo faxr bilan eslashsin.\n\nSizga sog‘lik, baxt, oilaviy xotirjamlik, ishlaringizda rivoj va hayotingizda cheksiz quvonch tilaymiz. Bayramingiz muborak bo‘lsin!",
    },
    "Nizomiddinov Zaynobiddin Saloxiddin o‘g‘li": {
        "code": "905427",
        "congrats": "1-OKTABR — O'QITUVCHI VA MURABBIYLAR KUNI\n\nHurmatli Ustoz!\n\nSizni bugungi qutlug‘ bayram – O‘qituvchi va murabbiylar kuni bilan muborakbod etamiz!\n\nSizning kasbingiz katta sabr, kuch va fidoyilikni talab qiladi. Shunga qaramay, Siz har kuni o‘quvchilaringizga mehr bilan bilim berib, ularning kelajagi uchun astoydil mehnat qilasiz.\n\nBizga bergan bilimlaringiz, vaqt va e’tiboringiz uchun Sizdan minnatdormiz. Sizning mehnatingiz kelajakda bizning yutuqlarimiz orqali o‘z samarasini ko‘rsatadi.\n\nSizga mustahkam sog‘lik, uzoq umr, oilangizga baxt va farovonlik tilaymiz. Har bir kuningiz yaxshi xabarlar, quvonch va xotirjamlik bilan o‘tsin. Barcha ezgu orzularingiz amalga oshsin. Bayramingiz muborak bo‘lsin!",
    },
    "Pozilova Ozodxon Azimovna": {
        "code": "614750",
        "congrats": "1-OKTABR — O'QITUVCHI VA MURABBIYLAR KUNI\n\nQadrli Ustoz!\n\nSizni O‘qituvchi va murabbiylar kuni bilan muborakbod etamiz! Ushbu go‘zal bayramda Sizga eng samimiy tilaklarimni bildiramiz.\n\nSizning hayotimizdagi o‘rningiz juda katta. Chunki Siz bizga nafaqat bilim, balki hayot yo‘lida kerak bo‘ladigan tajriba va saboq ham berasiz. Har bir darsingizdan o‘zimiz uchun foydali xulosa chiqarishga harakat qilamiz.\n\nSizga kasbingizda doimo rivoj, yangi yutuqlar va katta muvaffaqiyatlar tilaymiz. Shogirdlaringizning yutuqlari Sizning eng katta quvonchingiz bo‘lsin.\n\nOilangizda tinchlik, xonadoningizda fayz, qalbingizda xotirjamlik bo‘lsin. Doimo sog‘-salomat bo‘lib, shogirdlaringiz ardog‘ida yuring. Bayramingiz muborak!",
    },
    "Qaxorov Akmaljon Baxtiyorjon o‘g‘li": {
        "code": "887507",
        "congrats": "1-OKTABR — O'QITUVCHI VA MURABBIYLAR KUNI\n\nAziz Ustoz!\n\nSizni O‘qituvchi va murabbiylar kuni bilan chin qalbimdan tabriklaymiz! Sizga avvalo sog‘lik-salomatlik, oilaviy baxt va uzoq umr tilaymiz.\n\nSizning har kuni qilayotgan mehnatingiz kelajak avlod uchun katta ahamiyatga ega. Bizga bergan bilimlaringiz va tarbiyangiz hayotimiz davomida bizga yordam beradi.\n\nSizning sabringiz, mehringiz va bizga bo‘lgan ishonchingizni juda qadrlaymiz. Biz uchun qilayotgan barcha mehnatlaringiz uchun katta rahmat.\n\nHayotingiz doimo go‘zal voqealar va quvonchli kunlarga boy bo‘lsin. Ish faoliyatingizda omad va muvaffaqiyatlar hamisha hamroh bo‘lsin. Barcha niyatlaringiz amalga oshsin. Bayramingiz muborak bo‘lsin!",
    },
    "Qaxramonova Odinaxon Adaxamjon qizi": {
        "code": "910625",
        "congrats": "1-OKTABR — O'QITUVCHI VA MURABBIYLAR KUNI\n\nMuhtaram Ustoz!\n\nSizni kasb bayramingiz bilan chin dildan muborakbod etamiz! Bugungi kunda Sizga birgina \"rahmat\" so‘zi ham barcha mehnatingizni ifodalash uchun kamlik qiladi.\n\nSiz bizga bilim berdingiz, xatolarimizni ko‘rsatdingiz, yutuqlarimizdan quvondingiz va qiyin paytlarimizda dalda bo‘ldingiz. Sizning bizga bergan saboqlaringizni hech qachon unutmaymiz.\n\nSizga mustahkam sog‘lik, oilangizga baxt va farovonlik, faoliyatingizga esa ulkan muvaffaqiyatlar tilaymiz. Har bir mehnatingiz munosib qadrlansin.\n\nKelajakda shogirdlaringizning katta yutuqlarini ko‘rib, ularning muvaffaqiyatlaridan faxrlanib yuring. Bayramingiz muborak bo‘lsin, aziz Ustoz!",
    },
    "Raxmonova Gulshanoy Muxtorjon qizi": {
        "code": "715011",
        "congrats": "1-OKTABR — O'QITUVCHI VA MURABBIYLAR KUNI\n\nHurmatli Ustoz!\n\nSizni O‘qituvchi va murabbiylar kuni bilan muborakbod etamiz! Ushbu bayram munosabati bilan Sizga eng ezgu tilaklarimni yo‘llaymiz.\n\nSizning mehnatingiz tufayli biz bilim olamiz, dunyoqarashimizni kengaytiramiz va kelajakdagi maqsadlarimizni aniqroq tasavvur qilamiz. Sizning har bir darsingiz biz uchun muhim saboqdir.\n\nSizga qilayotgan sharafli mehnatingizda hech qachon charchamaslikni, doimo kuch-g‘ayrat va ilhom bilan ishlashingizni tilaymiz.\n\nSog‘lig‘ingiz mustahkam, umringiz uzoq, oilangiz tinch va xonadoningiz fayzli bo‘lsin. Shogirdlaringizning hurmati va mehridan doimo bahramand bo‘lib yuring. Bayramingiz muborak!",
    },
    "Rizzayeva Muxayo Kozimjonovna": {
        "code": "562521",
        "congrats": "1-OKTABR — O'QITUVCHI VA MURABBIYLAR KUNI\n\nAziz va qadrli Ustoz!\n\nSizni O‘qituvchi va murabbiylar kuni bilan samimiy muborakbod etamiz! Bugungi bayramda Sizga barcha ezgu tilaklarni tilaymiz.\n\nUstozning bir umr qilgan mehnati shogirdlarining kelajagida aks etadi. Sizning bizga bergan bilimingiz, tarbiyangiz va hayotiy saboqlaringiz ham kelajakda bizning hayotimizda o‘z aksini topadi.\n\nSiz bizga ishonch bildirasiz, bizni izlanishga undaysiz va har bir yutuqqa erishishimiz uchun yo‘l ko‘rsatasiz. Buning uchun Sizga cheksiz minnatdormiz.\n\nSizga uzoq umr, mustahkam sog‘lik, oilaviy baxt, xotirjamlik va farovon hayot tilaymiz. Har bir kuningiz shogirdlaringizning yaxshi xabarlari bilan bezansin. Bayramingiz muborak bo‘lsin!",
    },
    "Sadikova Nigoraxon Mukimovna": {
        "code": "351589",
        "congrats": "1-OKTABR — O'QITUVCHI VA MURABBIYLAR KUNI\n\nQadrli va hurmatli Ustoz!\n\nSizni 1-oktabr – O‘qituvchi va murabbiylar kuni bilan chin qalbimdan tabriklaymiz!\n\nO‘qituvchilik – kelajakni tarbiyalashdek ulkan mas’uliyatni zimmasiga oladigan sharafli kasb. Siz esa bu vazifani bilim, sabr va mehr bilan ado etib kelmoqdasiz.\n\nBizga o‘rgatayotgan har bir mavzuingiz, bergan har bir maslahatingiz va bildirgan har bir ishonchingiz kelajagimiz uchun katta ahamiyatga ega. Sizning mehnatingizni qadrlaymiz va kelajakda bu ishonchni oqlashga harakat qilamiz.\n\nSizga hayotingiz davomida faqat yaxshiliklar hamroh bo‘lishini tilaymiz. Oilangizga tinchlik, xonadoningizga fayz-u baraka, qalbingizga xotirjamlik tilaymiz. Kasbiy faoliyatingizda yanada katta yutuqlarga erishing. Bayramingiz muborak bo‘lsin!",
    },
    "Saydullayeva Maftunabonu Axmadjon qizi": {
        "code": "102657",
        "congrats": "1-OKTABR — O'QITUVCHI VA MURABBIYLAR KUNI\n\nAziz va mehribon Ustoz!\n\nSizni O‘qituvchi va murabbiylar kuni bilan chin yurakdan muborakbod etamiz! Ushbu qutlug‘ kunda Sizga qalbimdagi barcha ezgu tilaklarni yo‘llaymiz.\n\nSiz bizga bilim berish bilan birga, hayotda o‘z o‘rnimizni topish, to‘g‘ri qaror qabul qilish, mehnatdan qo‘rqmaslik va doimo oldinga intilish kabi muhim fazilatlarni ham o‘rgatyapsiz. Sizning har bir darsingiz va har bir nasihatingiz kelajagimiz uchun katta ahamiyatga ega.\n\nSizning sabringiz, fidoyiligingiz va shogirdlaringizga bo‘lgan mehringiz uchun chin dildan minnatdormiz. Sizning mehnatingizning eng katta mukofoti – shogirdlaringizning kelajakdagi yutuqlari bo‘lsin.\n\nSizga mustahkam sog‘lik, uzoq va mazmunli umr, oilaviy baxt, xotirjamlik va farovonlik tilaymiz. Xonadoningizdan fayz-u baraka, qalbingizdan quvonch, yuzingizdan tabassum hech qachon arimasin. Barcha orzu va ezgu niyatlaringiz amalga oshsin. Bayramingiz muborak bo‘lsin, aziz Ustoz!",
    },
    "Sotvoldiyev Xasanboy Qodirovich": {
        "code": "744039",
        "congrats": "1-OKTABR — O'QITUVCHI VA MURABBIYLAR KUNI\n\nAziz va qadrli Ustoz!\n\nSizni 1-oktabr – O‘qituvchi va murabbiylar kuni bilan chin qalbimdan muborakbod etamiz! Sizga avvalo mustahkam sog‘lik, oilaviy xotirjamlik, cheksiz baxt va ish faoliyatingizda ulkan muvaffaqiyatlar tilaymiz.\n\nUstozlik – inson hayotidagi eng sharafli va mas’uliyatli kasblardan biridir. Chunki ustoz nafaqat bilim beradi, balki o‘z shogirdining kelajagiga yo‘l ko‘rsatadi, uning qalbiga ezgulik, mehnatsevarlik va insoniylik tuyg‘ularini singdiradi. Sizning har bir darsingiz, har bir nasihatingiz va bizga bildirgan ishonchingiz hayotimizda alohida o‘rin egallaydi.\n\nBiz erishayotgan har bir yutuq ortida Sizning mehnatingiz, sabringiz va mehringiz borligini doimo qadrlaymiz. Siz bergan bilim va tarbiya biz bilan birga butun hayotimiz davomida hamroh bo‘lishiga ishonamiz.\n\nXonadoningizdan fayz-u baraka, qalbingizdan xotirjamlik, yuzingizdan tabassum hech qachon arimasin. Shogirdlaringizning yutuqlari Sizga doimo faxr va quvonch olib kelsin. Bayramingiz muborak bo‘lsin, aziz Ustoz!",
    },
    "Sotvoldiyeva Maxliyoxon Sayidg‘ofur qizi": {
        "code": "184644",
        "congrats": "1-OKTABR — O'QITUVCHI VA MURABBIYLAR KUNI\n\nHurmatli Ustoz!\n\nSizni O‘qituvchi va murabbiylar kuni bilan samimiy muborakbod etamiz! Ushbu go‘zal bayramda Sizga qalbimdagi eng ezgu tilaklarni izhor etishni istaymiz.\n\nSiz bizga oddiygina dars bermaysiz. Siz bizga hayotni anglashni, bilim olishni, o‘z maqsadimiz sari intilishni va har qanday qiyinchilik oldida taslim bo‘lmaslikni o‘rgatasiz. Har bir aytgan so‘zingiz, bergan maslahatingiz va bildirgan ishonchingiz biz uchun katta ahamiyatga ega.\n\nUstozning mehnati ko‘pincha ko‘zga ko‘rinmasligi mumkin, ammo uning natijasi shogirdlarining kelajagida namoyon bo‘ladi. Siz tarbiyalagan shogirdlarning har bir yutug‘i, har bir yaxshi natijasi Sizning mehnatingizning eng go‘zal mevasi bo‘lib qoladi.\n\nSizga uzoq umr, mustahkam sog‘lik, oilangizga tinchlik-xotirjamlik, ishlaringizga rivoj va hayotingizga ko‘plab quvonchli kunlar tilaymiz. Har doim shogirdlaringiz ardog‘ida bo‘ling. Bayramingiz muborak bo‘lsin!",
    },
    "To‘xtasinov Jaxongir Abduxalim o‘g‘li": {
        "code": "216115",
        "congrats": "1-OKTABR — O'QITUVCHI VA MURABBIYLAR KUNI\n\nAziz Ustoz!\n\nSizni kasb bayramingiz – O‘qituvchi va murabbiylar kuni bilan chin yurakdan tabriklaymiz! Sizga hayotdagi eng go‘zal ne’matlar – mustahkam sog‘lik, oilaviy baxt, qalb xotirjamligi va uzoq umr tilaymiz.\n\nInson hayotida ota-onadan keyin uning dunyoqarashiga eng katta ta’sir ko‘rsatadigan insonlardan biri, albatta, ustozdir. Sizning bergan bilimlaringiz, hayotiy maslahatlaringiz va tarbiyangiz biz uchun bebaho boylikdir.\n\nBa’zan birgina ustozning aytgan so‘zi insonning butun hayot yo‘lini o‘zgartirishi mumkin. Sizning har bir nasihatingiz bizni yaxshilikka, izlanishga va o‘z ustimizda ishlashga undaydi.\n\nSizga mehnatingizning rohatini ko‘rishingizni, shogirdlaringizning yutuqlaridan doimo faxrlanib yurishingizni tilaymiz. Qalbingizdagi mehr, ko‘zingizdagi quvonch va yuzingizdagi tabassum hech qachon so‘nmasin. Bayramingiz qutlug‘ bo‘lsin!",
    },
    "Tojiboyev Oybek Inomjonovich": {
        "code": "401193",
        "congrats": "1-OKTABR — O'QITUVCHI VA MURABBIYLAR KUNI\n\nQadrli Ustoz!\n\nSizni 1-oktabr – O‘qituvchi va murabbiylar kuni bilan muborakbod etamiz! Ushbu ulug‘ bayram munosabati bilan Sizga eng ezgu va samimiy tilaklarimni yo‘llaymiz.\n\nSizning har bir darsingiz biz uchun yangi bilim va yangi imkoniyatlar eshigini ochadi. Bizga o‘rgatayotgan faningiz bilan bir qatorda tartib-intizom, mas’uliyat, sabr, halollik va insoniylik kabi muhim fazilatlarni ham singdirib kelasiz.\n\nUstozlik – katta sabr va fidoyilikni talab qiladigan sharafli yo‘l. Siz bu yo‘lda o‘z bilimingiz va mehringizni biz bilan ayamasdan baham ko‘rib kelmoqdasiz. Buning uchun Sizga chin dildan rahmat aytamiz.\n\nHayotingiz doimo yorug‘ va mazmunli bo‘lsin. Oilangizga tinchlik, dasturxoningizga baraka, qalbingizga xotirjamlik, faoliyatingizga ulkan zafarlar tilaymiz. Barcha ezgu niyatlaringiz amalga oshsin. Bayramingiz muborak bo‘lsin!",
    },
    "Tojiboyeva Zohida Yuldashboy qizi": {
        "code": "956436",
        "congrats": "1-OKTABR — O'QITUVCHI VA MURABBIYLAR KUNI\n\nHurmatli va mehribon Ustoz!\n\nSizni O‘qituvchi va murabbiylar kuni bilan chin qalbimdan tabriklaymiz! Sizga avvalo sihat-salomatlik, uzoq umr, oilaviy baxt va barcha ishlaringizda omad tilaymiz.\n\nSizning kasbingiz oddiy kasb emas. Siz yosh avlodning kelajagini shakllantirayotgan, ularning qalbiga bilim va ezgulik urug‘larini ekayotgan buyuk insonlardan birisiz. Har kuni biz uchun sarflayotgan vaqtingiz, sabringiz va mehnatingiz albatta o‘z samarasini beradi.\n\nBizning har bir yaxshi natijamiz Sizga quvonch bag‘ishlashini bilamiz. Shuning uchun kelajakda Siz bergan bilimlarni munosib ravishda qo‘llab, yaxshi inson bo‘lishga harakat qilamiz.\n\nSizga hech qachon charchoq va tashvish hamroh bo‘lmasin. Har bir kuningiz quvonchli xabarlar bilan boshlangan, yaxshi kayfiyat bilan davom etgan va xotirjamlik bilan yakunlangan kunlardan iborat bo‘lsin. Bayramingiz muborak, aziz Ustoz!",
    },
    "Toshboltayev G‘ofurjon Zoxidjon o‘g‘li": {
        "code": "202814",
        "congrats": "1-OKTABR — O'QITUVCHI VA MURABBIYLAR KUNI\n\nAziz Ustoz!\n\nSizni O‘qituvchi va murabbiylar kuni bilan muborakbod etamiz! Bu kun Siz kabi fidoyi, mehribon va bilimdon insonlarga bo‘lgan hurmatimizni yanada chuqurroq ifoda etish uchun ajoyib imkoniyatdir.\n\nSiz bizga bilim berish bilan birga, hayotda qanday inson bo‘lish kerakligini ham o‘rgatyapsiz. Har bir nasihatingiz, har bir talabingiz va har bir qo‘llab-quvvatlashingiz bizning kelajagimiz uchun xizmat qiladi.\n\nSizning sabringiz, mehnatingiz va o‘quvchilaringizga bo‘lgan mehringiz tahsinga loyiq. Shogirdlaringizning yutuqlari, yaxshi natijalari va kelajakdagi muvaffaqiyatlari Siz uchun eng katta mukofot bo‘lsin.\n\nUmringiz uzoq, sog‘lig‘ingiz mustahkam bo‘lsin. Oilangizda doimo tinchlik va totuvlik hukm sursin. Hayotingiz baxtli onlar, yaxshi insonlar va unutilmas quvonchli voqealarga boy bo‘lsin. Bayramingiz muborak bo‘lsin!",
    },
    "Turdiyeva Nargizaxon Mansurali qizi": {
        "code": "571497",
        "congrats": "1-OKTABR — O'QITUVCHI VA MURABBIYLAR KUNI\n\nQadrli Ustoz!\n\nSizni O‘qituvchi va murabbiylar kuni bilan chin yurakdan tabriklaymiz!\n\nHayotimizda bizga yo‘l ko‘rsatadigan, xatolarimizni to‘g‘rilaydigan va kelajakka ishonch bilan qarashimizga yordam beradigan insonlar juda ko‘p emas. Siz ana shunday insonlardan birisiz.\n\nSizning mehnatingiz, sabringiz va bizga ajratayotgan vaqtingiz uchun cheksiz minnatdormiz. Sizdan olgan bilimlarimiz maktab yoki darsxona bilan cheklanib qolmay, butun hayotimiz davomida bizga xizmat qiladi.\n\nTilagim – doimo sog‘-salomat bo‘ling, oilangiz bag‘rida baxtli hayot kechiring. Mehnatlaringiz samarasi yanada ko‘paysin, shogirdlaringizning yutuqlari Sizni har kuni quvontirsin. Qalbingiz doimo xotirjam, ko‘nglingiz doimo bahoriy bo‘lsin. Bayramingiz muborak!",
    },
    "Turdiyeva Nigoraxon Iskandarbekovna": {
        "code": "112046",
        "congrats": "1-OKTABR — O'QITUVCHI VA MURABBIYLAR KUNI\n\nHurmatli Ustoz!\n\nSizni eng ulug‘ va sharafli kasb egalarining bayrami bilan muborakbod etamiz! O‘qituvchilik – kelajak avlodga yo‘l ko‘rsatish, ularning qalbiga ilm va tarbiya nurini olib kirish demakdir.\n\nSizning har bir darsingiz ortida katta mehnat, tayyorgarlik va mas’uliyat bor. Biz buni qadrlaymiz. Bizga o‘rgatayotgan bilimlaringiz, bildirayotgan ishonchingiz va doimo yaxshi natijaga undayotganingiz uchun Sizga katta rahmat.\n\nSizga avvalo sog‘lik, uzoq umr, oilangizga fayz-u baraka va xotirjamlik tilaymiz. Ish faoliyatingizda yangi marralarni zabt eting, shogirdlaringizning muvaffaqiyatlari Siz uchun eng katta faxr bo‘lsin.\n\nHar bir kuningiz quvonchli xabarlar, samimiy insonlar va go‘zal lahzalarga boy bo‘lsin. Bayramingiz muborak bo‘lsin, aziz Ustoz!",
    },
    "Umarova Minovvarxon Joxongir qizi": {
        "code": "954340",
        "congrats": "1-OKTABR — O'QITUVCHI VA MURABBIYLAR KUNI\n\nAziz Ustoz!\n\nSizni kasb bayramingiz bilan samimiy tabriklaymiz! Sizga aytadigan tilaklarimiz juda ko‘p, ammo ularning eng muhimi – doimo sog‘-salomat va baxtli bo‘lishingizdir.\n\nBizga bergan har bir bilimingiz, aytgan har bir nasihatingiz va ko‘rsatgan har bir yo‘l-yo‘rig‘ingiz uchun Sizdan minnatdormiz. Sizning darslaringiz bizga faqatgina fan o‘rganish emas, balki hayotga tayyorlanish imkonini ham beradi.\n\nShogirdlaringizning har bir muvaffaqiyati, yaxshi natijalari va yutuqlari Sizning qalbingizga quvonch olib kirsin. Mehnatlaringiz doimo qadrlansin, obro‘-e’tiboringiz yanada oshsin.\n\nXonadoningizdan tinchlik, dasturxoningizdan baraka, qalbingizdan mehr va yuzingizdan tabassum arimasin. Barcha orzu-niyatlaringiz ro‘yobga chiqsin. O‘qituvchi va murabbiylar kuni muborak bo‘lsin!",
    },
    "Usambayeva Bashoratxon Xolmirzayevna": {
        "code": "818461",
        "congrats": "1-OKTABR — O'QITUVCHI VA MURABBIYLAR KUNI\n\nQadrli va hurmatli Ustoz!\n\nSizni O‘qituvchi va murabbiylar kuni bilan chin qalbimdan muborakbod etamiz! Siz kabi ustozlarning mehnatini oddiy so‘zlar bilan ta’riflash juda qiyin.\n\nSiz bizga bilim berasiz, savollarimizga javob berasiz, xatolarimizni tushuntirasiz va eng muhimi, kelajagimizga ishonch bilan qarashga o‘rgatasiz. Sizning sabringiz va fidoyiligingiz har qanday maqtovga loyiq.\n\nTilaymanki, hayotingizning har bir kuni quvonch va baxt bilan o‘tsin. Sog‘lig‘ingiz mustahkam, umringiz uzoq, oilangiz tinch va farovon bo‘lsin. Kasbiy faoliyatingizda doimo yuqori natijalarga erishing.\n\nSiz tarbiyalagan shogirdlar kelajakda katta yutuqlarga erishib, Sizni faxr bilan eslab yurishsin. Bayramingiz muborak bo‘lsin, aziz Ustoz!",
    },
    "Xakimov Elmurodjon Dilmurodjon o‘g‘li": {
        "code": "614102",
        "congrats": "1-OKTABR — O'QITUVCHI VA MURABBIYLAR KUNI\n\nMuhtaram Ustoz!\n\nSizni O‘qituvchi va murabbiylar kuni bilan chin dildan muborakbod etamiz! Sizga ushbu bayramda eng ezgu va samimiy tilaklarimni yo‘llaymiz.\n\nUstoz – inson hayotida iz qoldiradigan buyuk kasb egasidir. Sizning bizga bergan bilimlaringiz, tarbiyangiz va maslahatlaringiz kelajakda ham bizga yo‘l ko‘rsatib turadi.\n\nSizga o‘z kasbingizdan doimo zavq olib, shogirdlaringizning yutuqlaridan faxrlanib yurishingizni tilaymiz. Har bir mehnatingiz munosib e’tirof etilsin.\n\nSiz va oilangizga sog‘lik-salomatlik, xotirjamlik, baxt va farovonlik tilaymiz. Hayotingizda faqat yaxshi kunlar, quvonchli yangiliklar va unutilmas lahzalar ko‘p bo‘lsin. Bayramingiz muborak!",
    },
    "Xalilova Sevaraxon Ismoiljon qizi": {
        "code": "812390",
        "congrats": "1-OKTABR — O'QITUVCHI VA MURABBIYLAR KUNI\n\nAziz va hurmatli Ustoz!\n\nSizni go‘zal va sharafli bayram – O‘qituvchi va murabbiylar kuni bilan chin dildan tabriklaymiz!\n\nSizning mehnatingiz tufayli biz bilim olamiz, dunyoqarashimiz kengayadi va kelajakdagi maqsadlarimiz sari dadil qadam tashlashni o‘rganamiz. Har bir darsingiz bizga yangi bilim, yangi fikr va yangi imkoniyat beradi.\n\nSizning sabr-toqatingiz, mehringiz va fidoyiligingiz biz uchun juda qadrlidir. Bizga bergan bilimlaringiz va qilayotgan mehnatingiz uchun chin qalbimdan rahmat aytamiz.\n\nDoimo sog‘lom va bardam bo‘ling. Oilangizda tinchlik va farovonlik hukm sursin. Kasbiy faoliyatingizda omad va zafarlar Sizga doim hamroh bo‘lsin. Shogirdlaringizning yutuqlari Sizni hech qachon tark etmaydigan faxr va quvonchga aylansin. Bayramingiz muborak bo‘lsin!",
    },
    "Xamrakulov Yuldashboy xxx": {
        "code": "429497",
        "congrats": "1-OKTABR — O'QITUVCHI VA MURABBIYLAR KUNI\n\nHurmatli Ustoz!\n\nSizni O‘qituvchi va murabbiylar kuni bilan chin qalbimdan tabriklaymiz! Sizga hayotdagi eng yaxshi va ezgu tilaklarni tilaymiz.\n\nSizning bizga bergan bilimlaringizni hech qanday boylik bilan o‘lchab bo‘lmaydi. Chunki bilim inson bilan birga butun umr qoladigan eng katta boylikdir. Siz esa ana shu bebaho boylikni biz bilan baham ko‘ryapsiz.\n\nSizga qilayotgan mehnatingizda kuch-g‘ayrat, qalbingizda xotirjamlik va hayotingizda baxt tilaymiz. Har bir yangi kun Sizga yangi quvonchlar olib kelsin.\n\nOilangiz doimo sog‘-omon, xonadoningiz fayzli va barakali bo‘lsin. Siz tarbiyalayotgan shogirdlar kelajakda yurtimizga foydasi tegadigan, bilimli va yaxshi insonlar bo‘lib yetishsin. Bayramingiz muborak bo‘lsin!",
    },
    "Xojiboyeva Nasibaxon Zafarjon qizi": {
        "code": "320436",
        "congrats": "1-OKTABR — O'QITUVCHI VA MURABBIYLAR KUNI\n\nQadrli Ustoz!\n\nSizni kasb bayramingiz – O‘qituvchi va murabbiylar kuni bilan muborakbod etamiz!\n\nHar bir insonning hayotida uni ilhomlantirgan, bilim bergan va to‘g‘ri yo‘l ko‘rsatgan ustoz bo‘ladi. Siz ham biz uchun ana shunday qadrli insonlardan birisiz.\n\nSizning mehnatingiz, sabringiz va mehringiz tufayli ko‘plab o‘quvchilar o‘z kelajagiga ishonch bilan qarashni o‘rganmoqda. Sizning har bir darsingiz va har bir nasihatingiz biz uchun qimmatli.\n\nSizga mustahkam sog‘lik, uzoq umr, oilaviy baxt va kasbiy faoliyatingizda ulkan muvaffaqiyatlar tilaymiz. Har doim shogirdlaringizning hurmati va ehtiromida bo‘ling. Bayramingiz muborak bo‘lsin!",
    },
    "Xurboyeva Maktubaxon Abdulxafizovna": {
        "code": "516512",
        "congrats": "1-OKTABR — O'QITUVCHI VA MURABBIYLAR KUNI\n\nAziz Ustoz!\n\nBugungi bayramingiz bilan Sizni chin yurakdan tabriklaymiz! Sizga eng avvalo sihat-salomatlik, uzoq umr va oilaviy baxt tilaymiz.\n\nUstozning mehnati inson hayotida juda katta iz qoldiradi. Sizning bugun bergan bilimingiz ertaga bizning kelajagimizga aylanadi. Sizning bir og‘iz yaxshi so‘zingiz bizga kuch, birgina maslahatingiz esa to‘g‘ri yo‘l topishimizga yordam beradi.\n\nSizning shogirdlaringiz doimo yaxshi natijalarga erishib, Sizning nomingizni faxr bilan tilga olishsin. Har bir qilgan mehnatingizning rohatini ko‘rib yashang.\n\nXonadoningizdan fayz-u baraka arimasin, qalbingiz doimo quvonchga to‘lsin. Bayramingiz muborak bo‘lsin, hurmatli Ustoz!",
    },
    "Yuldasheva Zarifa Abdukaxar qizi": {
        "code": "363730",
        "congrats": "1-OKTABR — O'QITUVCHI VA MURABBIYLAR KUNI\n\nMuhtaram Ustoz!\n\nSizni O‘qituvchi va murabbiylar kuni bilan samimiy tabriklaymiz! Ushbu go‘zal kun Sizga bo‘lgan hurmatimiz va minnatdorligimizni ifodalash uchun eng yaxshi kunlardan biridir.\n\nSiz bizga bilim berish bilan birga, har kuni o‘z ustimizda ishlashni, maqsadlarimizga intilishni va insoniy fazilatlarni qadrlashni o‘rgatasiz. Buning uchun Sizga katta rahmat.\n\nSizga kelgusi faoliyatingizda ulkan zafarlar, yangi marralar va katta yutuqlar tilaymiz. Har bir boshlagan ishingiz omadli yakun topsin.\n\nSog‘lig‘ingiz mustahkam, oilangiz farovon, hayotingiz mazmunli va baxtli bo‘lsin. Doimo biz kabi shogirdlaringizning hurmati va mehrini his qilib yuring. Bayramingiz muborak!",
    },
    "Abdurashidova Muxsinabegim Dilshodbek qizi": {
        "code": "464545",
        "congrats": "1-OKTABR — O'QITUVCHI VA MURABBIYLAR KUNI\n\nAziz va mehribon Ustoz!\n\nSizni O‘qituvchi va murabbiylar kuni bilan chin dildan tabriklaymiz! Sizga ushbu bayramda eng go‘zal tilaklarimni yo‘llaymiz.\n\nSizning har bir darsingiz, har bir tushuntirishingiz va har bir nasihatingiz bizning bilimimiz va dunyoqarashimizni boyitib boradi. Siz bizga faqat kitobdagi bilimlarni emas, hayotda kerak bo‘ladigan sabr, mehnat, halollik va mas’uliyatni ham o‘rgatyapsiz.\n\nMehnatingizning eng katta mukofoti shogirdlaringizning yutuqlari bo‘lsin. Siz tarbiyalagan yoshlar kelajakda katta marralarni zabt etib, Sizni doimo faxr bilan eslashsin.\n\nSizga sog‘lik, baxt, oilaviy xotirjamlik, ishlaringizda rivoj va hayotingizda cheksiz quvonch tilaymiz. Bayramingiz muborak bo‘lsin!",
    },
    "Soxibov Doniyorbek Sarvarbek o`g`li": {
        "code": "473960",
        "congrats": "1-OKTABR — O'QITUVCHI VA MURABBIYLAR KUNI\n\nHurmatli Ustoz!\n\nSizni bugungi qutlug‘ bayram – O‘qituvchi va murabbiylar kuni bilan muborakbod etamiz!\n\nSizning kasbingiz katta sabr, kuch va fidoyilikni talab qiladi. Shunga qaramay, Siz har kuni o‘quvchilaringizga mehr bilan bilim berib, ularning kelajagi uchun astoydil mehnat qilasiz.\n\nBizga bergan bilimlaringiz, vaqt va e’tiboringiz uchun Sizdan minnatdormiz. Sizning mehnatingiz kelajakda bizning yutuqlarimiz orqali o‘z samarasini ko‘rsatadi.\n\nSizga mustahkam sog‘lik, uzoq umr, oilangizga baxt va farovonlik tilaymiz. Har bir kuningiz yaxshi xabarlar, quvonch va xotirjamlik bilan o‘tsin. Barcha ezgu orzularingiz amalga oshsin. Bayramingiz muborak bo‘lsin!",
    },
    "Abduqodirova Kamolaxon Abdujalil qizi": {
        "code": "944246",
        "congrats": "1-OKTABR — O'QITUVCHI VA MURABBIYLAR KUNI\n\nQadrli Ustoz!\n\nSizni O‘qituvchi va murabbiylar kuni bilan muborakbod etamiz! Ushbu go‘zal bayramda Sizga eng samimiy tilaklarimni bildiramiz.\n\nSizning hayotimizdagi o‘rningiz juda katta. Chunki Siz bizga nafaqat bilim, balki hayot yo‘lida kerak bo‘ladigan tajriba va saboq ham berasiz. Har bir darsingizdan o‘zimiz uchun foydali xulosa chiqarishga harakat qilamiz.\n\nSizga kasbingizda doimo rivoj, yangi yutuqlar va katta muvaffaqiyatlar tilaymiz. Shogirdlaringizning yutuqlari Sizning eng katta quvonchingiz bo‘lsin.\n\nOilangizda tinchlik, xonadoningizda fayz, qalbingizda xotirjamlik bo‘lsin. Doimo sog‘-salomat bo‘lib, shogirdlaringiz ardog‘ida yuring. Bayramingiz muborak!",
    },
    "Kuchqarova Barnoxon Xoldaraliyevna": {
        "code": "494625",
        "congrats": "1-OKTABR — O'QITUVCHI VA MURABBIYLAR KUNI\n\nAziz Ustoz!\n\nSizni O‘qituvchi va murabbiylar kuni bilan chin qalbimdan tabriklaymiz! Sizga avvalo sog‘lik-salomatlik, oilaviy baxt va uzoq umr tilaymiz.\n\nSizning har kuni qilayotgan mehnatingiz kelajak avlod uchun katta ahamiyatga ega. Bizga bergan bilimlaringiz va tarbiyangiz hayotimiz davomida bizga yordam beradi.\n\nSizning sabringiz, mehringiz va bizga bo‘lgan ishonchingizni juda qadrlaymiz. Biz uchun qilayotgan barcha mehnatlaringiz uchun katta rahmat.\n\nHayotingiz doimo go‘zal voqealar va quvonchli kunlarga boy bo‘lsin. Ish faoliyatingizda omad va muvaffaqiyatlar hamisha hamroh bo‘lsin. Barcha niyatlaringiz amalga oshsin. Bayramingiz muborak bo‘lsin!",
    },
}


# Ismlar ro'yxati (tugmalar uchun barqaror tartibda)
NAMES = list(TEACHERS.keys())

# Suhbat holatlari (ConversationHandler uchun)
CHOOSING_NAME, ENTERING_CODE = range(2)


# ------------------------------------------------------------
# /start — ism tanlash (xabar ichidagi tugmalar orqali)
# ------------------------------------------------------------
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    buttons = [
        InlineKeyboardButton(NAMES[i], callback_data=f"name:{i}")
        for i in range(len(NAMES))
    ]
    keyboard = [[b] for b in buttons]
    reply_markup = InlineKeyboardMarkup(keyboard)

    await update.message.reply_text(
        "Assalomu alaykum, hurmatli ustoz!\n"
        "1-Oktabr — O'qituvchi va murabbiylar kuni munosabati bilan tabrik botiga xush kelibsiz.\n\n"
        "Iltimos, quyidagi ro'yxatdan o'z ismingizni tanlang:",
        reply_markup=reply_markup,
    )
    return CHOOSING_NAME


# ------------------------------------------------------------
# Ism tugmasi bosildi -> maxfiy kod so'raladi
# ------------------------------------------------------------
async def name_chosen(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    await query.answer()

    idx = int(query.data.split(":", 1)[1])
    name = NAMES[idx]
    context.user_data["name"] = name

    await query.edit_message_text(
        f"Xush kelibsiz, {name}!\nIltimos, sizga berilgan maxfiy kodni kiriting:"
    )
    return ENTERING_CODE


# ------------------------------------------------------------
# Kod tekshiriladi -> tabrik chiqariladi
# ------------------------------------------------------------
async def code_entered(update: Update, context: ContextTypes.DEFAULT_TYPE):
    name = context.user_data.get("name")
    code = update.message.text.strip()

    if TEACHERS.get(name, {}).get("code") != code:
        await update.message.reply_text(
            "❌ Kod noto'g'ri. Iltimos, qaytadan urinib ko'ring:"
        )
        return ENTERING_CODE

    congrats = TEACHERS[name]["congrats"]
    await update.message.reply_text(congrats)
    return ConversationHandler.END


# ------------------------------------------------------------
# /cancel — suhbatni bekor qilish
# ------------------------------------------------------------
async def cancel(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text(
        "Bekor qilindi. Qayta boshlash uchun /start ni bosing.",
    )
    return ConversationHandler.END


def main():
    app = ApplicationBuilder().token(BOT_TOKEN).build()

    conv_handler = ConversationHandler(
        entry_points=[CommandHandler("start", start)],
        states={
            CHOOSING_NAME: [CallbackQueryHandler(name_chosen, pattern=r"^name:\d+$")],
            ENTERING_CODE: [MessageHandler(filters.TEXT & ~filters.COMMAND, code_entered)],
        },
        fallbacks=[CommandHandler("cancel", cancel)],
    )

    app.add_handler(conv_handler)
    print("Bot ishga tushdi...")
    app.run_polling()


if __name__ == "__main__":
    main()

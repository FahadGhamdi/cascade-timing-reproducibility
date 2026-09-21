# حزمة تشغيل أصول التجارب — BRACE

الورقة: What Does Timing Add to Size? Probabilistic Forecasts of Recorded Cascade Growth on Two Archives.

## التكوين
هذه حزمة موزعة: ملف التحكم الحالي + ORIGINALS_PAYLOAD_01.zip + ORIGINALS_PAYLOAD_02.zip + ORIGINALS_PAYLOAD_03.zip. الحزم الثلاث هي التي سبق جمعها لديك، ولا تحتاج تنزيل نسخ أخرى منها. ملف التحكم وحده ليس حزمة البيانات. أبقِ DISTRIBUTION_INDEX.json بجوار reproduce.py. يتضمن مجلد paper نسخة IEEE Access Revision6 التي أُعدت في هذه المحادثة؛ لا يشمل أي تعديل خارجي لاحق.

السكربت reproduce.py جديد للتنسيق والتحقق. يتضمن محول إخراج gzip لتفريغ مخزن الكتابة كل128 صفًا أثناء استدعاء دالة التحليل الأصلية، لمعالجة انقطاع لوحظ هنا. لا يغير الحسابات أو المحتوى غير المضغوط؛ يقارن كامل المحتوى الناتج بالمرجع. السكربتات العلمية والبيانات والنماذج تُستخرج من أرشيفاتها الأصلية دون تغيير بايتاتها. لا يُستعمل old. لا يُستبدل إخراج موجود. لا تُفك نماذج pickle/joblib في مسارات التحقق والتحليل؛ مرحلتا test وnoise تستخدمان الأصل الموثق في بيئة الإصدارات المطلوبة.

## تشغيل سريع
فك ملف التحكم في Downloads. نفذ في Terminal:

```bash
cd ~/Downloads/BRACE_Original_Reproduction_Controller
python3 reproduce.py restore --assets /Users/fahad/Documents/Research-Projects/RADIC/ORIGINALS_EXPORT_20260914T074651Z --work /Users/fahad/Documents/Research-Projects/RADIC/REPRO_ORIGINALS_20260921
```

يجب أن يحتوي مسار assets على الحزم الثلاث الكاملة، وليس الأجزاء فقط. ملف ORIGINALS_PAYLOAD_03.zip الأصلي موجود بالفعل على جهازك؛ لا حاجة لإعادة تجميعه هناك.

افحص البيئة، مستخدمًا Python 3.12 الخاص ببيئة التجارب المسجلة:

```bash
python reproduce.py environment --work /Users/fahad/Documents/Research-Projects/RADIC/REPRO_ORIGINALS_20260921
```

ثم شغّل الاختبار المركب (يُنشئ مخرجات جديدة خارج مجلد الأصول):

```bash
python reproduce.py check-all --work /Users/fahad/Documents/Research-Projects/RADIC/REPRO_ORIGINALS_20260921 --out /Users/fahad/Documents/Research-Projects/RADIC/REPRO_CHECK_20260921
```

check-all يعيد تجهيز البيانات الخام، ثم يعيد التحليلات الأساسية والـbootstrap من الدرجات المحفوظة، وتحليل الشرائح والضجيج من الدرجات المحفوظة، ويتحقق من أدلة الورقة ويعيد الرسوم. لا يُدرّب النماذج ولا يعيد إنتاج الدرجات التوزيعية من التنبؤات. لا يُترجم PDF؛ ملفات LaTeX والـPDF السابقة ضمن paper، ويجب تجميعها بعد أي تحرير مستقل.

## إعادة التجارب الأصلية
تتطلب الأوامر التالية Python 3.12 وكل الإصدارات المثبتة في requirements.lock.txt دون تخفيف فحص البيئة:

```bash
python reproduce.py train --work /Users/fahad/Documents/Research-Projects/RADIC/REPRO_ORIGINALS_20260921 --out /Users/fahad/Documents/Research-Projects/RADIC/REPRO_TRAIN_20260921
python reproduce.py test --work /Users/fahad/Documents/Research-Projects/RADIC/REPRO_ORIGINALS_20260921 --out /Users/fahad/Documents/Research-Projects/RADIC/REPRO_TEST_20260921
python reproduce.py noise --work /Users/fahad/Documents/Research-Projects/RADIC/REPRO_ORIGINALS_20260921 --out /Users/fahad/Documents/Research-Projects/RADIC/REPRO_NOISE_20260921
```

- train: تشغيل التدريب والاختيار الأصلي 13E، بما في ذلك المرشحون المستبعدون. يسجل هل ملف قفل النماذج الجديد مطابق بايتًا؛ نجاح التشغيل وحده لا يعني تطابق التدريب.
- test: تشغيل التنبؤ والتقييم الأصلي 13F بالنماذج التاريخية المعتمدة في أرشيف 13E، ثم مقارنة الملخصات بالمرجع.
- noise: تشغيل المرحلة14 الأصلية، بما فيها ملاءمة الضجيج، مع أرشيف13F التاريخي المعتمد، ثم مقارنة النتائج والـbootstrap.

## الحد الجوهري: ليست سلسلة refit→test بديلة
13F يشترط بصمة أرشيف13E التاريخي، و14 يشترط بصمة أرشيف13F التاريخي. لذلك لا يمرر المشغّل ناتج train الجديد إلى test ولا ناتج test الجديد إلى noise. هذا فصل مقصود يحافظ على العقود الأصلية؛ لا تُغيّر البصمات أو الأقفال لتجاوزها.

لم تُختبر إعادة ملاءمة جميع النماذج هنا بسبب اختلاف19 اعتمادًا عن البيئة التاريخية. وجود أمر تشغيل ليس شهادة نجاحه. يلزم تشغيل هذه المراحل على Mac بالبيئة المطابقة، وفحص نتائج الاختيار والتنبؤات قبل القول إن التدريب من الصفر يعيد جميع النتائج. إعادة تغليف تشغيل جديد ستختلف بصمتها غالبًا بسبب السجلات والأزمنة حتى لو تطابقت نتائجه العلمية.

المقارنات العددية للتجميع تستخدم atol=1e-8 وrtol=1e-10 المعلنين أصلًا في مقارنة المرحلة14؛ البصمات وسلسلة بيانات الأصول تتطلب تطابقًا تامًا. لا تعديل للتسامحات بعد رؤية نتيجة اختبار. قد تختلف أهلية مرشح محدود بزمن بين جهازين؛ لا تُحذف هذه الإخفاقات.

## المخرجات
كل تشغيل يكتب RUN_REPORT.json وسجلات مستقلة ويحتفظ بالفشل كما هو. اختر مسار إخراج جديدًا لكل تشغيل مقصود؛ لا تمسح أقفال محاولة فاشلة لإعادة التدريب تلقائيًا. يستعمل المشغّل عمليات السكربتات الأصلية وبذورها وحدودها؛ لا يُضيف baseline أو تجربة جديدة.

راجع VALIDATION_AR.md لمعرفة ما اختُبر فعليًا، وCODEX_MAC_TASK_AR.md لإكمال فحص التدريب محليًا. يلزم Python مع NumPy/SciPy/Matplotlib للتحليلات؛ لا يتم تثبيت شيء آليًا. يتضمن environment/requirements.lock.txt الإصدارات الأصلية.

ملفات audit من مهمة جمع الأصول تاريخية وتصف حالة تلك المهمة؛ حدود الاختبار الحالية في VALIDATION_AR.md والسجل FINAL_RUN_REPORT.json. ملف التحكم هذا يستكمل حزم الأصول ويحل محل المشغّل الجزئي السابق لأغراض التنسيق؛ لا يحول الأدلة المحفوظة إلى شهادة إعادة تدريب.

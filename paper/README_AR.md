> آخر تحديث: المراجعة السادسة؛ المتن12 صفحة والملحق19 صفحة. راجع CONSULTANT_REVIEW_AR.md لتغييرات التنسيق والإفصاح والمراجع.

# حزمة BRACE — IEEE Access / Overleaf

هذه النسخة الثانية بعد ملاحظات المستشار، للمراجعة والتحرير، مبنية على النتائج المجمدة حتى المرحلة 14. افتح `CONSULTANT_REVIEW_AR.md` أولًا لفهم نطاق الإنجاز وحدوده.

## الرفع إلى Overleaf

1. نزّل ZIP ثم اختر مشروعًا جديدًا من ملف ZIP في Overleaf وارفعه.
2. اجعل `main.tex` الملف الرئيسي، واختر المترجم **pdfLaTeX** ثم أعد التجميع. المراجع تعمل بواسطة BibTeX؛ لا تحتاج shell-escape أو تشغيل Python لتجميع الورقة.
3. لعرض الملحق، غيّر الملف الرئيسي إلى `supplementary.tex` وأعد التجميع؛ ثم أعد الاختيار إلى `main.tex` عند العودة للمخطوطة.
4. عدّل فصول الورقة داخل `sections/`، والجداول داخل `tables/`، والمراجع داخل `references.bib`.
5. بيانات المؤلفين والإفصاحات والسير في `config/`. لا تستبدل حقول «pending» بتصريحات لم تتحقق منها.
6. مخطط المنهجية قابل للتعديل في `figures/methodology.tikz`. رسوم النتائج PDF متجهة وPNG، ومصدرها `support/make_publication_figures.py`.

أُثبت نجاح التجميع محليًا؛ لم يُفتح حسابك على Overleaf أو يُختبر المشروع داخله. القالب المرفق مستعاد من نسخة مشتقة من قالب Access، ومصدره موثق. لم تنجح مطابقة ملف الفئة مع أحدث تنزيل رسمي؛ راجع `audit/TEMPLATE_PROVENANCE.md` قبل التقديم.

## الملفات

- `main.tex`: المخطوطة الإنجليزية؛ `supplementary.tex`: الملحق التقني.
- `pdf/`: نسختا PDF الناتجتان عن المصادر الحالية.
- `CONSULTANT_REVIEW_AR.md`: ملخص التدقيق والمطلوب من المستشار.
- `TASK_BRIEF_AR.md`: تعريف المهمة ونطاقها ومعايير اكتمالها.
- `submission/AUTHOR_QUESTIONS_AR.md`: البيانات اللازمة من المؤلفين.
- `submission/COVER_LETTER_DRAFT_EN.md`: خطاب تغطية غير مرسل.
- `audit/REPORTING_CHECKS.json`: نتائج فحص اتساق التقرير؛ `REFERENCE_AUDIT.csv`: نطاق التحقق من كل مرجع.
- `support/`: أدلة وجداول وبروتوكولات محفوظة وسكربتات إنتاج الرسومات.
- `source/`: نسخ مرجعية سابقة محفوظة للمقارنة؛ ليست الملفات التي يجمعها Overleaf.

## إعادة إنتاج العرض محليًا

```sh
python support/make_publication_figures.py
python support/verify_reporting.py
latexmk -pdf -interaction=nonstopmode -halt-on-error main.tex
latexmk -pdf -interaction=nonstopmode -halt-on-error supplementary.tex
```

إعادة الرسوم تتطلب Python وNumPy وMatplotlib. الإصدارات التي استُخدمت موثقة في `audit/BUILD_ENVIRONMENT.json`. هذه الأوامر لا تعيد التجارب أو التدريب؛ ملفات النتائج الخام الكاملة والنماذج ليست جزءًا من حزمة التحرير. السكربتات التاريخية في `support/code/` تحتاج أرشيفاتها الأصلية، فلا تتعامل معها كاختبار يعمل تلقائيًا من هذه الحزمة.

احتفظ بالنتائج المجمدة دون تعديل. أي تصحيح علمي لاحق يحتاج سجلًا يذكر سببه والأرقام المتأثرة؛ لا تعِد الضبط على مجموعة TEST لرفع الأداء.

## إضافات النسخة الثانية

`submission/RESPONSE_TO_BASELINE_REQUEST_EN.md` رد مسبق على طلب المقارنات المجالية. `submission/CURRENT_IEEE_REQUIREMENTS_AR.md` تدقيق السياسة والرسوم. `submission/gagraphic.png` ملخص رسومي اختياري مع مصادره القابلة للتحرير. سجل المستشار الحالي يحسم الاختلافات مع التقرير الوارد، ويحفظ السابق كسجل تاريخي.

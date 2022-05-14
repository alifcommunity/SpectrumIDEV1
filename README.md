<div dir="rtl">

# محرر طيف | Spectrum IDE


<ul>

<li> <a href="#pics"> <h3>صور</h3> </a> </li>
<li> <a href="#dep"> <h3>الاعتماديات</h3> </a> </li>
<li> <h3>طريقة التثبيت</h3> </li>

<ul>
<li> <a href="#windows"> <h3>علي نظام ويندوز</h3> </a> </li>
<li> <a href="#linux"> <h3>علي نظام لينكس</h3> </a> </li>
</ul>

</ul>

<hr>

## <a name="pics"></a>بيئة تطوير لغة ألف 3

![SpectrumUI](https://user-images.githubusercontent.com/77246874/129458934-1bd6166e-9f30-445e-ab9b-9a9b6e7b1d21.png)

## <a name="dep"></a>الاعتماديات 

</br>

<div dir=ltr>

`python3 python3-venv PyQt6`

</br>

<div dir=rtl>

## طريقة التتبيث

</br>

> ### <a name="windows"></a>على نظام ويندوز

<div dir=rtl>

اولا قم بتثبيت الخطوط المرفقة

<div dir=ltr>

```bash
# استنساخ المشروع من جت هب
git clone https://github.com/alifcommunity/SpectrumIDEV1

# تغيير دليل العمل الحالي
cd SpectrumIDE
```

<div dir="rtl">
إنشاء بيئة افتراضية (اختياري)
<div dir=ltr>

```bash
# إنشاء البيئة الافتراضية
python3 -m venv venv

# تفعيل البيئة الافتراضية في نظام تشغيل ويندوز
venv\Scripts\activate.bat
```

<div dir="rtl">

تنزيل المكاتب


<div dir="ltr">

```bash
pip install -r requirements.txt
```

<div dir="rtl">
تشغيل المحرر

<div dir=ltr>

```bash
python Spectrum.py
```

<div dir="rtl">

</br>

> ### على نظام لينكس ` (اوبنتو أو ديبيان) `

<div dir=rtl>

اولا قم بتثبيت الخطوط المرفقة

<div dir=ltr>

```bash
# استنساخ المشروع من جت هب
git clone https://github.com/alifcommunity/SpectrumIDEV1

# تغيير دليل العمل الحالي
cd SpectrumIDE
```

<div dir="rtl">
إنشاء بيئة افتراضية (اختياري)
<div dir=ltr>

```bash
# تنزيل الاعتمادية
apt install python3-venv

# إنشاء البيئة الافتراضية
python3 -m venv venv

# تفعيل البيئة الافتراضية في نظام تشغيل لينكس/ماك
source venv/bin/activate
```

<div dir="rtl">

تنزيل المكاتب


<div dir="ltr">

```bash
pip install -r requirements.txt
```

<div dir="rtl">
تشغيل المحرر

<div dir=ltr>

```bash
python3 Spectrum.py
```

<div dir="rtl">


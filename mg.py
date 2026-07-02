# -*- coding: utf-8 -*-
"""
⚖️ الأجندة القضائية - تطبيق موبايل
مع دعم كامل للغة العربية باستخدام Arabic Reshaper
"""

from kivy.app import App
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.label import Label
from kivy.uix.textinput import TextInput
from kivy.uix.button import Button
from kivy.uix.scrollview import ScrollView
from kivy.uix.screenmanager import ScreenManager, Screen
from kivy.core.text import LabelBase
from kivy.utils import get_color_from_hex
import os
import requests
from datetime import datetime

# ============================================================
#   Arabic Reshaper - لحل مشكلة الحروف غير المتصلة
# ============================================================

try:
    import arabic_reshaper
    from bidi.algorithm import get_display
    RESHAPER_AVAILABLE = True
    print("✅ تم تحميل Arabic Reshaper بنجاح")
except ImportError:
    RESHAPER_AVAILABLE = False
    print("⚠️ لم يتم العثور على Arabic Reshaper")
    print("   قم بتشغيل: pip install arabic-reshaper python-bidi")

def ar(text):
    """
    دالة لتنسيق النص العربي بحيث تظهر الحروف متصلة
    """
    if not text:
        return text
    if RESHAPER_AVAILABLE:
        try:
            reshaped = arabic_reshaper.reshape(text)
            return get_display(reshaped)
        except:
            return text
    return text

# ============================================================
#   تسجيل خط عربي
# ============================================================

fonts_list = [
    'C:/Windows/Fonts/arial.ttf',
    'C:/Windows/Fonts/arialbd.ttf',
    'C:/Windows/Fonts/tahoma.ttf',
    'C:/Windows/Fonts/georgia.ttf',
    'C:/Windows/Fonts/times.ttf',
    'C:/Windows/Fonts/SimplifiedArabic.ttf',
    'C:/Windows/Fonts/Arabic Typesetting.ttf',
]

font_found = False
for font_path in fonts_list:
    if os.path.exists(font_path):
        try:
            LabelBase.register(name='Arabic', fn_regular=font_path)
            print(f"✅ تم تحميل الخط: {font_path}")
            font_found = True
            break
        except:
            continue

if not font_found:
    print("⚠️ لم يتم العثور على خط عربي")
    try:
        LabelBase.register(name='Arabic', fn_regular='DejaVuSans.ttf')
    except:
        pass

# ============================================================
#   شاشات التطبيق
# ============================================================

class LoginScreen(Screen):
    """شاشة تسجيل الدخول"""
    
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        
        main_layout = BoxLayout(
            orientation='vertical',
            padding=40,
            spacing=15,
        )
        main_layout.md_bg_color = get_color_from_hex('#0F172A')
        
        # الشعار والعنوان
        title_layout = BoxLayout(
            orientation='vertical',
            size_hint_y=0.35,
            spacing=5
        )
        
        logo = Label(
            text='⚖️',
            font_size=70,
            halign='center',
            size_hint_y=0.6
        )
        title_layout.add_widget(logo)
        
        title = Label(
            text=ar('الأجندة القضائية'),
            font_name='Arabic',
            font_size=28,
            color=get_color_from_hex('#F5C518'),
            halign='center',
            size_hint_y=0.4
        )
        title_layout.add_widget(title)
        main_layout.add_widget(title_layout)
        
        # حقول الإدخال
        input_layout = BoxLayout(
            orientation='vertical',
            size_hint_y=0.35,
            spacing=12
        )
        
        self.username = TextInput(
            hint_text=ar('اسم المستخدم'),
            font_name='Arabic',
            font_size=18,
            multiline=False,
            size_hint_y=0.3,
            foreground_color=get_color_from_hex('#FFFFFF'),
            background_color=get_color_from_hex('#1E293B'),
            cursor_color=get_color_from_hex('#F5C518')
        )
        input_layout.add_widget(self.username)
        
        self.password = TextInput(
            hint_text=ar('كلمة المرور'),
            font_name='Arabic',
            font_size=18,
            password=True,
            multiline=False,
            size_hint_y=0.3,
            foreground_color=get_color_from_hex('#FFFFFF'),
            background_color=get_color_from_hex('#1E293B'),
            cursor_color=get_color_from_hex('#F5C518')
        )
        input_layout.add_widget(self.password)
        
        main_layout.add_widget(input_layout)
        
        # الأزرار
        button_layout = BoxLayout(
            orientation='vertical',
            size_hint_y=0.2,
            spacing=8
        )
        
        btn_login = Button(
            text=ar('دخول'),
            font_name='Arabic',
            font_size=20,
            background_color=get_color_from_hex('#F5C518'),
            color=get_color_from_hex('#000000'),
            size_hint_y=0.6
        )
        btn_login.bind(on_press=self.login)
        button_layout.add_widget(btn_login)
        
        main_layout.add_widget(button_layout)
        
        # معلومات المستخدمين
        info = Label(
            text=ar('admin / 112233\nlawyer / 1234\nsecretary / 1234'),
            font_name='Arabic',
            font_size=13,
            color=get_color_from_hex('#94A3B8'),
            halign='center',
            size_hint_y=0.1
        )
        main_layout.add_widget(info)
        
        self.add_widget(main_layout)
    
    def login(self, instance):
        users = {
            'admin': '112233',
            'lawyer': '1234',
            'secretary': '1234'
        }
        
        username = self.username.text.strip()
        password = self.password.text.strip()
        
        if username in users and users[username] == password:
            self.manager.current = 'main'
            self.username.text = ''
            self.password.text = ''
        else:
            pass

class MainScreen(Screen):
    """الشاشة الرئيسية"""
    
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        
        layout = BoxLayout(
            orientation='vertical',
            padding=16,
            spacing=8,
        )
        layout.md_bg_color = get_color_from_hex('#F1F5F9')
        
        title = Label(
            text=ar('الأجندة القضائية'),
            font_name='Arabic',
            font_size=26,
            color=get_color_from_hex('#0F172A'),
            halign='center',
            size_hint_y=0.08
        )
        layout.add_widget(title)
        
        scroll = ScrollView(size_hint_y=0.8)
        buttons_layout = BoxLayout(
            orientation='vertical',
            spacing=8,
            size_hint_y=None
        )
        buttons_layout.bind(minimum_height=buttons_layout.setter('height'))
        
        buttons = [
            (ar('القضايا'), '#3B82F6', 'cases'),
            (ar('الجلسات'), '#10B981', 'sessions'),
            (ar('العملاء'), '#8B5CF6', 'clients'),
            (ar('الإعلانات'), '#F59E0B', 'announcements'),
            (ar('المحاميين'), '#1E3A5F', 'lawyers'),
            (ar('المحاكم'), '#0D9488', 'courts'),
            (ar('الإشعارات'), '#EF4444', 'notifications'),
        ]
        
        for text, color, name in buttons:
            btn = Button(
                text=text,
                font_name='Arabic',
                font_size=18,
                background_color=get_color_from_hex(color),
                size_hint_y=None,
                height=50
            )
            btn.bind(on_press=lambda x, n=name: setattr(self.manager, 'current', n))
            buttons_layout.add_widget(btn)
        
        scroll.add_widget(buttons_layout)
        layout.add_widget(scroll)
        
        btn_logout = Button(
            text=ar('خروج'),
            font_name='Arabic',
            font_size=16,
            background_color=get_color_from_hex('#64748B'),
            size_hint_y=0.08
        )
        btn_logout.bind(on_press=self.logout)
        layout.add_widget(btn_logout)
        
        self.add_widget(layout)
    
    def logout(self, instance):
        self.manager.current = 'login'

class CasesScreen(Screen):
    """شاشة عرض القضايا"""
    
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        
        layout = BoxLayout(
            orientation='vertical',
            padding=10,
            spacing=8,
        )
        layout.md_bg_color = get_color_from_hex('#F1F5F9')
        
        # شريط العنوان
        top_layout = BoxLayout(size_hint_y=0.08)
        
        btn_back = Button(
            text=ar('رجوع'),
            font_name='Arabic',
            font_size=16,
            background_color=get_color_from_hex('#64748B'),
            size_hint_x=0.2,
            size_hint_y=1
        )
        btn_back.bind(on_press=lambda x: setattr(self.manager, 'current', 'main'))
        top_layout.add_widget(btn_back)
        
        title = Label(
            text=ar('القضايا'),
            font_name='Arabic',
            font_size=24,
            color=get_color_from_hex('#0F172A'),
            halign='center',
            size_hint_x=0.6
        )
        top_layout.add_widget(title)
        
        btn_add = Button(
            text=ar('إضافة'),
            font_name='Arabic',
            font_size=16,
            background_color=get_color_from_hex('#10B981'),
            size_hint_x=0.2,
            size_hint_y=1
        )
        btn_add.bind(on_press=lambda x: setattr(self.manager, 'current', 'add_case'))
        top_layout.add_widget(btn_add)
        
        layout.add_widget(top_layout)
        
        # شريط البحث
        self.search_input = TextInput(
            hint_text=ar('بحث'),
            font_name='Arabic',
            font_size=16,
            multiline=False,
            size_hint_y=0.07,
            foreground_color=get_color_from_hex('#1E293B'),
            background_color=get_color_from_hex('#FFFFFF')
        )
        layout.add_widget(self.search_input)
        
        # قائمة القضايا
        scroll = ScrollView(size_hint_y=0.7)
        self.cases_layout = BoxLayout(
            orientation='vertical',
            spacing=6,
            size_hint_y=None
        )
        self.cases_layout.bind(minimum_height=self.cases_layout.setter('height'))
        
        self.cases_data = [
            {'رقم القضية': '2024-001', 'نوع القضية': 'مدني', 'المحكمة': 'محكمة القاهرة'},
            {'رقم القضية': '2024-002', 'نوع القضية': 'جنائي', 'المحكمة': 'محكمة الجيزة'},
            {'رقم القضية': '2024-003', 'نوع القضية': 'تجاري', 'المحكمة': 'محكمة الإسكندرية'},
            {'رقم القضية': '2024-004', 'نوع القضية': 'إداري', 'المحكمة': 'محكمة المنصورة'},
            {'رقم القضية': '2024-005', 'نوع القضية': 'أسرة', 'المحكمة': 'محكمة أسيوط'},
        ]
        
        for case in self.cases_data:
            case_box = BoxLayout(
                orientation='vertical',
                size_hint_y=None,
                height=55,
                padding=8,
                spacing=2
            )
            case_box.md_bg_color = get_color_from_hex('#FFFFFF')
            
            case_num = Label(
                text=ar(f"رقم: {case['رقم القضية']}"),
                font_name='Arabic',
                font_size=15,
                color=get_color_from_hex('#0F172A'),
                halign='right',
                size_hint_y=0.5
            )
            case_box.add_widget(case_num)
            
            case_info = Label(
                text=ar(f"{case['نوع القضية']} - {case['المحكمة']}"),
                font_name='Arabic',
                font_size=13,
                color=get_color_from_hex('#475569'),
                halign='right',
                size_hint_y=0.5
            )
            case_box.add_widget(case_info)
            
            self.cases_layout.add_widget(case_box)
        
        scroll.add_widget(self.cases_layout)
        layout.add_widget(scroll)
        
        self.add_widget(layout)

class AddCaseScreen(Screen):
    """شاشة إضافة قضية"""
    
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        
        layout = BoxLayout(
            orientation='vertical',
            padding=16,
            spacing=10,
        )
        layout.md_bg_color = get_color_from_hex('#F1F5F9')
        
        # العنوان مع زر رجوع
        top_layout = BoxLayout(size_hint_y=0.08)
        
        btn_back = Button(
            text=ar('رجوع'),
            font_name='Arabic',
            font_size=16,
            background_color=get_color_from_hex('#64748B'),
            size_hint_x=0.2,
            size_hint_y=1
        )
        btn_back.bind(on_press=lambda x: setattr(self.manager, 'current', 'cases'))
        top_layout.add_widget(btn_back)
        
        title = Label(
            text=ar('إضافة قضية'),
            font_name='Arabic',
            font_size=24,
            color=get_color_from_hex('#0F172A'),
            halign='center',
            size_hint_x=0.6
        )
        top_layout.add_widget(title)
        
        top_layout.add_widget(Label(size_hint_x=0.2))
        layout.add_widget(top_layout)
        
        # حقول الإدخال
        scroll = ScrollView()
        fields_layout = BoxLayout(
            orientation='vertical',
            spacing=10,
            size_hint_y=None
        )
        fields_layout.bind(minimum_height=fields_layout.setter('height'))
        
        self.case_number = TextInput(
            hint_text=ar('رقم القضية'),
            font_name='Arabic',
            font_size=16,
            multiline=False,
            size_hint_y=None,
            height=50,
            foreground_color=get_color_from_hex('#1E293B'),
            background_color=get_color_from_hex('#FFFFFF')
        )
        fields_layout.add_widget(self.case_number)
        
        self.case_type = TextInput(
            hint_text=ar('نوع القضية'),
            font_name='Arabic',
            font_size=16,
            multiline=False,
            size_hint_y=None,
            height=50,
            foreground_color=get_color_from_hex('#1E293B'),
            background_color=get_color_from_hex('#FFFFFF')
        )
        fields_layout.add_widget(self.case_type)
        
        self.court = TextInput(
            hint_text=ar('المحكمة'),
            font_name='Arabic',
            font_size=16,
            multiline=False,
            size_hint_y=None,
            height=50,
            foreground_color=get_color_from_hex('#1E293B'),
            background_color=get_color_from_hex('#FFFFFF')
        )
        fields_layout.add_widget(self.court)
        
        self.plaintiff = TextInput(
            hint_text=ar('المدعي'),
            font_name='Arabic',
            font_size=16,
            multiline=False,
            size_hint_y=None,
            height=50,
            foreground_color=get_color_from_hex('#1E293B'),
            background_color=get_color_from_hex('#FFFFFF')
        )
        fields_layout.add_widget(self.plaintiff)
        
        self.defendant = TextInput(
            hint_text=ar('المدعى عليه'),
            font_name='Arabic',
            font_size=16,
            multiline=False,
            size_hint_y=None,
            height=50,
            foreground_color=get_color_from_hex('#1E293B'),
            background_color=get_color_from_hex('#FFFFFF')
        )
        fields_layout.add_widget(self.defendant)
        
        self.notes = TextInput(
            hint_text=ar('ملاحظات'),
            font_name='Arabic',
            font_size=16,
            multiline=True,
            size_hint_y=None,
            height=100,
            foreground_color=get_color_from_hex('#1E293B'),
            background_color=get_color_from_hex('#FFFFFF')
        )
        fields_layout.add_widget(self.notes)
        
        scroll.add_widget(fields_layout)
        layout.add_widget(scroll)
        
        btn_save = Button(
            text=ar('حفظ'),
            font_name='Arabic',
            font_size=18,
            background_color=get_color_from_hex('#10B981'),
            size_hint_y=0.08
        )
        btn_save.bind(on_press=self.save_case)
        layout.add_widget(btn_save)
        
        self.add_widget(layout)
    
    def save_case(self, instance):
        case_number = self.case_number.text.strip()
        court = self.court.text.strip()
        
        if not case_number or not court:
            return
        
        self.send_notification(case_number, self.case_type.text, court)
        
        self.case_number.text = ''
        self.case_type.text = ''
        self.court.text = ''
        self.plaintiff.text = ''
        self.defendant.text = ''
        self.notes.text = ''
        
        self.manager.current = 'cases'
    
    def send_notification(self, case_number, case_type, court):
        try:
            url = "https://ntfy.sh/agenda_lawyer"
            message = f"🔔 إضافة قضية\n════════════════\n🕐 {datetime.now().strftime('%Y-%m-%d %H:%M')}\n📌 رقم القضية: {case_number}\n📌 نوع القضية: {case_type}\n📌 المحكمة: {court}\n════════════════\n📱 الأجندة القضائية"
            
            response = requests.post(
                url,
                data=message.encode('utf-8'),
                headers={
                    'Content-Type': 'text/plain',
                    'Priority': '5',
                    'Tags': 'info'
                },
                timeout=10
            )
            print("✅ تم إرسال الإشعار" if response.ok else "❌ فشل الإرسال")
        except Exception as e:
            print(f"خطأ: {e}")

class SessionsScreen(Screen):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        layout = BoxLayout(orientation='vertical', padding=10, spacing=10)
        layout.md_bg_color = get_color_from_hex('#F1F5F9')
        
        top_layout = BoxLayout(size_hint_y=0.08)
        btn_back = Button(text=ar('رجوع'), font_name='Arabic', font_size=16, background_color=get_color_from_hex('#64748B'), size_hint_x=0.2, size_hint_y=1)
        btn_back.bind(on_press=lambda x: setattr(self.manager, 'current', 'main'))
        top_layout.add_widget(btn_back)
        title = Label(text=ar('الجلسات'), font_name='Arabic', font_size=24, color=get_color_from_hex('#0F172A'), halign='center')
        top_layout.add_widget(title)
        top_layout.add_widget(Label(size_hint_x=0.2))
        layout.add_widget(top_layout)
        
        content = Label(text=ar('لا توجد جلسات'), font_name='Arabic', font_size=18, color=get_color_from_hex('#94A3B8'), halign='center')
        layout.add_widget(content)
        self.add_widget(layout)

class ClientsScreen(Screen):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        layout = BoxLayout(orientation='vertical', padding=10, spacing=10)
        layout.md_bg_color = get_color_from_hex('#F1F5F9')
        
        top_layout = BoxLayout(size_hint_y=0.08)
        btn_back = Button(text=ar('رجوع'), font_name='Arabic', font_size=16, background_color=get_color_from_hex('#64748B'), size_hint_x=0.2, size_hint_y=1)
        btn_back.bind(on_press=lambda x: setattr(self.manager, 'current', 'main'))
        top_layout.add_widget(btn_back)
        title = Label(text=ar('العملاء'), font_name='Arabic', font_size=24, color=get_color_from_hex('#0F172A'), halign='center')
        top_layout.add_widget(title)
        top_layout.add_widget(Label(size_hint_x=0.2))
        layout.add_widget(top_layout)
        
        clients_data = [
            {'الاسم': 'أحمد محمد', 'التليفون': '01012345678'},
            {'الاسم': 'سامي رضا', 'التليفون': '01087654321'},
            {'الاسم': 'نادين عادل', 'التليفون': '01011223344'},
        ]
        
        scroll = ScrollView()
        clients_layout = BoxLayout(orientation='vertical', spacing=6, size_hint_y=None)
        clients_layout.bind(minimum_height=clients_layout.setter('height'))
        
        for client in clients_data:
            client_box = BoxLayout(orientation='vertical', size_hint_y=None, height=45, padding=8)
            client_box.md_bg_color = get_color_from_hex('#FFFFFF')
            
            name = Label(text=ar(f"{client['الاسم']}"), font_name='Arabic', font_size=15, color=get_color_from_hex('#0F172A'), halign='right', size_hint_y=0.6)
            client_box.add_widget(name)
            
            phone = Label(text=ar(f"ت: {client['التليفون']}"), font_name='Arabic', font_size=13, color=get_color_from_hex('#475569'), halign='right', size_hint_y=0.4)
            client_box.add_widget(phone)
            
            clients_layout.add_widget(client_box)
        
        scroll.add_widget(clients_layout)
        layout.add_widget(scroll)
        self.add_widget(layout)

class AnnouncementsScreen(Screen):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        layout = BoxLayout(orientation='vertical', padding=10, spacing=10)
        layout.md_bg_color = get_color_from_hex('#F1F5F9')
        
        top_layout = BoxLayout(size_hint_y=0.08)
        btn_back = Button(text=ar('رجوع'), font_name='Arabic', font_size=16, background_color=get_color_from_hex('#64748B'), size_hint_x=0.2, size_hint_y=1)
        btn_back.bind(on_press=lambda x: setattr(self.manager, 'current', 'main'))
        top_layout.add_widget(btn_back)
        title = Label(text=ar('الإعلانات'), font_name='Arabic', font_size=24, color=get_color_from_hex('#0F172A'), halign='center')
        top_layout.add_widget(title)
        top_layout.add_widget(Label(size_hint_x=0.2))
        layout.add_widget(top_layout)
        
        content = Label(text=ar('لا توجد إعلانات'), font_name='Arabic', font_size=18, color=get_color_from_hex('#94A3B8'), halign='center')
        layout.add_widget(content)
        self.add_widget(layout)

class LawyersScreen(Screen):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        layout = BoxLayout(orientation='vertical', padding=10, spacing=10)
        layout.md_bg_color = get_color_from_hex('#F1F5F9')
        
        top_layout = BoxLayout(size_hint_y=0.08)
        btn_back = Button(text=ar('رجوع'), font_name='Arabic', font_size=16, background_color=get_color_from_hex('#64748B'), size_hint_x=0.2, size_hint_y=1)
        btn_back.bind(on_press=lambda x: setattr(self.manager, 'current', 'main'))
        top_layout.add_widget(btn_back)
        title = Label(text=ar('المحاميين'), font_name='Arabic', font_size=24, color=get_color_from_hex('#0F172A'), halign='center')
        top_layout.add_widget(title)
        top_layout.add_widget(Label(size_hint_x=0.2))
        layout.add_widget(top_layout)
        
        content = Label(text=ar('لا يوجد محاميين'), font_name='Arabic', font_size=18, color=get_color_from_hex('#94A3B8'), halign='center')
        layout.add_widget(content)
        self.add_widget(layout)

class CourtsScreen(Screen):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        layout = BoxLayout(orientation='vertical', padding=10, spacing=10)
        layout.md_bg_color = get_color_from_hex('#F1F5F9')
        
        top_layout = BoxLayout(size_hint_y=0.08)
        btn_back = Button(text=ar('رجوع'), font_name='Arabic', font_size=16, background_color=get_color_from_hex('#64748B'), size_hint_x=0.2, size_hint_y=1)
        btn_back.bind(on_press=lambda x: setattr(self.manager, 'current', 'main'))
        top_layout.add_widget(btn_back)
        title = Label(text=ar('المحاكم'), font_name='Arabic', font_size=24, color=get_color_from_hex('#0F172A'), halign='center')
        top_layout.add_widget(title)
        top_layout.add_widget(Label(size_hint_x=0.2))
        layout.add_widget(top_layout)
        
        content = Label(text=ar('لا توجد محاكم'), font_name='Arabic', font_size=18, color=get_color_from_hex('#94A3B8'), halign='center')
        layout.add_widget(content)
        self.add_widget(layout)

class NotificationsScreen(Screen):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        layout = BoxLayout(orientation='vertical', padding=16, spacing=12)
        layout.md_bg_color = get_color_from_hex('#F1F5F9')
        
        top_layout = BoxLayout(size_hint_y=0.08)
        btn_back = Button(text=ar('رجوع'), font_name='Arabic', font_size=16, background_color=get_color_from_hex('#64748B'), size_hint_x=0.2, size_hint_y=1)
        btn_back.bind(on_press=lambda x: setattr(self.manager, 'current', 'main'))
        top_layout.add_widget(btn_back)
        title = Label(text=ar('الإشعارات'), font_name='Arabic', font_size=24, color=get_color_from_hex('#0F172A'), halign='center')
        top_layout.add_widget(title)
        top_layout.add_widget(Label(size_hint_x=0.2))
        layout.add_widget(top_layout)
        
        content_layout = BoxLayout(orientation='vertical', spacing=10)
        
        Label(text=ar('نظام إشعارات ntfy'), font_name='Arabic', font_size=20, color=get_color_from_hex('#3B82F6'), halign='center', size_hint_y=0.1)
        content_layout.add_widget(Label(text=ar('الموضوع: agenda_lawyer'), font_name='Arabic', font_size=16, color=get_color_from_hex('#64748B'), halign='center', size_hint_y=0.08))
        
        btn_test = Button(text=ar('اختبار الإشعار'), font_name='Arabic', font_size=18, background_color=get_color_from_hex('#3B82F6'), size_hint_y=0.1)
        btn_test.bind(on_press=self.test_notification)
        content_layout.add_widget(btn_test)
        
        self.test_status = Label(text='', font_name='Arabic', font_size=14, halign='center', size_hint_y=0.06)
        content_layout.add_widget(self.test_status)
        
        info = Label(text=ar('لتلقي الإشعارات على هاتفك\nحمّل تطبيق ntfy من Google Play\nواشترك في: agenda_lawyer'), font_name='Arabic', font_size=12, color=get_color_from_hex('#94A3B8'), halign='center', size_hint_y=0.15)
        content_layout.add_widget(info)
        
        layout.add_widget(content_layout)
        self.add_widget(layout)
    
    def test_notification(self, instance):
        try:
            url = "https://ntfy.sh/agenda_lawyer"
            message = f"🔔 اختبار الإشعارات\n════════════════\n🕐 {datetime.now().strftime('%Y-%m-%d %H:%M')}\n📌 نوع الإشعار: اختبار\n📌 الحالة: نجاح\n════════════════\n📱 الأجندة القضائية v4.0"
            
            response = requests.post(
                url,
                data=message.encode('utf-8'),
                headers={
                    'Content-Type': 'text/plain',
                    'Priority': '3',
                    'Tags': 'white_check_mark'
                },
                timeout=10
            )
            
            if response.ok:
                self.test_status.text = ar('✅ تم إرسال الإشعار بنجاح!')
                self.test_status.color = get_color_from_hex('#10B981')
            else:
                self.test_status.text = ar(f'❌ فشل الإرسال: {response.status_code}')
                self.test_status.color = get_color_from_hex('#EF4444')
        except Exception as e:
            self.test_status.text = ar(f'❌ خطأ: {str(e)[:30]}')
            self.test_status.color = get_color_from_hex('#EF4444')

# ============================================================
#   تشغيل التطبيق
# ============================================================

class AgendaApp(App):
    def build(self):
        self.title = 'الأجندة القضائية'
        sm = ScreenManager()
        
        sm.add_widget(LoginScreen(name='login'))
        sm.add_widget(MainScreen(name='main'))
        sm.add_widget(CasesScreen(name='cases'))
        sm.add_widget(AddCaseScreen(name='add_case'))
        sm.add_widget(SessionsScreen(name='sessions'))
        sm.add_widget(ClientsScreen(name='clients'))
        sm.add_widget(AnnouncementsScreen(name='announcements'))
        sm.add_widget(LawyersScreen(name='lawyers'))
        sm.add_widget(CourtsScreen(name='courts'))
        sm.add_widget(NotificationsScreen(name='notifications'))
        
        return sm

if __name__ == '__main__':
    AgendaApp().run()
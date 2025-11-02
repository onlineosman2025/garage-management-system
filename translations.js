/**
 * Centralized Translation Manager for Garage Management System
 * Supports English, Arabic, and Urdu
 */

const TranslationManager = {
    translations: {
        en: {
            // Common
            'welcome': 'Welcome',
            'logout': 'Logout',
            'save': 'Save',
            'cancel': 'Cancel',
            'delete': 'Delete',
            'edit': 'Edit',
            'add': 'Add',
            'search': 'Search',
            'filter': 'Filter',
            'export': 'Export',
            'loading': 'Loading...',
            'no_data': 'No data available',
            'success': 'Success',
            'error': 'Error',
            'confirm': 'Confirm',
            'back': 'Back',
            'next': 'Next',
            'previous': 'Previous',
            'close': 'Close',
            'view': 'View',
            'download': 'Download',
            'print': 'Print',
            'refresh': 'Refresh',
            
            // Dashboard
            'garage_dashboard': 'Garage Dashboard',
            'my_garage': 'My Garage',
            'total_customers': 'Total Customers',
            'active_customers': 'Active customers in system',
            'active_jobs': 'Active Jobs',
            'jobs_in_progress': 'Jobs in progress',
            'monthly_revenue': 'Monthly Revenue',
            'total_earnings': 'Total earnings this month',
            'pending_invoices': 'Pending Invoices',
            'awaiting_payment': 'Awaiting payment',
            'new_job': 'New Job',
            'create_invoice': 'Create Invoice',
            'view_invoices': 'View Invoices',
            'customers': 'Customers',
            'reports': 'Reports',
            'inventory': 'Inventory',
            'users': 'Users',
            'settings': 'Settings',
            'recent_jobs': 'Recent Jobs',
            
            // Settings
            'garage_profile': 'Garage Profile',
            'business_settings': 'Business Settings',
            'services_management': 'Services',
            'email_config': 'Email Config',
            'sms_config': 'SMS Config',
            'payments': 'Payments',
            'notifications': 'Notifications',
            'security': 'Security',
            'garage_name': 'Garage Name',
            'contact_email': 'Contact Email',
            'phone_number': 'Phone Number',
            'website': 'Website',
            'address': 'Address',
            'description': 'Description',
            'currency': 'Currency',
            'timezone': 'Timezone',
            'default_language': 'Default Language',
            'date_format': 'Date Format',
            'working_hours': 'Working Hours',
            'tax_rate': 'Tax Rate',
            'save_garage_profile': 'Save Garage Profile',
            'save_business_settings': 'Save Business Settings',
            'save_changes': 'Save Changes',
            
            // Customers
            'customer_management': 'Customer Management',
            'add_customer': 'Add Customer',
            'customer_name': 'Customer Name',
            'email': 'Email',
            'phone': 'Phone',
            'vehicle': 'Vehicle',
            'actions': 'Actions',
            'total': 'Total',
            'search_customers': 'Search customers...',
            
            // Invoices
            'invoice_management': 'Invoice Management',
            'invoice_number': 'Invoice Number',
            'customer': 'Customer',
            'amount': 'Amount',
            'status': 'Status',
            'due_date': 'Due Date',
            'paid': 'Paid',
            'unpaid': 'Unpaid',
            'overdue': 'Overdue',
            'all': 'All',
            
            // Jobs
            'job_management': 'Job Management',
            'service_type': 'Service Type',
            'estimated_cost': 'Estimated Cost',
            'priority': 'Priority',
            'pending': 'Pending',
            'in_progress': 'In Progress',
            'completed': 'Completed',
            
            // Reports
            'revenue_report': 'Revenue Report',
            'customer_report': 'Customer Report',
            'job_report': 'Job Report',
            'export_pdf': 'Export PDF',
            
            // Forms
            'full_name': 'Full Name',
            'enter_name': 'Enter name',
            'enter_email': 'Enter email',
            'enter_phone': 'Enter phone',
            'select_customer': 'Select Customer',
            'select_service': 'Select Service',
            'required_field': 'Required field',
            'notes': 'Notes',
            'loading_customers': 'Loading customers...',
            'no_customers': 'No customers available',
            'error_loading': 'Error loading customers',
            
            // Modal titles
            'add_new_customer': 'Add New Customer',
            'edit_customer': 'Edit Customer',
            'add_new_job': 'Add New Job',
            'edit_job': 'Edit Job',
            'create_new_invoice': 'Create New Invoice',
            'view_invoice': 'View Invoice',
            'add_inventory_item': 'Add Inventory Item',
            'edit_inventory_item': 'Edit Inventory Item',
            
            // Form fields
            'customer_details': 'Customer Details',
            'job_details': 'Job Details',
            'invoice_details': 'Invoice Details',
            'vehicle_info': 'Vehicle Information',
            'select_job': 'Select Job (Optional)',
            'invoice_amount': 'Invoice Amount',
            'tax_amount': 'Tax Amount',
            'total_amount': 'Total Amount',
            'payment_terms': 'Payment Terms',
            'due_on_receipt': 'Due on Receipt',
            'net_15': 'Net 15 Days',
            'net_30': 'Net 30 Days',
            'net_60': 'Net 60 Days',
            
            // Service types
            'oil_change': 'Oil Change',
            'brake_service': 'Brake Service',
            'engine_repair': 'Engine Repair',
            'ac_service': 'AC Service',
            'transmission_repair': 'Transmission Repair',
            'diagnostic': 'Diagnostic',
            'tire_service': 'Tire Service',
            'battery_service': 'Battery Service',
            
            // Priority levels
            'normal': 'Normal',
            'high': 'High',
            'urgent': 'Urgent',
            
            // Job status
            'pending': 'Pending',
            'in_progress': 'In Progress',
            'completed': 'Completed',
            'update_job_status': 'Update Job Status',
            'select_new_status': 'Select New Status',
            'update_status': 'Update Status',
            
            // Messages
            'settings_saved': 'Settings saved successfully!',
            'customer_added': 'Customer added successfully!',
            'invoice_created': 'Invoice created successfully!',
            'job_created': 'Job created successfully!',
            'confirm_delete': 'Are you sure you want to delete this?',
            'confirm_logout': 'Are you sure you want to logout?',
            'please_select_customer': 'Please select a customer',
            'creating_job': 'Creating Job...',
            'creating_invoice': 'Creating Invoice...',
            'saving': 'Saving...',
        },
        
        ar: {
            // Common - Arabic
            'welcome': 'مرحباً',
            'logout': 'تسجيل الخروج',
            'save': 'حفظ',
            'cancel': 'إلغاء',
            'delete': 'حذف',
            'edit': 'تعديل',
            'add': 'إضافة',
            'search': 'بحث',
            'filter': 'تصفية',
            'export': 'تصدير',
            'loading': 'جاري التحميل...',
            'no_data': 'لا توجد بيانات',
            'success': 'نجح',
            'error': 'خطأ',
            'confirm': 'تأكيد',
            'back': 'رجوع',
            'next': 'التالي',
            'previous': 'السابق',
            'close': 'إغلاق',
            'view': 'عرض',
            'download': 'تحميل',
            'print': 'طباعة',
            'refresh': 'تحديث',
            
            // Dashboard
            'garage_dashboard': 'لوحة تحكم الورشة',
            'my_garage': 'ورشتي',
            'total_customers': 'إجمالي العملاء',
            'active_customers': 'العملاء النشطون في النظام',
            'active_jobs': 'الأعمال النشطة',
            'jobs_in_progress': 'الأعمال قيد التنفيذ',
            'monthly_revenue': 'الإيرادات الشهرية',
            'total_earnings': 'إجمالي الأرباح هذا الشهر',
            'pending_invoices': 'الفواتير المعلقة',
            'awaiting_payment': 'في انتظار الدفع',
            'new_job': 'عمل جديد',
            'create_invoice': 'إنشاء فاتورة',
            'view_invoices': 'عرض الفواتير',
            'customers': 'العملاء',
            'reports': 'التقارير',
            'inventory': 'المخزون',
            'users': 'المستخدمون',
            'settings': 'الإعدادات',
            'recent_jobs': 'الأعمال الأخيرة',
            
            // Settings
            'garage_profile': 'ملف الورشة',
            'business_settings': 'إعدادات العمل',
            'services_management': 'الخدمات',
            'email_config': 'إعدادات البريد',
            'sms_config': 'إعدادات الرسائل',
            'payments': 'المدفوعات',
            'notifications': 'الإشعارات',
            'security': 'الأمان',
            'garage_name': 'اسم الورشة',
            'contact_email': 'البريد الإلكتروني',
            'phone_number': 'رقم الهاتف',
            'website': 'الموقع الإلكتروني',
            'address': 'العنوان',
            'description': 'الوصف',
            'currency': 'العملة',
            'timezone': 'المنطقة الزمنية',
            'default_language': 'اللغة الافتراضية',
            'date_format': 'تنسيق التاريخ',
            'working_hours': 'ساعات العمل',
            'tax_rate': 'معدل الضريبة',
            'save_garage_profile': 'حفظ ملف الورشة',
            'save_business_settings': 'حفظ إعدادات العمل',
            'save_changes': 'حفظ التغييرات',
            
            // Customers
            'customer_management': 'إدارة العملاء',
            'add_customer': 'إضافة عميل',
            'customer_name': 'اسم العميل',
            'email': 'البريد الإلكتروني',
            'phone': 'الهاتف',
            'vehicle': 'المركبة',
            'actions': 'الإجراءات',
            'total': 'المجموع',
            'search_customers': 'البحث عن العملاء...',
            
            // Invoices
            'invoice_management': 'إدارة الفواتير',
            'invoice_number': 'رقم الفاتورة',
            'customer': 'العميل',
            'amount': 'المبلغ',
            'status': 'الحالة',
            'due_date': 'تاريخ الاستحقاق',
            'paid': 'مدفوع',
            'unpaid': 'غير مدفوع',
            'overdue': 'متأخر',
            'all': 'الكل',
            
            // Jobs
            'job_management': 'إدارة الأعمال',
            'service_type': 'نوع الخدمة',
            'estimated_cost': 'التكلفة المقدرة',
            'priority': 'الأولوية',
            'pending': 'معلق',
            'in_progress': 'قيد التنفيذ',
            'completed': 'مكتمل',
            
            // Reports
            'revenue_report': 'تقرير الإيرادات',
            'customer_report': 'تقرير العملاء',
            'job_report': 'تقرير الأعمال',
            'export_pdf': 'تصدير PDF',
            
            // Forms
            'full_name': 'الاسم الكامل',
            'enter_name': 'أدخل الاسم',
            'enter_email': 'أدخل البريد الإلكتروني',
            'enter_phone': 'أدخل رقم الهاتف',
            'select_customer': 'اختر العميل',
            'select_service': 'اختر الخدمة',
            'required_field': 'حقل مطلوب',
            'notes': 'ملاحظات',
            'loading_customers': 'جاري تحميل العملاء...',
            'no_customers': 'لا يوجد عملاء متاحون',
            'error_loading': 'خطأ في تحميل العملاء',
            
            // Modal titles
            'add_new_customer': 'إضافة عميل جديد',
            'edit_customer': 'تعديل العميل',
            'add_new_job': 'إضافة عمل جديد',
            'edit_job': 'تعديل العمل',
            'create_new_invoice': 'إنشاء فاتورة جديدة',
            'view_invoice': 'عرض الفاتورة',
            'add_inventory_item': 'إضافة عنصر للمخزون',
            'edit_inventory_item': 'تعديل عنصر المخزون',
            
            // Form fields
            'customer_details': 'تفاصيل العميل',
            'job_details': 'تفاصيل العمل',
            'invoice_details': 'تفاصيل الفاتورة',
            'vehicle_info': 'معلومات المركبة',
            'select_job': 'اختر العمل (اختياري)',
            'invoice_amount': 'مبلغ الفاتورة',
            'tax_amount': 'مبلغ الضريبة',
            'total_amount': 'المبلغ الإجمالي',
            'payment_terms': 'شروط الدفع',
            'due_on_receipt': 'مستحق عند الاستلام',
            'net_15': 'خلال 15 يوم',
            'net_30': 'خلال 30 يوم',
            'net_60': 'خلال 60 يوم',
            
            // Service types
            'oil_change': 'تغيير الزيت',
            'brake_service': 'خدمة الفرامل',
            'engine_repair': 'إصلاح المحرك',
            'ac_service': 'خدمة التكييف',
            'transmission_repair': 'إصلاح ناقل الحركة',
            'diagnostic': 'فحص تشخيصي',
            'tire_service': 'خدمة الإطارات',
            'battery_service': 'خدمة البطارية',
            
            // Priority levels
            'normal': 'عادي',
            'high': 'عالي',
            'urgent': 'عاجل',
            
            // Job status
            'pending': 'قيد الانتظار',
            'in_progress': 'قيد التنفيذ',
            'completed': 'مكتمل',
            'update_job_status': 'تحديث حالة العمل',
            'select_new_status': 'اختر الحالة الجديدة',
            'update_status': 'تحديث الحالة',
            
            // Messages
            'settings_saved': 'تم حفظ الإعدادات بنجاح!',
            'customer_added': 'تمت إضافة العميل بنجاح!',
            'invoice_created': 'تم إنشاء الفاتورة بنجاح!',
            'job_created': 'تم إنشاء العمل بنجاح!',
            'confirm_delete': 'هل أنت متأكد من الحذف؟',
            'confirm_logout': 'هل أنت متأكد من تسجيل الخروج؟',
            'please_select_customer': 'الرجاء اختيار عميل',
            'creating_job': 'جاري إنشاء العمل...',
            'creating_invoice': 'جاري إنشاء الفاتورة...',
            'saving': 'جاري الحفظ...',
        },
        
        ur: {
            // Common - Urdu
            'welcome': 'خوش آمدید',
            'logout': 'لاگ آؤٹ',
            'save': 'محفوظ کریں',
            'cancel': 'منسوخ کریں',
            'delete': 'حذف کریں',
            'edit': 'ترمیم کریں',
            'add': 'شامل کریں',
            'search': 'تلاش کریں',
            'filter': 'فلٹر کریں',
            'export': 'ایکسپورٹ کریں',
            'loading': 'لوڈ ہو رہا ہے...',
            'no_data': 'کوئی ڈیٹا دستیاب نہیں',
            'success': 'کامیاب',
            'error': 'خرابی',
            'confirm': 'تصدیق کریں',
            'back': 'واپس',
            'next': 'اگلا',
            'previous': 'پچھلا',
            'close': 'بند کریں',
            'view': 'دیکھیں',
            'download': 'ڈاؤن لوڈ کریں',
            'print': 'پرنٹ کریں',
            'refresh': 'تازہ کریں',
            
            // Dashboard
            'garage_dashboard': 'گیراج ڈیش بورڈ',
            'my_garage': 'میری گیراج',
            'total_customers': 'کل گاہک',
            'active_customers': 'سسٹم میں فعال گاہک',
            'active_jobs': 'فعال کام',
            'jobs_in_progress': 'جاری کام',
            'monthly_revenue': 'ماہانہ آمدنی',
            'total_earnings': 'اس ماہ کی کل کمائی',
            'pending_invoices': 'زیر التواء رسیدیں',
            'awaiting_payment': 'ادائیگی کا انتظار',
            'new_job': 'نیا کام',
            'create_invoice': 'رسید بنائیں',
            'view_invoices': 'رسیدیں دیکھیں',
            'customers': 'گاہک',
            'reports': 'رپورٹس',
            'inventory': 'انوینٹری',
            'users': 'صارفین',
            'settings': 'ترتیبات',
            'recent_jobs': 'حالیہ کام',
            
            // Settings
            'garage_profile': 'گیراج پروفائل',
            'business_settings': 'کاروباری ترتیبات',
            'services_management': 'خدمات',
            'email_config': 'ای میل کنفیگریشن',
            'sms_config': 'ایس ایم ایس کنفیگریشن',
            'payments': 'ادائیگیاں',
            'notifications': 'اطلاعات',
            'security': 'سیکیورٹی',
            'garage_name': 'گیراج کا نام',
            'contact_email': 'رابطہ ای میل',
            'phone_number': 'فون نمبر',
            'website': 'ویب سائٹ',
            'address': 'پتہ',
            'description': 'تفصیل',
            'currency': 'کرنسی',
            'timezone': 'ٹائم زون',
            'default_language': 'ڈیفالٹ زبان',
            'date_format': 'تاریخ کی شکل',
            'working_hours': 'کام کے اوقات',
            'tax_rate': 'ٹیکس کی شرح',
            'save_garage_profile': 'گیراج پروفائل محفوظ کریں',
            'save_business_settings': 'کاروباری ترتیبات محفوظ کریں',
            'save_changes': 'تبدیلیاں محفوظ کریں',
            
            // Customers
            'customer_management': 'گاہک کا انتظام',
            'add_customer': 'گاہک شامل کریں',
            'customer_name': 'گاہک کا نام',
            'email': 'ای میل',
            'phone': 'فون',
            'vehicle': 'گاڑی',
            'actions': 'اقدامات',
            'total': 'کل',
            'search_customers': 'گاہک تلاش کریں...',
            
            // Invoices
            'invoice_management': 'رسید کا انتظام',
            'invoice_number': 'رسید نمبر',
            'customer': 'گاہک',
            'amount': 'رقم',
            'status': 'حالت',
            'due_date': 'مقررہ تاریخ',
            'paid': 'ادا شدہ',
            'unpaid': 'غیر ادا شدہ',
            'overdue': 'تاخیر شدہ',
            'all': 'تمام',
            
            // Jobs
            'job_management': 'کام کا انتظام',
            'service_type': 'سروس کی قسم',
            'estimated_cost': 'تخمینہ لاگت',
            'priority': 'ترجیح',
            'pending': 'زیر التواء',
            'in_progress': 'جاری',
            'completed': 'مکمل',
            
            // Reports
            'revenue_report': 'آمدنی کی رپورٹ',
            'customer_report': 'گاہک کی رپورٹ',
            'job_report': 'کام کی رپورٹ',
            'export_pdf': 'PDF ایکسپورٹ کریں',
            
            // Forms
            'full_name': 'پورا نام',
            'enter_name': 'نام درج کریں',
            'enter_email': 'ای میل درج کریں',
            'enter_phone': 'فون نمبر درج کریں',
            'select_customer': 'گاہک منتخب کریں',
            'select_service': 'سروس منتخب کریں',
            'required_field': 'ضروری فیلڈ',
            'notes': 'نوٹس',
            'loading_customers': 'گاہک لوڈ ہو رہے ہیں...',
            'no_customers': 'کوئی گاہک دستیاب نہیں',
            'error_loading': 'گاہک لوڈ کرنے میں خرابی',
            
            // Modal titles
            'add_new_customer': 'نیا گاہک شامل کریں',
            'edit_customer': 'گاہک میں ترمیم کریں',
            'add_new_job': 'نیا کام شامل کریں',
            'edit_job': 'کام میں ترمیم کریں',
            'create_new_invoice': 'نئی رسید بنائیں',
            'view_invoice': 'رسید دیکھیں',
            'add_inventory_item': 'انوینٹری آئٹم شامل کریں',
            'edit_inventory_item': 'انوینٹری آئٹم میں ترمیم کریں',
            
            // Form fields
            'customer_details': 'گاہک کی تفصیلات',
            'job_details': 'کام کی تفصیلات',
            'invoice_details': 'رسید کی تفصیلات',
            'vehicle_info': 'گاڑی کی معلومات',
            'select_job': 'کام منتخب کریں (اختیاری)',
            'invoice_amount': 'رسید کی رقم',
            'tax_amount': 'ٹیکس کی رقم',
            'total_amount': 'کل رقم',
            'payment_terms': 'ادائیگی کی شرائط',
            'due_on_receipt': 'وصولی پر واجب الادا',
            'net_15': '15 دن میں',
            'net_30': '30 دن میں',
            'net_60': '60 دن میں',
            
            // Service types
            'oil_change': 'تیل کی تبدیلی',
            'brake_service': 'بریک کی سروس',
            'engine_repair': 'انجن کی مرمت',
            'ac_service': 'اے سی کی سروس',
            'transmission_repair': 'ٹرانسمیشن کی مرمت',
            'diagnostic': 'تشخیصی جانچ',
            'tire_service': 'ٹائر کی سروس',
            'battery_service': 'بیٹری کی سروس',
            
            // Priority levels
            'normal': 'عام',
            'high': 'زیادہ',
            'urgent': 'فوری',
            
            // Job status
            'pending': 'زیر التواء',
            'in_progress': 'جاری ہے',
            'completed': 'مکمل',
            'update_job_status': 'کام کی حالت اپ ڈیٹ کریں',
            'select_new_status': 'نئی حالت منتخب کریں',
            'update_status': 'حالت اپ ڈیٹ کریں',
            
            // Messages
            'settings_saved': 'ترتیبات کامیابی سے محفوظ ہو گئیں!',
            'customer_added': 'گاہک کامیابی سے شامل ہو گیا!',
            'invoice_created': 'رسید کامیابی سے بن گئی!',
            'job_created': 'کام کامیابی سے بن گیا!',
            'confirm_delete': 'کیا آپ واقعی حذف کرنا چاہتے ہیں؟',
            'confirm_logout': 'کیا آپ واقعی لاگ آؤٹ کرنا چاہتے ہیں؟',
            'please_select_customer': 'براہ کرم گاہک منتخب کریں',
            'creating_job': 'کام بنایا جا رہا ہے...',
            'creating_invoice': 'رسید بنائی جا رہی ہے...',
            'saving': 'محفوظ ہو رہا ہے...',
        }
    },

    currentLanguage: 'en',

    /**
     * Initialize translation system
     */
    init() {
        // Load saved language preference
        const savedLang = localStorage.getItem('preferred_language') || 
                         (window.SettingsManager ? window.SettingsManager.getLanguage() : 'en');
        this.setLanguage(savedLang);
        
        // Start observing DOM for dynamically added content
        this.observeDOM();
    },

    /**
     * Set current language and apply translations
     */
    setLanguage(lang) {
        if (!this.translations[lang]) {
            console.warn(`Language ${lang} not supported, falling back to English`);
            lang = 'en';
        }
        
        this.currentLanguage = lang;
        localStorage.setItem('preferred_language', lang);
        
        // Update document direction for RTL languages
        document.documentElement.dir = (lang === 'ar' || lang === 'ur') ? 'rtl' : 'ltr';
        document.documentElement.lang = lang;
        
        // Apply translations to all elements with data-translate attribute
        this.translatePage();
        
        console.log(`Language set to: ${lang}`);
    },

    /**
     * Get translation for a key
     */
    t(key) {
        const translation = this.translations[this.currentLanguage][key];
        if (!translation) {
            console.warn(`Translation missing for key: ${key} in language: ${this.currentLanguage}`);
            return this.translations['en'][key] || key;
        }
        return translation;
    },

    /**
     * Translate all elements on the page
     */
    translatePage() {
        document.querySelectorAll('[data-translate]').forEach(element => {
            const key = element.getAttribute('data-translate');
            const translation = this.t(key);
            
            // Check if element is an input with placeholder
            if (element.tagName === 'INPUT' && element.hasAttribute('placeholder')) {
                element.placeholder = translation;
            } else if (element.tagName === 'TEXTAREA' && element.hasAttribute('placeholder')) {
                element.placeholder = translation;
            } else {
                // Preserve any icons/emojis at the start
                const currentText = element.textContent;
                const emojiMatch = currentText.match(/^[\u{1F300}-\u{1F9FF}\u{2600}-\u{26FF}\u{2700}-\u{27BF}]+/u);
                
                if (emojiMatch) {
                    element.textContent = emojiMatch[0] + ' ' + translation;
                } else {
                    element.textContent = translation;
                }
            }
        });
    },

    /**
     * Observe DOM changes and translate new elements
     */
    observeDOM() {
        const observer = new MutationObserver((mutations) => {
            mutations.forEach((mutation) => {
                mutation.addedNodes.forEach((node) => {
                    if (node.nodeType === 1) { // Element node
                        // Translate the new element if it has data-translate
                        if (node.hasAttribute && node.hasAttribute('data-translate')) {
                            const key = node.getAttribute('data-translate');
                            const translation = this.t(key);
                            if (node.tagName === 'INPUT' || node.tagName === 'TEXTAREA') {
                                node.placeholder = translation;
                            } else {
                                node.textContent = translation;
                            }
                        }
                        // Translate any children with data-translate
                        if (node.querySelectorAll) {
                            this.translatePage();
                        }
                    }
                });
            });
        });

        observer.observe(document.body, {
            childList: true,
            subtree: true
        });
    },

    /**
     * Get current language
     */
    getCurrentLanguage() {
        return this.currentLanguage;
    },

    /**
     * Check if current language is RTL
     */
    isRTL() {
        return this.currentLanguage === 'ar' || this.currentLanguage === 'ur';
    }
};

// Make it globally available
window.TranslationManager = TranslationManager;

// Auto-initialize when DOM is ready
if (document.readyState === 'loading') {
    document.addEventListener('DOMContentLoaded', () => {
        TranslationManager.init();
    });
} else {
    TranslationManager.init();
}

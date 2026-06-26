export type Lang = 'ru' | 'kz' | 'en'

export const translations: Record<Lang, Record<string, string>> = {
  ru: {
    // Tabs
    'tab.home': 'Главная',
    'tab.appeal': 'Подать обращение',
    'tab.contacts': 'Контакты',

    // Header
    'header.homeTitle': 'Контакт-центр "АО НПК"',
    'header.openChat': 'Открыть чат',

    // Header statuses
    'status.online': 'Онлайн',
    'status.support': 'Служба поддержки',
    'status.callcenter': 'Колл-центр',

    // Greetings
    'greeting.morning': 'Доброе утро! Я — НПКОТ. Задайте вопрос — найду ответ в базе знаний.',
    'greeting.afternoon': 'Добрый день! Я — НПКОТ. Задайте вопрос — найду ответ в базе знаний.',
    'greeting.evening': 'Добрый вечер! Я — НПКОТ. Задайте вопрос — найду ответ в базе знаний.',

    // Input
    'input.placeholder': 'Введите сообщение...',
    'input.send': 'Отправить',

    // Errors
    'error.generic': 'Не удалось связаться с сервером. Попробуйте позже.',
    'error.timeout': 'Сервер долго не отвечает (возможно, просыпается после простоя). Попробуйте ещё раз через 30 секунд.',
    'error.502': 'Сервис временно недоступен. Попробуйте через минуту.',
    'error.429': 'Лимит запросов к ИИ исчерпан. Попробуйте через несколько минут.',
    'error.500': 'Ошибка на сервере при обработке запроса. Попробуйте позже.',
    'error.network': 'Нет соединения с сервером. Проверьте интернет или попробуйте позже.',

    // Header actions
    'header.reset': 'Сбросить диалог',
    'header.close': 'Закрыть',
    'header.logoAlt': 'НПК',

    // Contacts tab
    'contacts.heroText': 'Мы всегда на связи и готовы помочь',
    'contacts.phoneBadge': 'Телефон колл-центра',
    'contacts.phoneSub': 'Звонок по тарифам вашего оператора',
    'contacts.callNow': 'Позвонить сейчас',
    'contacts.scheduleTitle': 'Время работы',
    'contacts.dayWeek': 'Пн – Пт',
    'contacts.dayWeekend': 'Сб – Вс',
    'contacts.timeWeek': 'с 07:00 до 20:00',
    'contacts.timeWeekend': 'Выходной',
    'contacts.socialsTitle': 'Мы в социальных сетях',
    'contacts.address': 'г. Алматы, Микрорайон Коктем-3, 21',

    // Appeal tab
    'appeal.step1': 'Стать клиентом',
    'appeal.step2': 'Подать обращение',
    'appeal.newClientLabel': 'Стать клиентом',
    'appeal.newClientDesc': 'Нет личного кабинета? Ознакомьтесь с инструкцией по подключению и скачайте шаблон заявления.',
    'appeal.newClientMeta': 'support@npck.kz',
    'appeal.instruction': 'Инструкция',
    'appeal.template': 'Шаблон',
    'appeal.existingClientLabel': 'Являюсь клиентом',
    'appeal.existingClientDesc': 'Есть доступ к личному кабинету? Подайте заявку онлайн.',
    'appeal.existingClientMeta1': 'Быстрая подача',
    'appeal.existingClientMeta2': 'Отслеживание статуса',
    'appeal.personalCabinet': 'Личный кабинет',
    'appeal.hint': 'Нужна помощь? Звоните',

    // FAQ
    'faq.heading': 'FAQ',
    'faq.empty': 'Вопросы по этой категории появятся позже.',
    'faq.langNote': 'Раздел FAQ доступен на русском языке.',

    // Lang switcher
    'lang.ru': 'RU',
    'lang.kz': 'KZ',
    'lang.en': 'EN',
  },

  kz: {
    // Tabs
    'tab.home': 'Басты бет',
    'tab.appeal': 'Шағым жіберу',
    'tab.contacts': 'Байланыс',

    // Header
    'header.homeTitle': 'НПК Байланыс орталығы',
    'header.openChat': 'Чатты ашу',

    // Header statuses
    'status.online': 'Онлайн',
    'status.support': 'Қолдау қызметі',
    'status.callcenter': 'Call-орталық',

    // Greetings
    'greeting.morning': 'Қайырлы таң! Мен — НПКОТ. Сұрақ қойыңыз — білім базасынан жауап табамын.',
    'greeting.afternoon': 'Қайырлы күн! Мен — НПКОТ. Сұрақ қойыңыз — білім базасынан жауап табамын.',
    'greeting.evening': 'Қайырлы кеш! Мен — НПКОТ. Сұрақ қойыңыз — білім базасынан жауап табамын.',

    // Input
    'input.placeholder': 'Хабарлама жазыңыз...',
    'input.send': 'Жіберу',

    // Errors
    'error.generic': 'Серверге қосылу сәтсіз аяқталды. Кейінірек көріңіз.',
    'error.timeout': 'Сервер ұзақ уақыт жауап бермейді (мүмкін, ұйықтап қалған). 30 секундтан кейін қайталап көріңіз.',
    'error.502': 'Қызмет уақытша қолжетімсіз. Бір минуттан кейін көріңіз.',
    'error.429': 'ЖІ сұраныстарының лимиті аяқталды. Бірнеше минуттан кейін көріңіз.',
    'error.500': 'Серверде сұрауды өңдеу қатесі. Кейінірек көріңіз.',
    'error.network': 'Серверге байланыс жоқ. Интернетті тексеріңіз немесе кейінірек көріңіз.',

    // Header actions
    'header.reset': 'Диалогты тастау',
    'header.close': 'Жабу',
    'header.logoAlt': 'НПК',

    // Contacts tab
    'contacts.heroText': 'Біз әрқашан байланыста және көмектесуге дайынбыз',
    'contacts.phoneBadge': 'Call-орталық телефоны',
    'contacts.phoneSub': 'Операторыңыздың тарифтері бойынша қоңырау',
    'contacts.callNow': 'Қазір қоңырау шалу',
    'contacts.scheduleTitle': 'Жұмыс уақыты',
    'contacts.dayWeek': 'Дс – Жм',
    'contacts.dayWeekend': 'Сб – Жс',
    'contacts.timeWeek': '07:00-ден 20:00-ге дейін',
    'contacts.timeWeekend': 'Демалыс',
    'contacts.socialsTitle': 'Біз әлеуметтік желілердеміз',
    'contacts.address': 'Алматы қ., Көктем-3 шағын ауданы, 21',

    // Appeal tab
    'appeal.step1': 'Клиент болу',
    'appeal.step2': 'Шағым жіберу',
    'appeal.newClientLabel': 'Клиент болу',
    'appeal.newClientDesc': 'Жеке кабинет жоқ па? Қосылу нұсқаулығымен танысып, өтініш үлгісін жүктеп алыңыз.',
    'appeal.newClientMeta': 'support@npck.kz',
    'appeal.instruction': 'Нұсқаулық',
    'appeal.template': 'Үлгі',
    'appeal.existingClientLabel': 'Клиенттімін',
    'appeal.existingClientDesc': 'Жеке кабинетке қол жеткізу бар ма? Өтінішті онлайн жіберіңіз.',
    'appeal.existingClientMeta1': 'Жедел жіберу',
    'appeal.existingClientMeta2': 'Мәртебені қадағалау',
    'appeal.personalCabinet': 'Жеке кабинет',
    'appeal.hint': 'Көмек керек пе? Қоңырау шалыңыз',

    // FAQ
    'faq.heading': 'FAQ',
    'faq.empty': 'Бұл санат бойынша сұрақтар кейінірек қосылады.',
    'faq.langNote': 'FAQ бөлімі тек орыс тілінде қолжетімді.',

    // Lang switcher
    'lang.ru': 'RU',
    'lang.kz': 'KZ',
    'lang.en': 'EN',
  },

  en: {
    // Tabs
    'tab.home': 'Home',
    'tab.appeal': 'Submit Appeal',
    'tab.contacts': 'Contacts',

    // Header
    'header.homeTitle': 'Contact Center "AO NPK"',
    'header.openChat': 'Open chat',

    // Header statuses
    'status.online': 'Online',
    'status.support': 'Support Service',
    'status.callcenter': 'Call Center',

    // Greetings
    'greeting.morning': 'Good morning! I am NPKOT. Ask a question — I will find the answer in the knowledge base.',
    'greeting.afternoon': 'Good afternoon! I am NPKOT. Ask a question — I will find the answer in the knowledge base.',
    'greeting.evening': 'Good evening! I am NPKOT. Ask a question — I will find the answer in the knowledge base.',

    // Input
    'input.placeholder': 'Type a message...',
    'input.send': 'Send',

    // Errors
    'error.generic': 'Failed to connect to the server. Please try again later.',
    'error.timeout': 'The server is taking too long to respond (possibly waking up after idle). Please try again in 30 seconds.',
    'error.502': 'Service temporarily unavailable. Please try again in a minute.',
    'error.429': 'AI request limit exceeded. Please try again in a few minutes.',
    'error.500': 'Server error while processing the request. Please try again later.',
    'error.network': 'No connection to the server. Check your internet or try again later.',

    // Header actions
    'header.reset': 'Reset dialog',
    'header.close': 'Close',
    'header.logoAlt': 'NPK',

    // Contacts tab
    'contacts.heroText': 'We are always in touch and ready to help',
    'contacts.phoneBadge': 'Call Center Phone',
    'contacts.phoneSub': 'Call at your operator rates',
    'contacts.callNow': 'Call now',
    'contacts.scheduleTitle': 'Working hours',
    'contacts.dayWeek': 'Mon – Fri',
    'contacts.dayWeekend': 'Sat – Sun',
    'contacts.timeWeek': '07:00 to 20:00',
    'contacts.timeWeekend': 'Day off',
    'contacts.socialsTitle': 'We are on social media',
    'contacts.address': 'Almaty, Koktem-3 microdistrict, 21',

    // Appeal tab
    'appeal.step1': 'Become a Client',
    'appeal.step2': 'Submit Appeal',
    'appeal.newClientLabel': 'Become a Client',
    'appeal.newClientDesc': 'No personal account? Check the connection guide and download the application template.',
    'appeal.newClientMeta': 'support@npck.kz',
    'appeal.instruction': 'Guide',
    'appeal.template': 'Template',
    'appeal.existingClientLabel': 'I am a Client',
    'appeal.existingClientDesc': 'Have access to the personal account? Submit an application online.',
    'appeal.existingClientMeta1': 'Quick submission',
    'appeal.existingClientMeta2': 'Track status',
    'appeal.personalCabinet': 'Personal Account',
    'appeal.hint': 'Need help? Call',

    // FAQ
    'faq.heading': 'FAQ',
    'faq.empty': 'Questions for this category will appear later.',
    'faq.langNote': 'FAQ section is available in Russian only.',

    // Lang switcher
    'lang.ru': 'RU',
    'lang.kz': 'KZ',
    'lang.en': 'EN',
  },
}

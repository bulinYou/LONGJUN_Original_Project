(() => {
  'use strict';
  const root = document.documentElement;
  root.classList.add('js');
  const elements = [...document.querySelectorAll('[data-i18n]')];
  const ariaElements = [...document.querySelectorAll('[data-aria]')];
  const images = [...document.querySelectorAll('[data-alt]')];
  const picker = document.getElementById('language-picker');
  const pickerSummary = picker.querySelector('summary');
  const menuButton = document.getElementById('menu-toggle');
  const menu = document.getElementById('main-nav');
  const english = {
    title: document.title,
    metaDescription: document.querySelector('meta[name="description"]').content,
    closeMenu: 'Close menu',
    languageChanged: 'Language changed to English',
    enquirySubject: 'LONGJUN — Ingredient enquiry',
    documentationSubject: 'LONGJUN Rose Otto — Documentation enquiry',
    enquiryBody: 'Hello LONGJUN team,\n\nI would like to discuss:\nMaterial:\nApplication:\nDestination:\nApproximate quantity:\nCompany:\n\nThank you.',
    documentationBody: 'Hello LONGJUN team,\n\nI would like to request relevant product and batch information for Rose Otto.\nDocuments needed:\nIntended use:\nDestination market:\nCompany:\n\nThank you.'
  };
  for (const el of elements) english[el.dataset.i18n] = el.textContent;
  for (const el of ariaElements) english[el.dataset.aria] = el.getAttribute('aria-label');
  for (const el of images) english[el.dataset.alt] = el.alt;
  const translations = { en: english, ...window.LONGJUN_TRANSLATIONS };
  const locales = { en: 'en', zh: 'zh-CN', fr: 'fr', ja: 'ja', ko: 'ko', es: 'es', ar: 'ar' };
  let currentLanguage = 'en';
  const isSupported = code => Object.prototype.hasOwnProperty.call(locales, code);

  function setMenu(open, returnFocus = false) {
    menu.classList.toggle('is-open', open);
    menuButton.setAttribute('aria-expanded', String(open));
    menuButton.setAttribute('aria-label', translations[currentLanguage][open ? 'closeMenu' : 'openMenu']);
    if (returnFocus) menuButton.focus({ preventScroll: true });
  }

  function changeLanguage(code, { persist = false, updateUrl = false, announce = false } = {}) {
    if (!isSupported(code)) code = 'en';
    const dict = translations[code];
    currentLanguage = code;
    root.lang = locales[code];
    root.dir = code === 'ar' ? 'rtl' : 'ltr';
    const titleKey = document.body.dataset.titleKey || document.body.dataset.page + 'PageTitle';
    document.title = dict[titleKey] ? dict[titleKey] + ' | LONGJUN' : dict.title;
    document.querySelector('meta[name="description"]').content = dict.metaDescription;
    for (const el of elements) el.textContent = dict[el.dataset.i18n] ?? english[el.dataset.i18n];
    for (const el of ariaElements) el.setAttribute('aria-label', dict[el.dataset.aria] ?? english[el.dataset.aria]);
    for (const el of images) el.alt = dict[el.dataset.alt] ?? english[el.dataset.alt];
    document.getElementById('language-code').textContent = code.toUpperCase();
    for (const link of document.querySelectorAll('[data-language]')) {
      const url = new URL(window.location.href);
      url.searchParams.set('lang', link.dataset.language);
      link.href = url.pathname + url.search + url.hash;
      if (link.dataset.language === code) link.setAttribute('aria-current', 'true');
      else link.removeAttribute('aria-current');
    }
    for (const link of document.querySelectorAll('[data-mail]')) {
      const kind = link.dataset.mail;
      link.href = 'mailto:yutengma@longjunintl.com?subject=' + encodeURIComponent(dict[kind + 'Subject']) + '&body=' + encodeURIComponent(dict[kind + 'Body']);
    }
    for (const link of document.querySelectorAll('a[data-route]')) {
      const url = new URL(link.getAttribute('href'), window.location.href);
      url.searchParams.set('lang', code);
      link.href = url.pathname + url.search + url.hash;
    }
    if (document.getElementById('enquiry-result') && !document.getElementById('enquiry-result').hidden) {
      document.getElementById('enquiry-result').hidden = true;
      document.getElementById('form-status').textContent = '';
    }
    for (const link of document.querySelectorAll('[data-product-mail]')) {
      link.href = 'mailto:yutengma@longjunintl.com?subject=' + encodeURIComponent('LONGJUN — ' + link.dataset.productMail) + '&body=' + encodeURIComponent(dict.enquiryBody);
    }
    if (persist) {
      try { window.localStorage.setItem('longjun-language', code); } catch { /* Reading works when device storage is unavailable. */ }
    }
    if (updateUrl) {
      const url = new URL(window.location.href);
      url.searchParams.set('lang', code);
      history.pushState({ language: code }, '', url.pathname + url.search + url.hash);
    }
    if (announce) document.getElementById('language-announcement').textContent = dict.languageChanged;
    setMenu(false);
  }

  for (const link of document.querySelectorAll('[data-language]')) {
    link.addEventListener('click', event => {
      if (event.ctrlKey || event.metaKey || event.shiftKey || event.altKey) return;
      event.preventDefault();
      changeLanguage(link.dataset.language, { persist: true, updateUrl: true, announce: true });
      picker.open = false;
      pickerSummary.focus({ preventScroll: true });
    });
  }
  menuButton.addEventListener('click', () => {
    picker.open = false;
    setMenu(menuButton.getAttribute('aria-expanded') !== 'true');
  });
  for (const link of menu.querySelectorAll('a')) link.addEventListener('click', () => setMenu(false));
  picker.addEventListener('toggle', () => { if (picker.open) setMenu(false); });
  document.addEventListener('click', event => {
    if (!picker.contains(event.target)) picker.open = false;
    if (!menu.contains(event.target) && !menuButton.contains(event.target)) setMenu(false);
  });
  document.addEventListener('keydown', event => {
    if (event.key !== 'Escape') return;
    if (picker.open) { picker.open = false; pickerSummary.focus({ preventScroll: true }); }
    if (menuButton.getAttribute('aria-expanded') === 'true') setMenu(false, true);
  });
  document.getElementById('footer-language').addEventListener('click', event => {
    event.preventDefault();
    event.stopPropagation();
    window.scrollTo({ top: 0, behavior: window.matchMedia('(prefers-reduced-motion: reduce)').matches ? 'instant' : 'smooth' });
    picker.open = true;
    pickerSummary.focus({ preventScroll: true });
  });
  window.addEventListener('popstate', () => {
    const code = new URLSearchParams(window.location.search).get('lang');
    changeLanguage(isSupported(code) ? code : 'en');
  });
  window.matchMedia('(min-width: 1201px)').addEventListener('change', () => setMenu(false));
  let initial = new URLSearchParams(window.location.search).get('lang');
  if (!initial) {
    try { initial = window.localStorage.getItem('longjun-language'); } catch { initial = 'en'; }
  }
  changeLanguage(isSupported(initial) ? initial : 'en');
  const form = document.getElementById('enquiry-form');
  if (form) {
    const params = new URLSearchParams(location.search);
    const material = form.elements.material;
    if ([...material.options].some(option => option.value === params.get('material'))) material.value = params.get('material');
    if (params.get('request') === 'documents') form.elements.requirements.value = 'TDS / COA / SDS';
    const fields = [['material','materialField'], ['application','applicationField'], ['destination','destinationField'], ['quantity','quantityField'], ['company','companyField'], ['email','emailField'], ['requirements','documentsField']];
    function prepareDraft() {
      if (!form.reportValidity()) return null;
      const dict = translations[currentLanguage];
      const selected = material.selectedOptions[0];
      const values = fields.map(([name,key]) => {
        const value = name === 'material' ? selected.textContent + (selected.dataset.name ? ' (' + selected.dataset.name + ')' : '') : form.elements[name].value.trim();
        return dict[key] + ': ' + value;
      });
      const body = 'LONGJUN\n\n' + values.join('\n\n');
      const subject = dict.enquirySubject + ' — ' + (selected.dataset.name || selected.textContent);
      const draft = document.getElementById('enquiry-draft');
      draft.value = body;
      document.getElementById('enquiry-result').hidden = false;
      document.getElementById('open-email').href = 'mailto:yutengma@longjunintl.com?subject=' + encodeURIComponent(subject) + '&body=' + encodeURIComponent(body);
      return body;
    }
    form.addEventListener('submit', event => {
      event.preventDefault();
      if (prepareDraft() === null) return;
      document.getElementById('form-status').textContent = translations[currentLanguage].draftReady;
      document.getElementById('enquiry-draft').focus({preventScroll: true});
      document.getElementById('enquiry-result').scrollIntoView({block:'nearest', behavior:window.matchMedia('(prefers-reduced-motion: reduce)').matches ? 'instant' : 'smooth'});
    });
    document.getElementById('copy-enquiry').addEventListener('click', async () => {
      const body = prepareDraft();
      if (body === null) return;
      let copied = false;
      try { await navigator.clipboard.writeText(body); copied = true; } catch {
        document.getElementById('enquiry-draft').select();
        try { copied = document.execCommand('copy'); } catch { copied = false; }
      }
      document.getElementById('form-status').textContent = translations[currentLanguage][copied ? 'copySuccess' : 'copyFailure'];
    });
    form.addEventListener('input', () => {
      document.getElementById('enquiry-result').hidden = true;
      document.getElementById('form-status').textContent = '';
    });
  }
  document.getElementById('year').textContent = new Date().getFullYear();
})();

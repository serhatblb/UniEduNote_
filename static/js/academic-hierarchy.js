/**
 * Akademik Hiyerarşi Selector — Arama Destekli Özel Dropdown
 * University → Faculty → Department → Course
 */

/* ────────────────────────────────────────────────
   CSS — tek seferlik inject
   ──────────────────────────────────────────────── */
(function injectCSS() {
    if (document.getElementById('academic-hierarchy-css')) return;
    const s = document.createElement('style');
    s.id = 'academic-hierarchy-css';
    s.textContent = `
.ss-wrap { position: relative; }

.ss-trigger {
    display: flex;
    align-items: center;
    justify-content: space-between;
    padding: 0 12px;
    height: 44px;
    border: 1.5px solid rgba(102,126,234,0.2);
    border-radius: 10px;
    background: #fff;
    cursor: pointer;
    transition: border-color .2s, box-shadow .2s;
    user-select: none;
    gap: 8px;
    box-sizing: border-box;
}
.ss-wrap.ss-disabled .ss-trigger {
    background: rgba(0,0,0,0.04);
    cursor: not-allowed;
    opacity: .6;
    pointer-events: none;
}
.ss-wrap.ss-open .ss-trigger {
    border-color: var(--primary-purple, #667eea);
    box-shadow: 0 0 0 3px rgba(102,126,234,.12);
}

.ss-value {
    flex: 1;
    font-size: .87rem;
    font-weight: 500;
    color: var(--text-primary, #1a1a2e);
    overflow: hidden;
    text-overflow: ellipsis;
    white-space: nowrap;
}
.ss-value.ss-placeholder { color: var(--text-light, #a0aec0); }

.ss-chevron {
    font-size: .65rem;
    color: var(--text-light, #a0aec0);
    transition: transform .2s;
    flex-shrink: 0;
}
.ss-wrap.ss-open .ss-chevron { transform: rotate(180deg); }

.ss-panel {
    position: absolute;
    top: calc(100% + 4px);
    left: 0; right: 0;
    background: #fff;
    border: 1.5px solid rgba(102,126,234,.2);
    border-radius: 10px;
    box-shadow: 0 8px 28px rgba(0,0,0,.13);
    z-index: 9999;
    overflow: hidden;
}
.ss-search-row {
    display: flex;
    align-items: center;
    gap: 7px;
    padding: 8px 12px;
    border-bottom: 1px solid rgba(0,0,0,.07);
}
.ss-search-row i { color: var(--text-light, #a0aec0); font-size: .75rem; flex-shrink: 0; }
.ss-search-input {
    border: none;
    outline: none;
    font-size: .84rem;
    width: 100%;
    font-family: inherit;
    color: var(--text-primary, #1a1a2e);
    background: transparent;
}
.ss-list {
    list-style: none;
    margin: 0; padding: 4px 0;
    max-height: 220px;
    overflow-y: auto;
}
.ss-option {
    padding: 8px 14px;
    font-size: .84rem;
    cursor: pointer;
    color: var(--text-primary, #1a1a2e);
    transition: background .1s;
    white-space: nowrap;
    overflow: hidden;
    text-overflow: ellipsis;
}
.ss-option:hover  { background: rgba(102,126,234,.07); }
.ss-option.ss-active { background: rgba(102,126,234,.14); font-weight: 600; }
.ss-empty {
    padding: 12px 14px;
    font-size: .82rem;
    color: var(--text-light, #a0aec0);
    text-align: center;
    list-style: none;
}

/* Yeni ders oluşturma */
.new-course-wrapper { margin-top: 8px; }
.new-course-input {
    width: 100%;
    padding: 10px 12px;
    border: 1.5px solid rgba(102,126,234,.3);
    border-radius: 8px;
    font-size: .87rem;
    font-family: inherit;
    box-sizing: border-box;
    outline: none;
    transition: border-color .2s;
}
.new-course-input:focus { border-color: var(--primary-purple, #667eea); }
.new-course-hint {
    display: block;
    font-size: .74rem;
    color: var(--text-light, #a0aec0);
    margin-top: 4px;
}
`;
    document.head.appendChild(s);
})();


/* ────────────────────────────────────────────────
   SearchableSelect — tek dropdown bileşeni
   ──────────────────────────────────────────────── */
class SearchableSelect {
    constructor(container, placeholder, onSelect, disabled = true) {
        this.container   = container;
        this.placeholder = placeholder;
        this.onSelect    = onSelect;
        this._disabled   = disabled;
        this.options     = [];
        this.selectedId  = null;
        this._build();
    }

    _build() {
        this.container.innerHTML = `
            <div class="ss-wrap${this._disabled ? ' ss-disabled' : ''}">
                <div class="ss-trigger" tabindex="${this._disabled ? -1 : 0}">
                    <span class="ss-value ss-placeholder">${this.placeholder}</span>
                    <i class="fa-solid fa-chevron-down ss-chevron"></i>
                </div>
                <div class="ss-panel" hidden>
                    <div class="ss-search-row">
                        <i class="fa-solid fa-magnifying-glass"></i>
                        <input class="ss-search-input" type="text" placeholder="Ara..." autocomplete="off">
                    </div>
                    <ul class="ss-list"></ul>
                </div>
            </div>`;

        this._wrap    = this.container.querySelector('.ss-wrap');
        this._trigger = this.container.querySelector('.ss-trigger');
        this._panel   = this.container.querySelector('.ss-panel');
        this._input   = this.container.querySelector('.ss-search-input');
        this._list    = this.container.querySelector('.ss-list');
        this._value   = this.container.querySelector('.ss-value');

        this._trigger.addEventListener('click', (e) => {
            e.stopPropagation();
            if (!this._disabled) this._toggleOpen();
        });

        this._input.addEventListener('input', () => this._render(this._input.value));
        this._input.addEventListener('click', e => e.stopPropagation());

        // Dışarıya tıklanınca kapat
        document.addEventListener('click', (e) => {
            if (!this.container.contains(e.target)) this._close();
        });
    }

    _toggleOpen() {
        this._panel.hidden ? this._open() : this._close();
    }

    _open() {
        // Diğer açık panelleri kapat
        document.querySelectorAll('.ss-wrap.ss-open').forEach(w => {
            if (w !== this._wrap) {
                w.classList.remove('ss-open');
                const p = w.querySelector('.ss-panel');
                if (p) p.hidden = true;
            }
        });
        this._wrap.classList.add('ss-open');
        this._panel.hidden = false;
        this._input.value  = '';
        this._render('');
        requestAnimationFrame(() => this._input.focus());
    }

    _close() {
        this._wrap.classList.remove('ss-open');
        this._panel.hidden = true;
    }

    _render(query) {
        const q        = query.trim().toLowerCase();
        const filtered = q
            ? this.options.filter(o => o.name.toLowerCase().includes(q))
            : this.options;

        if (filtered.length === 0) {
            this._list.innerHTML = '<li class="ss-empty">Sonuç bulunamadı</li>';
            return;
        }

        this._list.innerHTML = filtered
            .map(o => `<li class="ss-option${String(o.id) === String(this.selectedId) ? ' ss-active' : ''}"
                            data-id="${o.id}">${o.name}</li>`)
            .join('');

        this._list.querySelectorAll('.ss-option').forEach(li => {
            li.addEventListener('mousedown', (e) => {
                e.preventDefault(); // blur önle
                this._pick(li.dataset.id, li.textContent.trim());
            });
        });
    }

    _pick(id, name) {
        this.selectedId = id;
        this._value.textContent = name;
        this._value.classList.remove('ss-placeholder');
        this._close();
        this.onSelect(id);
    }

    /* ── Public ── */

    setOptions(options, placeholder) {
        this.options   = options;
        this._disabled = false;
        this._wrap.classList.remove('ss-disabled');
        this._trigger.tabIndex = 0;
        if (placeholder) this.placeholder = placeholder;
        this._clear();
    }

    _clear() {
        this.selectedId = null;
        this._value.textContent = this.placeholder;
        this._value.classList.add('ss-placeholder');
        this._close();
    }

    reset(placeholder) {
        this.options   = [];
        this._disabled = true;
        this._wrap.classList.add('ss-disabled');
        this._trigger.tabIndex = -1;
        if (placeholder) this.placeholder = placeholder;
        this._clear();
    }

    loading(text) {
        this._disabled = true;
        this._wrap.classList.add('ss-disabled');
        this._value.textContent = text || 'Yükleniyor...';
        this._value.classList.remove('ss-placeholder');
        this._close();
    }

    /** Dışarıdan seçilmiş değeri set et (setValues için) */
    setSelectedValue(id, name) {
        this.selectedId = String(id);
        this._value.textContent = name;
        this._value.classList.remove('ss-placeholder');
    }

    getValue()    { return this.selectedId; }
    isSelected()  { return !!this.selectedId; }
}


/* ────────────────────────────────────────────────
   AcademicHierarchySelector
   ──────────────────────────────────────────────── */
class AcademicHierarchySelector {
    constructor(options) {
        this.container = typeof options.container === 'string'
            ? document.querySelector(options.container)
            : options.container;

        if (!this.container) throw new Error('Container bulunamadı: ' + options.container);

        this.onSelectionChange = options.onSelectionChange || (() => {});
        this.onReady           = options.onReady           || null;
        this.apiBaseUrl        = options.apiBaseUrl        || '/api/academic/';
        this.allowCreate       = options.allowCreate       || false;

        this.selected = { university_id: null, faculty_id: null, department_id: null, course_id: null };

        this._init();
    }

    /* ── Kurulum ── */

    _init() {
        this._createHTML();

        this.uni = new SearchableSelect(
            this.container.querySelector('[data-level="university"]'),
            'Üniversite seçin...', (id) => this._onUni(id), true
        );
        this.fac = new SearchableSelect(
            this.container.querySelector('[data-level="faculty"]'),
            'Önce üniversite seçiniz', (id) => this._onFac(id), true
        );
        this.dep = new SearchableSelect(
            this.container.querySelector('[data-level="department"]'),
            'Önce fakülte seçiniz', (id) => this._onDep(id), true
        );
        this.cou = new SearchableSelect(
            this.container.querySelector('[data-level="course"]'),
            'Önce bölüm seçiniz', (id) => this._onCou(id), true
        );

        this._loadUniversities();
    }

    _createHTML() {
        this.container.innerHTML = `
        <div class="academic-hierarchy-grid">
            <div class="form-group">
                <label class="hier-label">
                    <i class="fa-solid fa-university"></i> Üniversite
                    <span class="required">*</span>
                </label>
                <div data-level="university"></div>
            </div>
            <div class="form-group">
                <label class="hier-label">
                    <i class="fa-solid fa-building-columns"></i> Fakülte
                    <span class="required">*</span>
                </label>
                <div data-level="faculty"></div>
            </div>
            <div class="form-group">
                <label class="hier-label">
                    <i class="fa-solid fa-layer-group"></i> Bölüm
                    <span class="required">*</span>
                </label>
                <div data-level="department"></div>
            </div>
            <div class="form-group">
                <label class="hier-label">
                    <i class="fa-solid fa-book-open"></i> Ders
                    <span class="required">*</span>
                </label>
                <div data-level="course"></div>
            </div>
        </div>`;
    }

    /* ── Veri yükleme ── */

    async _loadUniversities() {
        try {
            const data = await this._fetch(this.apiBaseUrl + 'universities/');
            this.uni.setOptions(data, 'Üniversite seçin...');
        } catch (e) {
            console.error('Üniversiteler yüklenemedi:', e);
        }
        if (this.onReady) this.onReady(this);
    }

    async _onUni(id) {
        this.selected = { university_id: id || null, faculty_id: null, department_id: null, course_id: null };
        this.fac.reset('Fakülte seçin...');
        this.dep.reset('Önce fakülte seçiniz');
        this.cou.reset('Önce bölüm seçiniz');
        this._removeCourseInput();

        if (!id) { this._notify(); return; }

        this.fac.loading();
        try {
            const data = await this._fetch(`${this.apiBaseUrl}faculties/?university_id=${id}`);
            this.fac.setOptions(data, 'Fakülte seçin...');
        } catch (e) {
            this.fac.reset('Yükleme hatası');
        }
        this._notify();
    }

    async _onFac(id) {
        this.selected.faculty_id    = id || null;
        this.selected.department_id = null;
        this.selected.course_id     = null;
        this.dep.reset('Bölüm seçin...');
        this.cou.reset('Önce bölüm seçiniz');
        this._removeCourseInput();

        if (!id) { this._notify(); return; }

        this.dep.loading();
        try {
            const data = await this._fetch(`${this.apiBaseUrl}departments/?faculty_id=${id}`);
            this.dep.setOptions(data, 'Bölüm seçin...');
        } catch (e) {
            this.dep.reset('Yükleme hatası');
        }
        this._notify();
    }

    async _onDep(id) {
        this.selected.department_id = id || null;
        this.selected.course_id     = null;
        this.cou.reset('Ders seçin...');
        this._removeCourseInput();

        if (!id) { this._notify(); return; }

        this.cou.loading();
        try {
            const data = await this._fetch(`${this.apiBaseUrl}courses/?department_id=${id}`);
            if (data.length === 0 && this.allowCreate) {
                this.cou.reset('Ders bulunamadı');
                this._showCourseInput(id);
            } else {
                this.cou.setOptions(data, 'Ders seçin...');
            }
        } catch (e) {
            this.cou.reset('Yükleme hatası');
        }
        this._notify();
    }

    _onCou(id) {
        this.selected.course_id = id || null;
        this._notify();
    }

    /* ── Yardımcı ── */

    async _fetch(url) {
        const res = await fetch(url);
        if (!res.ok) throw new Error(`HTTP ${res.status}`);
        return res.json();
    }

    _notify() {
        this.onSelectionChange({ ...this.selected });
    }

    _removeCourseInput() {
        const el = this.container.querySelector('.new-course-wrapper');
        if (el) el.remove();
    }

    _showCourseInput(departmentId) {
        const self    = this;
        const wrapper = document.createElement('div');
        wrapper.className = 'new-course-wrapper';
        wrapper.innerHTML = `
            <input type="text" class="new-course-input"
                placeholder="Ders adı yazın, Enter'a basın..." />
            <small class="new-course-hint">Bu bölüm için ders bulunamadı — yeni ders adı girin.</small>`;

        this.container.querySelector('[data-level="course"]').appendChild(wrapper);

        wrapper.querySelector('input').addEventListener('keydown', async function (e) {
            if (e.key !== 'Enter') return;
            e.preventDefault();
            const name = this.value.trim();
            if (!name) return;

            const csrf = document.cookie.split(';')
                .find(c => c.trim().startsWith('csrftoken='))?.split('=')[1] || '';
            try {
                const res   = await fetch(`${self.apiBaseUrl}courses/create/`, {
                    method:  'POST',
                    headers: { 'Content-Type': 'application/json', 'X-CSRFToken': csrf },
                    body:    JSON.stringify({ name, department_id: departmentId })
                });
                const course = await res.json();
                if (course.id) {
                    wrapper.remove();
                    self.cou.setOptions([course], 'Ders seçin...');
                    self.cou.setSelectedValue(course.id, course.name);
                    self.selected.course_id = String(course.id);
                    self._notify();
                }
            } catch (err) { console.error('Ders oluşturulamadı:', err); }
        });
    }

    /* ── Public API ── */

    isValid() {
        return !!(this.selected.university_id && this.selected.faculty_id &&
                  this.selected.department_id && this.selected.course_id);
    }

    getSelected() { return { ...this.selected }; }

    /**
     * Sayfa yüklendiğinde önceden seçilmiş değerleri set et.
     * Üniversite listesi zaten yüklenmiş olmalı (onReady'de çağır).
     */
    async setValues(universityId, facultyId, departmentId, courseId) {
        if (!universityId) return;

        // 1. Üniversite
        const uniOpt = this.uni.options.find(o => String(o.id) === String(universityId));
        if (!uniOpt) return;
        this.selected.university_id = String(universityId);
        this.uni.setSelectedValue(universityId, uniOpt.name);
        this._notify();

        // 2. Fakülte
        if (!facultyId) return;
        this.fac.loading();
        let facData;
        try {
            facData = await this._fetch(`${this.apiBaseUrl}faculties/?university_id=${universityId}`);
        } catch (e) { this.fac.reset('Yükleme hatası'); return; }
        this.fac.setOptions(facData, 'Fakülte seçin...');
        const facOpt = facData.find(o => String(o.id) === String(facultyId));
        if (!facOpt) return;
        this.selected.faculty_id = String(facultyId);
        this.fac.setSelectedValue(facultyId, facOpt.name);
        this._notify();

        // 3. Bölüm
        if (!departmentId) return;
        this.dep.loading();
        let depData;
        try {
            depData = await this._fetch(`${this.apiBaseUrl}departments/?faculty_id=${facultyId}`);
        } catch (e) { this.dep.reset('Yükleme hatası'); return; }
        this.dep.setOptions(depData, 'Bölüm seçin...');
        const depOpt = depData.find(o => String(o.id) === String(departmentId));
        if (!depOpt) return;
        this.selected.department_id = String(departmentId);
        this.dep.setSelectedValue(departmentId, depOpt.name);
        this._notify();

        // 4. Ders
        if (!courseId) return;
        this.cou.loading();
        let couData;
        try {
            couData = await this._fetch(`${this.apiBaseUrl}courses/?department_id=${departmentId}`);
        } catch (e) { this.cou.reset('Yükleme hatası'); return; }
        this.cou.setOptions(couData, 'Ders seçin...');
        const couOpt = couData.find(o => String(o.id) === String(courseId));
        if (!couOpt) return;
        this.selected.course_id = String(courseId);
        this.cou.setSelectedValue(courseId, couOpt.name);
        this._notify();
    }

    reset() {
        this.selected = { university_id: null, faculty_id: null, department_id: null, course_id: null };
        this.uni._clear();
        this.fac.reset('Önce üniversite seçiniz');
        this.dep.reset('Önce fakülte seçiniz');
        this.cou.reset('Önce bölüm seçiniz');
        this._notify();
    }
}

if (typeof module !== 'undefined' && module.exports) {
    module.exports = { AcademicHierarchySelector, SearchableSelect };
}

/**
 * Akademik Hiyerarşi Selector — Native Select (Select2'siz)
 * University → Faculty → Department → Course
 */
class AcademicHierarchySelector {
    constructor(options) {
        this.container = typeof options.container === 'string'
            ? document.querySelector(options.container)
            : options.container;

        if (!this.container) throw new Error('Container bulunamadı: ' + options.container);

        this.onSelectionChange = options.onSelectionChange || (() => {});
        this.onReady           = options.onReady           || null;
        this.required          = options.required          || [];
        this.apiBaseUrl        = options.apiBaseUrl        || '/api/academic/';
        this.allowCreate       = options.allowCreate       || false;

        this.selected = {
            university_id: null,
            faculty_id:    null,
            department_id: null,
            course_id:     null
        };

        this.init();
    }

    /* ── KURULUM ── */

    init() {
        this.createHTML();
        this.uni = this.container.querySelector('[data-level="university"]');
        this.fac = this.container.querySelector('[data-level="faculty"]');
        this.dep = this.container.querySelector('[data-level="department"]');
        this.cou = this.container.querySelector('[data-level="course"]');
        this.attachEvents();
        this.loadUniversities();
    }

    createHTML() {
        this.container.innerHTML = `
        <div class="academic-hierarchy-grid">
            <div class="form-group">
                <label class="hier-label">
                    <i class="fa-solid fa-university"></i> Üniversite
                    <span class="required">*</span>
                </label>
                <div class="hier-select-wrap">
                    <select class="hier-select" data-level="university">
                        <option value="">Üniversite seçin...</option>
                    </select>
                </div>
            </div>
            <div class="form-group">
                <label class="hier-label">
                    <i class="fa-solid fa-building-columns"></i> Fakülte
                    <span class="required">*</span>
                </label>
                <div class="hier-select-wrap">
                    <select class="hier-select" data-level="faculty" disabled>
                        <option value="">Önce üniversite seçiniz</option>
                    </select>
                </div>
            </div>
            <div class="form-group">
                <label class="hier-label">
                    <i class="fa-solid fa-layer-group"></i> Bölüm
                    <span class="required">*</span>
                </label>
                <div class="hier-select-wrap">
                    <select class="hier-select" data-level="department" disabled>
                        <option value="">Önce fakülte seçiniz</option>
                    </select>
                </div>
            </div>
            <div class="form-group">
                <label class="hier-label">
                    <i class="fa-solid fa-book-open"></i> Ders
                    <span class="required">*</span>
                </label>
                <div class="hier-select-wrap" id="course-select-wrap-${Date.now()}">
                    <select class="hier-select" data-level="course" disabled>
                        <option value="">Önce bölüm seçiniz</option>
                    </select>
                </div>
            </div>
        </div>`;
    }

    attachEvents() {
        this.uni.addEventListener('change', () => this.handleUniversityChange(this.uni.value));
        this.fac.addEventListener('change', () => this.handleFacultyChange(this.fac.value));
        this.dep.addEventListener('change', () => this.handleDepartmentChange(this.dep.value));
        this.cou.addEventListener('change', () => this.handleCourseChange(this.cou.value));
    }

    /* ── VERİ YÜKLEME ── */

    async loadUniversities() {
        try {
            const data = await this._fetch(this.apiBaseUrl + 'universities/');
            this._fill(this.uni, data, 'Üniversite seçin...', false /* disabled=false */);
        } catch (e) {
            console.error('Üniversiteler yüklenemedi:', e);
        }
        if (this.onReady) this.onReady(this);
    }

    async handleUniversityChange(id) {
        this.selected = { university_id: id || null, faculty_id: null, department_id: null, course_id: null };
        this._reset(this.fac, 'Fakülte seçin...');
        this._reset(this.dep, 'Önce fakülte seçiniz');
        this._reset(this.cou, 'Önce bölüm seçiniz');
        this._removeCourseInput();

        if (!id) { this.notifyChange(); return; }

        this._loading(this.fac);
        try {
            const data = await this._fetch(`${this.apiBaseUrl}faculties/?university_id=${id}`);
            this._fill(this.fac, data, 'Fakülte seçin...');
        } catch (e) {
            this._reset(this.fac, 'Yükleme hatası');
        }
        this.notifyChange();
    }

    async handleFacultyChange(id) {
        this.selected.faculty_id    = id || null;
        this.selected.department_id = null;
        this.selected.course_id     = null;
        this._reset(this.dep, 'Bölüm seçin...');
        this._reset(this.cou, 'Önce bölüm seçiniz');
        this._removeCourseInput();

        if (!id) { this.notifyChange(); return; }

        this._loading(this.dep);
        try {
            const data = await this._fetch(`${this.apiBaseUrl}departments/?faculty_id=${id}`);
            this._fill(this.dep, data, 'Bölüm seçin...');
        } catch (e) {
            this._reset(this.dep, 'Yükleme hatası');
        }
        this.notifyChange();
    }

    async handleDepartmentChange(id) {
        this.selected.department_id = id || null;
        this.selected.course_id     = null;
        this._reset(this.cou, 'Ders seçin...');
        this._removeCourseInput();

        if (!id) { this.notifyChange(); return; }

        this._loading(this.cou);
        try {
            const data = await this._fetch(`${this.apiBaseUrl}courses/?department_id=${id}`);
            if (data.length === 0 && this.allowCreate) {
                this._reset(this.cou, 'Ders bulunamadı');
                this._showCourseInput(id);
            } else {
                this._fill(this.cou, data, 'Ders seçin...');
            }
        } catch (e) {
            this._reset(this.cou, 'Yükleme hatası');
        }
        this.notifyChange();
    }

    handleCourseChange(id) {
        this.selected.course_id = id || null;
        this.notifyChange();
    }

    /* ── YARDIMCI ── */

    async _fetch(url) {
        const res = await fetch(url);
        if (!res.ok) throw new Error(`HTTP ${res.status}`);
        return res.json();
    }

    _reset(sel, placeholder) {
        sel.innerHTML = `<option value="">${placeholder}</option>`;
        sel.disabled  = true;
        sel.value     = '';
    }

    _loading(sel) {
        sel.innerHTML = '<option value="">Yükleniyor...</option>';
        sel.disabled  = true;
    }

    _fill(sel, items, placeholder, disabled = false) {
        sel.innerHTML = `<option value="">${placeholder}</option>`;
        items.forEach(item => sel.add(new Option(item.name, item.id)));
        sel.disabled = disabled || items.length === 0;
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

        this.cou.closest('.form-group').appendChild(wrapper);

        wrapper.querySelector('input').addEventListener('keydown', async function (e) {
            if (e.key !== 'Enter') return;
            e.preventDefault();
            const name = this.value.trim();
            if (!name) return;

            const csrf = document.cookie.split(';')
                .find(c => c.trim().startsWith('csrftoken='))?.split('=')[1] || '';
            try {
                const res  = await fetch(`${self.apiBaseUrl}courses/create/`, {
                    method: 'POST',
                    headers: { 'Content-Type': 'application/json', 'X-CSRFToken': csrf },
                    body: JSON.stringify({ name, department_id: departmentId })
                });
                const course = await res.json();
                if (course.id) {
                    wrapper.remove();
                    self._fill(self.cou, [course], 'Ders seçin...');
                    self.cou.value          = course.id;
                    self.selected.course_id = String(course.id);
                    self.notifyChange();
                }
            } catch (err) { console.error('Ders oluşturulamadı:', err); }
        });
    }

    notifyChange() {
        this.onSelectionChange({ ...this.selected });
    }

    /* ── PUBLIC API ── */

    isValid() {
        return !!(this.selected.university_id && this.selected.faculty_id &&
                  this.selected.department_id && this.selected.course_id);
    }

    getSelected() { return { ...this.selected }; }

    setValues(universityId, facultyId, departmentId, courseId) {
        if (!universityId) return;
        this.uni.value = universityId;
        this.uni.dispatchEvent(new Event('change'));

        const wait = (ms) => new Promise(r => setTimeout(r, ms));
        (async () => {
            await wait(500);
            if (facultyId) {
                this.fac.value = facultyId;
                this.fac.dispatchEvent(new Event('change'));
                await wait(500);
            }
            if (departmentId) {
                this.dep.value = departmentId;
                this.dep.dispatchEvent(new Event('change'));
                await wait(500);
            }
            if (courseId) {
                this.cou.value = courseId;
                this.cou.dispatchEvent(new Event('change'));
            }
        })();
    }

    reset() {
        this.uni.value = '';
        this.uni.dispatchEvent(new Event('change'));
    }
}

if (typeof module !== 'undefined' && module.exports) {
    module.exports = AcademicHierarchySelector;
}

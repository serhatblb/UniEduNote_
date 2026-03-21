/**
 * Akademik Hiyerarşi Selector Component
 * Reusable component for University → Faculty → Department → Course selection
 */
class AcademicHierarchySelector {
    constructor(options) {
        this.container = typeof options.container === 'string'
            ? document.querySelector(options.container)
            : options.container;

        if (!this.container) {
            throw new Error('Container element not found');
        }

        this.onSelectionChange = options.onSelectionChange || (() => {});
        this.required = options.required || [];
        this.searchEnabled = options.searchEnabled !== false;
        this.apiBaseUrl = options.apiBaseUrl || '/api/academic/';
        this.allowCreate = options.allowCreate || false;

        this.selected = {
            university_id: null,
            faculty_id: null,
            department_id: null,
            course_id: null
        };

        this.cache = {
            universities: null,
            faculties: {},
            departments: {},
            courses: {}
        };

        // Select2 ortak ayarlar
        this._s2opts = {
            width: '100%',
            language: {
                noResults: () => "Sonuç bulunamadı",
                searching: () => "Aranıyor..."
            },
            allowClear: false
        };

        this.init();
    }

    init() {
        this.createHTML();

        // Container'a özel scoped referanslar (global ID çakışmasını önler)
        this.$uni = $(this.container).find('[data-level="university"]');
        this.$fac = $(this.container).find('[data-level="faculty"]');
        this.$dep = $(this.container).find('[data-level="department"]');
        this.$cou = $(this.container).find('[data-level="course"]');

        this.initSelect2();
        this.attachEvents();
        this.loadUniversities();
    }

    createHTML() {
        this.container.innerHTML = `
            <div class="academic-hierarchy-grid">
                <div class="form-group">
                    <label>Üniversite <span class="required">*</span></label>
                    <select class="academic-select" data-level="university">
                        <option value="">Üniversite seçin...</option>
                    </select>
                </div>
                <div class="form-group">
                    <label>Fakülte <span class="required">*</span></label>
                    <select class="academic-select" data-level="faculty" disabled>
                        <option value="">Önce üniversite seçiniz</option>
                    </select>
                </div>
                <div class="form-group">
                    <label>Bölüm <span class="required">*</span></label>
                    <select class="academic-select" data-level="department" disabled>
                        <option value="">Önce fakülte seçiniz</option>
                    </select>
                </div>
                <div class="form-group">
                    <label>Ders <span class="required">*</span></label>
                    <select class="academic-select" data-level="course" disabled>
                        <option value="">Önce bölüm seçiniz</option>
                    </select>
                </div>
            </div>
        `;
    }

    initSelect2() {
        const placeholders = {
            university: 'Üniversite seçin veya arayın...',
            faculty: 'Fakülte seçin veya arayın...',
            department: 'Bölüm seçin veya arayın...',
            course: 'Ders seçin veya arayın...'
        };

        [this.$uni, this.$fac, this.$dep, this.$cou].forEach($el => {
            const level = $el.data('level');
            $el.select2({
                ...this._s2opts,
                placeholder: placeholders[level] || 'Seçiniz...',
                dropdownParent: $(this.container)
            });
        });
    }

    attachEvents() {
        const self = this;

        this.$uni.on('change', function () {
            self.handleUniversityChange($(this).val());
        });
        this.$fac.on('change', function () {
            self.handleFacultyChange($(this).val());
        });
        this.$dep.on('change', function () {
            self.handleDepartmentChange($(this).val());
        });
        this.$cou.on('change', function () {
            self.handleCourseChange($(this).val());
        });
    }

    async loadUniversities() {
        try {
            const response = await fetch(this.apiBaseUrl + 'universities/');
            const data = await response.json();

            this.cache.universities = data;
            data.forEach(uni => {
                this.$uni.append(new Option(uni.name, uni.id, false, false));
            });
            this.$uni.trigger('change.select2');
        } catch (error) {
            console.error('Üniversiteler yüklenemedi:', error);
        }
    }

    async handleUniversityChange(universityId) {
        this.selected.university_id = universityId || null;
        this.selected.faculty_id = null;
        this.selected.department_id = null;
        this.selected.course_id = null;

        // Alt seviyeleri sıfırla
        this._resetSelect(this.$fac, 'Önce üniversite seçiniz');
        this._resetSelect(this.$dep, 'Önce fakülte seçiniz');
        this._resetSelect(this.$cou, 'Önce bölüm seçiniz');
        this._removeCourseInput();

        if (!universityId) {
            this.notifyChange();
            return;
        }

        try {
            const response = await fetch(`${this.apiBaseUrl}faculties/?university_id=${universityId}`);
            const data = await response.json();

            this.cache.faculties[universityId] = data;
            this._fillSelect(this.$fac, data, 'Fakülte seçiniz...');
        } catch (error) {
            console.error('Fakülteler yüklenemedi:', error);
        }

        this.notifyChange();
    }

    async handleFacultyChange(facultyId) {
        this.selected.faculty_id = facultyId || null;
        this.selected.department_id = null;
        this.selected.course_id = null;

        this._resetSelect(this.$dep, 'Önce fakülte seçiniz');
        this._resetSelect(this.$cou, 'Önce bölüm seçiniz');
        this._removeCourseInput();

        if (!facultyId) {
            this.notifyChange();
            return;
        }

        try {
            const response = await fetch(`${this.apiBaseUrl}departments/?faculty_id=${facultyId}`);
            const data = await response.json();

            this.cache.departments[facultyId] = data;
            this._fillSelect(this.$dep, data, 'Bölüm seçiniz...');
        } catch (error) {
            console.error('Bölümler yüklenemedi:', error);
        }

        this.notifyChange();
    }

    async handleDepartmentChange(departmentId) {
        this.selected.department_id = departmentId || null;
        this.selected.course_id = null;

        this._resetSelect(this.$cou, 'Önce bölüm seçiniz');
        this._removeCourseInput();

        if (!departmentId) {
            this.notifyChange();
            return;
        }

        try {
            const response = await fetch(`${this.apiBaseUrl}courses/?department_id=${departmentId}`);
            const data = await response.json();

            this.cache.courses[departmentId] = data;

            if (data.length === 0 && this.allowCreate) {
                this._showCourseInput(departmentId);
                this.$cou.prop('disabled', true);
            } else {
                this._fillSelect(this.$cou, data, 'Ders seçiniz...');
            }
        } catch (error) {
            console.error('Dersler yüklenemedi:', error);
        }

        this.notifyChange();
    }

    handleCourseChange(courseId) {
        this.selected.course_id = courseId || null;
        this.notifyChange();
    }

    // ── Yardımcı metodlar ──

    _resetSelect($sel, placeholder) {
        $sel.val(null).empty()
            .append(new Option(placeholder, '', false, false))
            .prop('disabled', true)
            .trigger('change.select2');
    }

    _fillSelect($sel, items, placeholder) {
        $sel.empty().append(new Option(placeholder, '', false, false));
        items.forEach(item => {
            $sel.append(new Option(item.name, item.id, false, false));
        });
        $sel.prop('disabled', false).trigger('change.select2');
    }

    _removeCourseInput() {
        const wrapper = this.container.querySelector('#new-course-wrapper');
        if (wrapper) wrapper.remove();
    }

    _showCourseInput(departmentId) {
        const self = this;
        const wrapper = document.createElement('div');
        wrapper.id = 'new-course-wrapper';
        wrapper.style.cssText = 'margin-top:8px;';
        wrapper.innerHTML = `
            <input type="text" id="new-course-name-${departmentId}"
                placeholder="Ders adı yazın ve Enter'a basın..."
                style="width:100%;padding:10px 14px;border-radius:8px;
                       border:1.5px solid rgba(102,126,234,0.4);font-size:0.9rem;
                       box-sizing:border-box;outline:none;" />
            <small style="color:#888;font-size:0.75rem;margin-top:4px;display:block;">
                Bu bölüm için ders bulunamadı. Yeni ders adı girin.
            </small>
        `;

        this.$cou.closest('.form-group')[0].appendChild(wrapper);

        const input = wrapper.querySelector('input');
        input.addEventListener('keydown', async function (e) {
            if (e.key !== 'Enter') return;
            e.preventDefault();
            const courseName = this.value.trim();
            if (!courseName) return;

            const csrfToken = document.cookie.split(';')
                .find(c => c.trim().startsWith('csrftoken='))
                ?.split('=')[1] || '';

            try {
                const res = await fetch(`${self.apiBaseUrl}courses/create/`, {
                    method: 'POST',
                    headers: {
                        'Content-Type': 'application/json',
                        'X-CSRFToken': csrfToken
                    },
                    body: JSON.stringify({ name: courseName, department_id: departmentId })
                });
                const course = await res.json();
                if (course.id) {
                    wrapper.remove();
                    self._fillSelect(self.$cou, [course], 'Ders seçiniz...');
                    self.$cou.val(course.id).trigger('change.select2');
                    self.selected.course_id = String(course.id);
                    self.notifyChange();
                }
            } catch (err) {
                console.error('Ders oluşturulamadı:', err);
            }
        });
    }

    notifyChange() {
        this.onSelectionChange({
            university_id: this.selected.university_id,
            faculty_id: this.selected.faculty_id,
            department_id: this.selected.department_id,
            course_id: this.selected.course_id
        });
    }

    getSelected() {
        return { ...this.selected };
    }

    isValid() {
        return !!(this.selected.university_id &&
            this.selected.faculty_id &&
            this.selected.department_id &&
            this.selected.course_id);
    }

    setValues(universityId, facultyId, departmentId, courseId) {
        if (!universityId) return;
        this.$uni.val(universityId).trigger('change');
        setTimeout(() => {
            if (!facultyId) return;
            this.$fac.val(facultyId).trigger('change');
            setTimeout(() => {
                if (!departmentId) return;
                this.$dep.val(departmentId).trigger('change');
                setTimeout(() => {
                    if (!courseId) return;
                    this.$cou.val(courseId).trigger('change');
                }, 400);
            }, 400);
        }, 400);
    }

    reset() {
        this.$uni.val(null).trigger('change');
    }
}

if (typeof module !== 'undefined' && module.exports) {
    module.exports = AcademicHierarchySelector;
}

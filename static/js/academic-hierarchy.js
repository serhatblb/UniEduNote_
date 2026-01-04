/**
 * Akademik Hiyerarşi Selector Component
 * Reusable component for University → Faculty → Department → Course selection
 * 
 * Usage:
 * new AcademicHierarchySelector({
 *   container: '#selector-container',
 *   onSelectionChange: (data) => console.log(data),
 *   required: ['university', 'faculty', 'department', 'course'],
 *   searchEnabled: true
 * });
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
        
        // State
        this.selected = {
            university_id: null,
            faculty_id: null,
            department_id: null,
            course_id: null
        };
        
        // Cache
        this.cache = {
            universities: null,
            faculties: {},
            departments: {},
            courses: {}
        };
        
        this.init();
    }
    
    init() {
        this.createHTML();
        this.initSelect2();
        this.attachEvents();
        this.loadUniversities();
    }
    
    createHTML() {
        this.container.innerHTML = `
            <div class="academic-hierarchy-grid">
                <div class="form-group">
                    <label for="academic-university">Üniversite <span class="required">*</span></label>
                    <select id="academic-university" class="academic-select" data-level="university">
                        <option value="">Seçiniz...</option>
                    </select>
                </div>
                <div class="form-group">
                    <label for="academic-faculty">Fakülte <span class="required">*</span></label>
                    <select id="academic-faculty" class="academic-select" data-level="faculty" disabled>
                        <option value="">Önce üniversite seçiniz</option>
                    </select>
                </div>
                <div class="form-group">
                    <label for="academic-department">Bölüm <span class="required">*</span></label>
                    <select id="academic-department" class="academic-select" data-level="department" disabled>
                        <option value="">Önce fakülte seçiniz</option>
                    </select>
                </div>
                <div class="form-group">
                    <label for="academic-course">Ders <span class="required">*</span></label>
                    <select id="academic-course" class="academic-select" data-level="course" disabled>
                        <option value="">Önce bölüm seçiniz</option>
                    </select>
                </div>
            </div>
        `;
    }
    
    initSelect2() {
        const self = this;
        
        $('.academic-select').select2({
            width: '100%',
            placeholder: function() {
                const level = $(this.element).data('level');
                const placeholders = {
                    'university': 'Üniversite seçin veya arayın...',
                    'faculty': 'Fakülte seçin veya arayın...',
                    'department': 'Bölüm seçin veya arayın...',
                    'course': 'Ders seçin veya arayın...'
                };
                return placeholders[level] || 'Seçiniz...';
            },
            language: {
                noResults: function() {
                    return "Sonuç bulunamadı";
                },
                searching: function() {
                    return "Aranıyor...";
                }
            },
            allowClear: false  // X işaretini kaldır
        });
    }
    
    attachEvents() {
        const self = this;
        
        // University change
        $('#academic-university').on('change', function() {
            const universityId = $(this).val();
            self.handleUniversityChange(universityId);
        });
        
        // Faculty change
        $('#academic-faculty').on('change', function() {
            const facultyId = $(this).val();
            self.handleFacultyChange(facultyId);
        });
        
        // Department change
        $('#academic-department').on('change', function() {
            const departmentId = $(this).val();
            self.handleDepartmentChange(departmentId);
        });
        
        // Course change
        $('#academic-course').on('change', function() {
            const courseId = $(this).val();
            self.handleCourseChange(courseId);
        });
    }
    
    async loadUniversities() {
        try {
            const response = await fetch(this.apiBaseUrl + 'universities/');
            const data = await response.json();
            
            this.cache.universities = data;
            const $select = $('#academic-university');
            
            data.forEach(uni => {
                $select.append(new Option(uni.name, uni.id, false, false));
            });
            
            $select.trigger('change');
        } catch (error) {
            console.error('Error loading universities:', error);
        }
    }
    
    async handleUniversityChange(universityId) {
        // Reset lower levels
        this.selected.university_id = universityId;
        this.selected.faculty_id = null;
        this.selected.department_id = null;
        this.selected.course_id = null;
        
        const $faculty = $('#academic-faculty');
        const $department = $('#academic-department');
        const $course = $('#academic-course');
        
        // Clear and disable lower levels
        $faculty.val(null).empty().append('<option value="">Önce üniversite seçiniz</option>').prop('disabled', true).trigger('change');
        $department.val(null).empty().append('<option value="">Önce fakülte seçiniz</option>').prop('disabled', true).trigger('change');
        $course.val(null).empty().append('<option value="">Önce bölüm seçiniz</option>').prop('disabled', true).trigger('change');
        
        if (!universityId) {
            this.notifyChange();
            return;
        }
        
        // Load faculties
        try {
            const response = await fetch(`${this.apiBaseUrl}faculties/?university_id=${universityId}`);
            const data = await response.json();
            
            this.cache.faculties[universityId] = data;
            $faculty.empty().append('<option value="">Seçiniz...</option>');
            
            data.forEach(fac => {
                $faculty.append(new Option(fac.name, fac.id, false, false));
            });
            
            $faculty.prop('disabled', false).trigger('change');
        } catch (error) {
            console.error('Error loading faculties:', error);
        }
        
        this.notifyChange();
    }
    
    async handleFacultyChange(facultyId) {
        this.selected.faculty_id = facultyId;
        this.selected.department_id = null;
        this.selected.course_id = null;
        
        const $department = $('#academic-department');
        const $course = $('#academic-course');
        
        // Clear and disable lower levels
        $department.val(null).empty().append('<option value="">Önce fakülte seçiniz</option>').prop('disabled', true).trigger('change');
        $course.val(null).empty().append('<option value="">Önce bölüm seçiniz</option>').prop('disabled', true).trigger('change');
        
        if (!facultyId) {
            this.notifyChange();
            return;
        }
        
        // Load departments
        try {
            const response = await fetch(`${this.apiBaseUrl}departments/?faculty_id=${facultyId}`);
            const data = await response.json();
            
            this.cache.departments[facultyId] = data;
            $department.empty().append('<option value="">Seçiniz...</option>');
            
            data.forEach(dept => {
                $department.append(new Option(dept.name, dept.id, false, false));
            });
            
            $department.prop('disabled', false).trigger('change');
        } catch (error) {
            console.error('Error loading departments:', error);
        }
        
        this.notifyChange();
    }
    
    async handleDepartmentChange(departmentId) {
        this.selected.department_id = departmentId;
        this.selected.course_id = null;
        
        const $course = $('#academic-course');
        
        // Clear course
        $course.val(null).empty().append('<option value="">Önce bölüm seçiniz</option>').prop('disabled', true).trigger('change');
        
        if (!departmentId) {
            this.notifyChange();
            return;
        }
        
        // Load courses
        try {
            const response = await fetch(`${this.apiBaseUrl}courses/?department_id=${departmentId}`);
            const data = await response.json();
            
            this.cache.courses[departmentId] = data;
            $course.empty().append('<option value="">Seçiniz...</option>');
            
            data.forEach(course => {
                $course.append(new Option(course.name, course.id, false, false));
            });
            
            $course.prop('disabled', false).trigger('change');
        } catch (error) {
            console.error('Error loading courses:', error);
        }
        
        this.notifyChange();
    }
    
    handleCourseChange(courseId) {
        this.selected.course_id = courseId;
        this.notifyChange();
    }
    
    notifyChange() {
        this.onSelectionChange({
            university_id: this.selected.university_id,
            faculty_id: this.selected.faculty_id,
            department_id: this.selected.department_id,
            course_id: this.selected.course_id
        });
    }
    
    // Public methods
    getSelected() {
        return {...this.selected};
    }
    
    isValid() {
        return this.selected.university_id && 
               this.selected.faculty_id && 
               this.selected.department_id && 
               this.selected.course_id;
    }
    
    setValues(universityId, facultyId, departmentId, courseId) {
        // Set values programmatically
        $('#academic-university').val(universityId).trigger('change');
        setTimeout(() => {
            $('#academic-faculty').val(facultyId).trigger('change');
            setTimeout(() => {
                $('#academic-department').val(departmentId).trigger('change');
                setTimeout(() => {
                    $('#academic-course').val(courseId).trigger('change');
                }, 300);
            }, 300);
        }, 300);
    }
    
    reset() {
        $('#academic-university').val(null).trigger('change');
    }
}

// Export for use in other scripts
if (typeof module !== 'undefined' && module.exports) {
    module.exports = AcademicHierarchySelector;
}


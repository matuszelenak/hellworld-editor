$( document ).ready(function() {
    let diseases = {
        'ADHD': new ADHD(0),
        'Parkinson': new Parkinson(0),
        'Stutter': new Stutter(0),
        'Sleeping': new Sleeping(0),
        'Flu': new Flu(0),
        'Shortsightedness': new Shortsightedness(0)
    };

    function setCursor(element){
        $('#editor-window').find('.editor-char').removeClass('editor-char-cursor');
        $('#editor-window').find('.editor-sentinel-char').removeClass('editor-char-cursor');
        editor.cursored_element = element;
    }

    class EditorRow {
        constructor(content, pos, parent){
            this.handleCharClick = this.handleCharClick.bind(this);
            this.parent = parent;
            this.position = pos;
            this.html = $('<div/>')
                .addClass('editor-row')
                .attr('tabindex', "0");
            this.content = content.split('');
            this.buildCharacters();
            this.html.focus();
        }

        buildCharacters(){
            this.characters = this.content.map(
                (char, i) => {
                    let el = $('<div/>')
                        .addClass('editor-char')
                        .html(char)
                        .data('position', i)
                        .click(this.handleCharClick);
                    if (diseases['Shortsightedness'].active){
                        el.addClass('editor-char-blurred')
                    }
                    return el;
                }
            );
            this.characters.push(
                $('<div/>')
                    .addClass('editor-sentinel-char')
                    .html(' ')
                    .data('position', this.characters.length)
                    .click(this.handleCharClick)
            );
            this.html.empty().append(this.characters);
        }

        append(content){
            this.content.push(...content);
            this.buildCharacters();
        }

        insertCharacter(c, position){
            this.content.splice(position, 0, c);
            this.buildCharacters();
        }

        removeCharacter(position){
            this.content.splice(position -1, 1);
            this.buildCharacters();
        }

        splitAfter(position){
            let remainder = this.getContent().slice(position);
            this.content = this.content.slice(0, position);
            this.buildCharacters();
            return remainder;
        }

        getContent(){
            return this.characters.filter((x) => x.hasClass('editor-char')).reduce(
                (acc, char_el) => {
                    return acc + char_el.text()
                }, ""
            )
        }

        handleCharClick(e){
            e.preventDefault();
            this.parent.setCursorPosition(this.position, $(event.currentTarget).data('position'));
        }
    }

    class EditorWindow {
        constructor(){
            this.html = $('#editor-window');
            setInterval(() => {
                if (editor.cursored_element){
                    if (!editor.cursored_element.hasClass('editor-char-cursor')){
                        editor.cursored_element.addClass('editor-char-cursor');
                    } else {
                        editor.cursored_element.removeClass('editor-char-cursor');
                    }
                }
            }, 500);
            this.html.keydown(this.handleKeyDown.bind(this));
            this.selectedRowIndex = 0;
            this.selectedColumnIndex = 0;
        }

        setContent(content){
            this.cursor_position = 0;
            this.rows = content.split('\n').map(
                (c, i) => {
                    return new EditorRow(c, i, this)
                }
            );
            this.html.children().remove();
            this.html.append(...this.rows.map((x) => x.html));
        }

        removeLine(position, remainder){
            if (position > 0){
                this.rows.forEach((row, index) => {
                    if (index > position) row.position--;
                });
                this.rows.splice(position, 1);
                this.html.children().slice(position, position + 1).remove();
                let prev_line_len = this.rows[position -1].content.length;
                this.rows[position - 1].append(remainder);
                this.setCursorPosition(position - 1, prev_line_len);
            }
        }

        newLine(position, content){
            this.rows.forEach((row, index) => {
                if (index > position) row.position++;
            });
            let new_row = new EditorRow(content, position + 1, this);
            this.rows.splice(position + 1, 0, new_row);
            $("#editor-window > div:nth-child(" + (position + 1) + ")").after(new_row.html);
        }

        getContent(){
            let c = this.rows.reduce((acc, row) => { return acc + row.getContent() + '\n' }, '');
            return c.slice(0, c.length - 1);
        }

        handleKeyDown(e){
            console.log(e.keyCode, e.key);
            switch (e.keyCode) {
                case 13: {
                    let remainder = this.rows[this.selectedRowIndex].splitAfter(this.selectedColumnIndex);
                    this.newLine(this.selectedRowIndex, remainder);
                    this.setCursorPosition(this.selectedRowIndex + 1, 0);
                    break;
                }
                case 8: {
                    if (this.selectedColumnIndex === 0){
                        this.removeLine(this.selectedRowIndex, this.rows[this.selectedRowIndex].content.slice(this.cursor_position));
                    } else {
                        this.rows[this.selectedRowIndex].removeCharacter(this.selectedColumnIndex);
                        this.moveCursorPosition(-1, 0)
                    }
                    break
                }
                case 37: {
                    this.moveCursorPosition(-1, 0);
                    break
                }
                case 38: {
                    this.moveCursorPosition(0, -1);
                    break
                }
                case 39: {
                    this.moveCursorPosition(+1, 0);
                    break
                }
                case 40: {
                    this.moveCursorPosition(0, +1);
                    break
                }
                default: {
                    if ([16, 17, 18, 20, 46, 9, 38, 40, 113, 114, 115, 116, 117, 118, 119, 120, 121, 122, 123].includes(e.keyCode)) break;
                    let mangled_key = diseases['Parkinson'].mangleKey(e.key);
                    for (let i = 0; i < diseases['Stutter'].getRepeats(); i++){
                        this.rows[this.selectedRowIndex].insertCharacter(mangled_key, this.selectedColumnIndex);
                        this.moveCursorPosition(+1, 0);
                    }
                }
            }
        }

        moveCursorPosition(deltaX, deltaY){
            let newRowIndex = Math.min(this.selectedRowIndex + deltaY, this.rows.length - 1);
            newRowIndex = Math.max(newRowIndex, 0);
            let newColumnIndex = Math.min(this.selectedColumnIndex + deltaX, this.rows[newRowIndex].content.length);
            newColumnIndex = Math.max(newColumnIndex, 0);
            this.setCursorPosition(newRowIndex, newColumnIndex);
        }

        setCursorPosition(row_index, column_index){
            this.selectedRowIndex = row_index;
            this.selectedColumnIndex = column_index;
            setCursor(this.rows[this.selectedRowIndex].characters[this.selectedColumnIndex]);
        }
    }

    class DiseasePanel {
        constructor(){
            this.disease_tabs = {};
            this.container = $('#disease-panel');

            Object.entries(diseases).forEach((disease) => {
                disease.onStatusChange = this.markActiveStatus
            });
            this.updateDiseases();
            setInterval(
                () => this.updateDiseases(),
                2000,
            );
        }

        markActiveStatus(disease_name, status){
            if (status) {
                this.disease_tabs[disease_name].addClass('disease-tab-active');
            }
            else {
                this.disease_tabs[disease_name].removeClass('disease-tab-active')
            }
        }

        render(){
            let disease_list = Object.entries(diseases).map(
                ([disease_name, disease]) => {
                    let stats = '(Cooldown ' + disease.cooldown_duration / 1000 + 's, effect '+ disease.effect_duration / 1000 + 's)';
                    let el = $('<div/>')
                        .html(disease_name + stats)
                        .addClass('disease-tab');
                    if (diseases[disease_name].active)
                        el.addClass('disease-tab-active');
                    this.disease_tabs[disease_name] = el;
                    return el;
                }
            );
            this.container.children().remove();
            this.container.append(disease_list)
        }

        updateDiseases(){
            getJson(editor_urls['active_diseases'], (data) => {
                data.forEach((instance) => {
                    let disease_name = instance.disease.name;
                    let params = [
                        disease_name,
                        instance.severity,
                        instance.effect_duration * 1000,
                        instance.cooldown_duration * 1000,
                        instance.disease.description,
                    ];
                    let cls = diseases[disease_name];
                    cls.setParameters(...params);
                    this.render();
                });
            });
        }
    }

    class MedicinePanel{
        constructor(){
            setInterval(
                () => this.updateMedicine(),
                2000
            );
            this.balance = 0;
            this.container = $('#medicine-inventory');
            this.useMedicine = this.useMedicine.bind(this);
            this.purchaseMedicine = this.purchaseMedicine.bind(this);
            this.updateMedicine();
        }

        render(data){
            let meds = data.map(
                (med) => {
                    return $('<div/>')
                        .addClass('medicine-item')
                        .append(
                        $('<button/>')
                            .data('medicine_pk', med.medicine_pk)
                            .addClass('btn btn-info')
                            .html('Use '+ med.medicine_name + '('+ med.amount +')')
                            .click(this.useMedicine))
                        .append(
                        $('<button/>')
                            .data('medicine_pk', med.medicine_pk)
                            .addClass('btn btn-danger')
                            .html('Purchase for $' + med.price)
                            .click(this.purchaseMedicine)
                        )
                }
            );
            this.container.children().remove();
            this.container.append(
                $('<h3/>').html('Current accout balance: $' + this.balance)
            );
            this.container.append(meds);
        }

        purchaseMedicine(event){
            postJson(editor_urls['medicine_purchase'], {medicine_pk: $(event.currentTarget).data('medicine_pk')}, (data) => {
                this.balance = data.balance;
                this.updateMedicine();
                editor.disease_panel.updateDiseases();
            });
        }

        useMedicine(event){
            postJson(editor_urls['medicine_inventory'], {medicine_pk: $(event.currentTarget).data('medicine_pk')}, (data) => {
                if (!data.message) this.render(data);
            });
        }

        updateMedicine(){
            getJson(editor_urls['medicine_inventory'], (data) => {
                this.render(data);
            });
        }
    }

    class SubmitHistory {
        constructor(){
            this.container = $('#submit-history');
            this.submits = []
        }

        addSubmit(submit_id, task_name){
            this.submits.push({
                id: submit_id,
                task_name: task_name,
                status: 'Processing'
            });
            this.render()
        }

        updateSubmitStatus(id, status){
            this.submits.map((submit) => {
                if (submit.id === id){
                    submit.status = editor.rules.submit_statuses[status];
                }
                return submit;
            });
            this.render()
        }

        render(){
            this.container.children().remove();
            this.container.append(
                this.submits.map((submit) => {
                    return $('<div/>').html('Submit ' + submit.id + ' for ' + submit.task_name + ': '+ submit.status)
                        .addClass(submit.status === 2 ? 'submit-ok' : 'submit-wrong')
                })
            )
        }
    }

    class Editor {
        constructor(){
            this.cursored_element = undefined;

            this.updateRules();
            setInterval(
                () => this.updateRules(),
                20000
            );

            this.editor_window = new EditorWindow();
            let saved = localStorage.getItem('saved_code');
            if (!saved){
                saved = 'Welcome to HellWorld!';
            }
            this.editor_window.setContent(saved);
            this.submit_history = new SubmitHistory();
            this.medicine_panel = new MedicinePanel();
            this.disease_panel = new DiseasePanel();

            $('#submit-button').click(this.submitCode.bind(this));
            $('#quicksave-button').click(() => {
                localStorage.setItem('saved_code', this.editor_window.getContent());
            });
            $('#restore-button').click(() => {
                this.editor_window.setContent(localStorage.getItem('saved_code'));
            });

            $('#task-selector').change(this.changeTask);
            this.changeTask();
            this.saved_code = "";
        }

        changeTask(){
            let val = $('#task-selector').val();
                $('#task-pdf').attr(
                    'src', editor_urls['assignment'].replace('4247', val) + "?" + new Date().getTime()
            )
        }

        submitCode(){
            let payload = {
                code: this.editor_window.getContent(),
                language: $('#language-selector').val(),
                task: $('#task-selector').val()
            };
            postJson(editor_urls['submit'], payload, (response) => {
                console.log(response);
                this.submit_history.addSubmit(response.submit_id, response.task_name);
                this.submit_result_timer = setInterval(
                    () => this.pollSubmitResult(response.submit_id),
                    2000
                );
            })
        }

        pollSubmitResult(submit_id){
            let base_url = editor_urls['submit_status'];
            getJson(base_url.replace('4247', submit_id), (response) => {
                if (response.status > 1){
                    this.submit_history.updateSubmitStatus(submit_id, response.status);
                    clearInterval(this.submit_result_timer);
                }
            })
        }

        updateRules(){
            getJson(editor_urls['rules'], (data) => {this.rules = data});
        }
    }

    this.logout_interval = setInterval(() => {
        fetch(editor_urls['logout'], {
            method: 'POST',
              headers: {
                'X-CSRFToken': csrftoken
              },
            body: ""
        })
        .then(() => {
            clearInterval(this.logout_interval);
            location.href = editor_urls['login']
        });
    }, 60 * 1000 * 25);
    let editor = new Editor();
});
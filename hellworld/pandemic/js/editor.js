'use strict';

class EditorWindowCharacter extends React.Component {
    constructor(props) {
        super(props);
        console.log(this.props.value);
        this.state = {value: this.props.value, parent_row: this.props.parent_row};
        this.handleMouseDown = this.handleMouseDown.bind(this);
    }

    handleMouseDown(e){
        console.log(this.props.index);
        this.state.parent_row.changeCursorPosition(this.props.index);
    }

    render() {
        return <div className='editor-char' onClick={this.handleMouseDown}>{this.state.value}{this.props.index} </div>
    }
}

class EditorWindowRow extends React.Component {
   constructor(props) {
        super(props);
        this.state = {character_values: this.props.value.split('')};
        this.handleKeyPress = this.handleKeyPress.bind(this);
        this.changeCursorPosition = this.changeCursorPosition.bind(this);
        this.cursor_position = 0;
    }

    changeCursorPosition(clicked_child_id){
       ///this.cursor_position = this.characters.findIndex((ch) => ch.props.id === clicked_child_id);
        this.cursor_position = clicked_child_id;
        console.log(this.cursor_position);
    }

    handleKeyPress(e){
       if (e.keyCode !== 13 && e.key !== 8){
           let character_values = [...this.state.character_values];
           character_values.splice(this.cursor_position, 0, e.key);
           this.setState({character_values: character_values});
           console.log(this.state);
       }
    }

    componentDidMount(){
        document.addEventListener("keydown", this.handleKeyPress, false);
    }

    componentWillUnmount(){
        document.removeEventListener("keydown", this.handleKeyPress, false);
    }

    getContent(){
       return this.state.character_values.reduce((acc, c) => {return acc + c}, "")
    }

    render() {
        return (
            <div className="editor-row">{
                this.state.character_values.map(
            (c, i) => {return <EditorWindowCharacter index={i} value={c} parent_row={this}/>}
                )
            }</div>
        )
    }
}

class EditorWindow extends React.Component {
    constructor(props) {
        super(props);
        this.state = {code_value: '', language: 0, row_values: ['Hello World', 'Please work']};
        this.rows = [];

        this.submitCode = this.submitCode.bind(this);
        this.handleCodeChange = this.handleCodeChange.bind(this);
        this.handleLanguageChange = this.handleLanguageChange.bind(this);
    }

    getContent(){
        return this.rows.reduce((acc, r) => {return acc + '\n'+ r.getContent()}, "")
    }

    submitCode(e) {
        e.preventDefault();
        this.props.parent.submitCode({code: this.state.code_value, language: this.state.language, task: 1});
    }

    handleCodeChange (event) {
        this.setState({code_value: event.target.value});
    }

    handleLanguageChange (event) {
        this.setState({language: event.target.value});
    }

    render() {
        let language_options = Object.entries(this.props.languages).map(
            ([key, value]) => <option value={value}>{key}</option>
        );
        this.rows = this.state.row_values.map(
            (r) => <EditorWindowRow value={r}/>
        );
        return (
            <div>
                <select onChange={this.handleLanguageChange}>
                    {language_options}
                </select>
                <textarea onChange={this.handleCodeChange}>a</textarea>
                <div>
                    {this.rows}
                </div>
                <button onClick={this.submitCode}>Submit</button>
            </div>
        );
    }
}

class LogoutBtn extends React.Component {
    render() {
        return (<form method="post" action={logout_link}><input type="submit" value="Logout" /></form>)
    }
}

class TaskViewer extends React.Component {
    render() {
        return (
            <embed src={task_pdf_link} type="application/pdf" width="100%" height="600px" />
        )
    }
}

class SubmitList extends React.Component {
    constructor(props) {
        super(props);
        this.state = {submits: this.props.submits};
    }

    componentWillReceiveProps(nextProps) {
        this.setState({ submits: nextProps.submits});
    }

    render() {
        let submits = this.state.submits.map(
            (submit) => <div>{submit.id}: {submit.status}</div>
        );
        return (<div>{submits}</div>)
    }
}

class Editor extends React.Component {
    constructor(props) {
        super(props);
        this.state = {submits: [], active_diseases: [], rules: {languages: {}}};

        this.updateRules = this.updateRules.bind(this);
        this.submitCode = this.submitCode.bind(this);
        this.pollSubmitResult = this.pollSubmitResult.bind(this);

    }

    handleKeyPress(e){
        console.log(e)
    }

    pollSubmitResult(id) {
        let url = submit_status_url.replace('4247', id);
        fetch(url)
            .then(response => {
                return response.json()
            })
            .then(data => {
                if (data.status > 1){
                    clearInterval(this.submit_result_timer);
                    let submits_copy = [...this.state.submits];
                    let submit_index = submits_copy.findIndex(x => x.id === id);
                    let submit = this.state.submits[submit_index];
                    submit.status = data.status;
                    this.setState({
                        submits: submits_copy
                    })
                }
            })
    }

    submitCode(data){
        fetch(code_submit_url, {
            method: 'POST',
              headers: {
                'Accept': 'application/json',
                'Content-Type': 'application/json; charset=UTF-8',
                'X-CSRFToken': csrftoken
              },
            body: JSON.stringify(data)
        }).then(
            response => {
                return response.json()
            }
        ).then(
            data => {
                console.log(data);
                this.submit_result_timer = setInterval(
                    () => this.pollSubmitResult(data.submit_id),
                    2000
                );
                this.setState({
                    submits: [{id: data.submit_id, status: 'Waiting'}, ...this.state.submits]
                })
            });
    }

    updateRules(){
        fetch(rules_url)
            .then(results => {
                return results.json();
            })
            .then(
                data => {
                    console.log(data);
                    this.setState({rules: data})
                }
            );
    }

    componentDidMount(){
        fetch(active_diseases_url)
            .then(results => {
                return results.json();
            })
            .then(
                data => {
                    console.log(data);
                    this.setState({active_diseases: data})
                }
            );

        this.updateRules();
        this.rule_update_timer = setInterval(
            () => this.updateRules(),
            2000000
        )
    }

    componentWillUnmount(){
        clearInterval(this.rule_update_timer);
    }

    render() {
        console.log(this.state.rules);
        return (
            <div>
                <EditorWindow languages={this.state.rules.languages} parent={this}/>
                <SubmitList submits={this.state.submits} />
                <LogoutBtn/>
            </div>
        );
    }
}


$( document ).ready(function() {
    let editor = ReactDOM.render(<Editor/>, document.querySelector('#editor-container'));
});
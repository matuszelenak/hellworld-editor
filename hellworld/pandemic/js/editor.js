'use strict';

class EditorWindow extends React.Component {
    constructor(props) {
        super(props);
        console.log(this.props);
        this.state = {code_value: '', language: 0};

        this.submitCode = this.submitCode.bind(this);
        this.handleCodeChange = this.handleCodeChange.bind(this);
        this.handleLanguageChange = this.handleLanguageChange.bind(this);
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

        return (
            <div>
                <select onChange={this.handleLanguageChange}>
                    {language_options}
                </select>
                <textarea onChange={this.handleCodeChange}>a</textarea>
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

class Editor extends React.Component {
    constructor(props) {
        super(props);
        this.state = {active_diseases: [], rules: {languages: {}}};

        this.updateRules = this.updateRules.bind(this);
        this.submitCode = this.submitCode.bind(this);
        this.pollSubmitResult = this.pollSubmitResult.bind(this);

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
                    //TODO add submit results to some list
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
            20000
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
                <LogoutBtn/>
            </div>
        );
    }
}


$( document ).ready(function() {
    let editor = ReactDOM.render(<Editor/>, document.querySelector('#editor-container'));
});